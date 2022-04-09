from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.authentication import *
from app.serializers import FileSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
import jwt

User = get_user_model()


def login_view(request):
    print("hey", request)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = get_object_or_404(User, email=email)
        if user.approved:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_token = jwt.encode({'email': user.email, 'full_name': user.full_name, 'id': user.id},
                                        'JWT_SECRET_KEY')
                login(request, user)
                return Response(data={'message': 'login success', 'token': auth_token}, status=HTTP_200_OK)
            else:
                return Response(data={'message': 'unauthorized'}, status=HTTP_401_UNAUTHORIZED)
    else:
        return Response(data={'invalid method'}, status=HTTP_405_METHOD_NOT_ALLOWED)


class CreateUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


# Create your views here.
class UserView(APIView):

    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        return Response({
            'username': user.fullname,
        })

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


class GFileUploadAPIView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        serializer.save()
