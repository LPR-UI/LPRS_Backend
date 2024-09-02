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
    path('add-owner/', views.AddOwner.as_view(), name="add_owner")
]
