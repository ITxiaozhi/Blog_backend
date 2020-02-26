from rest_framework import serializers

from apps.article.models import Article, BigCategory, Category


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
        fields = ('id', 'title', 'summary', 'update_date', 'views', 'loves')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
