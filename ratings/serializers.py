from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):

    rating_author = serializers.CharField(source='rating_author.username', read_only=True)

    class Meta:
        model = Rating
        fields = ('rating', 'post', 'rating_author')
        read_only_field = ('post', 'rating_author')

    def validate(self, attrs):
        request = self.context.get('request')
        post = attrs.get('post')
        rating_author = request.user

        if Rating.objects.filter(post=post, rating_author=rating_author).exists():
            raise serializers.ValidationError("You have already rated this post.")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        rating_author = request.user
        return Rating.objects.create(rating_author=rating_author, **validated_data)


class RatingUpdateSerializer(serializers.ModelSerializer):
    rating_author = serializers.CharField(source='rating_author.username', read_only=True)

    class Meta:
        model = Rating
        fields = ('rating', 'post', 'rating_author')
        read_only_field = ('post', 'rating_author')