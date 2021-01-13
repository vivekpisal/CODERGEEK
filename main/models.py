from django.db import models
from django.contrib.auth.models import User

#Create your models here.
class Article(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="article")
	title=models.CharField(max_length=200)
	html=models.TextField()
	domain=models.CharField(max_length=40)
	status=models.CharField(max_length=20)

	def __str__(self):
		return f"{self.title}"


class PublishedArticle(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="published_article")
	title=models.CharField(max_length=200)
	html=models.TextField()
	domain=models.CharField(max_length=40)

	def __str__(self):
		return f"{self.title}"


class Info(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="info")
	name=models.CharField(max_length=20,null=True)
	profile=models.ImageField(upload_to="images/profile",default="download.png",null=True)
	sex=models.CharField(max_length=10)
	college=models.CharField(max_length=100)
	github=models.URLField(max_length=200,blank=True)
	linkdln=models.URLField(max_length=200,blank=True)

	def __str__(self):
		return f"{self.user}"


class Jobs(models.Model):
	company_name=models.CharField(max_length=50)
	company_website=models.URLField(max_length=200,blank=True)
	application_link=models.URLField(max_length=200,blank=True)
	job_role=models.CharField(max_length=15)
	description=models.TextField()
	last_date=models.DateField(null=True)

	def __str__(self):
		return f"company_name:-{self.company_name} Job_Role:{self.job_role}"


class Course(models.Model):
	course_name=models.CharField(max_length=50)
	course_link=models.URLField(max_length=300)
	description=models.TextField()
	course_mentor=models.CharField(max_length=50,null=True)
	course_pic=models.ImageField(upload_to="images/course/",null=True)


	def __str__(self):
		return f"Course :- {self.course_name} Mentor :- {self.course_mentor}"