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

    # partial GETs
    path('owners-dropdown/', views.GetOwnersInCarCreation.as_view(), name="get_dropdown_owner"),
    path('permissions-dropdown/', views.GetLPsInPermissionCreation.as_view(), name="get_dropdown_permission"),

    # DELETE
    path('delete-owner/<int:owner_id>/', views.DeleteOwner.as_view(), name="delete_owner"),
    path('delete-car/<str:license_plate>/', views.DeleteCar.as_view(), name="delete_car"),
    path('delete-permission/<int:permission_id>/', views.DeletePermission.as_view(), name="delete_permission"),
    path('delete-camera/<int:camera_id>/', views.DeleteCamera.as_view(), name="delete_camera"),

    # EDIT
    path('edit-owner/<int:owner_id>/', views.EditOwner.as_view(), name='edit-owner'),
    path('edit-car/<str:license_plate>/', views.EditCar.as_view(), name='edit-car'),
    path('edit-permission/<int:permission_id>/', views.EditPermission.as_view(), name='edit-permission'),
    path('edit-camera/<int:camera_id>/', views.EditCamera.as_view(), name='edit-camera'),


    # LISTS
    path('owners/', views.CarOwnerListView.as_view(), name='car_owner_list'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('permissions/', views.PermissionListView.as_view(), name='permission_list'),
    path('cameras/', views.CameraListView.as_view(), name="camera_list")
]
