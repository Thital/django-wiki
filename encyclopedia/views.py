from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django import forms
import random
import markdown2
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="",widget=forms.Textarea,)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def getpage(request, page):
    if util.get_entry(page) == None:
        return render(request, f"encyclopedia/error.html", )

    return render(request, f"encyclopedia/entry.html", {
        "title": page,
        "content": markdown2.markdown(util.get_entry(page))
    })

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return HttpResponse("Error \n This entry already exists")
            util.save_entry(title, content)
            return getpage(request,title)
    return render(request, "encyclopedia/new_entry.html",{
        "form": NewEntryForm()
    })

def search(request):
    query = request.GET.get('query')
    if util.get_entry(query) != None:
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": markdown2.markdown(util.get_entry(query))
        })
    return render(request, "encyclopedia/search.html", {
        "entries": util.list_entries(),
        "query": query
    })

def random_page(request):
    pages = util.list_entries()
    page = pages[random.randint(0,len(pages)-1)]
    return render(request, "encyclopedia/entry.html", {
        "title": page,
        "content": markdown2.markdown(util.get_entry(page))
    })

def edit(request, page):
    form_content = util.get_entry(page)
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return getpage(request,title)
    return render(request, "encyclopedia/edit.html", {
        "title": page,
        "form": NewEntryForm(initial={"content":form_content, "title": page})
    })
