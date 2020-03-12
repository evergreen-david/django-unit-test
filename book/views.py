import json
from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Book, Author, AuthorBook

class AuthorView(View):

    def post(self, request):
        data = json.loads(request.body)
        try:
            if Author.objects.filter(name = data["name"]).exists():
                return JsonResponse({'message':'DUPLICATED_NAME'}, status = 400)
            Author(
                name = data['name'],
                email = data['email']
            ).save()
            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)

class AuthorBookView(View):
    def get(self, request, title):
        try:
            if Book.objects.filter(title = title).exists():
                book = Book.objects.get(title = title)
                authors = list(AuthorBook.objects.filter(book = book).values('author'))
                return JsonResponse({'authors':authors}, status = 200)
            return JsonResponse({'message':'NO_AUTHOR'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
