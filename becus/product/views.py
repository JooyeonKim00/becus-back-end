from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .utils import FileUploadToS3
from .models import Product
from .serializers import GetProductSerializer, PostProductSerializer, PutProductSerializer

class ListProductView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = Product.objects.all()
        serializer = GetProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # get datas
        data = request.data
        p_picture = request.data['p_picture']
        p_manual = request.data['p_manual']
        # upload to s3
        p_picture_url = FileUploadToS3(p_picture).upload("IMAGE")
        p_manual_url = FileUploadToS3(p_manual).upload("FILE")
        # set url
        data['p_picture'] = p_picture_url
        data['p_manual'] = p_manual_url
        # serializing
        serializer = PostProductSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save(
                p_author = request.user,
            )
            response = {"id": serializer.data['id']}
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OneProductView(APIView):
    def get_object(self, pk):
        product = get_object_or_404(Product, pk=pk)
        return product

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = GetProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        # get datas
        data = request.data
        product = self.get_object(pk)
        # get request file
        p_picture = data['p_picture']
        p_manual = data['p_manual']
        p_picture_url = FileUploadToS3(p_picture).upload("IMAGE")
        p_manual_url = FileUploadToS3(p_manual).upload("FILE")
        data['p_picture'] = p_picture_url
        data['p_manual'] = p_manual_url
        serializer = PutProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"id": serializer.data['id']}
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        response = {'id': pk}
        return Response(response, status=status.HTTP_204_NO_CONTENT)