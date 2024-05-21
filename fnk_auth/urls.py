from django.urls import path
from .views.email import email_verify
from .views.auth import register, change_password, get_user_email, CustomTokenObtainPairView
from .views.accounts import change_nickname
from .views.test import ItemListView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('change-nickname/', change_nickname, name='change_nickname'),
    path('verify/<uidb64>/<token>', email_verify, name='email-verify'),
    path('change-password/', change_password, name='change_password'),
    path('register/', register, name='register'),
    path('get_user_email/', get_user_email, name='get_user_email'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # ... other URL patterns for fnk_auth ...
]
