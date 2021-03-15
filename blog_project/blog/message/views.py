from django.http import JsonResponse
from django.shortcuts import render
import json
from tools.login_check import login_check
from topic.models import Topic
from message.models import Message


# Create your views here.
@login_check("POST")
def messages(request, topic_id):
    if not request.method != "post":
        result = {"code": 401, "error": "Please use POST"}
        return JsonResponse(result)
    # 發表留言/回覆
    # 獲取用戶
    user = request.user
    json_str = request.body
    json_obj = json.loads(json_str)
    content = json_obj.get('content')
    if not content:
        result = {"code": 402, "error": "Please give me content"}
        return JsonResponse(result)
    parent_id = json_obj.get('parent_id', 0)
    try:
        topic = Topic.objects.get(id=topic_id)
    except:
        # Topic被刪除了or 當前topic_id不存在
        result = {"code": 403, "error": "NO Topic!"}
        return JsonResponse(result)

    # 私有的部落客只能版主留言
    if topic.limit == "private":
        # 檢查身份
        if user.username != topic.author.username:
            result = {"code": 404, "error": "Please get out!"}
            return JsonResponse(result)
    print(content)
    Message.objects.create(conten=content, publisher=user, topic=topic, parent_message=parent_id)
    return JsonResponse({"code": 200, "data": {}})
