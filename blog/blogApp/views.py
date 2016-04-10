from django.shortcuts import render, get_object_or_404, redirect, RequestContext,render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
# from django.db.models import Max
from django.conf import settings
from django.contrib import auth
from .forms import *
from .models import *
import os ,string
# from django.contrib.auth.models import User


# Create your views here.
# users_list = User.objects.all()


# categories = Tag.objects.annotate(most_recent=Max(article_add_date)).order_by('-most_recent')[:5]

# posts = list()
# for category in categories:
#   posts.append(category.post_set.latest())


def home(request):

    articles_list = Article.objects.all().order_by("-article_add_date")
    users_list = UserProfile.objects.all()
    paginator = Paginator(articles_list, 5) # Show 5 Articles per page

    page = request.GET.get('page')
    try:
        articles_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles_list = paginator.page(paginator.num_pages)


    title = "This is the Home page"
    inc = 2

    if request.user.is_authenticated():
        msg = 'Welcome %s' %(request.user)
        context = {
            'home' : True,
            'title': title,
            'users': users_list,
            'articles': articles_list,
            'i': inc,
            # 'recent': posts,
    #        'user' : user  / this doesn't work here it works directly in the HTML {{user}}
        }
    else:
        context = {
            'home' : True,
            'title': title,
            'users': users_list,
            'user': 'Login',
            'articles': articles_list,
            'i': inc,
        }
    
    return render(request, "home.html", context)



def article_create(request):
    if not request.user.is_authenticated():
        raise Http404
    form = ArticleUserForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.article_author = request.user
        instance.save()
        messages.success(request, "Article Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
        
    context = {
        'form': form
    }
    return render(request, "article_form.html", context)



def article_details(request, id):
    instance = get_object_or_404(Article, id=id)
    context = {
        'title': "Details Page",
        'instance': instance,
    }
    return render(request, "article_details.html", context)




def article_update(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Article, id=id)

    form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Article Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        'title': "Update Page",
        'instance': instance,
        'form': form,
    }
    return render(request, "article_form.html", context)



def article_delete(request, id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Article, id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("articles:home")







#----------------------------Register -----------------------#

#function to generate random string 
def generate_random_string(length, stringset=string.ascii_letters):
    return ''.join([stringset[i%len(stringset)] \
        for i in [ord(x) for x in os.urandom(length)]])
    
def register(request):
    context = RequestContext(request)
    email="not entered"
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() 
            user.set_password(user.password)           
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()
            email = user_form.cleaned_data['email']
            title="welcom"
            content="You are Welcom To Our Blog ^_^"
            send_mail(title, content, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            login_form = LoginForm()
            return render_to_response('login.html',{'login_form': login_form},context)

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm(initial={'captcha1': generate_random_string(6)})
        profile_form = UserProfileForm()
    return render_to_response('register.html',{'user_form': user_form,'profile_form': profile_form},context)

#----------------------------Login -----------------------#
def login(request):
    context = RequestContext(request)
    if request.COOKIES.get("sessionid",None):
        return render_to_response('profile.html',{},context)

    login_form = LoginForm(request.POST)
    return render_to_response('login.html',{'login_form':login_form},context)
#@csrf_exempt
def auth_view(request):
    context = RequestContext(request)
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    #---------remember me --------------#
    if not request.POST.get('remember_me', None):
        request.session.set_expiry(0)

    if user is not None:
        auth.login(request,user)
        userDetail = UserProfile.objects.get(user_id=request.session['_auth_user_id'])
        #request.session['profile_image'] = userDetail.image

        return render_to_response('profile.html',{'user_profile':user,'image':userDetail.image},context_instance=RequestContext(request))
    else:
        #return HttpResponseRedirect(reverse('login', kwargs={}))
        #return reverse('login')
        return render(request,'invalid.html')
          #---------Logout --------------#
@login_required
def logout(request):
    auth.logout(request)
    context = RequestContext(request)
    login_form = LoginForm(request.POST)
    return redirect("articles:home")


#----------------------------Profile -----------------------#
@login_required
def user_profile(request):
    userDetail = UserProfile.objects.get(user_id=request.session['_auth_user_id'])
    return render_to_response('profile.html',{'image':userDetail.image },context_instance=RequestContext(request))

@login_required
def editProfile(request):
    user_id = request.user.id
    instance1=get_object_or_404(User,id=user_id)
   # userDetail = UserProfile.objects.get(user_id=user_id)
    userDetail = UserProfile.objects.get(user_id=request.session['_auth_user_id'])
        
    form1=UpdateUserForm(request.POST or None, instance=instance1)
    form2=UserProfileForm(request.POST or None, instance=userDetail)

    context={
        'insatance1':instance1,
        'image':userDetail.image,
        'form1':form1 ,
        'form2':form2 ,
    }
    #form3=UserProfileForm(request.POST,instance=request.user)

    if form1.is_valid() and form2.is_valid():
        #instance1=form1.save(commit=True)

        user = form1.save()            
        user.save()
        profile = form2.save(commit=False)
        profile.user = user
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        profile.save()
        return render(request,'profile.html',context)


#    updateuserform = UpdateUserForm(request.POST)
#    updateprofileform = UpdateProfileForm(request.POST)
    return render(request,'edit_profile.html',context)


