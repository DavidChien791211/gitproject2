import json

from django.http import JsonResponse

from message import models
from tools.login_check import login_check, get_user_by_request
from user.models import UserProfile
# Create your views here.
from .models import Topic
from message.models import Message


@login_check("POST", "DELETE")
def topics(request, author_id):
    if request.method == "GET":
        # 獲取用戶部落格數據
        # http://127.0.0.1:5000/<username>/topics
        # author_id 被訪問的部落客的版主用戶名
        # visitor 訪客『1.登錄了 2.未登入』
        # author 版主
        authors = UserProfile.objects.filter(username=author_id)
        if not authors:
            result = {"code": 308, "error": "no author"}
            return JsonResponse(result)
        author = authors[0]

        # visitor 訪客
        visitor = get_user_by_request(request)
        visitor_name = None
        if visitor:
            visitor_name = visitor.username

        t_id = request.GET.get("t_id")
        if t_id:
            # 是否為自己訪問自己
            is_self = False
            t_id = int(t_id)
            if author_id == visitor_name:
                is_self = True
                print(is_self)
                # 版主訪問自己
                try:
                    author_topic = Topic.objects.get(id=t_id)
                except Exception as e:
                    result = {"code": 312, "error": "no topic"}
                    return JsonResponse(result)
            else:
                try:
                    author_topic = Topic.objects.get(id=t_id, limit="public")
                except Exception as e:
                    result = {"code": 313, "error": "no topic!"}
                    return JsonResponse(result)
            res = make_topic_res(author, author_topic, is_self)
            return JsonResponse(res)
        else:
            category = request.GET.get("category")
            if category in ["tec", "no-tec"]:
                # /v1/topics/<author_id>？category=[tec|no-tec]
                if author_id == visitor_name:
                    topics = Topic.objects.filter(author_id=author_id, category=category)
                else:
                    topics = Topic.objects.filter(author_id=author_id, category=category, limit="public")
            else:
                # /v1/topics/<author_id>用戶全量數據
                if author_id == visitor_name:
                    # 當前版主訪問自己的部落客 獲取全部數據
                    topics = Topic.objects.filter(author_id=author_id)
                else:
                    # 訪客訪問部落格 指獲取public數據
                    topics = Topic.objects.filter(author_id=author_id, category="tec")
            res = make_topics_res(author, topics)
            return JsonResponse(res)

    elif request.method == "POST":
        # 創建用戶部落格
        json_str = request.body
        if not json_str:
            result = {"code": 301, "error": "Give me json"}
            return JsonResponse(result)
        json_obj = json.loads(json_str)
        title = json_obj.get("title")

        # xss注入防止對方使用javasprict輸入盜取東西
        import html
        # 使用轉義
        title = html.escape(title)
        if not title:
            result = {"code": 302, "error": "Give me title"}
            return JsonResponse(result)
        content = json_obj.get("content")
        if not content:
            result = {"code": 303, "error": "Give me content"}
            return JsonResponse(result)
        # 獲取純文本內容-用於切割文章作為簡介
        content_text = json_obj.get("content_text")
        if not content_text:
            result = {"code": 304, "error": "Give me content_text"}
            return JsonResponse(result)
        # 切割簡介
        introduce = content_text[:30]
        limit = json_obj.get("limit")
        if limit not in ["public", "private"]:
            result = {"code": 305, "error": "Your limit is wrong"}
            return JsonResponse(result)
        category = json_obj.get("category")
        if category not in ["tec", "No-tec"]:
            result = {"code": 306, "error": "Your limit is category"}
            return JsonResponse(result)

        # 創建數據
        Topic.objects.create(title=title, category=category, limit=limit, content=content, introduce=introduce,
                             author=request.user)
        result = {"code": 200, "username": request.user.username}
        return JsonResponse(result)
    elif request.method == "DELETE":
        # token裡存儲的用戶
        author = request.user
        token_author_id = author.username
        # url中傳過來的authorid 必須與token中用戶名相等
        if token_author_id != author_id:
            result = {"code": 309, "error": "you can not do it"}
            return JsonResponse(result)
        delete_id = request.GET.get("topic_id")
        try:
            topic = Topic.objects.get(id=delete_id)
        except:
            result = {"code": 310, "error": "you can not do it!"}
            return JsonResponse(result)
        if topic.author.username != author_id:
            result = {"code": 311, "error": "you can not do it !!"}
            return JsonResponse(result)

        topic.delete()
        res = {"code": 200}
        return JsonResponse(res)
    # delete_id = request.GET["topic_id"]
    # authors = UserProfile.objects.filter(username=author_id)
    # if not authors:
    #     result = {"code": 308, "error": "no author"}
    #     return JsonResponse(result)
    # delete_target = Topic.objects.get(id=delete_id)
    # delete_target.delete()

    return JsonResponse({"code": 200, "error": "this is a test"})


