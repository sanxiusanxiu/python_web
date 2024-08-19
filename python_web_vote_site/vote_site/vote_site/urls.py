"""
Django 项目的 URL 声明，就像你网站的“目录”

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


path() 函数： path(route, view, [kwargs, name])
其中 route 和 view 是必须参数， kwargs 和 name 是可选参数

route：
一个匹配 URL 的准则，类似于正则，
当 Django 响应一个请求时，它会从 urlpatterns 的首项开始，按顺序依次匹配列表中的项，直到找到匹配的项，
这些准则不会匹配 GET 和 POST 参数或域名，
例如，请求为 https://www.example.com/myapp/ 时，它会尝试匹配 myapp/ ，
请求为 https://www.example.com/myapp/?page=3 时，也只会尝试匹配 myapp/

view：
当 Django 找到了一个匹配的准则，就会调用这个特定的视图函数，并传入一个 HttpRequest 对象作为第一个参数，
被“捕获”的参数以关键字参数的形式传入

kwargs：
在这里，任意个关键字参数可以作为一个字典传递给目标视图函数

name：
为 URL 取别名，能使你在 Django 的任意地方唯一地引用它，尤其是在模板中，这个特性允许你只改一个文件就能全局地修改某个 URL 模式

"""

from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]
