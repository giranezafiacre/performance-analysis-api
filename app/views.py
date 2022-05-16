from http.client import responses
import json
from telnetlib import STATUS
from urllib import response
from warnings import filters
from django.http import JsonResponse
from django.shortcuts import render
from requests import request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core import serializers
from rest_framework.status import *
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.authentication import *
from rest_framework.decorators import api_view
from rest_framework.filters import *
from app.serializers import FileSerializer, ListSerializer, StudentSerializer, UserSerializer
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .analysis import OverviewAnalysis, genderHistoAnalysis, fileDetails, healthHistoAnalysis, normal_correlation, teacherHistoAnalysis
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
            'role':user.role,
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


class ListFilesAPIView(ListAPIView):
    """list of all files"""
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['File_name']


class fileDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsOrderOwnerOrReadOnly]
    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'


@api_view(('GET',))
def fileDetail(request, pk):
    file = File.objects.get(id=pk)
    return JsonResponse(fileDetails(file.Actual_file), status=200)


@api_view(['POST'])
def correlationResult(request, pk):
    print(request.data)
    file = File.objects.get(id=pk)
    course = request.data['course']
    factor = request.data['factor']
    return Response(normal_correlation(file.Actual_file, course, factor), status=HTTP_200_OK)


class ListStudentsAPIView(ListAPIView):
    """list of all student"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['fname']


def reportLatestFileOverview(request):
    lastFile = File.objects.all().last()
    return JsonResponse(OverviewAnalysis(lastFile.Actual_file), status=200)


def genderHistogram(request):
    lastFile = File.objects.all().last()
    return JsonResponse({'data':genderHistoAnalysis(lastFile.Actual_file)}, status=200)

def teacherHistogram(request):
    lastFile = File.objects.all().last()
    return JsonResponse(teacherHistoAnalysis(lastFile.Actual_file), status=200)

def healthHistogram(request):
    lastFile = File.objects.all().last()
    data=healthHistoAnalysis(lastFile.Actual_file)
    return JsonResponse({'data':data}, status=200)
