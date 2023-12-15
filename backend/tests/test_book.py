import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
from views.book import create_book, get_books, get_book_by_id
from models.book import Book, Base
from sqlalchemy.orm import sessionmaker
from aiohttp.web_app import Application
import os


class BookAPITestCase(AioHTTPTestCase):
    async def get_application(self) -> Application:
        app = web.Application()
        app.router.add_post('/create_book', create_book)
        app.router.add_get('/get_books', get_books)
        app.router.add_get('/get_book/{id}', get_book_by_id)
        self.engine = engine_test
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        return app

    async def tearDownAsync(self) -> None:
        async with self.engine.connect() as conn:
            await conn.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA public;')

    async def test_create_book(self):
        # Create a test PDF file
        pdf_content = b'%PDF-1.4\n1 0 obj\n<< /Title (Test Book) /Author (Test Author) >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF'

        data = {'name': 'Test Book', 'author': 'Test Author', 'genre': 'Fiction'}
        files = {'file': ('test_book.pdf', pdf_content, 'application/pdf')}

        response = await self.client.post('/create_book', data=data, headers={'Content-Type': 'multipart/form-data'}, files=files)

        self.assertEqual(response.status, 201)

        async with self.Session() as session:
            books = session.query(Book).filter_by(name='Test Book').all()
            self.assertEqual(len(books), 1)
            book = books[0]
            self.assertEqual(book.author, 'Test Author')
            self.assertEqual(book.genre, 'Fiction')

        self.assertTrue(os.path.isfile(f'uploads/books/{book.file_path}'))

    async def test_get_books(self):
        async with self.Session() as session:
            book = Book(name='Test Book', author='Test Author', genre='Fiction')
            session.add(book)
            session.commit()

        response = await self.client.get('/get_books?author=Test Author')

        self.assertEqual(response.status, 200)

        data = await response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Book')

    async def test_get_book_by_id(self):
        async with self.Session() as session:
            book = Book(name='Test Book', author='Test Author', genre='Fiction')
            session.add(book)
            session.commit()

        response = await self.client.get(f'/get_book/{book.id}')

        self.assertEqual(response.status, 200)

        data = await response.json()
        self.assertEqual(data['name'], 'Test Book')
        self.assertEqual(data['author'], 'Test Author')


if __name__ == '__main__':
    import unittest
    unittest.main()