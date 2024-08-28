from django.http import Http404
from rest_framework import generics
from .serializers import CommentSerializer
from .models import Comment
from .permissions import IsStaffOrReadOnly


class CommentListView(generics.ListAPIView):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['pk'])


class CommentCreateView(generics.CreateAPIView):

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(post_id=post_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CommentSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_object(self):
        try:
            return Comment.objects.get(pk=self.kwargs['ck'], post_id=self.kwargs['pk'])
        except Comment.DoesNotExist:
            raise Http404

