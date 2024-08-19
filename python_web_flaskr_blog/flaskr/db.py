import sqlite3

import click
# current_app 是一个特殊的对象，它指向处理请求的 Flask 应用
# 当应用被创建并且正在处理一个请求时，get_db 将会被调用，所以可以使用 current_app
# g 是一个特殊的对象，它对每一个请求都是唯一的，g 用来存储可能会被多个函数访问的数据
# 如果 get_db 在同一个请求中被二次调用，该连接会被存储和复用，而不是创建一个新的连接
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        # sqlite3.connect() 建立一个连接到配置键 DATABASE 指向的文件，这个文件在初始化数据库时会被创建
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row 告诉这个连接返回行为和字典一样的行，这允许你通过名称访问列
        g.db.row_factory = sqlite3.Row

    return g.db


# 检查一个连接是否被创建
def close_db(e=None):
    db = g.pop('db', None)

    # 如果连接存在，它将被关闭
    if db is not None:
        db.close()
        # 接下来，你将会在应用工厂里把 close_db 函数引入你的应用，以便在每个请求之后调用它


def init_db():
    db = get_db()

    # open_resource() 打开 schema.sql
    with current_app.open_resource('schema.sql') as f:
        # 运行 schema.sql 中 SQL 的命令
        db.executescript(f.read().decode('utf8'))


# click.command() 定义了一个名为 init-db 的命令行命令，这个命令会调用 init_db 函数并向用户显示一个成功消息
@click.command('init-db')
@with_appcontext
def init_db_command():
    """清空已经存在的数据并创建新的数据表"""
    init_db()
    click.echo('Initialized the database.')


# close_db 和 init_db_command 函数需要被注册到应用实例里
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

