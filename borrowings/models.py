from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrowings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    def __str__(self):
        return (f"{self.book} borrowed by "
                f"{self.user} {self.borrow_date}")

    def clean(self):
        if self.borrow_date > self.expected_return_date:
            raise ValidationError(
                "Expected return date should be after the borrowing date"
            )

        if self.actual_return_date > self.borrow_date:
            raise ValidationError(
                "Expected return date should after the borrowing date"
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
