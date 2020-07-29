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

def index(request):
    entries = util.list_entries()
    searched = []

    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_date["item"]
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