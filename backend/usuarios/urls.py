from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserUpdateView, UserDeactivateView, UserProfileView, TestJWTView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/deactivate/', UserDeactivateView.as_view(), name='user-deactivate'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('test/', TestJWTView.as_view(), name='test'),
]
