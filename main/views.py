from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from datetime import date
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
#Create your views here.

def home(request):
	home="active"
	articles=PublishedArticle.objects.all()
	countP=Article.objects.filter(status="Pending")
	article=PublishedArticle.objects.filter(title="How to write an Article?")[0]
	sidebar=PublishedArticle.objects.all()
	context={"home":home,"articles":articles,"countP":len(countP),"article":article,"sidebar":sidebar}
	return render(request,"main/home.html",context)



def register(request):
	if request.method == 'POST':
		get_otp = request.POST.get('otp') #213243 #None

		if get_otp:
			get_usr = request.POST.get('usr')
			usr = User.objects.get(username=get_usr)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				messages.success(request, f'Account is Created For {usr.username}')
				return redirect('login')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'main/register.html', {'otp': True, 'usr': usr})

		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			usr = User.objects.get(username=username)
			usr.email = usr.email
			usr.is_active = False
			usr.save()
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)

			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to CoderGeek - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)

			return render(request, 'main/register.html', {'otp': True, 'usr': usr})

		
	else:
		form = SignUpForm()

	return render(request, 'main/register.html', {'form':form})
		


def resend_otp(request):
	if request.method == "GET":
		get_usr = request.GET['usr']
		if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
			usr = User.objects.get(username=get_usr)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to CoderGeek - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return HttpResponse("Resend")

	return HttpResponse("Can't Send ")


def login_view(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':
		get_otp = request.POST.get('otp') #213243 #None

		if get_otp:
			get_usr = request.POST.get('usr')
			usr = User.objects.get(username=get_usr)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				login(request, usr)
				return redirect('home')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'registration/login.html', {'otp': True, 'usr': usr})


		usrname = request.POST['username']
		passwd = request.POST['password']

		user = authenticate(request, username = usrname, password = passwd) #None
		if user is not None:
			login(request, user)
			return redirect('home')
		elif not User.objects.filter(username = usrname).exists():
			messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
			return redirect('login')
		elif not User.objects.get(username=usrname).is_active:
			usr = User.objects.get(username=usrname)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to CoderGeek - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return render(request, 'registration/login.html', {'otp': True, 'usr': usr})
		else:
			messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
			return redirect('login')

	form = AuthenticationForm()
	return render(request, 'registration/login.html', {'form': form})







@login_required(login_url="/login/")
def writearticle(request):
	if request.method=="POST":
		title=request.POST.get("title")
		domain=request.POST.get("domain")
		html=request.POST.get("editordata")
		if Article.objects.filter(user=request.user,title=title,domain=domain).exists():
			article=Article.objects.filter(user=request.user,title=title,domain=domain)[0]
			article.status="Pending"
			article.html=html
			article.save()
		else:	
			article=Article(user=request.user,title=title,html=html,domain=domain,status="Pending")
			article.save()
		return render(request,"main/writearticle.html",{"title":title,"domain":domain,"html":html})
	else:
		pass
	return render(request,"main/writearticle.html")



@login_required(login_url="/login/")
def save(request):
	if request.method=="POST":
		title=request.POST.get("title")
		domain=request.POST.get("domain")
		html=request.POST.get("editordata")
		if Article.objects.filter(user=request.user,title=title,domain=domain).exists():
			article=Article.objects.filter(user=request.user,title=title,domain=domain)[0]
			article.status="Draft"
			article.html=html
			article.save()
		else:
			article=Article(user=request.user,title=title,html=html,domain=domain,status="Draft")
			article.save()
		return render(request,"main/writearticle.html",{"title":title,"domain":domain,"html":html})
	else:
		pass
	return render(request,"main/writearticle.html")



@login_required(login_url="/login/")
def editarticle(request,id):
	if request.method=="POST":
		article=Article.objects.filter(id=id)[0]
		article.title=request.POST.get("title")
		article.html=request.POST.get("editordata")
		article.domain=request.POST.get("domain")
		article.status="Pending"
		article.save()
		return HttpResponse('')
	else:
		article=Article.objects.filter(id=id)
		return render(request,"main/editarticle.html",{"article":article[0]})





@login_required(login_url="/login/")
def reviewarticle(request):
	article=Article.objects.filter(status="Pending")
	articles=PublishedArticle.objects.all()
	reviewarticle="active"
	if article == []:
		context={"reviewarticle":reviewarticle,"articles":articles}
	else:
		context={"article":article,"reviewarticle":reviewarticle,"articles":articles}
	return render(request,"main/reviewarticle.html",context)




@login_required(login_url="/login/")
def review(request,id):
	if request.method=="POST":
		article=Article.objects.filter(id=id)[0]
		article.status="Published"
		article.save()
		if PublishedArticle.objects.filter(user=article.user,title=article.title).exists():
			published=PublishedArticle.objects.filter(user=article.user,title=article.title)
			published.html=article.html
			published.domain=article.domain
			published.save()
			mess = f"Congratulation {request.user} your article {published.title} is published on our website."
			send_mail(
				"CoderGeek",
				mess,
				settings.EMAIL_HOST_USER,
				[request.user.email],
				fail_silently = False
				)
		else:
			published=PublishedArticle(user=article.user,title=article.title,html=article.html,domain=article.domain)
			published.save()
			mess = f"Congratulation {request.user} your article {published.title} is published on our website."
			send_mail(
				"CoderGeek",
				mess,
				settings.EMAIL_HOST_USER,
				[request.user.email],
				fail_silently = False
				)
		return redirect('reviewarticle')
	else:
		article=Article.objects.filter(id=id)
		return render(request,"main/particularreview.html",{"article":article[0]})




