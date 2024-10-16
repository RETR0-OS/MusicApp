from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "accounts"

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),
    path('oauth/google/login/callback/', views.google_callback, name="googleLoginCallback"),
    path('oauth/google/login/', views.google_login, name="googleLogin"),
    path('set_up_profile/', views.set_profile, name="setProfile"),
    path('user/profile/', views.load_profile, name="load_profile"),
    path('user/profile/edit', views.edit_profile, name="edit_profile")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)