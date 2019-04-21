# -*- coding: utf-8 -*-
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('inputLogin', '')
        password = request.POST.get('inputPassword', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('product')
        else:
            args['login_error'] = "пользователь не найден"
            return  render_to_response('loginsys/login.html',args)

    else:
        # args['login_error'] = "Вы ничего не ввели"
        return render_to_response('loginsys/login.html',args)

@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))