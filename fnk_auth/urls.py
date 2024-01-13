from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('change-password/', views.change_password, name='change_password'),
    path('get_user_email/', views.get_user_email, name='get_user_email'),
    path('items/', views.ItemListView.as_view(), name='item-list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.register, name='register')
    # ... other URL patterns for fnk_auth ...
]
