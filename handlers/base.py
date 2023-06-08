import tornado.web
from settings import secret_key
import jwt


# 进行预设 继承tornado的RequestHandler
class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        super(BaseHandler, self).prepare()

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    # def set_default_headers(self):
    #     super().set_default_headers()


# 进行token校验，继承上面的BaseHandler
class TokenHandler(BaseHandler):

    def prepare(self):
        """
        通过Authorization请求头传递token
        :return:
        """
        head = self.request.headers
        token = head.get("Authorization", "")
        data = {'status': False, 'code': 200}
        try:
            # 解析 JWT 并校验是否过期
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            username = payload.get("sub")
            data['data'] = {
                'username': username
            }
        except jwt.exceptions.ExpiredSignatureError as err:
            data.update({'code': 403, 'error': 'token过期'})
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError) as e:
            data.update({'code': 201, 'error': '签名验证失败'})
        except Exception as e:
            data.update({'code': 500, 'error': str(e)})
        self.data = data


