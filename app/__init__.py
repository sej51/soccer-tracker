from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)

    return app