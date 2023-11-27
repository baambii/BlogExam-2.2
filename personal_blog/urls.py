from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import auth_views
from django.contrib.auth.views import LoginView
from users import views as users_views  # Import your users views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path('signup/', users_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/../users/templates/registration/login.html'), name='login'),
    path('sign_out/', users_views.signout, name='signout'),
    path('profile/', users_views.profile, name='profile'),
    path('profile/profile_update/', users_views.profile_update, name="profile-update"),
    path('users/', include('django.contrib.auth.urls')),
    #path('users/', include('blog.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




