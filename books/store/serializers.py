from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    discount_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


    class Meta:
        model = Book
        fields = ["id", "name", "price", "author_name", "likes_count", "discount", "rating", "discount_value"]

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ["book", "like", "in_bookmarks", "rate"]