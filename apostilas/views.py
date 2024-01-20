from django.shortcuts import render, redirect
from apostilas.models import Apostila, ViewApostila
from django.contrib.messages import constants
from django.contrib import messages

def adicionar_apostilas(request):    
    if not request.user.is_authenticated:
        messages.add_message(
                    request,
                    constants.INFO,
                    'Efetue o login para acessar',
                )
        return redirect('/usuarios/logar/')
    
    if request.method == 'GET':
        apostilas = Apostila.objects.filter(user=request.user)
        views_totais = ViewApostila.objects.filter(apostila__user = request.user).count()                
        return render(
            request, 'adicionar_apostilas.html',
            {'apostilas': apostilas, 'views_totais': views_totais},
                    
        )
        
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo']
        apostila = Apostila(user=request.user, titulo=titulo, arquivo=arquivo)
        apostila.save()
        messages.add_message(
            request, constants.SUCCESS, 'Apostila adicionada com sucesso.'
        )
        return redirect('/apostilas/adicionar_apostilas/')
    
def apostila(request, id):
    if not request.user.is_authenticated:
        messages.add_message(
                    request,
                    constants.INFO,
                    'Efetue o login para acessar',
                )
        return redirect('/usuarios/logar/')
    
    apostila = Apostila.objects.get(id=id)    
    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()

    view = ViewApostila(
        ip=request.META['REMOTE_ADDR'],
        apostila=apostila
    )
    view.save()
    return render(request, 'apostila.html', {'apostila' : apostila, 'views_unicas' : views_unicas, 'views_totais' : views_totais})
