from django.views.decorators.http import require_http_methods
from .models import Profile
from django.http import JsonResponse
import json, hashlib

success = 'success'
base_keys = ['username','password','email']
# Reading the necessary data from json flow.
def data_flow(request,keys,Maxlength=32):
    user_info = {}
    # read
    req = json.loads(request.body)
    for key in keys:
        user_info[key] = req.get(key)
    # check
    for key in keys: 
        if not 0< len(user_info[key]) <= Maxlength:
            raise Exception("大于{}字节or信息不完整".format(Maxlength))
    return user_info


#==============================================================================
@require_http_methods(["POST"])
def register(request):
    response, keys = {}, base_keys + ['confirm your password']
    try:
        user_info = data_flow(request,keys)
        sam_name_obj = Profile.objects.filter(username=user_info['username'])
        same_email_obj = Profile.objects.filter(email=user_info['email'])
        if len(sam_name_obj) != 0:
            raise Exception("用户名{}已注册".format(sam_name_obj))
        elif len(same_email_obj) != 0:
            raise Exception("邮箱{}已注册".format(same_email_obj))
        elif user_info['password'] != user_info['confirm your password']:
            raise Exception("密码不一致")
        # success!
        new_user = Profile(username=user_info['username'],password=user_info['password'],email=user_info['email'])
        new_user.save()
        response['msg'] = success
    except Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)


#get token
@require_http_methods(["POST"])
def get_token(request):
    response = {}
    keys = ['username','password']
    user_info = data_flow(request,keys)
    try:
        tmppwd = Profile.objects.get(username=user_info['username']).password
        if user_info['password'] == tmppwd:
            md5 = hashlib.md5()
            #把密码变成一个长度固定的字符串
            md5.update(user_info['password'].encode("utf-8"))
            response['X-Token'] = md5.hexdigest()
            response['msg'] = success
        else:
            raise Exception("username or password may wrong.")
    except Exception as e:
        response['msg'] = str(e) 
    return JsonResponse(response)
        

@require_http_methods(["POST"])
def userlogin(request):
    response = {} 
    try:
        user_info = data_flow(request,base_keys)
        ###执行登录操作 返回token
        response = user_info
        response['msg'] = success
    except Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)


@require_http_methods(["POST"])
def userlogout(request):
    response = {}
    try:
        user_info = data_flow(request,base_keys)
        ###执行登出操作
        response['msg'] = success
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

