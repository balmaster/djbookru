# -*- coding: utf-8 -*-

from decorators import render_to
from main.models import Book
from django.http import Http404
from django.db.models import ObjectDoesNotExist
from main.forms import FeedbackForm
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
import markdown


@render_to('main/index.html')
def index(request):
    book = Book.get()
    return {
        'book': book
    }


@render_to('main/first_page.html')
def first_page(request):
    try:
        book = Book.get()
        page = book.pages.get(slug='index')
    except ObjectDoesNotExist:
        page = None
    return {
        'page': page
    }


@render_to('main/page.html')
def page(request, slug):
    try:
        book = Book.get()
        page = book.pages.get(slug=slug)
    except ObjectDoesNotExist:
        raise Http404
    return {
        'page': page
    }


@render_to('main/search.html')
def search(request):
    return {}


@render_to('main/feedback.html')
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, initial={'captcha': request.META['REMOTE_ADDR']})
        if form.is_valid():
            form.send(request)
            messages.success(request, _(u'Feedback sent success!'))
            return redirect('main:feedback')
    else:
        form = FeedbackForm(initial={'referer': request.META.get('HTTP_REFERER', '')})
    return {
        'form': form
    }


def test_error_email(request):
    raise Exception('Test!')
    return


@login_required
@render_to('main/markdown_preview.html')
def markdown_preview(request):
    data = request.POST.get('data', '')
    data = markdown.markdown(data, safe_mode='escape')
    return {'data': data}
