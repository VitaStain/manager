from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CategoriesViewSet, RegisterApi, TransactionViewSet,
                    UserViewSet)

cat = routers.SimpleRouter()
cat.register(r'category', CategoriesViewSet, basename='category')

tr = routers.SimpleRouter()
tr.register(r'transaction', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('register/', RegisterApi.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserViewSet.as_view({'get': 'list'}), name='profile'),
    path('profile/', include(cat.urls)),
    path('profile/', include(tr.urls)),
]
