from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .forms import *
from .Serializer import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


class OperationUserRegistration(APIView):
    def post(self, request):
        print(request.data)
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            user= User.objects.get(username = serializer.data['username'])
            user.is_operationUser = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 200,
                'message': 'User created successfully',
                'data': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 403,
                'message': 'Validation failed',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
from rest_framework.authtoken.models import Token

class clientUserRegistration(APIView):
    def post(self, request):
        print(request.data)
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user= User.objects.get(username = serializer.data['username'])
            user.is_clientUser = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 200,
                'message': 'User created successfully',
                'data': serializer.data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 403,
                'message': 'Validation failed',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    

from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generate a token
            token, created = Token.objects.get_or_create(user=user)

            # Check user type
            if user.is_clientUser:
                user_type = 'ClientUser'
            elif user.is_operationUser:
                user_type = 'OperationUser'
            else:
                user_type = 'Unknown'

            return Response({
                'token': token.key,
                'user_type': user_type
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# class FileViewSet(viewsets.ModelViewSet):
    
#     # Serialize the Our Files Model
#     serializer_class = FileSerializer
#     def get_queryset(self):
#         return Files.objects.all()

from rest_framework import status
class filesUploading(APIView): #Only GET Method
    def get(self, request):
        files = Files.objects.all()
        fileseril = FileSerializer(files, many=True)
        # print(fileseril)
        return Response({'status': 200, 'message':'Getting Data', 'data':fileseril.data })
    

    def post(self, request):
        serializer = FileSerializer(data=request.data)
        
        if not serializer.is_valid():
            print("Validation Errors:", serializer.errors)
            return Response(
                {'status': 'error', 'message': 'Invalid data', 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        print("Uploaded Data:", request.data)
        
        return Response(
            {'status': 'success', 'message': 'File uploaded successfully', 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )





from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class clientUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id != None:
            print('---------------->',id)
            document = get_object_or_404(Files, id=id)
            response = HttpResponse(document.File, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={document.File}'
            return response
        else:
            files = Files.objects.all()
        fileseril = FileSerializer(files, many=True)
        # print(fileseril)
        return Response({'status': 200, 'message':'Getting Data', 'data':fileseril.data })




