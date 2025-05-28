from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.article_list),
    path('article_create/', views.article_create),
    path('article_detail/<int:article_id>/', views.article_detail),
    # 댓글 목록 읽기 / 쓰기
    path('article_detail/<int:article_id>/comments/', views.article_comments),
    # 댓글 삭제하기
    path('article_detail/<int:article_id>/comment_delete/<int:comment_id>/', views.article_comment_delete),
    # 스크랩, 스크랩취소
    path('article_detail/<int:article_id>/scrap/', views.article_scrap),
    # 스크랩되어있는지 확인
    path('article_detail/<int:article_id>/is_scrapped/', views.is_article_scrapped),
]
