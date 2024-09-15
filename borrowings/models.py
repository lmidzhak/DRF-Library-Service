from django.conf import settings
from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    borrowed_book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrowings'
    )
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    def __str__(self):
        return (f"{self.borrowed_book} borrowed by "
                f"{self.borrower} {self.borrow_date}")
