from django.urls import path
from .views import RatingCreateView, RatingUpdateView

urlpatterns = [
    path('post/<int:pk>/mark_add/', RatingCreateView.as_view()),
    path('post/<int:pk>/mark/<int:rk>/', RatingUpdateView.as_view()),
]
