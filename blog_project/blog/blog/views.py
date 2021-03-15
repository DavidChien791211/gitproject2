from django.http import JsonResponse
from user.models import UserProfile


def test_api(request):
    # 加入分佈式鎖
    import redis
    r = redis.Redis(host="127.0.0.1", port=6379, db=0)
    # 防止鎖取不到所以用循環。
    while True:
        try:
            #給鎖一個key名，3秒沒成功強置解鎖
            with r.lock("onlock", blocking_timeout=3):
                # 對score字段進行+1操作
                u = UserProfile.objects.get(username="slash")
                u.score += 1
                u.save()
            break
        except Exception as e:
            print("lock is failed", e)
    return JsonResponse({"code": 200})
