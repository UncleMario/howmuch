from howmuch.core.forms import RequestItemForm, ProfferForm, AssignmentForm
from howmuch.core.models import RequestItem, Proffer
from howmuch.core.functions import UserRequestItem
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta, date
from django.template import RequestContext
import datetime

@login_required(login_url="/login/")
def home(request):
	return render_to_response('core/home.html', context_instance=RequestContext(request))


@login_required(login_url="/login/")
def requestItem(request):
	if request.method == 'GET':
		title = "Pago $ " + request.GET['precio'] + " Por " + request.GET['descripcion'] 
	if request.method == 'POST':
		form = RequestItemForm(request.POST)
		if form.is_valid():
			newItem = form.save(commit=False)
			newItem.owner = request.user
			newItem.save()
			return HttpResponseRedirect('/thanks/')
	else:
		form = RequestItemForm(initial={'title' : title, 'price' : request.GET['precio'], 'addressDelivery' : request.user.get_profile().getAddressDelivery()})
	return render_to_response('core/newitem.html', {'form' : form}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def newProffer(request,itemId):
	"""
	Validar que el RequestItemF exista, si no existe regresa error 404
	"""

	requestItem = get_object_or_404(RequestItem, pk = itemId)

	"""
	Se crea una instancia de UserRequestItem
	"""

	userRequestItem = UserRequestItem(request.user, itemId)

	"""
	Se valida la instancia: USer is not candidate, is not owner, is not assigned
	"""

	if userRequestItem.is_valid():
		pass
	else:
		return render_to_response('core/candidatura.html', {'errors' : userRequestItem.errors() }, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = ProfferForm(request.POST)
		if form.is_valid():
			newProffer = form.save(commit=False)
			newProffer.owner = request.user
			newProffer.requestItem = requestItem
			newProffer.save()
			return HttpResponseRedirect('/Thanks/')
	else:
		form = ProfferForm()
	return render_to_response('core/candidatura.html', {'form' : form, 'requestItem' : requestItem, 'user' : request.user }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def viewCandidates(request, itemId):
	candidates = get_list_or_404(Proffer, requestItem = itemId)
	return render_to_response('core/candidatesList.html', {'candidates' : candidates }, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def newAssignment(request, itemId, candidateID):
	candidate = get_object_or_404(Proffer, owner = candidateID)
	candidateUser = get_object_or_404(User, pk = candidateID)
	item = get_object_or_404(RequestItem, pk= itemId)

	if request.method == 'POST':
		form = AssignmentForm(request.POST)
		if form.is_valid():
			newAssignment = form.save(commit=False)
			newAssignment.owner = candidateUser 
			newAssignment.requestItem = item
			newAssignment.save()
			return HttpResponseRedirect("/Thanks/")
	else:
		form = AssignmentForm()
	return render_to_response('core/newAssignment.html', {'form' : form}, context_instance=RequestContext(request))
