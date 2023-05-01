from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation

class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class BooksSerializer(ModelSerializer):
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    discount_value = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(source="owner.username", default="", read_only=True)
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "name", "price", "author_name", "discount", "rating", "discount_value", "owner_name", "readers"]



class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ["book", "like", "in_bookmarks", "rate"]