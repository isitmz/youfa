from django.shortcuts import render

# Vista per la pagina principale dell'applicazione.
def index(request):
    """
    Renderizza la pagina principale (homepage) dell'applicazione.

    Args:
        request: L'oggetto HttpRequest.

    Returns:
        HttpResponse: La pagina HTML 'home/index.html' renderizzata.
    """
    return render(request, 'home/index.html')