from django.shortcuts import render, get_object_or_404, redirect

from myapp.forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
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
            feedback_choices = form.cleaned_data['feedback']
            feedback_display = {
                'B': 'Borrow',
                'P': 'Purchase'
            }
            feedback_full_names = [feedback_display[choice] for choice in feedback_choices]
            return render(request, 'myapp/fb_results.html', {'choices': feedback_full_names})
    else:
        form = FeedbackForm()
    return render(request, 'myapp/feedback.html', {'form': form})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            if category:
                booklist = Book.objects.filter(category=category, price__lte=max_price)
            else:
                booklist = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html', {
                'name': name,
                'category': category,
                'booklist': booklist,
                'max_price': max_price
            })

            return render(request, 'myapp/results.html', {'name': name, 'booklist': booklist})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            form.save_m2m()  # Save the many-to-many data for the form
            member = order.member
            if order.order_type == 1:  # If order type is 'Borrow'
                for book in order.books.all():
                    member.borrowed_books.add(book)
            return render(request, 'myapp/order_response.html', {'order': order, 'books': order.books.all()})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save()
                book = review.book
                book.num_reviews += 1
                book.save()
                return redirect('myapp:index')  # Change 'index' to your actual index view name
            else:
                return render(request, 'myapp/review.html', {'form': form, 'error': 'You must enter a rating between 1 and 5!'})
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})