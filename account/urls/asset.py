from django.urls import path

from account.apis import asset as asset_api


urlpatterns = [
    path('asset/', asset_api.AssetApi.as_view()),
    path('asset/list/', asset_api.ListAssetApi.as_view()),
    path('asset/create/', asset_api.CreateAssetApi.as_view()),
    path('asset/update/', asset_api.UpdateAssetApi.as_view()),
    path('asset/delete/', asset_api.DeleteAssetApi.as_view()),
]
