from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, register_user,login_user
from django.urls import path

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')

urlpatterns = router.urls + [
    path('register/', register_user),
    path('login/',login_user),
]