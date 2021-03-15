from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *
import hashlib
import time
from btoken.views import make_token
from tools.login_check import login_check


# Create your views here.
@login_check("PUT")
def users(request, username=None):
    if request.method == "GET":
        # 獲取用戶數據
        if username:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception as e:
                user = None
                if not user:
                    result = {"code": 208, "error": "no user"}
                    return JsonResponse(result)
            if request.GET.keys():
                # 查詢指定字段
                data = {}
                for k in request.GET.keys():
                    if hasattr(user, k):
                        value = getattr(user, k)
                        if k == "avatar":
                            data[k] = str(value)
                        else:
                            data[k] = value
                result = {"code": 200, "username": username, "data": data}
                return JsonResponse(result)
            else:
                # 全量查詢[]
                result = {"code": 200, "username": username, "data": {"sign": user.sign, "avatar": str(user.avatar),
                                                                      "nickname": user.nickname}}
            return JsonResponse(result)

        else:
            return JsonResponse({"code": 200, "error": "i'am coming GET"})
    elif request.method == "POST":
        # 創建用戶
        # http://127.0.0.1:5000/register發請求過來
        json_str = request.body
        if not json_str:
            result = {"code": 201, "error": "Please give me data"}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        username = json_obj.get("username")
        if not username:
            result = {"code": 202, "error": "Please give me username"}
            return JsonResponse(result)
        email = json_obj.get("email")
        if not email:
            result = {"code": 203, "error": "Please give me email"}
            return JsonResponse(result)
        if not email:
            result = {"code": 203, "error": "Please give me email"}
            return JsonResponse(result)
        password_1 = json_obj.get("password_1")
        password_2 = json_obj.get("password_2")
        if not password_1 or not password_2:
            result = {"code": 204, "error": "Please give me password"}
            return JsonResponse(result)
        if password_1 != password_2:
            result = {"code": 205, "error": "Your password not same"}
            return JsonResponse(result)

        old_user = UserProfile.objects.filter(username=username)
        if old_user:
            result = {"code": 206, "error": "Your username is already existed"}
            return JsonResponse(result)

        m = hashlib.md5()
        m.update(password_1.encode())
        # =======charfield 盡量避免使用 null = True 會多一個字節 ===========
        sign = info = ""
        try:
            UserProfile.objects.create(username=username, nickname=username, email=email, password=m.hexdigest(),
                                       sign=sign,
                                       info=info)
        except Exception as e:
            result = {"code": 207, "error": "Server is busy"}
            return JsonResponse(result)

        token = make_token(username)
        result = {"code": 200, "username": username, "data": {"token": token.decode()}}
        return JsonResponse(result)
        # if request.body:
        #     data = json.loads(request.body)
        #     if not data['username']:
        #         return JsonResponse({'code': 203, 'error': '請入用戶名'})
        #     if not data['email']:
        #         return JsonResponse({'code': 204, 'error': '請入電子郵箱'})
        #     if not data['password_1']:
        #         return JsonResponse({'code': 205, 'error': '請入密碼'})
        #     if data['password_1'] != data['password_2']:
        #         return JsonResponse({'code': 206, 'error': '密碼兩次入不同'})
        #     username = data['username']
        #     import hashlib
        #     m = hashlib.md5()
        #     m.update(username.encode())
        #     s = m.hexdigest()
        # else:
        #     return JsonResponse({'code': 202, 'error': '請入內容'})
        # return JsonResponse({"code": 200, 'username': username, "data": {"token": s}})
    elif request.method == "PUT":
        user = request.user
        json_str = request.body
        if not json_str:
            result = {"code": 209, "error": "Please giveme json"}
            return JsonResponse(result)

        json_obj = json.loads(json_str)
        if 'sign' not in json_obj:
            result = {"code": 210, "error": "no sign"}
            return JsonResponse(result)
        if 'info' not in json_obj:
            result = {"code": 211, "error": "no info"}
            return JsonResponse(result)
        sign = json_obj.get('sign')
        info = json_obj.get('info')
        request.user.sign = sign
        request.user.info = info
        request.user.save()
        result = {'code': 200, "username": request.user.username}
        return JsonResponse(result)
    else:
        raise
    return JsonResponse({"code": 200})


@login_check("POST")
def user_avatar(request, username):
    """
        上傳圖片
    :param request:
    :param username:
    :return:
    """
    if request.method != "POST":
        result = {"code": 212, "error": "i need POST"}
        return JsonResponse(result)
    avatar = request.FILES.get("avatar")
    if not avatar:
        result = {"code": 212, "error": "i need avatar"}
        return JsonResponse(result)
    # TODO 判斷url中的username是否跟token中的username一致，若不一致返回error
    request.user.avatar = avatar
    request.user.save()
    result = {"code": 200, "username": request.user.username}
    return JsonResponse(result)
