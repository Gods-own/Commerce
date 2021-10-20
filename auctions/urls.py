from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="listing"),
    path("page/<int:auction_id>", views.page, name="page"),
    path("watch", views.watch, name="watch"),
    path("category", views.category, name="category"),
    path("catlist/<int:list_id>", views.catlist, name="catlist"),
    path("search", views.search, name="search"),
    path("getCategory/<str:category>", views.get_category, name="getCategory"),
    path("remove_watch/<int:auction_id>", views.remove_watch, name="remove_watch"),
]