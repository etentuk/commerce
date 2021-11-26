from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/close/<int:listing_id>",
         views.close_listing, name="close_listing"),
    path("listing/comment/<int:listing_id>",
         views.create_comment, name="listing_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category_page, name="category_page"),
    path("watchlist/<str:action>/<int:listing_id>",
         views.watchlist_action, name="watchlist_action")
]
