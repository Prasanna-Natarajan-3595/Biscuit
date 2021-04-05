from flask import Flask

def create_app():
    from .view import view
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '*$@&*(%@(*YHFRUFHOWUHO*@$(FHSUkgfauguo'
    app.register_blueprint(view, url_prefix='/')
    return app