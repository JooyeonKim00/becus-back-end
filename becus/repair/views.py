from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Repair
from .serializers import GetRepairSerializer, PostRepairSerializer, PutRepairSerializer

from product.models import Product
# Create your views here.
# client view
class ListRepairView(APIView):
    def get(self, request):
        author = request.user
        repairs = Repair.objects.filter(r_author=author)
        serializer = GetRepairSerializer(repairs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        # find product
        product_id = data['product_id']
        product = get_object_or_404(Product, pk=product_id)
        # remove product_id
        data.pop('product_id')
        serializer = PostRepairSerializer(data=data)

        if(serializer.is_valid()):
            # save order
            serializer.save(
                r_product=product,
                r_author=request.user
            )
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OneRepairView(APIView):
    def get_object(self, pk):
        repair = get_object_or_404(Repair, pk=pk)
        return repair

    def get(self, request, pk):
        repair = self.get_object(pk)
        serializer = GetRepairSerializer(repair)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        data = request.data
        repair = self.get_object(pk)
        serializer = PutRepairSerializer(repair, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        repair = self.get_object(pk)
        repair.delete()
        response = {'id': pk}
        return Response(response, status=status.HTTP_204_NO_CONTENT)