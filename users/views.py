from django.views.decorators.http import require_http_methods
from .models import Profile
from django.http import JsonResponse
import jwt, datetime

success = 'success'
timeout = 1# 设置JWT过期时间为1小时
# Reading the necessary data from json flow.
def data_flow(request,keys,Maxlength=32):
    user_info = {}
    #== read
    for key in keys:
        user_info[key] = request.headers.get(key)
    print(user_info)
    #== check
    for key in keys:
        if user_info[key] is None:
            raise Exception("{}输入为空".format(key))
        elif not 0< len(user_info[key]) <= Maxlength:
            raise Exception("{}大于{}字节or信息不完整".format(key,Maxlength))
    return user_info

# generate token
def genrate_token(username,password):
    expires_at = datetime.datetime.utcnow()+datetime.timedelta(hours=timeout)
    payload = {'username': username,
                'exp': expires_at}
    #encnde token
    token = jwt.encode(payload, password, algorithm='HS256')
    return token

# chek the token
def authenticate_check(request):
    response = {}
    token = request.headers.get('token')
    username = request.headers.get('username')
    if not token:
        raise Exception('no carry token')
    if not username:
        raise Exception('no carry username')
    try:
        obj_user = Profile.objects.get(username=username)
    except Exception as e:
        raise Exception('{} 用户不存在'.format(username))
    try: # token decode
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
        # success!
        new_user = Profile(username=user_info['username'],password=user_info['password'],email=user_info['email'])
        new_user.save()
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

