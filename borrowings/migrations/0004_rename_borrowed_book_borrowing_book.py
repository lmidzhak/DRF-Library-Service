# Generated by Django 4.1 on 2024-09-13 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0003_alter_borrowing_actual_return_date"),
    ]

    operations = [
        migrations.RenameField(
            model_name="borrowing",
            old_name="borrowed_book",
            new_name="book",
        ),
    ]
