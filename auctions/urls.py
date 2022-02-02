from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.newListing, name="new"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categories, name="allCategories"),
    path("auction/watchCount", views.watchCount, name="watchCount"),
]
