from django.shortcuts import render, get_object_or_404

from myapp.forms import FeedbackForm
from myapp.models import Book
from django.http import HttpResponse


# Create your views here.
def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})


def about(request):
    return render(request, 'myapp/about.html')


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'myapp/detail.html', {'book': book})


def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = 'to borrow books.'
            elif feedback == 'P':
                choice = 'to purchase books.'
            else:
                choice = 'None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})
