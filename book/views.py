import json
import jwt
import requests
import SECRET_KEY
from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Book, Author, AuthorBook, User

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


class SocialKakaoView(View):
    def post(self, request):
        kakao_token = request.headers["Authorization"]
        if not kakao_token:
            return JsonResponse({"MESSAGE" : "INVALID_KAKAO_TOKEN"}, status=400)

        headers = {'Authorization' : f"Bearer {kakao_token}"}
        url = "api_url"
        response = requests.get(url, headers = headers)
        kakao_user = response.json()

        if User.objects.filter(kakao = kakao_user['id']).exists():
            user = User.objects.get(kakao = kakao_user['id'])
            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token' : access_token.decode('utf-8'),}, status=200)
        else :
            newUser = User.objects.create(
                kakao = kakao_user['id'],
                nick_name = kakao_user['properties']['nickname']
            )

            access_token = jwt.encode({'id' : newUser.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token': access_token.decode('utf-8')}, status=200)
