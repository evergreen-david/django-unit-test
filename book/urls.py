from django.urls import path
from .views      import AuthorView, AuthorBookView, SocialKakaoView

urlpatterns = [
    path('/author', AuthorView.as_view()),
    path('/author-book/<slug:title>', AuthorBookView.as_view()),
    path('/kakao-signin', SocialKakaoView.as_view()),
]
