from aiohttp import web
from views.book import create_book, get_books, get_book_by_id


def setup_routes(app: web.Application):
    # book routers
    app.router.add_post('/create_book', create_book)
    app.router.add_get('/get_books', get_books)
    app.router.add_get('/get_book/{id}', get_book_by_id)
