from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def base(request, username=None):
    result = {"code": 200, "username": username,"data": {"nickname": username}}
    return JsonResponse(result)
