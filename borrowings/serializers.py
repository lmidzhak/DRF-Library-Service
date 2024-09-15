from rest_framework import serializers
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"
        )


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField(read_only=True)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "expected_return_date"
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book.title", read_only=False)
    book_author = serializers.CharField(source="book.author", read_only=False)
    book_cover = serializers.CharField(source="book.cover", read_only=False)
    book_daily_fee = serializers.CharField(source="book.daily_fee", read_only=False)
    user = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "book_author",
            "book_cover",
            "book_daily_fee",
            "user"
        )
