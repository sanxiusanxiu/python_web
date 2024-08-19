# __init__.py 主要用于告诉 Python，flaskr 目录应该被看做一个包
# 在这里 __init__.py 将包含应用工厂（在一个函数里创建 Flask 类实例，应用所需要的任何配置都将在这个函数里进行，然后应用会被返回）

import os

from flask import Flask


# 应用工厂函数
def create_app(test_config=None):
    # 创建并配置应用，
    # __name__ 是当前 Python 模块的名称，
    # ？instance_relative_config=True 设置了配置文件的位置是相对于实例文件夹 python_web_flaskr_blog
    app = Flask(__name__, instance_relative_config=True)
    # 默认配置
    app.config.from_mapping(
        # 保持数据安全
        SECRET_KEY='dev',
        # 保存 SQLite 数据库文件的路径
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # 如果实例文件夹里存在config.py，就使用 config.py 覆写默认配置
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # 确保 app.instance_path 指向的路径存在
    # Flask 不会自动创建实例文件夹，但它需要被创建，因为你的项目将在那里创建 SQLite 数据库文件
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 创建一个简单的路由
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # 在工厂里导入并调用这个函数（注册 close_db 和 init_db_command 函数）
    from . import db
    db.init_app(app)

    # 导入并使用 app.register_blueprint() 注册认证蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    # 导入并注册 博客 蓝图
    from . import blog
    app.register_blueprint(blog.bp)
    # app.add_url_rule() 把端点名 index 和 / 关联到一起
    app.add_url_rule('/', endpoint='index')

    return app
