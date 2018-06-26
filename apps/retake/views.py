from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'retake/index.html')

def createUser(request):
	result = User.objects.validateRegistration(request.POST)
	if type(result) is list:
		for error in result:
			messages.error(request, error)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
	return redirect('/home')

def login(request):
	result = User.objects.validateLogin(request.POST)
	if type(result) is str:
		messages.error(request, result)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/home')

def home(request):
    context = {
        'quotes': Quote.objects.all(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'retake/home.html', context)

def post(request):
    quotes = Quote.objects.create(
        author=request.POST['author'],
        quote=request.POST['desc'],
        uploader= User.objects.get(id=request.session['user_id'])
    )
    return redirect('/home')

def like(request):
    this_quote = Quote.objects.get(id=request.POST['quote_id'])
    this_user = User.objects.get(id=request.session['user_id'])
    this_quote.liked_by.add(this_user)
    this_quote.save()
    return redirect('/home')

def user(request, uploader_id):
    context = {
        'quotes' : Quote.objects.filter(uploader=uploader_id),
        'user' : User.objects.get(id=uploader_id)
    }
    return render(request, 'retake/user.html', context)

def edit(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'retake/edit.html', context)

def update(request, user_id):
    user = User.objects.get(id=request.POST['user_id'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect('/home')

def delete(request, quote_id):
    this = Quote.objects.get(id=quote_id)
    this.delete()
    return redirect('/home')


def logout(request):
    request.session.clear()
    return redirect('/')
# Create your views here.
