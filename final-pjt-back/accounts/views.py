from django.shortcuts import render
from dj_rest_auth.views import LoginView
from .serializers import CustomLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from policies.models import PolicyScrap
from policies.serializers import PolicySerializer
from articles.models import ArticleScrap
from articles.serializers import ArticleSerializer

# Create your views here.



class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

# 스크랩한 정책
class ScrapedPolicesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        scraps = PolicyScrap.objects.filter(user=user)
        policies = [scrap.policy for scrap in scraps]
        
        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data)

# 스크랩한 게시글
class ScrapedArticlesView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        scraps = ArticleScrap.objects.filter(user=user)
        articles = [scrap.article for scrap in scraps]
        
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)