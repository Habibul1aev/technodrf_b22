from django.shortcuts import render
from rest_framework.views import APIView
from techno.models import Product, Category
from techno.serializer import ProductSerializer, ProductCreateUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from techno.paginator import ProductPaginator
from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from techno import mixins
from rest_framework.decorators import action

class ProductViewSet(mixins.ProModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ProductPaginator
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'category']
    search_fields = ['title']
    ordering_fields = ['price']

    serializer_classes = {
        'list': ProductSerializer,
        'create': ProductCreateUpdateSerializer,
        'update': ProductCreateUpdateSerializer,
    }

    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated],
        'destroy': [IsAdminUser]
    }   


    @action(detail=False, methods=['get'])
    def sum(self, request):
        products = self.get_queryset()
        all_price = 0

        for i in products:
            all_price += i.price

        return Response({'count': len(products), 'sum': all_price})

    @action(detail=False, methods=['get'])
    def expensive(self, request):
        product = Product.objects.order_by('-price').first()

        serializer = self.get_serializer(product)

        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def my_product(self, request):
        products = Product.objects.filter(user=request.user)

        serializer = self.get_serializer(products, many=True)

        return Response(serializer.data)








# class ProductViewSet(viewsets.ViewSet):
#     def list(self, request):
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)

#         return Response(serializer.data)

#     def retrieve(self, request, pk):
#         products = Product.objects.all()
#         product = get_object_or_404(products, pk=pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)

#     def create(self,request):
#         serializers = ProductSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#         return Response(serializers.data)

#     def update(self, request, pk):
#         product = Product.objects.get(id=pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

#     def partial_update(self, request, pk):
#         product = Product.objects.get(pk = pk)
#         serializer = ProductSerializer(product, data = request.data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

#     def destroy(self, pk):
#         product = Product.objects.get(pk = pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)






# class ProductGenerics(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     pagination_class = ProductPaginator
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['title', 'category']
    # search_fields = ['title']
    # ordering_fields = ['price']




# class ProductDetailGenerics(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


















# class ProductAPIView(APIView):
#     def get(self, request):
#         product = Product.objects.all()
#         paginator = ProductPaginator()
#         page = paginator.paginate_queryset(product, request)
#         serializer = ProductSerializer(page, many=True)
#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=201)


# class ProductDetailAPIView(APIView):
#     def get(self, request, id):
#         product = Product.objects.get(id=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, id):
#         product = Product.objects.get(id=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#     def patch(self, request, id):
#         product = Product.objects.get(id=id)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

#     def delete(self, request, id):
#         product = Product.objects.get(id=id)
#         product.delete()
#         return Response({'message': 'Your product was deleted'}, status=status.HTTP_200_OK)



        