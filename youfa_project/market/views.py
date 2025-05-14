from django.shortcuts import render

def market_home(request):
    return render(request, 'market/index.html')