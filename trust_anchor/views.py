from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        pass
    return render(request, 'trust_anchor/index.html', {})
