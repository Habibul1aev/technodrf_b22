from django.urls import path, include
from techno.views import ProductViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('products', ProductViewSet)

print(router.urls)


urlpatterns = [
    path('', include(router.urls)),

    # path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put' : 'update', 'patch': 'partial_update', 'delete':'destroy'})),
]
