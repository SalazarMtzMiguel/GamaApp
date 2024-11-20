from django.shortcuts import render

# Create your views here.


def my_view(request):
    lista=[
        {
            "title":"BMW"
        },{
            "title":"Mazda"
        },{
            "title":"Nissan"
        },
    ]
    context = {"lista":lista}
    return render(request, 'index.html',context)