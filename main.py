from core import create_app

if __name__ == '__main__':
    app = create_app()
    print('URIS:\n',app.url_map)
    app.run()