def make_topic_res(author, author_topic, is_self):
    """
        拼接詳情頁 返回的數據
    :param author: 作者的對象
    :param author_topic: 文章的對象
    :param is_self: 是否自己訪問自己
    :return:
    """
    if is_self:
        # 版主訪問自己
        # 取出大於當前文章的id的第一個且author為當前作者的
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
        # 上一篇文章:取出ID小於當前部落客的id的最後一個
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()
    else:
        # 下一篇 考慮 limit = public
        next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit="public").first()
        # 上一篇同上
        last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit="public").last()
    if next_topic:
        next_id = next_topic.id
        print(next_id)
        next_title = next_topic.title
    else:
        next_id = None
        next_title = None
    if last_topic:
        last_id = last_topic.id
        last_title = last_topic.title
    else:
        last_id = None
        last_title = None
    all_message = Message.objects.filter(topic=author_topic).order_by("-created_time")
    # 所有留言
    msg_list = []
    reply_dict = {}
    msg_count = 0
    for msg in all_message:
        msg_count += 1
        if msg.parent_message == 0:
            # 當前留言
            msg_list.append({"id": msg.id,
                             "content": msg.conten,
                             "publisher": msg.publisher.nickname,
                             "publisher_avatar": str(msg.publisher.avatar),
                             "created_time": msg.created_time.strftime("%Y-%m-%d"),
                             "reply": []})
        else:
            # 當前是回覆
            reply_dict.setdefault(msg.parent_message, [])
            reply_dict[msg.parent_message].append({"msg_id": msg.id,
                                                   "content": msg.conten,
                                                   "publisher": msg.publisher.nickname,
                                                   "publisher_avatar": str(msg.publisher.avatar),
                                                   "created_time": msg.created_time.strftime("%Y-%m-%d")})

    # 合併 msg_list 和 reply_dict
    for _msg in msg_list:
        if _msg["id"] in reply_dict:
            _msg["reply"] = reply_dict[_msg["id"]]

    res = {"code": 200, "data": {}}
    res["data"]["nickname"] = author.nickname
    res["data"]["title"] = author_topic.title
    res["data"]["category"] = author_topic.category
    res["data"]["created_time"] = author_topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
    res["data"]["content"] = author_topic.content
    res["data"]["introduce"] = author_topic.introduce
    res["data"]["author"] = author.nickname
    res["data"]["next_id"] = next_id
    res["data"]["next_title"] = next_title
    res["data"]["last_id"] = last_id
    res["data"]["last_title"] = last_title
    # messages暫時數據

    res["data"]["messages"] = msg_list
    res["data"]["messages_count"] = msg_count

    return res


def make_topics_res(author, topics):
    res = {"code": 200, "data": {}}
    data = {}
    data["nickname"] = author.nickname
    topics_list = []
    for topic in topics:
        d = {}
        d["id"] = topic.id
        d["title"] = topic.title
        d["category"] = topic.category
        d["introduce"] = topic.introduce
        d["author"] = author.nickname
        d["created_time"] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
        topics_list.append(d)

    data["topics"] = topics_list
    res['data'] = data
    return res
