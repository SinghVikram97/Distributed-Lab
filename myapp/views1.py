# Import necessary classes
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Publisher, Book, Member, Order


# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('pk')[:10]
    publisherlist = Publisher.objects.all().order_by('-city')

    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    heading2 = '<p>' + 'List of publishers: ' + '</p>'
    response.write(heading2)
    for publisher in publisherlist:
        para = '<p>' + publisher.name + ' (' + publisher.city + ')' + '</p>'
        response.write(para)

    return response


def about(request):
    return HttpResponse("This is an eBook APP.")


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    response = HttpResponse()
    title = '<p>' + 'Title: ' + book.title.upper() + '</p>'
    price = '<p>' + 'Price: $' + str(book.price) + '</p>'
    publisher = '<p>' + 'Publisher: ' + str(book.publisher) + '</p>'

    response.write(title)
    response.write(price)
    response.write(publisher)

    return response