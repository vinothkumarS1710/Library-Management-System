from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Book, Member, BorrowTransaction, Author
from .forms import BookForm, MemberForm, BorrowForm
from django.utils import timezone
from datetime import date

def home(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    borrowed = BorrowTransaction.objects.filter(returned_at__isnull=True).count()
    context = {"total_books": total_books, "total_members": total_members, "borrowed": borrowed}
    return render(request, "library/home.html", context)

def book_list(request):
    books = Book.objects.all().order_by("title")
    return render(request, "library/book_list.html", {"books": books})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, "Book added.")
            return redirect("library:book_list")
    else:
        form = BookForm()
    return render(request, "library/book_form.html", {"form": form, "title": "Add Book"})

def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect("library:book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "library/book_form.html", {"form": form, "title": "Edit Book"})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted.")
        return redirect("library:book_list")
    return render(request, "library/book_confirm_delete.html", {"book": book})

def member_list(request):
    members = Member.objects.all().order_by("first_name")
    return render(request, "library/member_list.html", {"members": members})

def member_create(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Member added.")
            return redirect("library:member_list")
    else:
        form = MemberForm()
    return render(request, "library/member_form.html", {"form": form, "title": "Add Member"})

def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Member updated.")
            return redirect("library:member_list")
    else:
        form = MemberForm(instance=member)
    return render(request, "library/member_form.html", {"form": form, "title": "Edit Member"})

def borrow_list(request):
    borrows = BorrowTransaction.objects.select_related("book", "member").all().order_by("-borrowed_at")
    return render(request, "library/borrow_list.html", {"borrows": borrows})

def borrow_create(request):
    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            bt = form.save(commit=False)
            book = bt.book
            if book.copies_available < 1:
                messages.error(request, "No copies available for this book.")
                return redirect("library:borrow_add")
        
            book.copies_available -= 1
            book.save()
            bt.save()
            messages.success(request, "Book borrowed.")
            return redirect("library:borrow_list")
    else:
        form = BorrowForm()
    return render(request, "library/borrow_form.html", {"form": form, "title": "Borrow Book"})

def borrow_return(request, pk):
    bt = get_object_or_404(BorrowTransaction, pk=pk)
    if bt.returned_at:
        messages.info(request, "This book is already returned.")
        return redirect("library:borrow_list")

    if request.method == "POST":
        bt.returned_at = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        today = date.today()
        if bt.due_date < today:
            days_late = (today - bt.due_date).days
            bt.fine = days_late * 1  # adjust rate as needed
        bt.save()
        
        book = bt.book
        book.copies_available = min(book.copies_total, book.copies_available + 1)
        book.save()
        messages.success(request, "Book returned.")
        return redirect("library:borrow_list")

    return render(request, "library/borrow_confirm_return.html", {"borrow": bt})