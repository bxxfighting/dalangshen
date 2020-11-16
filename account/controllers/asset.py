from django.db import transaction
from django.db.models import Q

from base import errors
from base import controllers as base_ctl
from account.models import AssetModel
from utils.onlyone import onlyone


@onlyone.lock(AssetModel.model_sign, 'name', 'name', 30)
def create_asset(name, password, remark, operator):
    '''
    创建资产
    '''
    query = {
        'user_id': operator.id,
        'name': name,
    }
    obj = AssetModel.objects.filter(**query).first()
    if obj:
        raise errors.CommonError('资产已存在')
    data = {
        'user_id': operator.id,
        'name': name,
        'password': password,
        'remark': remark,
    }
    obj = base_ctl.create_obj(AssetModel, data, operator)
    data = obj.to_dict()
    return data


@onlyone.lock(AssetModel.model_sign, 'obj_id', 'obj_id', 30)
def update_asset(obj_id, name, password, remark, operator):
    '''
    编辑资产
    '''
    obj = base_ctl.get_obj(AssetModel, obj_id)
    if obj.user_id != operator.id:
        raise errors.CommonError('数据异常')
    data = {
        'name': name,
        'password': password,
        'remark': remark,
    }
    obj = base_ctl.update_obj(AssetModel, obj_id, data, operator)
    data = obj.to_dict()
    return data


@onlyone.lock(AssetModel.model_sign, 'obj_id', 'obj_id', 30)
def delete_asset(obj_id, operator):
    '''
    删除资产
    '''
    obj = base_ctl.get_obj(AssetModel, obj_id)
    if obj.user_id != operator.id:
        raise errors.CommonError('数据异常')
    base_ctl.delete_obj(AssetModel, obj_id, operator)


def get_asset(obj_id, operator=None):
    '''
    获取资产信息
    '''
    obj = base_ctl.get_obj(AssetModel, obj_id)
    data = obj.to_dict()
    return data


def get_assets(keyword, page_num, page_size, operator):
    '''
    获取资产列表
    '''
    query = {
        'user_id': operator.id,
    }
    base_query = AssetModel.objects.filter(**query)
    if keyword:
        base_query = base_query.filter(name__icontains=keyword)
    base_query = base_query.order_by('-id')
    total = base_query.count()
    if page_num and page_size:
        end = page_num * page_size
        start = end - page_size
        base_query = base_query[start:end]
    objs = base_query.all()
    data_list = [obj.to_dict() for obj in objs]
    data = {
        'total': total,
        'data_list': data_list,
    }
    return data
