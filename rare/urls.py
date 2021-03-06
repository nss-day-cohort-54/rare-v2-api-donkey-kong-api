"""rare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from rareapi.views.auth import login_user, register_user
from rareapi.views.categories import CategoryView
from rareapi.views.comments import CommentView
from rareapi.views.posts import PostView

from rareapi.views.subscriptions import SubscriptionView

from rareapi.views.reactions import ReactionView

from rareapi.views.tags import TagView
from rareapi.views.rare_user import RareUserView

from rareapi.views.users import UserView

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'posts', PostView, 'post')
router.register(r'rareUsers', RareUserView, 'rareUser')
router.register(r'tags', TagView, 'tag')
router.register(r'comments', CommentView, 'comment')
router.register(r'categories', CategoryView, 'category')
router.register(r'users', UserView, 'user')

router.register(r'subscriptions', SubscriptionView, 'subscription')

router.register(r'reactions', ReactionView, 'reaction')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
