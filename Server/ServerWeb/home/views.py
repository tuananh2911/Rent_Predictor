import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


async def index(request):
    # if request.method == 'POST':
    #     price = request.POST.get('price')
    #     data = {'price': price}
    #     print(data)
    #     return JsonResponse(data, safe=False)
    # else:
    #     return render(request, 'pages/home.html', {})
    return HttpResponse(1000000)