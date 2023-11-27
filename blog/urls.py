from django.urls import path
from . import views  # Import views from the current directory
from users import views as users_views  # 
from .views import PostUpdateView, PostDeleteView, PostCreateView, LikeView, CommentView


urlpatterns = [
    path("", views.homepage, name="homepage"),
    #path("login/", users_views.login_view, name="login"),  # Reference login view from 'users' app
    #path("signup/", users_views.signup, name="signup"),  # Reference signup view from 'users' app
    path('welcome/', views.welcome, name='welcome'),
    path("home/", views.home, name="home"),
    path('sign_out/', users_views.signout, name='signout'),
    path('welcomeback/',views.welcomeback, name='welcomeback'),
    path('post/<int:pk>/', views.post_detail, name='postdetail'),
    path('create_post/', PostCreateView.as_view(), name='createpost'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='editpost'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='deletepost'),
    path('like/<int:pk>', LikeView, name='like'),
    path('post/<int:pk>/comment/', CommentView, name="comment")


]

    




