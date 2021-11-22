from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from rest_framework import permissions

from products.models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly


class ProductsList(ListAPIView):

    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['^name', '^description',
                     'measure_unit', '^materials__material_name']
    ordering_fields = ['created_at', 'price', 'amount']
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Product.objects.prefetch_related("materials").filter(owner=self.request.user)


class ProductCreate(CreateAPIView):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ProductDetail(RetrieveUpdateDestroyAPIView):

    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly, )
    queryset = Product.objects.all()
    lookup_field = 'id'
