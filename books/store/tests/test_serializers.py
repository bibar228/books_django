import json
from django.test import TestCase

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, F

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        user3 = User.objects.create(username="user3")
        book_1 = Book.objects.create(name="Test book 1", price=25, author_name="Author 1")
        book_2 = Book.objects.create(name="Test book 2", price=55, author_name="Author 2")
        UserBookRelation.objects.create(user=user1, book=book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, rate=5)
        user_book_3 = UserBookRelation.objects.create(user=user3, book=book_1, like=True)
        user_book_3.rate = 4
        user_book_3.save()

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.all().annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))), discount_value=F("price")-(F("price")/100)*F("discount")).select_related("owner").prefetch_related("readers").order_by("id")
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                "id": book_1.id,
                "name": "Test book 1",
                "price": "25.00",
                "author_name": "Author 1",
                'discount': 0,
                "rating": "4.67",
                'discount_value': '25.00',
                'owner_name': '',
                'readers': []

            },
            {
                "id": book_2.id,
                "name": "Test book 2",
                "price": "55.00",
                "author_name": "Author 2",
                'discount': 0,
                "rating": "3.50",
                'discount_value': '55.00',
                'owner_name': '',
                'readers': []
            }
        ]
        self.assertEqual(expected_data, json.loads(json.dumps(data)))