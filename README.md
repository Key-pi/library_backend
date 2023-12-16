just run setup_project file 

sh setup_project.sh

after setup_project
run docker-compose up


!TESTS NIT IMPLEMENTATION!(

    app.router.add_post('/create_book', create_book) 
    app.router.add_get('/get_books', get_books) : allow params - download=true or false or without params. 
    app.router.add_get('/get_book/{id}', get_book_by_id) : allowed params - name, genre, author
