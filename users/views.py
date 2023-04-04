from django.views.decorators.http import require_http_methods
from .models import Profile
from django.http import JsonResponse
import jwt, datetime, json, random
from django.core.mail import send_mail


success = 'success'
timeout = 1 # 设置JWT过期时间为1小时
retry = 5 # 验证次数
# Reading the necessary data from json flow.
def data_flow(request,keys,Maxlength=256):
    user_info = {}
    #== read
    data = json.loads(request.body)
    user_info = {key:data[key] for key in keys}
    '''
    for key in keys:
        user_info[key] = request.headers.get(key)
    '''
    print(user_info)
    #== check
    for key in keys:
        if user_info[key] is None:
            raise Exception("{}输入为空".format(key))
        elif not 0<len(user_info[key]) <= Maxlength:
            raise Exception("{}大于{}字节or信息不完整".format(key,Maxlength))
    return user_info


# 发送验证码
# https://blog.csdn.net/qq_51014805/article/details/119987513
def send_sms_code(to_email):
    """
    发送邮箱验证码
    :param to_mail: 发到这个邮箱
    :return: 成功 1 和验证码
    """
    # 生成邮箱验证码
    sms_code = '%06d' % random.randint(1, 999998) #随机6位码
    EMAIL_FROM = "3253084721@qq.com"  #邮箱来自
    email_title = '邮箱激活'
    email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
    return send_status, sms_code


# generate token
def genrate_token(username,password):
    expires_at = datetime.datetime.utcnow()+datetime.timedelta(hours=timeout)
    payload = {'username': username,
                'exp': expires_at}
    #encnde token
    token = jwt.encode(payload,password,algorithm='HS256')
    return token


# chek the token
def authenticate_check(request,keys={}):
    response, keys = {}, ['username','token']
    user_info = data_flow(request,keys)
    token = user_info['token']
    username = user_info['username']
    if not token:
        raise Exception('no carry token')
    if not username:
        raise Exception('no carry username')
    try:
        obj_user = Profile.objects.get(username=username)
    except Exception as e:
        raise Exception('{} 用户不存在'.format(username))
    try: #token decode
        decoded_payload = jwt.decode(token,obj_user.password,algorithms=['HS256'])
    except Exception as e:
        raise Exception('{} token decode 失败/验证已过期'.format(username))
    if username != decoded_payload['username']:
        raise Exception('{} 与 decode 名称 {} 不一致'.format(username,decoded_payload['username']))

    response['auth_data'] = datetime.datetime.utcfromtimestamp(int(decoded_payload['exp'])) - datetime.timedelta(hours=timeout)   
    response['username'] = username
    response['auth'] = True
    return response


#==============================================================================
#register
@require_http_methods(["POST"])
def register(request):
    response, keys = {}, ['username','password','email','confirmedPassword']
    try:
        user_info = data_flow(request,keys)
        sam_name_obj = Profile.objects.filter(username=user_info['username'])
        same_email_obj = Profile.objects.filter(email=user_info['email'])
        if len(sam_name_obj) != 0:
            raise Exception("用户名{}已注册".format(sam_name_obj))
        elif len(same_email_obj) != 0:
            raise Exception("邮箱{}已注册".format(same_email_obj))
        elif user_info['password'] != user_info['confirmedPassword']:
            raise Exception("密码不一致")
        # send a email, 成功则发送验证码
        response['sendEmail'],user_info['smsCode'] = send_sms_code(user_info['email'])
        if response['sendEmail'] != 1:
            raise Exception('验证码发送失败,检查邮箱:{}'.format(user_info['email']))
        # success! 但权限为0
        new_user = Profile(username=user_info['username'],password=user_info['password'],email=user_info['email'],smsCode=user_info['smsCode'])
        new_user.save()
        response['msg'] = success
    except Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

# 验证码校验
@require_http_methods(["POST"])
def smsCode(request):
    response, keys = {}, ['username','password','email','smsCode']
    try:
        user_info = data_flow(request,keys)
        sam_name_obj = Profile.objects.filter(username=user_info['username'])
        same_email_obj = Profile.objects.filter(email=user_info['email'])
        if len(sam_name_obj) == 0:
            raise Exception("用户名{}不存在".format(sam_name_obj))
        elif len(same_email_obj) == 0:
            raise Exception("邮箱{}不存在".format(same_email_obj))
        
        profile = Profile.objects.get(username=user_info['username'])
        # 验证密码
        if user_info['password'] != profile.password:
            raise Exception("密码错误。")
        # 验证码检查
        if profile.smsCode == '000000':
            raise Exception("已激活")
        
        if profile.smsCode == '999999':
            raise Exception("请重新发送验证码")
    
        # 验证码检查
        if user_info['smsCode'] != profile.smsCode:
            profile.permissions = profile.permissions - 1
            if profile.permissions <= -retry:
                profile.permissions = 0
                profile.smsCode = '999999' 
                profile.save() #保存
                raise Exception("验证码失效")
            else:
                profile.save() #保存
                raise Exception("验证码错误,剩余次数{}".format(retry+profile.permissions))
            
        # 验证通过 权限为1
        profile.permissions = 1
        profile.smsCode = '000000'
        profile.save()
        response['msg'] = success
    except Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)


# https://www.jianshu.com/p/d61db3008cd8
#get token
@require_http_methods(["POST"])
def get_token(request):
    response, keys = {}, ['username','password']
    try:
        user_info = data_flow(request,keys)
        tmppwd = Profile.objects.get(username=user_info['username']).password
        if user_info['password'] == tmppwd:
            response['token']  = genrate_token(user_info['username'],user_info['password'])
            response['msg'] = success
        else:
            raise Exception("username or password may wrong.")
    except Exception as e:
        response['msg'] = str(e) 
    return JsonResponse(response)


@require_http_methods(["POST"])
def authenticate(request):
    response = {}
    try:# check token
        response = authenticate_check(request)
    except Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)


@require_http_methods(["POST"])
def userlogout(request):
    response, keys = {}, ['username']
    try:
        user_info = data_flow(request,keys)
        ###执行登出操作
        response['msg'] = success
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

