from aiohttp.web import HTTPBadRequest, Request


async def validate_book_create_data(data: Request.post) -> None:
    required_fields = {'name', 'author', 'genre', 'file'}

    for field in required_fields:
        if field not in data:
            raise HTTPBadRequest(text=f'Missing required field: {field}')

    file = data['file']

    if not isinstance(data['name'], str):
        raise HTTPBadRequest(text='Invalid name. Name should be a non-empty string')

    if not isinstance(data['author'], str):
        raise HTTPBadRequest(text='Invalid author. Author should be a non-empty string')

    if not isinstance(data['genre'], str):
        raise HTTPBadRequest(text='Invalid genre. Genre should be a non-empty string')

    if not file:
        raise HTTPBadRequest(text='Invalid file. File must not be empty')

    if file.content_type != "application/pdf":
        raise HTTPBadRequest(text='Invalid file. File must be a pdf file')


async def validate_get_books_params(params):
    valid_params = {'name', 'author', 'date_published', 'genre'}

    if params and not all(key in valid_params for key in params.keys()):
        raise HTTPBadRequest(text='Invalid parameters for get_books endpoint')


async def validate_get_book_param(request: Request):
    book_id = request.match_info.get('id')

    if not book_id or not book_id.isdigit():
        raise HTTPBadRequest(text='Invalid Book ID. It should be a non-empty numeric value')

    if request.query:
        if 'download' not in request.query:
            raise HTTPBadRequest(text='Invalid parameter name. Use "download" for the parameter')

        download_param = request.query['download']
        download_param_lower = download_param.lower()

        if download_param_lower not in {'true', 'false'}:
            raise HTTPBadRequest(text='Invalid value for download parameter. Use either "true" or "false"')
