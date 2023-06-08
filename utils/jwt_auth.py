import jwt
from datetime import datetime, timedelta
from settings import secret_key


def create_token(username):
    """生成token"""
    access_token_expires = timedelta(seconds=60)  # 60秒内有效
    access_token_payload = {"sub": username, "exp": datetime.utcnow() + access_token_expires}
    return jwt.encode(payload=access_token_payload, key=secret_key)


def parse_payload(token):
    """
    检验TOKNE是否过期
    :param token:
    :return:
    """
    try:
        # 解析 JWT 并校验是否过期
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        username = payload.get("sub")
        return username
    except Exception as e:
        print(e)
