from django.views.decorators.http import require_http_methods
from .models import Galaxies, UserClassifyRecord
from users.models import Profile
from django.http import JsonResponse
from django.db.models import F
from users.views import data_flow, authenticate_check,success

# retrn galaxy info, include image url
def get_galaxy_info(username,galaxy_name=None):
    galaxy_info = {}
    # 按未分类列表分配galaxy
    if galaxy_name == None:
        # 已被此用户分类的galaxies
        classfied_object  = UserClassifyRecord.objects.filter(username=username)
        classfied_galaxy = classfied_object.all().values('galaxy_name')
        # 排除它们
        galaxy_names = [galaxy['galaxy_name'] for galaxy in classfied_galaxy]
        none_classfied_galaxy = Galaxies.objects.exclude(galaxy_name__in = galaxy_names)
        if len(none_classfied_galaxy) == 0:
            raise Exception("无未分类 galaxy ")
        # 挑选出 classify_num < hope_classify_num的galaxy的
        none_classfied_galaxy = none_classfied_galaxy.filter(classify_num__lt=F('hope_classify_num'))
        if len(none_classfied_galaxy) == 0:
            raise Exception("所有 galaxy 已满足分类次数")
    # 分配特定galaxy
    else:
        try:
            none_classfied_galaxy = Galaxies.objects.get(galaxy_name=galaxy_name)
        except Exception as e:
            raise Exception("galaxy {} 不存在".format(galaxy_name))
    # 返回第一个galaxy
    return_objects = none_classfied_galaxy.first()
    galaxy_info['galaxy_name'] = return_objects.galaxy_name
    galaxy_info['raj'] = return_objects.raj
    galaxy_info['decj']= return_objects.decj
    galaxy_info['url'] = 'hppt:...test_url.com'
    return galaxy_info


# 检查分类是否有效并保存
def check_classfy_results(classify_info):
    response = {}
    # 检查用户权限 检查用户是否存在
    try:
        obj_user = Profile.objects.get(username=classify_info['username'])
    except Exception as e:
        raise Exception('{} 用户不存在'.format(classify_info['username']))
    #检查galaxy分类次数 检查galaxy是否存在
    try:
        obj_galaxy = Galaxies.objects.get(galaxy_name=classify_info['galaxy_name'])
    except Exception as e:
        raise Exception('{} galaxy不存在'.format(classify_info['galaxy_name']))
    #检查是否已经给该用户分类了
    classify_id =  classify_info['username']+'_'+classify_info['galaxy_name']
    record = UserClassifyRecord.objects.filter(classify_id=classify_id)
    if len(record) != 0:
        raise Exception('{}目标已被您分类了'.format(record[0].galaxy_name))
    #检查分类次数是否足够
    if obj_galaxy.classify_num > obj_galaxy.hope_classify_num:
        raise Exception("{}分类次数{}>期望次数{}".format(obj_galaxy.galaxy_name,obj_galaxy.classify_num,obj_galaxy.hope_classify_num))
    
    new_classfy_obj = UserClassifyRecord(classify_id=classify_id,galaxy_name=classify_info['galaxy_name'],username=classify_info['username'],type1=classify_info['type1'])
    new_classfy_obj.save()
    obj_galaxy.classify_num = obj_galaxy.classify_num + 1
    obj_galaxy.save()
    response['results'] = '结果已保存'
    response['msg'] = success
    return response

# ======================================================================
# Create your views here. return image url
@require_http_methods(["POST"])
def requry_image(request):
    response = {}
    try:
        response = authenticate_check(request)
        if response['auth'] == True: # check out
            galaxy_info = get_galaxy_info(response['username'])
            response.update(galaxy_info)
            response['msg'] = success
        else:
            raise Exception("authenticate check fails")
    except Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)


#return classify results
@require_http_methods(["POST"])
def classify_result(request):
    response, keys = {}, ['username','galaxy_name','type1']
    try:
        response = authenticate_check(request)
        if response['auth'] == True: # check out
            # save results
            classify_info = data_flow(request,keys)
            results = check_classfy_results(classify_info)
            response.update(results)
            response['msg'] = success
        else:
            raise Exception("authenticate check fails")
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

