from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Gconsult, Pconsult
from .serializers import *

from product.models import Product

# client view
class ListGlobalConsultView(APIView):
    def get(self, request):
        author = request.user
        gconsults = Gconsult.objects.filter(gc_author=author)
        serializer = GetGlobalConsultSerializer(gconsults, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = PostGlobalConsultSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save(
                gc_author=request.user
            )
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OneGlobalConsultView(APIView):
    def get_object(self, pk):
        gconsult = get_object_or_404(Gconsult, pk=pk)
        return gconsult
    
    def get(self, request, pk):
        gconsult = self.get_object(pk)
        serializer = GetGlobalConsultSerializer(gconsult)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        data = request.data
        gconsult = self.get_object(pk)
        serializer = PutGlobalConsultSerializer(gconsult, data=data)
        if(serializer.is_valid()):
            serializer.save()
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        gconsult = self.get_object(pk)
        gconsult.delete()
        response = {'id': pk}
        return Response(response, status=status.HTTP_204_NO_CONTENT)

class ListProductConsultView(APIView):
    def get(self, request):
        author = request.user
        pconsults = Pconsult.objects.filter(pc_author=author)
        serializer = GetProductConsultSerializer(pconsults, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        product_id = data['product_id'] # find product
        product = get_object_or_404(Product, pk=product_id)
        data.pop('product_id') # remove product_id
        serializer = PostProductConsultSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save(
                pc_product=product,
                pc_author=request.user
            )
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OneProductConsultView(APIView):
    def get_object(self, pk):
        pconsult = get_object_or_404(Pconsult, pk=pk)
        return pconsult
    
    def get(self, request, pk):
        pconsult = self.get_object(pk)
        serializer = GetProductConsultSerializer(pconsult)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        data = request.data
        pconsult = self.get_object(pk)
        serializer = PutProductConsultSerializer(pconsult, data=data)
        if(serializer.is_valid()):
            serializer.save()
            response = {'id': serializer.data['id']}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pconsult = self.get_object(pk)
        pconsult.delete()
        response = {'id': pk}
        return Response(response, status=status.HTTP_204_NO_CONTENT)
# admin view
