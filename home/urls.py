from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path("", views.home, name="home"),

    path("books/", views.book_list, name="book_list"),
    path("books/add/", views.book_create, name="book_add"),
    path("books/<int:pk>/edit/", views.book_update, name="book_edit"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),

    path("members/", views.member_list, name="member_list"),
    path("members/add/", views.member_create, name="member_add"),
    path("members/<int:pk>/edit/", views.member_update, name="member_edit"),

    path("borrows/", views.borrow_list, name="borrow_list"),
    path("borrows/add/", views.borrow_create, name="borrow_add"),
    path("borrows/<int:pk>/return/", views.borrow_return, name="borrow_return"),
]