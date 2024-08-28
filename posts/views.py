from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from .permissions import IsAuthorOrIsStaff
from .serializers import PostSerializer
from .models import Post
from .utils import send_telegram_message


class PostListView(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateView(generics.CreateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):

        serializer.save(post_author=self.request.user)

        chat_id = self.request.user.telegram_chat_id
        message = f"'{self.request.user.username}' your post's successfully created!"
        send_telegram_message(chat_id, message)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrIsStaff,]
