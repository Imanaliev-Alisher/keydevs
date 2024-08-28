from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView

urlpatterns = [
    path('post/', PostListView.as_view()),
    path('post_add/', PostCreateView.as_view()),
    path('post/<int:pk>/', PostDetailView.as_view()),
]
