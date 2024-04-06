"""Urls patterns for quotes."""

from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.index, name="index"),
    path("tag_quotes/<int:tag_id>/", views.tag_quotes, name="tag_quotes"),
    path("search_tag/", views.search_tag, name="search_tag"),
    path("author/<int:author_id>/", views.author, name="author"),
    path("new_author/", views.new_author, name="new_author"),
    path("edit_author/<int:author_id>/", views.edit_author, name="edit_author"),
    path("delete_author/<int:author_id>/", views.delete_author, name="delete_author"),
    path("new_tag/", views.new_tag, name="new_tag"),
    path("edit_tag/<int:tag_id>/", views.edit_tag, name="edit_tag"),
    path("new_quote/", views.new_quote, name="new_quote"),
    path("edit_quote/<int:quote_id>/", views.edit_quote, name="edit_quote"),
    path("delete_quote/<int:quote_id>/", views.delete_quote, name="delete_quote"),
    path("scrape_data/", views.scrape_data, name="scrape_data"),

]
