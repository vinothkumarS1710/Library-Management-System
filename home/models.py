from django.db import models
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("BORROWED", "Borrowed"),
    ]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    isbn = models.CharField(max_length=20, unique=True, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="AVAILABLE")

    def __str__(self):
        return f"{self.title} ({self.author})"

    def save(self, *args, **kwargs):
        if self.copies_available > self.copies_total:
            self.copies_available = self.copies_total
        self.status = "AVAILABLE" if self.copies_available > 0 else "BORROWED"
        super().save(*args, **kwargs)

class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    join_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class BorrowTransaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def is_returned(self):
        return self.returned_at is not None

    def __str__(self):
        return f"{self.book.title} -> {self.member}"