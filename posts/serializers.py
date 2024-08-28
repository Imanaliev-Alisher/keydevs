from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):

    post_author = serializers.CharField(source='post_author.username', read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('text', 'post_author', 'created_at', 'average_rating',)
        read_only_fields = ('created_at',)

    def get_average_rating(self, obj):
        return obj.get_average_rating()
