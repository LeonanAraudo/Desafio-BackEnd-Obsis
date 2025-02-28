from rest_framework import viewsets, status
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.response import Response
from django.db.models import Count

class AuthorViewSet(viewsets.ViewSet):

    def list(self, request):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  
        return Response(serializer.errors, status=400)
    
    def requestTopAuthors(self, request):
        authorsTop = Author.objects.annotate(total_livros=Count('book')).order_by('-total_livros')[:5]
        serializer = AuthorSerializer(authorsTop, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        try:
            author = Author.objects.get(pk=pk)
            author.delete()
            return Response({"message": "Autor deletado com sucesso"}, status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response({"error": "Autor não encontrado"}, status=status.HTTP_404_NOT_FOUND)

class BookViewSet(viewsets.ViewSet):

    def list(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)  
        return Response(serializer.errors, status=400) 
    
    def partial_update(self, request, pk=None):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):  
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({"message": "Livro deletado com sucesso"}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({"error": "Livro não encontrado"}, status=status.HTTP_404_NOT_FOUND)
