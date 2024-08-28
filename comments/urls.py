from django.urls import path
from .views import CommentListView, CommentCreateView, CommentDetailView

urlpatterns = [
    path('post/<int:pk>/comment/', CommentListView.as_view()),
    path('post/<int:pk>/comment_add/', CommentCreateView.as_view()),
    path('post/<int:pk>/comment/<int:ck>/', CommentDetailView.as_view()),
]
