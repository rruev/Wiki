from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from . import util
from .forms import NewPageForm


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, title):
    contentMd = util.get_entry(title)

    if not contentMd:
        results = [entry for entry in util.list_entries() if title.lower() in entry.lower()]

        if len(results) == 0:
            return render(request, "encyclopedia/error.html", {
                "title": title
            })
        
        return render(request, "encyclopedia/search.html", {
            "title": title,
            "results": results
        })

    content = util.markdown_to_html(contentMd)

    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": content
    })


def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            existing_entry = any(entry == form.cleaned_data["title"] for entry in util.list_entries())
            
            if existing_entry:
                messages.error(request, "An entry with this title already exists.")
                return redirect(reverse("encyclopedia:new"))
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])

