from django.db import models
from django.conf import settings


class Post(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_author

    def get_average_rating(self):
        return self.ratings.aggregate(average_rating=models.Avg('rating'))['average_rating'] or 0