from aiohttp import web
from routes import setup_routes


def init_app() -> web.Application:
    app = web.Application()
    setup_routes(app)
    return app


if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=8080)