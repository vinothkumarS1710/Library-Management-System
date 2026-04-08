from django import forms
from .models import Book, Member, BorrowTransaction, Author
from django.forms.widgets import DateInput

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "publication_date", "copies_total", "copies_available"]
        widgets = {"publication_date": DateInput(attrs={"type": "date"})}

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["first_name", "last_name", "email", "join_date"]
        widgets = {"join_date": DateInput(attrs={"type": "date"})}

class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowTransaction
        fields = ["book", "member", "due_date"]
        widgets = {"due_date": DateInput(attrs={"type": "date"})}