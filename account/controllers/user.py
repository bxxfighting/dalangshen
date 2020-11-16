from django.db import transaction
from django.db.models import Q

from base import errors
from base import controllers as base_ctl
from account.models import UserModel
from utils.onlyone import onlyone


def login(username, password):
    '''
    登录
    '''
    base_query = UserModel.objects.filter(username=username)
    obj = base_query.first()
    if not obj:
        raise errors.CommonError('用户名或密码错误')
    if not obj.check_password(password):
        raise errors.CommonError('用户名或密码错误')
    if obj.status == UserModel.ST_FORBIDDEN:
        raise errors.CommonError('用户已被禁止登录')
    data = {
        'token': obj.gen_token(),
    }
    return data


@onlyone.lock(UserModel.model_sign, 'username', 'username', 30)
def create_user(username, password, name=None, phone=None, email=None, operator=None):
    '''
    创建用户
    '''
    user_obj = UserModel.objects.filter(username=username).first()
    if user_obj:
        raise errors.CommonError('用户已存在')
    data = {
        'username': username,
        'name': name,
        'phone': phone,
        'email': email,
    }
    with transaction.atomic():
        user_obj = base_ctl.create_obj(UserModel, data, operator)
        if not password:
            password = '123456'
        user_obj.set_password(password)
    data = user_obj.to_dict()
    return data


@onlyone.lock(UserModel.model_sign, 'obj_id', 'obj_id', 30)
def update_user(obj_id, name=None, password=None, phone=None, email=None, operator=None):
    '''
    编辑用户
    '''
    obj = base_ctl.get_obj(UserModel, obj_id)
    if not obj:
        raise errors.CommonError('用户不存在')
    if is_admin(obj):
        raise errors.CommonError('超级管理员用户不允许编辑')
    data = {
        'name': name,
        'phone': phone,
        'email': email,
    }
    with transaction.atomic():
        user_obj = base_ctl.update_obj(UserModel, obj_id, data, operator)
        if password:
            user_obj.set_password(password)
    data = user_obj.to_dict()
    return data


@onlyone.lock(UserModel.model_sign, 'obj_id', 'obj_id', 30)
def delete_user(obj_id, operator=None):
    '''
    删除用户
    '''
    obj = base_ctl.get_obj(UserModel, obj_id)
    if is_admin(obj):
        raise errors.CommonError('超级管理员用户不允许删除')

    with transaction.atomic():
        base_ctl.delete_obj(UserModel, obj_id, operator)


def get_user(obj_id, operator=None):
    '''
    获取用户信息
    '''
    obj = base_ctl.get_obj(UserModel, obj_id)
    data = obj.to_dict()
    return data
