from django.contrib import admin
from .models import Author, Book, Member, BorrowTransaction

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "copies_total", "copies_available", "status")
    search_fields = ("title", "isbn", "author__name")

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "join_date")
    search_fields = ("first_name", "last_name", "email")

@admin.register(BorrowTransaction)
class BorrowTransactionAdmin(admin.ModelAdmin):
    list_display = ("book", "member", "borrowed_at", "due_date", "returned_at", "fine")
    list_filter = ("returned_at",)