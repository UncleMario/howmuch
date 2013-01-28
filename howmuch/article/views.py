from datetime import timedelta, date
import datetime
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from howmuch import settings
from howmuch.article.forms import ArticleForm, AssignmentForm, OfferForm
from howmuch.article.functions import AboutArticle, AboutAssignment
from howmuch.article.models import Article, Offer, Assignment
from howmuch.messages.functions import ConversationOptions
from howmuch.messages.models import Conversation
from howmuch.notifications.functions import NotificationOptions
from howmuch.notifications.models import Notification
from howmuch.profile.models import Profile
from howmuch.pictures.models import Picture

@login_required(login_url='/login/')
def post(request):
    if request.method == 'POST':
        form=ArticleForm(request.POST)
        if form.is_valid():
            newPost = form.save(commit=False)
            newPost.owner = request.user
            #Se genera el campo url sustituyendo caracteres
            newPost.title_url=newPost.title.replace(u'\xf1', 'n').replace(' ','-')
            newPost.save()
            #Se anade un +1 al total_purchases del usario
            profileUser = get_object_or_404(Profile, user=request.user)
            profileUser.total_purchases += 1
            profileUser.save()
            return HttpResponseRedirect(str(newPost.get_url()) + '?new_post=True')
    else:
        form=ArticleForm()
    return render_to_response('article/post.html', {'form' : form }, context_instance=RequestContext(request))

#Para ver un articulo no es necesario hacer login
def view(request, articleID, title_url):
    article = get_object_or_404(Article, pk=articleID)
    if request.GET.__contains__('new_post') and request.GET['new_post']:
        new_post = True
    else:
        new_post = False
    return render_to_response('article/viewArticle.html', {'article' : article, 'new_post' : new_post }, context_instance = RequestContext(request))

@login_required(login_url="/login/")
def offer(request,articleID):
    #Validar que el Article exista, si no existe regresa error 404
    article = get_object_or_404(Article, pk = articleID)    
    #Se crea una instancia de AboutArticle, funcion que realiza algunas verificaciones
    aboutArticle = AboutArticle(request.user, articleID) 
    #Se valida la instancia: User is not candidate, is not owner, is not assigned
    if aboutArticle.is_valid():
        pass
    else:
        return render_to_response('article/offer.html', {'errors' : aboutArticle.errors() }, context_instance=RequestContext(request))
    #Formulario
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            pictures=[]
            quantity=form.cleaned_data['quantity'] 
            cprice = form.cleaned_data['cprice']
            message = form.cleaned_data['message']

            #Verifica cada campo de tipo input file, si el usuario lo uso, entonces lo agrega al diccionario para enseguida guardarlos
            pictures.append(form.cleaned_data['picture1'])
            if form.cleaned_data['picture2'] is not None:
                pictures.append(form.cleaned_data['picture2'])
            if form.cleaned_data['picture3'] is not None:
                pictures.append(form.cleaned_data['picture3'])
            if form.cleaned_data['picture4'] is not None:
                pictures.append(form.cleaned_data['picture4'])
            if form.cleaned_data['picture5'] is not None:
                pictures.append(form.cleaned_data['picture5'])

            thisOffer = Offer(owner=request.user, article=article, quantity=quantity ,cprice=cprice, message=message)
            thisOffer.save()

            #Guarda el diccionario de imagenes en thisOffer.pictures
            for picture in pictures:
                thisPicture = Picture(owner = request.user, picture = picture)
                thisPicture.save()
                thisOffer.pictures.add(thisPicture)
                thisOffer.save()

            #Se envia una notificacion 
            newNotification = NotificationOptions(thisOffer, 'offer')
            newNotification.send()


            return HttpResponseRedirect('/account/sales/possible/')
    else:
        form = OfferForm()
    return render_to_response('article/offer.html', {'form' : form, 'article' : article, 'user' : request.user }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def candidates(request, articleID):
    """
    Si cuenta con los parametros get notif_type and idBack, se hacen verificaciones y se actualiza la notificacion a has_been_readed = True
    """
    if request.GET.__contains__('notif_type') and request.GET.__contains__('idBack'):
        if request.GET['notif_type'] == 'offer' and request.GET['idBack'] is not '' :
            idBack = request.GET['idBack']
            try:
                #Me aseguro que el usuario sea el dueno de la notificacion, que la notificacion este en False y la paso a True
                notification = Notification.objects.get(owner=request.user, tipo = 'offer', has_been_readed = False ,idBack = idBack)
            except Notification.DoesNotExist:
                pass
            else:
                notification.has_been_readed = True
                notification.save()
                """
                Se le quita una notificacion al total de notificaciones del usuario
                """
                profileUser = Profile.objects.get(user = request.user)
                profileUser.unread_notifications -= 1
                profileUser.save()


    candidates = Offer.objects.filter(article = articleID)
    article = get_object_or_404(Article, pk = articleID)
    return render_to_response('article/candidatesList.html', {'candidates' : candidates, 'article' : article }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def assignment(request, articleID, candidateID):
    #Validar que el item exista y que el owner de el sea el request.user
    try:
        article = Article.objects.get(pk= articleID, owner=request.user)
    except Article.DoesNotExist:
        return HttpResponse("No tienes permiso para Asignar este Solicutud")
    else:
        pass
    
    offer = get_object_or_404(Offer, owner = candidateID, article = article)
    candidate = get_object_or_404(User, pk = candidateID)

    #Validar que no exista Asignacion

    try:
        Assignment.objects.get(article = article )
    except Assignment.DoesNotExist:
        pass
    else:
        return HttpResponse("Esta Asignacion ya Existe")

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            newAssignment = form.save(commit=False)
            newAssignment.owner = candidate
            newAssignment.article = article
            newAssignment.save()
            #Se crea la Conversation correspondiente a la Asignacion
            conversation = Conversation.objects.create(assignment = newAssignment)
            conversation.save()
            #Se crea una instancia de InitialConversationContext
            newContext = ConversationOptions(article.owner, newAssignment.owner, conversation)
            newContext.createMessageByBuyer()
            newContext.createMessageBySeller()
            #Se Activa el Sistema de Notificaciones
            newNotification = NotificationOptions(newAssignment,'assignment')
            newNotification.send()
            #se anade un +1 al total_sales del usuario
            profileUser = get_object_or_404(Profile, user = newAssignment.owner)
            profileUser.total_sales += 1
            profileUser.save()

            return HttpResponseRedirect('/messages/' + str(newAssignment.conversation.pk))
    else:
        form = AssignmentForm()
    return render_to_response('article/assignment.html', {'form' : form, 'candidate' : candidate, 'article' : article }, context_instance=RequestContext(request))


