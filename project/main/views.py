from venv import create
from django.http import Http404
from django.db import IntegrityError
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes

from .permissions import IsAdminOrReadOnly

from .models import Profile, User, Book, Journal

from .serializers import UserSerializer, ProfileSerializer, BookSerializer, JournalSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(['POST'])
@permission_classes([~IsAuthenticated])
def register(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "User with same email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    profile = Profile.objects.filter(user__id = request.user.id).first()
    
    if profile:
        if request.method == 'GET':
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = ProfileSerializer(instance=profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



class BookViewSet(viewsets.ViewSet, mixins.DestroyModelMixin):
    
    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated & IsAdminOrReadOnly, )
        return [permission() for permission in permission_classes]
    
    def get_object(self):
        return Book.objects.filter(id=self.kwargs.get('pk')).first()
    
    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def create(self, request):
        self.check_object_permissions(request, None)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def retrieve(self, request, pk=None):
        book = self.get_object()
        if book:
            serializer = BookSerializer(instance=book)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        book = self.get_object()
        if book:
            self.check_object_permissions(request, book)
            serializer = BookSerializer(instance=book, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        if book:
            self.check_object_permissions(request, book)
            book.delete()
            return Response({"message": "Book deleted"})
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class JournalModelViewSet(viewsets.ModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer
    
    def get_permissions(self):
        if self.action in ['retrieve', 'list']:
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsAuthenticated & IsAdminOrReadOnly, )
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        self.check_object_permissions(request, None)
        return super().create(request)
    