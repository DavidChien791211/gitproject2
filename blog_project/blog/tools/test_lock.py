"""
    模擬30個用戶像8000跟8001端口隨機發請求
"""
from threading import Thread
import random
import requests


# 線程事件函數
def get_request():
    """
        隨機向8000或8001發送請求
    :return:
    """
    url1 = "http://127.0.0.1:8000/test/"
    url2 = "http://127.0.0.1:8001/test/"
    url = random.choice([url1, url2])
    # 發請求 - 在瀏覽器地址欄輸入 url 敲 enter
    requests.get(url)

t_list=[]

for i in range(30):
    t = Thread(target=get_request)
    t_list.append(t)
    t.start()

for t in t_list:
    t.join()