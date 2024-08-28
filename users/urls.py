from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterUserView, LoginView, UserListView, LogoutView
from . import views

urlpatterns = [
    path('account_register/', RegisterUserView.as_view()),
    path('account/', UserListView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify/', views.verify_code, name='verify_code'),
]