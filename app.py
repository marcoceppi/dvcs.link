import tornado.escape
import tornado.ioloop
import tornado.web


class Router(object):
    def __init__(self, base='api', version=1):
        self.version = version
        self.base = base
        self.routes = []

    def add(self, route, call):
        self.routes.append((r"%s" % self._build_url(route), call))

    def _build_base(self):
        return "/%s/%s" % (self.base, self.version)

    def _build_url(self, url):
        if url.startswith('/'):
            url = url[1:]

        return "%s/%s" % (self._build_base(), url)


class APIRouter(tornado.web.RequestHandler):
    def get(self, version=None, route=None):
        self.route(version, route)

    def post(self, version=None, route=None):
        self.route(version, route)

    def route(self, version=None, route=None):
        response = {'version': version,
                    'route': route}
        self.write(response)


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': 'whatever',
                    'route': 'obama'}
        self.write(response)


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({'a': self.get_arguments('fart')})

    def post(self):
        key = self.get_argument('key')
        secret = self.get_argument('secret')

        self.write({'key': key, 'secret': secret})


r = Router()
r.add(r'/version', VersionHandler)
r.add(r'/login', LoginHandler)
# r.add(r'/fart', FartHandler)

if __name__ == "__main__":
    application = tornado.web.Application(r.routes, debug=True)
    application.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
