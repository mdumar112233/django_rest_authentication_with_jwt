from django.urls import path, include
from account.views import UserChangePassword, UserProfileview, UserRegistrations, Userlogin


urlpatterns = [
    path('register/', UserRegistrations.as_view(), name='register'),
    path('login/', Userlogin.as_view(), name='login'),
    path('profile/', UserProfileview.as_view(), name='profile'),
    path('changepassword/', UserChangePassword.as_view(), name='changepassword'),
] 