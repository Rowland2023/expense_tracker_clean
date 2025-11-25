import io
import csv
from datetime import datetime

import pandas as pd
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from django import forms

from .models import BookCategory, Book


# ===== CRUD views for categories =====
class CategoryListView(ListView):
    model = BookCategory
    template_name = "books/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(CreateView):
    model = BookCategory
    fields = ["name"]
    template_name = "books/category_form.html"
    success_url = reverse_lazy("books:category_list")


class CategoryUpdateView(UpdateView):
    model = BookCategory
    fields = ["name"]
    template_name = "books/category_form.html"
    success_url = reverse_lazy("books:category_list")


class CategoryDeleteView(DeleteView):
    model = BookCategory
    template_name = "books/category_confirm_delete.html"
    success_url = reverse_lazy("books:category_list")


# ===== CRUD views for books =====
class BookListView(ListView):
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 20


class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "publishing_date", "category", "distribution_expenses"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", "author", "publishing_date", "category", "distribution_expenses"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:book_list")


# ===== Import view (CSV/XLSX) =====

class ImportForm(forms.Form):
    file = forms.FileField(
        help_text="Upload a CSV or XLSX file with columns: title, author, publishing_date (YYYY-MM-DD), category, distribution_expenses"
    )


class ImportView(FormView):
    template_name = "books/import.html"
    form_class = ImportForm
    success_url = reverse_lazy("books:book_list")

    def form_valid(self, form):
        upload = form.cleaned_data["file"]
        name = upload.name.lower()

        try:
            if name.endswith(".csv"):
                self._import_csv(upload)
            elif name.endswith(".xlsx"):
                self._import_xlsx(upload)
            else:
                messages.error(self.request, "Unsupported file type. Please upload .csv or .xlsx.")
                return HttpResponseRedirect(self.request.path)
        except Exception as e:
            messages.error(self.request, f"Import failed: {e}")
            return HttpResponseRedirect(self.request.path)

        messages.success(self.request, "Import completed successfully.")
        return super().form_valid(form)

    def _import_csv(self, upload):
        data = upload.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(data))
        self._upsert_rows(reader)

    def _import_xlsx(self, upload):
        df = pd.read_excel(upload)  # requires openpyxl
        # Normalize headers
        df.columns = [str(c).strip().lower() for c in df.columns]
        required = {"title", "author", "publishing_date", "category", "distribution_expenses"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        rows = df.to_dict(orient="records")
        self._upsert_rows(rows)

    def _upsert_rows(self, rows):
        # Expect keys: title, author, publishing_date, category, distribution_expenses
        for row in rows:
            title = str(row["title"]).strip()
            author = str(row["author"]).strip()
            # Parse date
            publishing_date_raw = row["publishing_date"]
            if isinstance(publishing_date_raw, (datetime,)):
                publishing_date = publishing_date_raw.date()
            else:
                publishing_date = datetime.strptime(str(publishing_date_raw).strip(), "%Y-%m-%d").date()
            # Category
            category_name = str(row["category"]).strip()
            category, _ = BookCategory.objects.get_or_create(name=category_name)
            # Expenses
            expenses = str(row["distribution_expenses"]).replace(",", "").strip()
            distribution_expenses = float(expenses) if expenses else 0.0

            # Create or update by (title, author, date)
            obj, created = Book.objects.update_or_create(
                title=title,
                author=author,
                publishing_date=publishing_date,
                defaults={
                    "category": category,
                    "distribution_expenses": distribution_expenses,
                },
            )


# ===== Report view (aggregate expenses by category) =====

class ReportView(TemplateView):
    template_name = "books/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggregate total distribution_expenses per category
        aggregates = (
            Book.objects
            .values("category__name")
            .annotate(total_expenses=Sum("distribution_expenses"))
            .order_by("category__name")
        )
        context["aggregates"] = aggregates
        # Grand total
        context["grand_total"] = Book.objects.aggregate(total=Sum("distribution_expenses"))["total"] or 0
        return context
