from django.db import models
from django.core.signing import TimestampSigner
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from base.models import BaseModel


class UserModel(BaseModel):
    '''
    用户表
    '''
    model_name = '用户'
    model_sign = 'user'

    ST_NORMAL = 10
    ST_FORBIDDEN = 20
    ST_CHOICES = (
        (ST_NORMAL, '正常'),
        (ST_FORBIDDEN, '禁用'),
    )

    username = models.CharField('账户', max_length=128)
    password = models.CharField('密码', max_length=256)
    name = models.CharField('姓名', max_length=128, default='')
    email = models.CharField('邮箱', max_length=128, null=True, default='')
    phone = models.CharField('联系方式', max_length=64, null=True, default='')
    status = models.IntegerField('状态', choices=ST_CHOICES, default=ST_NORMAL)

    class Meta:
        db_table = 'user'

    def to_dict(self):
        '''
        用户信息，不返回密码
        '''
        data = super().to_dict()
        data.pop('password')
        return data

    def set_password(self, password):
        '''
        设置密码
        '''
        self.password = make_password(password)
        self.save()

    def check_password(self, password):
        '''
        校验密码
        '''
        return check_password(password, self.password)

    def gen_token(self):
        '''
        生成接口认证的token
        '''
        signer = TimestampSigner()
        token = signer.sign(self.id)
        return token


class AssetModel(BaseModel):
    '''
    资产表
    '''
    model_name = '资产'
    model_sign = 'asset'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=128, default='')
    password = models.CharField('密码', max_length=256)
    remark = models.TextField('说明', default='', null=True)

    class Meta:
        db_table = 'asset'
