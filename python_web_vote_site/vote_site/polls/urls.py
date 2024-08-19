from django.urls import path
from . import views


# urlpatterns = [
#     # 在这里进行 URL 映射，不过你还需要在根目录下 urls.py 的 urlpatterns 列表里插入一个 include()
#     path('', views.index, name='index'),
# ]

# # 将URL映射到第一个视图
# urlpatterns = [
#     path('', views.index, name='index'),
#     # path('<int:question_id>/', views.detail, name='detail'),
#     path('specifics/<int:question_id>/', views.detail, name='detail'),
#     path('<int:question_id>/results/', views.results, name='results'),
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

# 加上 app_name 设置命名空间
# 改良 URLconf
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

