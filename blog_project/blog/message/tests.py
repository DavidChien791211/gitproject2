from django.test import TestCase

# Create your tests here.
data = [
    {"id": 1, "parnet_message": 0, "content": "我是發表者"},
    {"id": 2, "parnet_message": 1, "content": "我是回覆id號碼1的回覆者"},
    {"id": 3, "parnet_message": 0, "content": "我是發表者"},
    {"id": 4, "parnet_message": 3, "content": "我是回覆id號碼3的回覆者"},
    {"id": 5, "parnet_message": 1, "content": "我是回覆id號碼1的回覆者"},
]

format_data = [
    {
        "id": 0,
        "content": "",
        "reply": [{
            "content": "",
            "msg_id": 0
        }]
    }
]
parent = []
child= {}
def make_json_data(data):

    for message_data in data:
        if message_data["parnet_message"] !=0:
            if message_data["parnet_message"] in child:
                child[message_data["parnet_message"]].append(message_data)
            else:
                child[message_data["parnet_message"]]=[]
                child[message_data["parnet_message"]].append(message_data)
            # child.setdefault(message_data["parnet_message"],[])
        else:
            parent.append(message_data)


make_json_data(data)
for p in parent:
    if p["id"] in child:
        p["reply"] = child[p["id"]]


print(parent)