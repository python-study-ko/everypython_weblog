from django.shortcuts import render

# Create your views here.
def index(request):
    test = 'this is index page!!'
    context = {'text':test}
    return render(request,'testboot/index.html',context)