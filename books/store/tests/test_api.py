import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_username")
        self.book_1 = Book.objects.create(name="Test book 1", price=25, author_name="Author 1")
        self.book_2 = Book.objects.create(name="Test book 2", price=550, author_name="Author 5")
        self.book_3 = Book.objects.create(name="Test book Author 1", price=55, author_name="Author 2")

    def test_get(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data, response.data)

    def test_get_solo_object(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BooksSerializer(self.book_1, many=False).data, response.data)


    def test_get_filter(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"price": 55})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BooksSerializer([self.book_3], many=True).data, response.data)


    def test_get_search(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"search": "Author 1"})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BooksSerializer([self.book_1, self.book_3], many=True).data, response.data)

    def test_get_sorted(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"ordering": "-price"})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(BooksSerializer([self.book_2, self.book_3, self.book_1], many=True).data, response.data)

    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse("book-list")
        data = {
            "name": "Programming in Python 3",
            "price": 150,
            "author_name": "Mark Summerfield"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(4, Book.objects.all().count())


    def test_update(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author_name": self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)

    def test_delete(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Book.objects.count(), 2)


