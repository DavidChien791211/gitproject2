from django.conf.urls import url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/v1/user
    url(r'^$', views.users),
    # http://127.0.0.1:8000/v1/user/<username>
    # APPEND_SLASH 自動補全URL後面會自動補上/
    url(r'^/(?P<username>[\w]{1,11})$',views.users),
    url(r'^/(?P<username>[\w]{1,11})/avatar$',views.user_avatar)
]
