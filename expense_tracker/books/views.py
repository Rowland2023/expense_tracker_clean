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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Import your models from the current application
# NOTE: Ensure BookCategory and Book models exist in your models.py
from .models import BookCategory, Book

# ----------------------------------------------------------------------
# 🔑 Authentication Views
# ----------------------------------------------------------------------

class RegisterView(CreateView):
    """Handles user registration using Django's built-in UserCreationForm."""
    form_class = UserCreationForm
    template_name = 'books/register.html'
    
    # Redirects to the namespaced login URL after successful registration
    success_url = reverse_lazy('books:login')


# ----------------------------------------------------------------------
# 📚 CRUD views for categories (Login Required)
# ----------------------------------------------------------------------

class CategoryListView(LoginRequiredMixin, ListView):
    model = BookCategory
    template_name = "books/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = BookCategory
    fields = ["name"]
    template_name = "books/category_form.html"
    success_url = reverse_lazy("books:category_list")


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = BookCategory
    fields = ["name"]
    template_name = "books/category_form.html"
    success_url = reverse_lazy("books:category_list")


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = BookCategory
    template_name = "books/category_confirm_delete.html"
    success_url = reverse_lazy("books:category_list")


# ----------------------------------------------------------------------
# 📖 CRUD views for books (Login Required)
# ----------------------------------------------------------------------

class BookListView(LoginRequiredMixin, ListView):
    # This is the class that was reported as missing
    model = Book
    template_name = "books/book_list.html"
    context_object_name = "books"
    paginate_by = 20


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["title", "subtitle", "authors", "publisher", "published_date", "category", "distribution_expenses"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ["title", "subtitle", "authors", "publisher", "published_date", "category", "distribution_expenses"]
    template_name = "books/book_form.html"
    success_url = reverse_lazy("books:book_list")


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "books/book_confirm_delete.html"
    success_url = reverse_lazy("books:book_list")


# ----------------------------------------------------------------------
# 📥 Import view (CSV/XLSX) (Login Required)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# 📥 Import view (CSV/XLSX) (Login Required)
# ----------------------------------------------------------------------

class ImportForm(forms.Form):
    file = forms.FileField(
        help_text="Upload a CSV or XLSX file with columns: title, subtitle, authors, publisher, published_date (YYYY-MM-DD), category, distribution_expenses"
    )


class ImportView(LoginRequiredMixin, FormView):
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
        df = pd.read_excel(upload)
        # Normalize headers
        df.columns = [str(c).strip().lower() for c in df.columns]
        required = {"title", "subtitle", "authors", "publisher", "published_date", "category", "distribution_expenses"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        rows = df.to_dict(orient="records")
        self._upsert_rows(rows)

    def _upsert_rows(self, rows):
        for row in rows:
            title = str(row["title"]).strip()
            subtitle = str(row.get("subtitle", "")).strip()
            authors = str(row["authors"]).strip()
            publisher = str(row.get("publisher", "")).strip()

            # --- Date Parsing ---
            published_date_raw = row["published_date"]
            if isinstance(published_date_raw, (datetime,)):
                published_date = published_date_raw.date()
            else:
                try:
                    date_str = str(published_date_raw).strip()
                    published_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError(f"Invalid date format for '{published_date_raw}'. Expected YYYY-MM-DD.")

            # --- Category Handling ---
            category_name = str(row["category"]).strip()
            category, _ = BookCategory.objects.get_or_create(name=category_name)

            # --- Expenses Handling ---
            expenses = str(row["distribution_expenses"]).replace(",", "").strip()
            distribution_expenses = float(expenses) if expenses else 0.0

            # Create or update by (title, author, date)
            obj, created = Book.objects.update_or_create(
                title=title,
                authors=authors,
                published_date=published_date,
                defaults={
                    "subtitle": subtitle,
                    "publisher": publisher,
                    "category": category,
                    "distribution_expenses": distribution_expenses,
                },
            )


# ----------------------------------------------------------------------
# 📊 Report view (Login Required)
# ----------------------------------------------------------------------

class ReportView(LoginRequiredMixin, TemplateView):
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

        # NEW: Aggregate by category and publisher
        by_publisher = (
            Book.objects
            .values("category__name", "publisher")
            .annotate(total_expenses=Sum("distribution_expenses"))
            .order_by("category__name", "publisher")
        )
        context["by_publisher"] = by_publisher

        return context
