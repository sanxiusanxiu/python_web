from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# 创建一个名为 blog 的 蓝图
bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    # 索引页面将会显示所有的帖子，最新的博客排在前面，这里使用 JOIN 查询，可以在结果中获取到作者信息
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


# create 视图和认证的 register 视图的工作原理相同
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            # 要么表单被显示，要么提交的数据通过验证并将帖子添加到数据库，否则显示一个错误
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


# update 和 delete 视图都将需要通过 id 获取一个 post，并检查作者是否和登入的用户相匹配
# 为了避免代码重复，可以写一个函数来获取 post，然后在每一个视图里调用它
def get_post(id, check_author=True):
    # check_author 参数的定义可以使该函数可以在不检查作者的情况下获取一个 post
    # 如果你写了一个视图来在页面上显示一个单独的帖子，这个参数将会很有用，在这个页面上用户无关紧要，因为他们并不是在编辑帖子
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    # abort() 将会抛出一个异常，这个异常返回一个 HTTP 状态码
    # 404 表示“Not Found（未找到）”，403 表示“Forbidden（禁止）”，
    # （401 表示“Unauthorized（未授权）”，但是你会重定向到登录页面，而不是返回那个状态码）
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


# update 函数接受一个 id 参数
# 一个真实的 URL 看起来会像 /1/update，Flask 会捕捉到这个 1，确保它是一个 int，并把它作为 id 参数传递
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    # create 和 update 视图看起来非常相似
    # 主要的区别是，update 视图使用一个 post 对象和一个 UPDATE 查询，而不是 INSERT
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


# 删除视图没有自己的模板，删除按钮是 update.html 的一部分，并用来发送请求到 /<id>/delete
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

