from flask import Flask
from config import config
import pymysql


def create_app(config_name):
    # 初始化实例
    app = Flask(__name__, instance_relative_config=True)
    # 导入配置
    app.config.from_object(config[config_name])
    app.config.from_pyfile('myConfig.py')

    # 蓝图注册
    from .ac_controller.ac_controller import acController
    app.register_blueprint(acController, url_prefix='/acController')

    @app.route("/")
    def hello():
        return "Hello World!"

    return app
