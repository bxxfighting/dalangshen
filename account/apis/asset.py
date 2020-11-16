from base.api import BaseApi
from account.controllers import asset as asset_ctl


class AssetApi(BaseApi):
    need_params = {
        'obj_id': ('资产ID', 'required int'),
    }

    def post(self, request, params):
        data = asset_ctl.get_asset(**params)
        return data


class CreateAssetApi(BaseApi):
    need_params = {
        'name': ('名称', 'required str 128'),
        'password': ('密码', 'optional str 128'),
        'remark': ('备注', 'optional str 1024'),
    }
    def post(self, request, params):
        print(params)
        data = asset_ctl.create_asset(**params)
        return data


class UpdateAssetApi(BaseApi):
    need_params = {
        'obj_id': ('资产ID', 'required int'),
        'name': ('名称', 'required str 128'),
        'password': ('密码', 'optional str 128'),
        'remark': ('备注', 'optional str 1024'),
    }
    def post(self, request, params):
        data = asset_ctl.update_asset(**params)
        return data


class DeleteAssetApi(BaseApi):
    need_params = {
        'obj_id': ('资产ID', 'required int'),
    }
    def post(self, request, params):
        data = asset_ctl.delete_asset(**params)
        return data


class ListAssetApi(BaseApi):
    need_params = {
        'keyword': ('关键词', 'optional str 16'),
        'page_num': ('页码', 'optional int'),
        'page_size': ('页容量', 'optional int'),
    }
    def post(self, request, params):
        data = asset_ctl.get_assets(**params)
        return data
