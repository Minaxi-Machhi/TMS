from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views import LoginView, UserProfileViewSet
from apps.project_management.urls import project_router
# from apps.trip.urls import trip_router, trip_urlpatterns

router = DefaultRouter()
router.register('user_profile', UserProfileViewSet, basename='user_profile')
router.registry.extend(project_router.registry)

urlpatterns = ([
                   path('', include(router.urls)),
                   path('login/', LoginView.as_view(), name='login'),
               ])
                # + company_urlpatterns
