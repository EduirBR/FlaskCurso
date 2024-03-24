from core import create_app

app = create_app()

if __name__ == '__main__':
    print('URIS:\n',app.url_map)
    app.run()
