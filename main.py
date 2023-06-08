import tornado.web
from handlers.view import LoginHandler
from handlers.view import OrderHandler
from tornado_swagger.setup import setup_swagger


# 配置路由
class Application(tornado.web.Application):
    _routes = [
        tornado.web.url(r'/order', OrderHandler),
        tornado.web.url(r'/login', LoginHandler),
    ]

    def __init__(self):
        setup_swagger(self._routes, title='简单标题', description='简单的描述')
        super(Application, self).__init__(self._routes)


if __name__ == '__main__':
    application = Application()
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()
