from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('validate-access/', views.ValidateAccessView.as_view(), name="validate_access"),
    path('statistics/', views.Statistics.as_view(), name="Statistics"),
    path('report/', views.GenerateReport.as_view(), name="report"),
    
    # ADD
    path('add-owner/', views.AddOwner.as_view(), name="add_owner"),
    path('add-car/', views.AddCar.as_view(), name="add_car"),
    path('add-permission/', views.AddPermission.as_view(), name="add_permission"),
    path('add-camera/', views.AddCamera.as_view(), name="add_camera"),

    # LISTS
    path('owners/', views.CarOwnerListView.as_view(), name='car_owner_list'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('permissions/', views.PermissionListView.as_view(), name='permission_list'),
    path('cameras/', views.CameraListView.as_view(), name="camera_list")
]
