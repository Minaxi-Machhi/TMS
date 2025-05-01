from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views import LoginView

# from apps.trip.urls import trip_router, trip_urlpatterns

router = DefaultRouter()
# router.register('role', RoleViewSet, basename='role')

urlpatterns = ([
                   path('', include(router.urls)),
                   path('login/', LoginView.as_view(), name='login'),
                    router.register('user_profile', UserProfileViewSet, basename='user_profile')

                   # path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),

               ])
                # + company_urlpatterns
