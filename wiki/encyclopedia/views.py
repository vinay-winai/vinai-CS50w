import secrets
import markdown2
from . import util
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse




class NewForm(forms.Form):
    title = forms.CharField(required=True,label="Title",
    widget=forms.TextInput(attrs={'placeholder':'Enter title',
    'class': 'form-control col-md-10 col-lg-10'}))
    text = forms.CharField(label="content",required=True,
    widget=forms.Textarea(attrs={'placeholder':'Type...',
    'class': 'form-control col-md-10 col-lg-10','rows':24}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(),required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request,title):
    content = util.get_entry(title)
    if content:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": markdown2.markdown(content),
        })
    return render(request, "encyclopedia/entry.html",{
            "title":title,
            })

def search(request):
    sterm = request.GET.get('q','')
    lst=util.list_entries()
    sublist=[]
    for i in lst:
        if sterm.lower() in i.lower():
            sublist.append(i)
        if sterm.lower() == i.lower():
            return entry(request,i)
    if sublist:
        return render(request, "encyclopedia/index.html", {
            "entries": sublist,
            "search": True,
            "sterm": sterm,
        })
    return entry(request,sterm)

def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title[0].islower():
                title = title.capitalize()
            content = form.cleaned_data["text"]
            if content[:3] != '# '+title[0]: 
                content = '# '+title+'\n'*2+form.cleaned_data["text"]
            if not util.get_entry(title) or form.cleaned_data["edit"]:
                util.save_entry(title, bytes(content,'utf8'))
                return HttpResponseRedirect(reverse('entry', kwargs={'title': title}))
            return render(request, "encyclopedia/new.html", {
                "form": form,
                "title": title,
                "exists": True,
            })
        return render(request, "encyclopedia/new.html", {
                "form": form,
        })
    return render(request, "encyclopedia/new.html",{
                "form": NewForm(),
            })

def edit(request,title):
    pre = util.get_entry(title)
    if pre is None:
        return entry(request,title)
    form =NewForm()
    form.fields["title"].initial = title
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["text"].initial = pre
    form.fields["edit"].initial = True
    return render(request, "encyclopedia/new.html", {
                "form": form,
                "title":form.fields["title"].initial,
                "edit": True,
            })
    

def random(request):
    lst=util.list_entries()
    rdm=secrets.choice(lst)
    return entry(request,rdm)
