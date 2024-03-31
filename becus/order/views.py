from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Order
from .serializers import GetOrderSerializer, PostOrderSerializer, PutOrderSerializer

from product.models import Product
# Create your views here.
# client view
class ListOrderView(APIView):
    def get(self, request):
        author = request.user
        orders = Order.objects.filter(o_author=author)
        serializer = GetOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        # find product
        product_id = data['product_id']
        product = get_object_or_404(Product, pk=product_id)
        # remove product_id
        data.pop('product_id')
        serializer = PostOrderSerializer(data=data)

        if(serializer.is_valid()):
            # save order
            serializer.save(
                o_product=product,
                o_author=request.user
            )
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OneOrderView(APIView):
    def get_object(self, pk):
        order = get_object_or_404(Order, pk=pk)
        return order

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = GetOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        data = request.data
        order = self.get_object(pk)
        serializer = PutOrderSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        response = {'id': pk}
        return Response(response, status=status.HTTP_204_NO_CONTENT)

