import time
import aiofiles
import json
import os

from typing import Union
from aiohttp.web import Request, Response, FileResponse, HTTPNotFound
from models.book import Book
from models.book import Session
from views.validators.book import validate_book_create_data, validate_get_books_params, validate_get_book_param


async def create_book(request: Request) -> Response:
    data = await request.post()
    await validate_book_create_data(data)
    db = Session()

    name = data['name']
    author = data['author']
    genre = data['genre']
    file = data['file']
    timestamp = int(time.time())
    file_name = f'{timestamp}_{file.filename}'
    file_path = f'uploads/books/{file_name}'

    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file.file.read())

    book = Book(name=name, author=author, genre=genre, file_path=file_path)

    try:
        db.add(book)
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

    return Response(text=f"{name} by {author} created successfully", status=201)


async def get_books(request: Request) -> Response:
    params = request.query
    await validate_get_books_params(params)

    db = Session()

    query = db.query(Book)
    for key, value in params.items():
        query = query.filter(getattr(Book, key) == value)

    books = query.all()
    db.close()

    books_data = [{'id': book.id, 'name': book.name, 'author': book.author,
                   'date_published': book.date_published.strftime('%Y-%m-%d'),
                   'genre': book.genre, 'file_path': book.file_path} for book in books]
    response_data = json.dumps(books_data, ensure_ascii=False)

    return Response(text=response_data, content_type='application/json')


async def get_book_by_id(request: Request) -> Union[Response, FileResponse]:
    book_id = request.match_info.get('id')
    download_param = True if request.query.get('download') == 'true' else False
    await validate_get_book_param(request)
    db = Session()
    book = db.query(Book).filter_by(id=book_id).first()
    db.close()

    if not book:
        return HTTPNotFound(text=f'Book with ID {book_id} not found')

    file_path = book.file_path
    if not os.path.isfile(file_path):
        return HTTPNotFound(text='File not found')

    if download_param:
        return FileResponse(file_path, headers={'Content-Disposition': f'attachment; filename={file_path}'})
    else:
        async with aiofiles.open(file_path, 'rb') as file:
            file_content = await file.read()
        return Response(body=file_content, content_type='application/pdf')