@login_required(login_url="/login/")
def deletearticle(request,id):
	article=Article.objects.filter(id=id)
	article.delete()
	article=Article.objects.filter(status="Pending")
	reviewarticle="active"
	return render(request,"main/reviewarticle.html",{"article":article,"reviewarticle":reviewarticle})



@login_required(login_url="/login/")
def allarticles(request):
	allarticles="active"
	articles=Article.objects.filter(user=request.user)
	allcount=len(articles)
	pendingcount=len(Article.objects.filter(user=request.user,status="Pending"))
	publishedcount=len(PublishedArticle.objects.filter(user=request.user))
	draftcount=len(Article.objects.filter(user=request.user,status="Draft"))
	context={"articles":articles,"allcount":allcount,"publishedcount":publishedcount,"pendingcount":pendingcount,"draftcount":draftcount,"count":0,"allarticles":allarticles,"all":"active"}
	return render(request,"main/allarticles.html",context)




@login_required(login_url="/login/")
def addjob(request):
	if request.method == "POST":
		company_name=request.POST.get("company_name")
		job_role=request.POST.get("job_role")
		description=request.POST.get("description")
		print(description)
		company_website=request.POST.get("company_website")
		application_link=request.POST.get("application_link")
		last_date=request.POST.get("date")
		if Jobs.objects.filter(company_name=company_name,job_role=job_role,last_date=last_date,application_link=application_link).exists():
			pass
		else:
			newjob=Jobs(company_name=company_name,company_website=company_website,application_link=application_link,job_role=job_role,description=description,last_date=last_date)
			print(description)
			newjob.save()
			return HttpResponseRedirect("addjob")
	else:
		today=date.today()
		articles=PublishedArticle.objects.all()
		return render(request,"main/addjobs.html",{"addjob":"active","today":today,"articles":articles})



@login_required(login_url="/login/")
def filter_article(request,status):
	if status=="Published":
		articles=PublishedArticle.objects.filter(user=request.user)
	else:
		articles=Article.objects.filter(user=request.user ,status=status)
	total=Article.objects.filter(user=request.user)
	allcount=len(total)
	pendingcount=len(Article.objects.filter(user=request.user,status="Pending"))
	publishedcount=len(PublishedArticle.objects.filter(user=request.user))
	draftcount=len(Article.objects.filter(user=request.user,status="Draft"))
	if status == "Published":
		publish = "active"
		context={"articles":articles,"allcount":allcount,"publishedcount":publishedcount,"pendingcount":pendingcount,"draftcount":draftcount,"Published":publish,"allarticles":"active"}
	elif status == "Pending":
		context = {"articles":articles,"allcount":allcount,"publishedcount":publishedcount,"pendingcount":pendingcount,"draftcount":draftcount,"Pending":"active","allarticles":"active"}
	elif status == "Draft":
		context={"articles":articles,"allcount":allcount,"publishedcount":publishedcount,"pendingcount":pendingcount,"draftcount":draftcount,"Draft":"active","allarticles":"active"}
	return render(request,"main/allarticles.html",context)




def showarticle(request,title):
	article=PublishedArticle.objects.filter(title=title)[0]
	home="active"
	articles=PublishedArticle.objects.all()
	sidebar=PublishedArticle.objects.filter(domain=article.domain)
	countP=Article.objects.filter(status="Pending")
	context={"article":article,"countP":len(countP),"articles":articles,"home":home,'sidebar':sidebar}
	return render(request,"main/home.html",context)



#JOBS
@login_required(login_url="/login/")
def jobs(request):
	job="active"
	articles=PublishedArticle.objects.all()
	jobs=Jobs.objects.all()
	if len(jobs) == 0:
		context={"job":job,"articles":articles}
	else:
		context={"job":job,"jobs":jobs,"articles":articles}
		jobs=jobs[::-1]
	return render(request,"main/jobs.html",context)



@login_required(login_url="/login/")
def profile(request):
	if request.method == "POST":
		if not Info.objects.filter(user=request.user).exists():
			info=InfoForm(request.POST,request.FILES)
			new=info.save(commit=False)
			new.sex=request.POST["sex"]
			new.save()
			return redirect("profile")
		else:
			olduser=Info.objects.filter(user=request.user)[0]
			info=InfoForm(request.POST,request.FILES)
			info=info.save(commit=False)
			olduser.name=info.name
			olduser.college=info.college
			olduser.sex=request.POST["sex"]
			olduser.profile=info.profile
			olduser.github=info.github
			olduser.linkdln=info.linkdln
			olduser.save()
			return redirect("profile")
	else:
		profile="active"
		try:
			data=Info.objects.filter(user=request.user)[0]
			info=InfoForm(instance=data)
		except:
			info=InfoForm()
		articles=PublishedArticle.objects.all()
		return render(request,"main/profile.html",{"profile":profile,"articles":articles,"infoform":info})




def search(request):
	if request.method == "POST":
		articles=Article.objects.filter(status="Published")
		countP=Article.objects.filter(status="Pending")
		title=request.POST["search"]
		home="active"
		try:
			article=PublishedArticle.objects.filter(title=title)[0]
			sidebar=PublishedArticle.objects.filter(domain=article.domain)
		except:
			article="Article is not present"
			sidebar=PublishedArticle.objects.all()
		context={"article":article,"countP":len(countP),"articles":articles,"home":home,"sidebar":sidebar}		
		return render(request,"main/home.html",context)


def courses(request):
	courses=Course.objects.all()
	return render(request,"main/courses.html",{"course":"active","courses":courses})