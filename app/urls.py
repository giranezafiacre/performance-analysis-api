from django.urls import include, path
from . import views

urlpatterns = [
path('auth/', include('rest_auth.urls')),
path('auth/register/', views.CreateUserAPIView.as_view(), name="register"),
path('auths/current-user/', views.UserView.as_view(), name="user"),
path('upload/',views.GFileUploadAPIView.as_view(),name='upload'),
path('theFile/<int:pk>/',views.fileDetailAPIView.as_view(),name='file_detail'),
path('file/<int:pk>/',views.fileDetail,name='file_detail'),
path('files/',views.ListFilesAPIView.as_view(),name='files'),
path('correlation/<int:pk>/',views.correlationResult,name='correlation'),
path('students/',views.ListStudentsAPIView.as_view(),name='students'),
path('latest/',views.reportLatestFileOverview,name='latest'),
path('gender-histogram/',views.genderHistogram,name='gender-histogram'),
path('teacher-histogram/',views.teacherHistogram,name='teacher-histogram'),
path('health-histogram/',views.healthHistogram,name='health-histogram'),
]