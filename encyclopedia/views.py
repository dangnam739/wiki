import random

from django.shortcuts import render
from django import forms

from . import util

from markdown2 import Markdown

markdowner = Markdown()


class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'myfieldclass',
        'placeholder': 'Search'
    }))

class Post(forms.Form):
    title = forms.CharField(label="Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
    entries = util.list_entries()
    searched = []

    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    return render(request, "encyclopedia/entry.html", {
                        "page": page_converted,
                        "title": item,
                        "form": Search()
                    })
                if item.lower() in i.lower():
                    searched.append(i)
            return render(request, "encyclopedia/search.html", {
                "searched": searched,
                "form": Search()
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": Search()
        })


def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        return render(request, "encyclopedia/entry.html", {
            "page": page_converted,
            "title": title,
            "form": Search()
        })
    else:
        return (request, "encyclopedia/erro.html", {
            "message": "The requested page was not found.",
            "form": Search()
        })

def create(request):
    if request.method == "POST":
        forms = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {
                    "form": Search(),
                    "message": "Page already exist"
                })
            else:
                util.save_entry(title, textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)
                return render(request, "encyclopedia/entry.html", {
                    "form": Search(),
                    "page": page_converted,
                    "title":title
                })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": Search(),
            "post": Post()
        })