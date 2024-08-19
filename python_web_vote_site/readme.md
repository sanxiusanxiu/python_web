### 常用的 Django 命令


##### 创建项目
```text
(venv) PS D:\workspace\python_web\python_web_vote_site> django-admin startproject project_name
```


##### 运行项目
```text
# 浏览器访问 https://127.0.0.1:8000/ 即可
(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py runserver
# 更换服务器的监听端口为8080 
(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py runserver 8080
# 修改服务器监听的IP
(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py runserver 0.0.0.0:8080
```


##### 创建应用
```text
(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py startapp app_name
```


##### 为应用创建数据表
```text
# 默认开启的某些应用需要至少一个数据表，该命令会检查 INSTALLED_APPS 设置，为其中的每个应用创建需要的数据表
(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py migrate
```


##### 迁移数据表
```text
# 使用 makemigrations 命令后 Django 会检测你对模型文件的修改，并把修改的部分储存为一次 迁移（本质就是一个文件）
# 迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表，专注于使数据库平滑升级而不会丢失数据
(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py makemigrations app_name
```


##### 检查项目
```text
(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py check

```


(venv) PS D:\workspace\python_web\python_web_vote_site\vote_site> python .\manage.py





