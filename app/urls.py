from django.urls import include, path
from . import views

urlpatterns = [
path('auth/', include('rest_auth.urls')),
path('auth/register/', views.CreateUserAPIView.as_view(), name="register"),
path('auths/current-user/', views.UserView.as_view(), name="user"),
path('upload/',views.GFileUploadAPIView.as_view(),name='upload')
]