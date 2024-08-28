from django.http import Http404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from posts.models import Post
from .serializers import RatingSerializer, RatingUpdateSerializer
from .permissions import IsAuthorOrReadOnly
from .models import Rating


class RatingCreateView(generics.CreateAPIView):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        post = self.get_object(kwargs['pk'])
        data = request.data.copy()
        data['post'] = post.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404


class RatingUpdateView(generics.UpdateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingUpdateSerializer
    permission_classes = [IsAuthorOrReadOnly]
