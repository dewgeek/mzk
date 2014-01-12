from models import *

#from backends import ThirdPartyAuthBackend

from django.template import RequestContext, Context
from django.http import HttpResponse,Http404,HttpRequest
from django.shortcuts import render_to_response,HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import os

def profile(request,offset):

	try:
		kitchen = kitchen_data.objects.get(id = offset)

	except kitchen_data.DoesNotExist:
			raise Http404()
	try:
		orders_array = request.session["orders"]
	except:
		orders_array = []
		pictures_array = pictures.objects.filter(kitchen=kitchen)
	
	d = dict(kitchen = kitchen,orders = orders_array,pictures=pictures_array)
	d.update(csrf(request))	
	return render_to_response("profile.html",d,context_instance = RequestContext(request))
