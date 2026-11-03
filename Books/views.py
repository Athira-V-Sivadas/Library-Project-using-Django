from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from json import loads

# Create your views here.

books = []

@method_decorator(csrf_exempt, name='dispatch')
class AddBookView(View):

    def post(self, request):

        data = request.body
        form_data = loads(data)

        book = {
            "id": len(books) + 1,
            "book_name": form_data.get('book_name'),
            "author": form_data.get('author'),
            "category": form_data.get('category'),
            "price": form_data.get('price'),
            "quantity": form_data.get('quantity')
        }

        books.append(book)
        print("After adding:", books)


        return JsonResponse({
            "message": "Book added successfully",
            "book": book
        })

class ViewBooksView(View):

    def get(self, request):
        print("While viewing:", books)
        return JsonResponse(books, safe=False)

class SearchBookView(View):

    def get(self, request, id):

        for book in books:
            if book['id'] == id:

                return JsonResponse(book)

        return JsonResponse({
            "message": "Book not found"
        }, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateBookView(View):

    def put(self, request, id):

        data = request.body
        form_data = loads(data)

        for book in books:

            if book['id'] == id:

                book['book_name'] = form_data.get('book_name')
                book['author'] = form_data.get('author')
                book['category'] = form_data.get('category')
                book['price'] = form_data.get('price')
                book['quantity'] = form_data.get('quantity')

                return JsonResponse({
                    "message": "Book updated successfully",
                    "book": book
                })

        return JsonResponse({
            "message": "Book not found"
        }, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteBookView(View):

    def delete(self, request, id):

        for book in books:

            if book['id'] == id:

                books.remove(book)

                return JsonResponse({
                    "message": "Book deleted successfully"
                })

        return JsonResponse({
            "message": "Book not found"
        }, status=404)