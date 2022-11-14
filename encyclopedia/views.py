import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from markdown2 import Markdown
from . import util
markdowner = Markdown()

def index(request):
    entries = util.list_entries()
    title_list = []
    if request.method == 'POST':
        title = request.POST['title']
        for entry in entries:
            if title.lower() == entry.lower():
                return HttpResponseRedirect(reverse('encyclopedia:page', args=[title]))

        for entry in entries:
            if title.lower() in entry.lower():
                title_list.append(entry)

        if len(title_list) == 0:
            return render(request, 'encyclopedia/error.html')
        return render(request, 'encyclopedia/search_results.html', {'title_list': title_list})
    return render(request, 'encyclopedia/index.html', {
        'entries': entries
    })


def page(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, 'encyclopedia/page.html', {'title':title,
            'magic':markdowner.convert(entry)
        })
    else:
        return render(request, 'encyclopedia/error.html')


def new_page(request):
    if request.method == 'POST':
        entries = util.list_entries()
        title = request.POST['title']
        for entry in entries:
            if title.lower() == entry.lower():
                messages.warning(request, 'Similar page already exists')
                return HttpResponseRedirect(reverse('encyclopedia:new_page'))

        content = request.POST['content']
        util.save_entry(title, content)
        messages.success(request, 'Page added')
        return render(request, 'encyclopedia/new_page.html', {
            'title': title
        })
    return render(request, 'encyclopedia/new_page.html')


def edit_page(request, title):
    if request.method == 'POST':
        content = request.POST['content']
        util.save_entry(title, content)
        messages.success(request, 'Page modified.')
        return HttpResponseRedirect(reverse('encyclopedia:page', args=[title]))
    entry = util.get_entry(title)
    if entry:
        return render(request, 'encyclopedia/edit_page.html', {
            'title':title,
            'entry':entry
        })
    return render(request, 'encyclopedia/error.html')


def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse('encyclopedia:page', args=[title]))

