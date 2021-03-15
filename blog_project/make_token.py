import base64
import json
import time
import copy
import hmac


class Jwt():
    def __init__(self):
        pass

    @staticmethod
    def decode(token, key):
        # 老師版
        header_bs, paload_bs, sing_bs = token.split(b'.')
        if isinstance(key, str):
            key.encode()
        hm = hmac.new(key, header_bs + b'.' + paload_bs)
        if sing_bs != Jwt.b64encode(hm.digest()):
            raise
        payload_js = Jwt.b64encode(paload_bs)
        payload = json.loads(payload_js)

        if "exp" in payload:
            now = time.time()
            if now > payload['exp']:
                raise
        return payload

        # 驗證簽名 我的方法
        # result = token.decode().split(".")
        # header = result[0].encode()
        # payload = result[1].encode()
        # hm = hmac.new(key.encode(), header + b'.' + payload, digestmod="SHA256")
        # sign_bs = Jwt.b64encode(hm.digest())
        # if sign_bs == result[2].encode():
        #     print("一樣")
        # # 檢查exp是否過期
        # payload = Jwt.b64decode(payload).decode()
        # payload= json.loads(payload)
        # if payload["exp"] < time.time():
        #     print("超過時間")
        #
        # return payload

    @staticmethod
    def b64encode(content):
        return base64.urlsafe_b64encode(content).replace(b'=', b'')

    @staticmethod
    def b64decode(test_data):
        sem = len(test_data) % 4
        if sem > 0:
            test_data += b'=' * (4 - sem)
        # while len(test_data) % 4 != 0:
        #     test_data += (b'=')
        return base64.urlsafe_b64decode(test_data)

    @staticmethod
    def encode(payload, key, exp=300):
        header = {"alg": "HS256", "typ": "JWT"}
        header_json = json.dumps(header, separators=(',', ':'), sort_keys=True)
        header_bs = Jwt.b64encode(header_json.encode())

        payload_self = copy.deepcopy(payload)
        if not isinstance(exp, int) and not isinstance(exp, str):
            raise TypeError("Exp must be int or str！")
        payload_self["exp"] = time.time() + int(exp)
        payload_js = json.dumps(payload_self, separators=(",", ":"), sort_keys=True)
        payload_bs = Jwt.b64encode(payload_js.encode())

        if isinstance(key, str):
            key = key.encode()
        hm = hmac.new(key, header_bs + b'.' + payload_bs, digestmod="SHA256")
        sign_bs = Jwt.b64encode(hm.digest())

        return header_bs + b'.' + payload_bs + b'.' + sign_bs


if __name__ == "__main__":
    token = Jwt.encode({"user": "slash"}, "guitar", 300)
    print(token)
    print(Jwt.decode(token, "guitar"))
    # data = Jwt.b64encode(b'aaabbbccc')
    # print(data)
    # result = Jwt.b64decode(data)
    # print(result)
