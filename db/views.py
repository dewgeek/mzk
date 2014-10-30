from models import *

#from backends import ThirdPartyAuthBackend
from .form import *
from django.template import RequestContext, Context
from django.http import HttpResponse,Http404,HttpRequest,QueryDict
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import os,json,datetime,hashlib
from datetime import date,timedelta
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail

def home(request):
	pictures_array = pictures.objects.filter(display_as_main=True)
	kitchens = kitchen_data.objects.all()
	d = dict(kitchens=kitchens,pictures=pictures_array)
	return render_to_response("index.html",d,context_instance=RequestContext(request))

def meals(request):
	pictures_array = pictures.objects.filter(display_as_main=True)
	kitchens = kitchen_data.objects.all()
	d = dict(kitchens=kitchens,pictures=pictures_array)
	return render_to_response("index.html",d)

def breakfast(request):
	pictures_array = pictures.objects.filter(display_as_main=True)
	kitchens = kitchen_data.objects.all()
	d = dict(kitchens=kitchens,pictures=pictures_array)
	return render_to_response("index.html",d)

def profile(request,offset):

	#Query for kitchen Instance
	try:
		kitchen = kitchen_data.objects.get(id = offset)
	except kitchen_data.DoesNotExist:
			raise Http404()
	
	#Query for Orders in sessions
	try:
		orders_array = request.session["orders"]
	except:
		orders_array = []

	#pictures and prices	
	pictures_array = pictures.objects.filter(kitchen=kitchen)
	prices = price_list.objects.filter(level=kitchen.foodlevel,foodtype=kitchen.foodtype)
	
	d = dict(kitchen = kitchen,orders = orders_array,pictures=pictures_array,prices = prices)
	d.update(csrf(request))	
	return render_to_response("profile.html",d,context_instance = RequestContext(request))


def receive_orders(request):

	#Check for request Method
	if request.method == "POST":
		courses = food_course.objects.all()
		dataReceived = False

		#Query for Existing session['orders']
		try:
			orders_array = request.session['orders']
		except:
			orders_array = []	
				
		#remove orders with same kitchen instance
		for elem in orders_array:
			if elem['kitchen'] == request.POST['kitchen']:
				orders_array.remove(elem)
			else:
				return HttpResponse("something else")

		#form a dict object
		list_obj = {
			"kitchen" : request.POST["kitchen"],
			"orders":[]
		}

		#populate list_obj['orders']
		for i in courses:
			if request.POST.__contains__(i.name):
				temp_order = {
					"course" : i.name, 
					"span" : request.POST['span_'+i.name],
					"cost" : int(request.POST['price_'+i.name])*int(request.POST['span_'+i.name])
				}
				
				list_obj["orders"].append(temp_order)

		#Add list_obj to orders_array and assign it to sessions
		orders_array.append(list_obj)
		request.session['orders'] = orders_array
		d = dict(orders = orders_array)
		d.update(csrf(request))	
		return render_to_response('cart.html',d)

	else:
		raise Http404	


def delete_order(request):
	if request.method == "POST":
		orders_array = request.session['orders']
		kitchen = request.POST["kitchen"]
		course = request.POST["course"]

		for index1,elem in enumerate(orders_array):
			if elem['kitchen'] == kitchen:
				for index2,order in enumerate(elem['orders']):
					if order['course'] == course:
						del orders_array[index1]['orders'][index2]
						request.session['orders'] = orders_array
						return HttpResponse(orders_array)
		return HttpResponse("found nothing")
	else:
		raise Http404	

def list_orders(request):
	try:
		orders_array = request.session["orders"]
	except:
		orders_array = []

	if request.method == 'POST':
		d = dict(orders=orders_array)
		d.update(csrf(request))
		return render_to_response('cart.html',d)
	else:
		raise Http404


def register(request):
	if request.method == 'POST':
		regs = registerForm(request.POST)
		reply={}

		if regs.is_valid():
			user_id = User.objects.create_user(regs.cleaned_data['username'],regs.cleaned_data['email'],regs.cleaned_data['password'])
			user = auth.authenticate(username=regs.cleaned_data['username'],password=regs.cleaned_data['password'])
			auth.login(request, user)
			reply["status"] = "Success"
			reply["message"] = "/cart/"
		else:
			reply["status"] = "Failed"
			reply["message"] = regs.errors

		cookie_data = json.dumps(reply)
		return HttpResponse(cookie_data)
		
	else:
		raise Http404
	
