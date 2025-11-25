from django.db import models

from django.urls import reverse

class BookCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("books:category_list")


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    publishing_date = models.DateField()
    category = models.ForeignKey(BookCategory, on_delete=models.PROTECT, related_name="books")
    distribution_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ["title"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["publishing_date"]),
        ]

    def __str__(self):
        return f"{self.title} — {self.author}"

    def get_absolute_url(self):
        return reverse("books:book_list")

# Create your models here.
