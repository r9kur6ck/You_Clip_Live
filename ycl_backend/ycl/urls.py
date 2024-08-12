from django.urls import path
from . import views

# path('', views.index, name='index') の部分は、bookman/ にアクセスした際に views.index ビューが実行されるように設定
# name='index' は、この URL パターンに名前を付けることで、Django 内で簡単に参照できるようにするため
urlpatterns = [
    path('', views.index, name='index'),
]