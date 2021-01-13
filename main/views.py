from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from datetime import date
#Create your views here.

def home(request):
	home="active"
	articles=PublishedArticle.objects.all()
	countP=Article.objects.filter(status="Pending")
	article=PublishedArticle.objects.filter(title="How to write an Article?")[0]
	return render(request,"main/home.html",{"home":home,"articles":articles,"countP":len(countP),"article":article})



def register(response):
	if response.method == 'POST':
		form = UserCreationForm(response.POST)
		if form.is_valid():
			form.save()
			return redirect('login')
		else:
			form=UserCreationForm()
			return render(response,'main/register.html',{'form':form})
	else:
		if not response.user.is_authenticated:
			form=UserCreationForm()
			return render(response,'main/register.html',{'form':form})
		else:
			return redirect('home')
	return redirect('login')
		


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



def login(response):
	if response.user.is_authenticated:
		return redirect('home')
	else:
		return HttpResponseRedirect("/login/")




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
		else:
			published=PublishedArticle(user=article.user,title=article.title,html=article.html,domain=article.domain)
			published.save()
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
	countP=Article.objects.filter(status="Pending")
	return render(request,"main/home.html",{"article":article,"countP":len(countP),"articles":articles,"home":home})



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
		except:
			article="Article is not present"	
		return render(request,"main/home.html",{"article":article,"countP":len(countP),"articles":articles,"home":home})


def courses(request):
	courses=Course.objects.all()
	return render(request,"main/courses.html",{"course":"active","courses":courses})