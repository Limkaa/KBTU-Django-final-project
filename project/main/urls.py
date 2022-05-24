from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework.routers import DefaultRouter

from .views import register, profile, JournalModelViewSet, BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='books')
router.register(r'journals', JournalModelViewSet, basename='journals')

urlpatterns = [
    # Registration
    path('register/', register),
    
    # Authorization
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Profile
    path('profile/', profile),
    
    path('', include(router.urls)),
]