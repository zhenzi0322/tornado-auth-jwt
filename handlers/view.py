import json
from utils import jwt_auth
from handlers import base
from tornado_swagger.model import register_swagger_model
from tornado_swagger.parameter import register_swagger_parameter


@register_swagger_model
class SuccessPostModel:
    """
    ---
    type: object
    description: Post model representation
    properties:
        status:
            type: boolean
            default: true
        code:
            type: integer
        data:
            type: object
            properties:
                username:
                    type: string
    """


@register_swagger_model
class Post403Model:
    """
    ---
    type: object
    description: Post model representation
    properties:
        status:
            type: boolean
            default: false
        code:
            type: integer
            default: 403
        error:
            type: string
    """


class LoginHandler(base.BaseHandler):
    def post(self, *args, **kwargs):
        name = self.get_argument("username")
        pwd = self.get_argument("password")
        if name == "admin" and pwd == "admin":
            # 用户名密码正确 给用户生成token并返回
            token = jwt_auth.create_token(name)
            msg = {'username': name, 'token': token}
            self.write(json.dumps(msg, ensure_ascii=False))
        else:
            msg = json.dumps({'error': '账号或密码错误'}, ensure_ascii=False)
            self.write(msg)


@register_swagger_model
class OrderHandler(base.TokenHandler):

    def get(self):
        if self.data.get('status'):
            # 验证通过,处理业务逻辑
            self.write(self.data)
        else:
            self.set_status(self.data.get('code'))
            self.write(self.data)

    def post(self, *args, **kwargs):
        """
        ---
        tags:
        - 订单模块
        summary: 简单的描述summary
        description: 文档的描述
        produces:
        - application/json
        security:
        - OAuth2: [admin]   # Use OAuth with a different scope
        responses:
            200:
                description: 正确的响应
                schema:
                    $ref: '#/definitions/SuccessPostModel'
            201,403,500:
                description: 失败的响应
                schema:
                    $ref: '#/definitions/Post403Model'
        """
        if self.data.get('status'):
            # 验证通过,处理业务逻辑
            self.write(self.data)
        else:
            self.set_status(self.data.get('code'))
            self.write(self.data)
