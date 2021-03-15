from django.shortcuts import render
from django.http import JsonResponse
from .models import Image
from protice_test import settings


# Create your views here.
def picture_album(request):
    return render(request, "mypicture.html")


def show_picture(request):
    photos = Image.objects.all()
    photos_list = []
    for i in photos:
        photos_list.append(settings.MEDIA_URL+str(i.img))
    result = {"code":200,"data":photos_list}
    return JsonResponse(result)


def img_upload(request):
    file_img = request.FILES['img']  # 获取文件对象
    image = Image()
    image.img = file_img
    try:
        image.save()  # 保存数据
        return JsonResponse(1, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse(0, safe=False)

