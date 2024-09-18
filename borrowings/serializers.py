import datetime

from rest_framework import serializers
from books.models import Book
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "borrowed_book",
            "borrower"
        )


class BorrowingListSerializer(serializers.ModelSerializer):
    borrowed_book = serializers.StringRelatedField(read_only=True)
    borrower = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrowed_book",
            "borrower",
            "expected_return_date"
        )

    def validate(self, data):
        if self.data.user.id is None:
            raise serializers.ValidationError("To see this page, you must be logged in.")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    borrowed_book_title = serializers.CharField(source="borrowed_book.title", read_only=False)
    borrowed_book_author = serializers.CharField(source="borrowed_book.author", read_only=False)
    borrowed_book_cover = serializers.CharField(source="borrowed_book.cover", read_only=False)
    borrowed_book_daily_fee = serializers.CharField(source="borrowed_book.daily_fee", read_only=False)
    borrower = serializers.SlugRelatedField(slug_field="email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "borrowed_book_title",
            "borrowed_book_author",
            "borrowed_book_cover",
            "borrowed_book_daily_fee",
            "borrower"
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    borrowed_book = serializers.SlugRelatedField(
        slug_field="title", read_only=False, queryset=Book.objects.all()
    )
    expected_return_date = serializers.DateField(read_only=False)
    actual_return_date = serializers.DateField(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "borrowed_book",
            "borrower"
        )

    def validate(self, data):

        borrowed_book = data["borrowed_book"]
        expected_return_date = data["expected_return_date"]
        if not data.get("borrow_date"):
            borrow_date = datetime.date.today()

        if expected_return_date and borrow_date > expected_return_date:
            raise serializers.ValidationError(
                "Expected return date should be after the borrowing date"
            )

        if borrowed_book.inventory <= 0:
            raise serializers.ValidationError(
                "You cannot currently borrow this book"
            )

        return data

    def create(self, validated_data):
        borrower = validated_data.pop("borrower")
        borrowed_book = validated_data["borrowed_book"]
        borrowed_book.inventory -= 1
        borrowed_book.save()

        borrowing = Borrowing.objects.create(borrower=borrower, **validated_data)
        return borrowing
