from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from blog import settings
# Create your views here.

def my_picture(request,username):
    if username:
        user = UserProfile.objects.get(username=username)
        if not user:
            result = {"code": 208, "error": "no user"}
            return JsonResponse(result)
        photos = Image.objects.all()
        photos_list = []
        for i in photos:
            photos_list.append("http://127.0.0.1:8000"+settings.MEDIA_URL+str(i.img))


        result = {"code": 200, "username": username, "data": {"sign": user.sign,
                                                              "avatar": str(user.avatar),
                                                              "nickname": user.nickname,
                                                              "info":photos_list
                                                              }}
        return JsonResponse(result)
def uploadpicture(request, username):
    if request.method != "POST":
        result = {"code": 212, "error": "i need POST"}
        return JsonResponse(result)
    file_img = request.FILES.get("avatar")
    if not file_img:
        result = {"code": 212, "error": "i need avatar"}
        return JsonResponse(result)
    album_info = Image()
    album_info.img = file_img
    album_info.user_id = username
    try:
        album_info.save()
        print(file_img,username)
        result = {"code": 200, "error": "OK"}
        return JsonResponse(result)
    except Exception as e:
        print(e)
        result = {"code": 200, "error": "NO database error.........."}
        return JsonResponse(result)