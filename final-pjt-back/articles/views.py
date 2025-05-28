from django.shortcuts import render
from .serializers import ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, ArticleScrapSerializer
from .models import Article, Comment, ArticleScrap

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

# 게시글 조회, 비로그인도 가능
@api_view(['GET'])
def article_list(request):
    articles = Article.objects.all()
    serializers = ArticleListSerializer(articles, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)
    
# 게시글 작성 로그인 해야 가능
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_create(request):
    serializer = ArticleCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=request.user)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    

# 게시글 디테일, 수정, 삭제 (로그인 해야 읽기 가능 - 수정/삭제는 작성자만 가능)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)

    # 디테일 가져오기
    if request.method == 'GET':
        serializer = ArticleListSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 수정 또는 삭제는 작성자만 가능
    if request.user != article.user:
        return Response({'error': '게시글 수정/삭제는 작성자만 가능합니다.'},
                        status=status.HTTP_403_FORBIDDEN)
    
    # 수정
    if request.method == 'PUT':
        serializer = ArticleCreateSerializer(instance=article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
    # 삭제
    if request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 댓글 리스트 가져오기 (로그인 해야 가능)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_comments(request, article_id):
    article = Article.objects.get(id=article_id)
    # 댓글 가져오기
    if request.method == 'GET':
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 댓글 쓰기
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 삭제 (로그인 된 작성자만 가능)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def article_comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id, article_id=article_id)
    
    # 댓글 작성자만 삭제 가능
    if comment.user != request.user:
        return Response({'error': '게시글 수정/삭제는 작성자만 가능합니다.'},
                        status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 게시글 스크랩 (로그인 된 사용자만 가능)
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_scrap(request, article_id):
    # 현재 user의 pk
    # 현재 게시글의 pk
    if request.method == 'POST':
        print(request.data)
        serializer = ArticleScrapSerializer(data={'article': article_id})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    if request.method == 'DELETE':
        # article_id = request.data.get('article')

        article = ArticleScrap.objects.filter(user=request.user, article=article_id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# isScrapped 확인
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_article_scrapped(request, article_id):
    exists = ArticleScrap.objects.filter(user=request.user, article_id=article_id).exists()
    return Response({'is_scrapped': exists}, status=status.HTTP_200_OK)