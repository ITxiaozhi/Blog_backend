from rest_framework import serializers

from apps.article.models import Article, BigCategory, Category, Tag


class BigCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BigCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    # # 指定分类信息
    bigcategory_id = serializers.IntegerField()
    # 关联嵌套返回
    bigcategory = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'summary', 'create_date', 'views', 'loves')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('create_date',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

