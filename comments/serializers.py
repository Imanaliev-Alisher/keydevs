from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('post', 'text', 'comment_author', 'created_at',)
        read_only_field = ('post',)
