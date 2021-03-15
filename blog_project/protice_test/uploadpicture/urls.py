from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.picture_album),
    url(r'^/upload_picture',views.picture_album),
    url('^/upload_img/', views.img_upload),
    url('^/show_picture/', views.show_picture)
]