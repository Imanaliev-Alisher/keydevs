from datetime import timezone

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, UserListSerializer
from .models import User
from .utils import create_verification_code, check_telegram_updates


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class RegisterUserView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username
            })
            code = create_verification_code(user)

            return Response({
                'verification_code': code,
                'refresh': str(refresh),
                'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):

        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None or password is None:
            return Response({"Error": "Login and password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"Error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)}, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def post(self, request):

        refresh_token = request.data.get('refresh_token')

        if not refresh_token:

            return Response({'error': 'Required Refresh token'},

                            status=status.HTTP_400_BAD_REQUEST)

        try:

            token = RefreshToken(refresh_token)

            token.blacklist()

        except Exception as e:

            return Response({'error': 'Invalid Refresh token'},

                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Successfully log out'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_code(request):
    chat_id = request.data.get('chat_id')
    code = request.data.get('code')

    if not chat_id or not code:
        return Response({'error': 'Chat ID and code are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Запуск проверки обновлений
    success = check_telegram_updates()

    if success:
        return Response({'success': 'Code verified successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid code or chat ID'}, status=status.HTTP_400_BAD_REQUEST)
