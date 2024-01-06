from django.urls import path
from . import views
# from .views import CustomTokenObtainPairView
# from .views import CustomTokenObtainPairView

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('login/', views.CustomTokenObtainPairView.as_view(), name='admin_login'),
]
