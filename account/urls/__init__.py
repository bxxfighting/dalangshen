from account.urls import user
from account.urls import asset


urlpatterns = user.urlpatterns + \
              asset.urlpatterns
