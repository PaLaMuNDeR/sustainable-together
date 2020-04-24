from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Client
from .serializers import UserSerializer, ClientSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
import json


class IsCreateOrAuthenticated(BasePermission):
    """
    Custom permission:
        - allow anonymous POST
        - allow authenticated GET and PUT on *own* record
        - allow all actions for staff
    """

    def has_permission(self, request, view):
        if view.action == 'register' or view.action=='login':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'get_profile'] and request.user.is_authenticated or request.user.is_staff:
            return True
        elif view.action == 'list' and request.user.is_staff:
            return True
        else:
            return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]

    def retrieve(self, request, pk=None, *args, **kwargs):
        response = {'message': 'Nothing to see here'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        response = {'message': 'Nothing to see here'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        response = {'message': 'Nothing to see here'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsCreateOrAuthenticated, ]
    authentication_classes = (TokenAuthentication,)


    @action(detail=False, methods=['POST'])
    def register(self, request):
        if 'username' in request.data and 'password' in request.data:
            username = request.data['username']
            password = request.data['password']
            email = request.data['email'] if 'email' in request.data else None

            # Check if username is already existing
            if User.objects.filter(username=username).first() is not None:
                response = {'message': 'Such username already exists'}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                # Create user instance
                new_user = User.objects.create_user(username=username, password=password, email=email)
                new_user.save()

                # Create client instance
                firstname = request.data['firstname'] if 'firstname' in request.data else None
                lastname = request.data['lastname'] if 'lastname' in request.data else None
                if email:
                    client.email = email

                client.save()
                Token.objects.create(user=new_user)

                response = {'message': 'Ok', 'details': ClientSerializer(client).data}
                return Response(response, status=status.HTTP_200_OK)

        else:
            response = {'message': 'Please, insert username and password'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, *args, **kwargs):
        client = get_object_or_404(Client, id=pk)
        if client is not None:
            if client.user == request.user or request.user.is_staff:
                serializer = ClientSerializer(client, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)

        response = {'message': 'Nothing to see here'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def get_profile(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            client = get_object_or_404(Client, user=request.user)
            if client is not None:
                if client.user == request.user or request.user.is_staff:
                    serializer = ClientSerializer(client, many=False)
                    return Response(serializer.data, status=status.HTTP_200_OK)

        response = {'message': 'Nothing to see here'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        client = get_object_or_404(Client, id=pk)
        if client:
            if request.user == client.user or request.user.is_staff:
                firstname = request.data['firstname'] if 'firstname' in request.data else None
                lastname = request.data['lastname'] if 'lastname' in request.data else None
                email = request.data['email'] if 'email' in request.data else None
                calorie_limit = request.data['calorie_limit'] if 'calorie_limit' in request.data else None
                active = request.data['active'] if 'active' in request.data else None

                if firstname:
                    client.firstname = firstname
                if lastname:
                    client.lastname = lastname
                if email:
                    client.email = email
                    client.user.email = email
                if calorie_limit:
                    client.calorie_limit = int(calorie_limit)
                if active is not None:
                    client.active = active
                if request.user.is_superuser:
                    if 'staff' in request.data:
                        staff_status = request.data['staff']
                        user = client.user
                        user.is_staff = staff_status
                        user.save()
                client.save()

                response = {'detail': ClientSerializer(client).data}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {'message': 'No permissions to edit this client.'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'message': 'Please, choose existing client'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        if 'username' in request.data and 'password' in request.data:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_authenticated:
                client = Client.objects.get(user=user)
                if client.active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key})
                else:
                    return Response({'error': "This user is inactive"})
            else:
                response = {'error': 'Wrong username or password'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'error': 'Please, provide username and password'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
