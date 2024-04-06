from datetime import datetime
from typing import Any

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.urls import reverse

from .models import Author, Quote, Tag
from .forms import AuthorForm, TagForm, QuoteForm
from .scraper import get_data


# Create your views here.
def index(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    context = {"page_obj": page_obj, "top_tags": top_tags, }
    return render(request, "quotes/index.html", context)

def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    context = {"author": author}
    return render(request, "quotes/about.html", context)


@login_required
def new_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("quotes:index"))
        else:
            context = {"form": form}
            return render(request, "quotes/author.html", context)
        
    return render(request, "quotes/author.html", {"form": AuthorForm()})


@login_required
def edit_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            author.name = form.cleaned_data["name"]
            author.born_date = form.cleaned_data["born_date"]
            author.born_location = form.cleaned_data["born_location"]
            author.descryption = form.cleaned_data["descryption"]
            author.save()
            return redirect(reverse("quotes:index"))
        else:
            context = {"form": form, "author": author}
            return render(request, "quotes/author.html", context)
    context = {"form": AuthorForm(instance=author), "author": author}
    return render(request, "quotes/author.html", context)


@login_required
def delete_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    author.delete()
    return redirect(reverse("quotes:index"))


@login_required
def new_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data["name"].lower()
            tag_obj = form.save(commit=False)
            tag_obj.name = tag_name
            tag_obj.save()
            return redirect(reverse("quotes:index"))
        else:
            context = {"form": form}
            return render(request, "quotes/tag.html", context)
    
    return render(request, "quotes/tag.html", {"form": TagForm()})


@login_required
def edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag_name = form.cleaned_data["name"].lower()
            tag.name = tag_name
            tag.save()
            print(tag.name, tag.id)
            return redirect(reverse("quotes:index"))
        else:
            context = {"form": form, "tag": tag}
            return render(request, "quotes/tag.html", context)
    context = {"form": TagForm(instance=tag), "tag": tag}
    return render(request, "quotes/tag.html", context)


def tag_quotes(request, tag_id):
    viewing_tag = get_object_or_404(Tag, pk=tag_id)
    quotes = Quote.objects.filter(tags__name__in=[viewing_tag.name])
    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    context = {"viewing_tag": viewing_tag, "page_obj": page_obj, "top_tags": top_tags}
    return render(request, "quotes/index.html", context)


def search_tag(request):
    query_value = request.GET.get("q").lower()
    if Tag.objects.filter(name=query_value).exists():
        tag = Tag.objects.get(name=query_value)
        return tag_quotes(request, tag.id)
    else:
        close_up_tags = Tag.objects.filter(name__icontains=query_value)
        print(close_up_tags)
        context = {"close_up_tags": close_up_tags, "query_value": query_value}
        return render(request, "quotes/search_tag.html", context)
        
@login_required
def new_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()
    
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote_to_save = form.save(commit=False)
            quote_to_save.author = Author.objects.get(name=request.POST["author"])
            quote_to_save.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                quote_to_save.tags.add(tag)
            return redirect(to="quotes:index")
        else:
            context = {"form": form, "tags": tags, "authors": authors}
            return render(request, "quotes/quote.html", context)
        
    context = {"form": QuoteForm(), "tags": tags, "authors": authors}
    return render(request, "quotes/quote.html", context)


@login_required
def edit_quote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    tags = Tag.objects.all()
    authors = Author.objects.all()
    quote_author = Author.objects.get(pk=quote.author.id)
    selected_tags = Tag.objects.filter(quote=quote)

    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            quote.quote = form.cleaned_data["quote"]
            quote.author = Author.objects.get(name=request.POST["author"])
            quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            quote.tags.clear()
            for tag in choice_tags.iterator():
                quote.tags.add(tag)
            return redirect(to="quotes:index")
        else:
            context = {"form": form, "quote": quote, "tags": tags, "authors": authors}
            return render(request, "quotes/quote.html", context)
    
    context = {
        "form": QuoteForm(instance=quote),
        "quote": quote, 
        "tags": tags, "authors": authors,
        "quote_author": quote_author, 
        "selected_tags": selected_tags}
    return render(request, "quotes/quote.html", context)


@login_required
def delete_quote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.delete()
    return redirect(reverse("quotes:index"))


@login_required
def scrape_data(request):
    quotes, authors = get_data()
    for author in authors:
        author_object = Author.objects.get_or_create(
            name=author["fullname"], 
            born_date=datetime.strptime(author["born_date"], "%B %d, %Y").date(), 
            born_location=author["born_location"], 
            descryption=author["description"])
        for quote in quotes:
            if quote["author"] == author["fullname"]:
                quote_object = Quote.objects.get_or_create(
                    quote=quote["quote"],
                    author=author_object[0])
                for tag in quote["tags"]:
                    tag_object = Tag.objects.get_or_create(name=tag)
                    quote_object[0].tags.add(tag_object[0])
                quote_object[0].save()
                
    return redirect(to="quotes:index")