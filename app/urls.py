from django.urls import path
from .import views


urlpatterns = [
    path("", views.bloghome, name="blogHome"),
    path('signup/', views.handleSignUp, name="handleSignUp"),
    path('login/', views.handeLogin, name="handleLogin"),
    path('logout/', views.handelLogout, name="handleLogout"),
    path('search/', views.search, name="search"),
    path('postComment/', views.postComment, name="postComment"),
    path('<str:slug>/', views.blogPost, name="blogPost"),
]