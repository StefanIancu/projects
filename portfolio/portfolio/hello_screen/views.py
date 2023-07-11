from django.shortcuts import render

# Create your views here.
def hello_screen(request):
    return render(request, "index.html", {})