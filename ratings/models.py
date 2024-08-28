from django.db import models
from django.conf import settings
from posts.models import Post


class Rating(models.Model):

    RATE_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    rating_author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveBigIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return self.rating_author
