from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models




# Create your models here.
from xlwt.ExcelFormulaLexer import false_pattern


class Tag(models.Model):
    tag_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.tag_name

class UserProfile(models.Model):
    ROLE = (
              ('A', 'ADMIN'),
              ('E', 'EDITOR'),
              ('R', 'REGULAR'),
              )

    user = models.OneToOneField(User)
    role = models.CharField(max_length= 30, choices=ROLE, default='R')
    image = models.FileField(null=True, blank=True )
    # image = models.ImageField(upload_to='images_folder/articles', default='images_folder/none/no-img.jpg',null=False,blank=True)
    #other fields here
    
    def __str__(self):
        return "%s's profile" % self.user

    class Meta:
        ordering = ["-user"]

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Article(models.Model):
    # STATUS = (
    #                ('R', 'DRAFT'),
    #                ('P', 'PUBLISHED'),
    #                ('A', 'APPROVED'),
    #                ('D', 'DELETED'),
    #                )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100,null=False,blank=True)
    body = models.TextField(max_length=200,null=False,blank=True)
    image = models.FileField(null=True, blank=True)
    # article_img = models.ImageField(upload_to="images_folder/articles/", default='images_folder/none/no-img.jpg',null=False,blank=True)
    publish_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    update_date = models.DateField(auto_now_add=False, auto_now=True)
    publish = models.BooleanField(default=False)
    # status = models.CharField(max_length=30, choices=STATUS, default='R')
    approved = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    read_later = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='readlater+')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user), default=1)

    # article_readlater = models.ManyToManyField(User)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles:details", kwargs={'id': self.id})
    # return "/blog/%s" %(self.id)


class Comment(models.Model):
    comment_content = models.CharField(max_length=1000)
    comment_article_id = models.ForeignKey(Article, on_delete=models.CASCADE)
    # comment_user_id=models.ForeignKey(Article,on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)
    reply = models.OneToOneField('self',null=False,blank=True)
    # comment_by = models.ForeignKey(User)
    def __str__(self):
        return self.comment_content

class banned(models.Model):
    word = models.CharField(max_length=50)

    def __str__(self):
        return self.word
    

