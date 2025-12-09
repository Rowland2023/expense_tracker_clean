from django.contrib import admin
from .models import BookCategory, Book, Expense

@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "authors", "publisher", "published_date", "category", "distribution_expenses")
    search_fields = ("title", "authors", "publisher")
    list_filter = ("category", "published_date")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "category", "date")
    search_fields = ("name", "category")
    list_filter = ("category", "date")
