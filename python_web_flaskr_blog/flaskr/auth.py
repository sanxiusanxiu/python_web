# Flaskr 将会有两个蓝图，一个用于认证相关的函数，一个用于博客帖子相关的函数

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


# 创建一个名为 auth 的 Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


# @bp.route 把 URL /register 关联到 register 视图函数
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # 如果用户提交了表单，request.method 会是 POST ，在这种情况下，视图开始验证输入的数据
    if request.method == 'POST':
        # request.form 是一个特殊类型的 dict，它映射提交的表单键到相应的值
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # 验证 username 和 password 不为空
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # 如果验证通过，执行 SQL ，将 username 和 password 插入数据表
        if error is None:
            try:
                # generate_password_hash() is used to securely hash the password, and that hash is stored
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                # db.commit() needs to be called afterward to save the changes
                db.commit()
            except db.IntegrityError:
                error = f"用户 {username} 已存在。"
            else:
                # url_for() 根据其名称生成到 login 视图的 URL
                # redirect() 生成一个重定向响应到生成的 URL
                return redirect(url_for("auth.login"))

        # flash() 会存储消息，这些消息可以在渲染模板时被获取
        flash(error)

    return render_template('auth/register.html')


# @bp.route 把 URL /login 关联到 login 视图函数
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # 查询用户，并存储到一个变量供后面使用
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '无效的用户名。'
        # check_password_hash() 以存储散列值时相同的方式为提交的密码计算散列值，并对它们进行安全对比，就是验证密码的
        elif not check_password_hash(user['password'], password):
            error = '密码错误。'

        if error is None:
            # session 是一个 dict，用来存储跨请求的数据
            # 验证成功后，用户的 id 被存储到一个新的 session，数据存储到浏览器的 cookie 中，浏览器会在后续的请求中把 cookie 发送回来
            # Flask 对数据进行安全签名，使其无法被篡改
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# bp.before_app_request() 注册一个函数并让它在每一个视图函数之前运行，不管请求发到哪一个 URL
@bp.before_app_request
# load_logged_in_user 检查用户的 ID 是否存储在 session 中
# 并从数据库中获取对应用户的数据，将其存储到 g.user 上（它存在于单个请求的生命周期内）
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# 如果要退出，就需要从 session 中移除用户 ID，这样 load_logged_in_user 就不会在后续请求中加载用户
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    # 创建、编辑和删除博客帖子将需要用户登录才能操作，可以使用一个 装饰器 来为每一个使用它的视图检查登录状态
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
