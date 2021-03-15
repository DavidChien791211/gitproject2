from django.shortcuts import render
import time
import hashlib
from user.models import UserProfile
import json
from django.http import JsonResponse


# Create your views here.


def tokens(request):
    """
        創建token
    :param request:
    :return:
    """
    if not request.method == "POST":
        result = {'code': 101, 'error': "Please use POST"}
        return JsonResponse(result)

    json_str = request.body
    if not json_str:
        result = {"code": 102, "error": "Please give me json"}
        return JsonResponse(result)

    json_obj = json.loads(json_str)
    username = json_obj.get("username")
    if not username:
        result = {"code": 103, "error": "Please give me username"}
        return JsonResponse(result)
    password = json_obj.get("password")
    if not username:
        result = {"code": 104, "error": "Please give me password"}
        return JsonResponse(result)

    m = hashlib.md5()
    m.update(password.encode())
    try:
        UserProfile.objects.get(username=username, password=m.hexdigest())
    except Exception as e:
        result = {"code": 104, "error": "username or password is wrong!!"}
        return JsonResponse(result)
    token = make_token(username)
    result = {"code": 200, "username": username, "data": {"token": token.decode()}}
    return JsonResponse(result)

    # 獲取前端數據的數據/生成token
    # 獲取-驗證密碼-生成token


def make_token(username, expire=3600 * 24):
    # 官方jwt/字定義JWT
    import jwt
    key = '1234567'
    now = time.time()
    payload = {"username": username, "exp": int(now + expire)}
    return jwt.encode(payload, key, algorithm="HS256")
