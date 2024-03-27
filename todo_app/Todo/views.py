from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token

from .models import Todo, User
from .serializers import TodoSerializer, UserSerializer

# Create your views here.


# Create User Viewset
class CreateUserViewset(CreateAPIView):
    """
    Create User viewset
    """

    permission_classes = [AllowAny]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        seriailzer = self.get_serializer(data=request.data, many=False)
        if seriailzer.is_valid():
            seriailzer.save()
            return Response("User Created Successfuly", status=status.HTTP_201_CREATED)
        return Response(seriailzer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Viewsets
class UserViewsets(ModelViewSet):
    """
    User Viewsets
    Update ,Delete ,List (only logged in user)
    """

    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)  # type: ignore

    def create(self, request, *args, **kwargs):
        return Response("Method not allowed.", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"Token": token.key}, status=status.HTTP_200_OK)
        return Response(
            "Invalid username or password.", status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["get"])
    def logout(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            return Response("Logged out.", status=status.HTTP_200_OK)
        return Response("No user is authenticated. Logout not performed.")


# Todo Viewsets
class TodoViewsets(ModelViewSet):
    """
    Todo Viewsets
    Create , Update ,Delete ,List
    """

    serializer_class = TodoSerializer

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=False)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response("Task Created.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
