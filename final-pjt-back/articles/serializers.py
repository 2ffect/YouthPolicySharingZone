from rest_framework import serializers
from .models import Article, Comment, ArticleScrap

# 스크랩 시리얼라이즈
class ArticleSerializer(serializers.ModelSerializer):
    # 닉네임 출력용
    nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'user', 'title', 'created_at', 'nickname',)

# 게시글 작성 시리얼라이즈
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

        read_only_fields = ('user', )

# 게시글 리스트 시리얼라이즈
class ArticleListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title','content', 'created_at', 'user', 'nickname', 'user_id', )

# 댓글 시리얼라이즈
class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'nickname', 'user_id')

        read_only_fields = ('article', 'user')

# 게시글 스크랩 시리얼라이저
class ArticleScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleScrap
        fields = ('id', 'user', 'article')
        read_only_fields = ('user',)