@require_http_methods(["POST"])
def login(request):
	regs = loginForm(request.POST)
	reply={}
	#return HttpResponse("w")
	if regs.is_valid():
		username = regs.cleaned_data['username']
		password = regs.cleaned_data['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			reply["status"] = "Success"
			reply["message"] = "/cart/"
		else:
			reply["status"] = "Failed"
			reply["message"] = {}
			reply["message"]["default"]="Username and Password didn't match"
	else:
		reply["status"] = "Failed"
		reply["message"] = regs.errors

	cookie_data = json.dumps(reply)
	return HttpResponse(cookie_data)

	
def portal(request):
	if not request.user.is_authenticated():
		sample_url = request.GET.get('next', '/cart/')
		d = dict(reg_form = registerForm(),login_form=loginForm())
		d.update(csrf(request))
		return render_to_response("portal.html",d,context_instance=RequestContext(request))		
	else:
		return HttpResponseRedirect("/dashboard/")		

def test(request):
	if request.user.is_authenticated():
		return HttpResponse('Logged In')
	else:
		return HttpResponse('Anon')

@login_required(login_url='/portal/')		
def logout_view(request):
	if request.user.is_authenticated():
		logout(request)	
		return HttpResponseRedirect("/")
	else:
		raise Http404

@login_required(login_url='/portal/')		
def cart(request):
	try:
		orders_array = request.session["orders"]
		if orders_array == []:
			return HttpResponseRedirect("/")	
	except:
		return HttpResponseRedirect("/")
	
	courses_array = []
	
	#return HttpResponse(orders_array)
	for elem in orders_array:
		for order in elem['orders']:
			if order['course'] not in courses_array:
				courses_array.append(order['course'])

	form_elems = ["name","address","landmark"] #definiing form elems
	
	if request.method=="POST":

		for elem in orders_array:
			kitchen_obj = kitchen_data.objects.get(name=elem["kitchen"])
#			user_obj = user_data.objects.get(user_object=request.user)		
			for order in elem['orders']:
				order["name"] = request.POST[order['course']+"_name"]
				order["mobile"] = request.POST[order['course']+"_mobile"]	
				order["address"] = request.POST[order['course']+"_address"]
				order["landmark"] = request.POST[order['course']+"_landmark"]						
				order["start_date"] = str(date.today())
				order["end_date"] = str(date.today()+timedelta(days=int(order["span"])))
				order["quantity"] = 1
				temp_order = orders(user=request.user,kitchen=kitchen_obj,start_date=order["start_date"],end_date=order["end_date"],course=food_course.objects.get(name=order["course"]),mobile=order["mobile"],address=order["address"],landmark=order["landmark"])
				temp_order.save()
		request.session["orders"] = orders_array
		return HttpResponseRedirect('/dashboard/')

	d=dict(orders=orders_array,courses=courses_array)
	d.update(csrf(request))
	return render_to_response("main_cart.html",d,context_instance=RequestContext(request))

@login_required(login_url='/portal/')
def dashboard(request):
	if request.method == "POST":
		date=request.POST["date"]
		month=request.POST["month"]
		year=request.POST["year"]		
		req_date = datetime.date(int(year),int(month),int(date))
		temp_orders = orders.objects.filter(end_date__gt=req_date,start_date__lt=req_date)

		send_orders = include_crumbs(req_date,temp_orders)		
		
		d= dict(orders = send_orders,form=AddressForm(),date=date,month=month,year=year)	
		d.update(csrf(request))	

		return render_to_response("calender_sub.html",d)
	d= dict(orders = orders.objects.filter(user=request.user))
	d.update(csrf(request))
	return render_to_response("dashboard.html",d,context_instance=RequestContext(request))

@login_required(login_url='/portal/')
def edit_order(request):
	if request.method == "POST":
		form = AddressForm(request.POST)
		if form.is_valid():
			retr_order = orders.objects.get(id=form.cleaned_data['order_id'])
			if retr_order.quantity != form.cleaned_data["quantity"]:
				temp_crumb_data = crumb_data.objects.get(name="Increased")
			else:
				temp_crumb_data = crumb_data.objects.get(name="no change")

			date=request.POST["date"]
			month=request.POST["month"]
			year=request.POST["year"]		
			req_date = datetime.date(int(year),int(month),int(date))
			try:
				get_existing_crumb = crumbs.objects.get(order=retr_order,date=req_date)
				get_existing_crumb.delete()
			except:
				pass
			temp_crumb = crumbs(order=retr_order,options=temp_crumb_data,address=form.cleaned_data['address'],mobile=form.cleaned_data['mobile'],landmark=form.cleaned_data['landmark'],quantity=request.POST['quantity'],date=req_date)
			temp_crumb.save()
			temp_orders = orders.objects.filter(end_date__gt=req_date,start_date__lt=req_date)
			send_orders = include_crumbs(req_date,temp_orders)


			d= dict(orders = send_orders,form=AddressForm())	
			d.update(csrf(request))	

			return render_to_response("calender_sub.html",d)
			
		else: 
			return HttpResponse("Failed")
	else:
		raise Http404	


@login_required(login_url='/portal/')
def remove_db_order(request):
	if request.method == "POST":
		temp_order = orders.objects.get(id=request.POST["order_id"])
		
		date=request.POST["date"]
		month=request.POST["month"]
		year=request.POST["year"]		
		req_date = datetime.date(int(year),int(month),int(date))
		temp_crumb_data = crumb_data.objects.get(name="removed")
		
		try:
			get_existing_crumb = crumbs.objects.get(order=temp_order,date=req_date)
			get_existing_crumb.delete()
		except:
			pass


		temp_crumb = crumbs(order=temp_order,options=temp_crumb_data,date=req_date)
		temp_crumb.save()
		temp_orders = orders.objects.filter(end_date__gt=req_date,start_date__lt=req_date)

		send_orders=include_crumbs(req_date,temp_orders)
		d= dict(orders = send_orders,form=AddressForm())	
		d.update(csrf(request))	
		return render_to_response("calender_sub.html",d)
	else:
		raise Http404

def include_crumbs(req_date,temp_orders):
	#return temp_orders[2]
	send_orders=[]
	
	for sample_order in temp_orders:
		try:
			order_db_obj = crumbs.objects.get(order=orders.objects.get(pk=sample_order.id),date=req_date)
			
			if order_db_obj.options.name != "removed":
				sample_order.quantity = order_db_obj.quantity
				sample_order.address = order_db_obj.address
				sample_order.landmark = order_db_obj.landmark
				send_orders.append(sample_order)
		except:
			send_orders.append(sample_order)
	return send_orders

@login_required(login_url='/portal/')		
def end_user(request):
	send_orders = []
	orders_array = orders.objects.filter(user=request.user)
	for order in orders_array:
		crumbs_array = crumbs.objects.filter(order=order)	
		temp_dict = {}
		temp_dict["order"] = order
		temp_dict["crumbs"] = crumbs_array
		send_orders.append(temp_dict)
	
	if request.method == "POST":

		if request.POST["type"] == "pswdForm":
			form=pswdForm(request.POST)
			if form.is_valid():
				u = request.user
				u.set_password(form.cleaned_data['pswd'])
				u.save()
			
			d = dict(orders=send_orders,form=form)
		else: 
			if request.POST["email"]:
				user_obj = User.objects.filter(email=request.POST["email"])
				if len(user_obj)==0:
					u=request.user
					u.email=request.POST["email"]
					u.save()
					d = dict(orders=send_orders,form=pswdForm())
				else:
					d = dict(orders=send_orders,form=pswdForm(),message="Email already in Use")

			else:
				raise Http404
	else:
		
		d = dict(orders=send_orders,form=pswdForm())
	return render_to_response("end_user.html",d,context_instance=RequestContext(request))


def about(request):
	return render_to_response("about.html",context_instance=RequestContext(request))	

def contact_us(request):
	if request.method == "POST":
		form=contactForm(request.POST)
		if form.is_valid():

			temp_message = messages(name=form.cleaned_data["name"],email=form.cleaned_data["email"],message=form.cleaned_data["message"])
			temp_message.save()
			d=dict(form=contactForm(),message="Thank you, your response is submitted ")
			
		else:
			d=dict(form=form)
			
	else:
		form=contactForm()
	
		d=dict(form=form)
	d.update(csrf(request))
	return render_to_response("contact.html",d,context_instance=RequestContext(request))	

def forgot_password(request):
	message = ""
	if request.method == "POST":
		email = request.POST["email"]
		u = User.objects.filter(email = email)
		if len(u) == 0:
			message = "No user was found with that Email ID"
		else:
			string=email+str(u[0].id)+str(date.today())
			h = hashlib.new('ripemd160')
			h.update(string)
			key = h.hexdigest()
			reset_obj = reset_key(user_object=u[0],key=key)
			reset_obj.save()

			host = "127.0.0.1:8000"
			reset_link=host+"/reset_pswd/key="+key
			msg_body="Please click on the following link to reset your Password"+reset_link+". If you didn't ask for password change, please ignore this message"
			send_mail('Change Password', msg_body, 'admin@mzk.com',[email], fail_silently=False)
			message="Your confirmation link was sent to your Email, Please check your email. "

	d=dict(message=message,type="email_change")
	d.update(csrf(request))
	return render_to_response("forgot_password.html",d,context_instance=RequestContext(request))	

def reset_pswd(request):
	if request.method=="POST":
		form=pswdForm(request.POST)
		if form.is_valid():
			u = User.objects.get(id=request.session["user"])
			u.set_password(form.cleaned_data['pswd'])
			u.save()
			return HttpResponseRedirect("/portal/")
		else:
			d=dict(type="pswd_change",form=form)
			d.update(csrf(request))
			return render_to_response("forgot_password.html",d,context_instance=RequestContext(request))			

	else:
		key = request.GET.get('key', '')
		if key:
			reset_obj = reset_key.objects.filter(key=key)
			if len(reset_obj) != 0:
				request.session["user"] = reset_obj[0].user_object.id
			else:
				raise Http404

			form=pswdForm(request.POST)
			d=dict(type="pswd_change",form=form)
			d.update(csrf(request))
			return render_to_response("forgot_password.html",d,context_instance=RequestContext(request))			
		else:
			raise Http404
