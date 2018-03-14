from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django.contrib.auth import authenticate, login
from .forms import UserForm,LoginForm,DocumentForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from .models import Video
from django.conf import settings as set
import swiftclient

# Create your views here.

##############login()###########################################################
class LoginFormView(View):
    username=''
    form_class = LoginForm
    template_name = 'registration/login.html'

    def get(self,request):
        if request.session.has_key('username'):
          username = request.session['username']
          return redirect('/index')
        else :
            form = self.form_class(None)
            return render(request, self.template_name, {'form':form,})

    def post(self, request):
        form = self.form_class(request.POST)
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                username = user.username
                request.session['username'] = username
                return redirect('videos:index')

        else :
            form.add_error('username', 'credentials are incorrect!')

        return render(request, self.template_name, {'form':form,})

#################registration()#################################################
class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/signup.html'

    def get(self,request):
        if request.session.has_key('username'):
          username = request.session['username']
          return redirect('/index')
        else :
            form = self.form_class(None)
            return render(request, self.template_name, {'form':form,})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid() and form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = username
                    return redirect('videos:index')

        else :
            form.add_error('password_confirm', 'The password do not match')

        return render(request, self.template_name, {'form':form,})

###########logout()#############################################################
def logout(request):
    try:
        del request.session['username']
    except:
        pass
    return redirect('/')

###########swiftauth()##########################################################
def swiftauth():
    conn = swiftclient.Connection(set.SWIFT_AUTH_URL,set.SWIFT_USERNAME,set.SWIFT_KEY,auth_version=set.SWIFT_AUTH_VERSION,tenant_name=set.SWIFT_TENANT_NAME)
    return conn
##############index()###########################################################

def IndexView(request):
    if request.session.has_key('username'):
        username = request.session['username']
        x = Video.objects.all()
        conn = swiftauth()
        return render(request,'videos/index.html',{'x':x})
    else:
        return redirect('/')

###############yuploads()#######################################################

def yuploadView(request):
    if request.session.has_key('username'):
        username = request.session['username']
        x = request.user.video_set.all()
        return render(request, 'videos/yupload.html', {"username" : username , 'x':x})
    else:
        return redirect('/')

############upload()############################################################
def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.owner = request.user
            new.video_title=request.POST["title"]
            new.file_file=request.FILES["myfile"]
            new.save()
            return redirect('/')
    else:
        form = DocumentForm()
    return render(request, 'videos/upload.html', {
        'form': form
    })

############delete()########################################################
def delete(request,video_id):
    video = Video.objects.get(file_file=video_id)
    conn = swiftauth()
    conn.delete_object(set.SWIFT_CONTAINER_NAME,video_id)
    video.delete()
    return redirect('videos:yuploads')
##########search()#############################################################

def search(request):
    if request.session.has_key('username'):
        username = request.session['username']
        title = str(request.GET["q"])
        x = Video.objects.filter(video_title=title)
        if x:
            return render(request,'videos/index.html',{'x':x})
        else:
            p = "No such videos..."
            return render(request,'videos/index.html',{'p':p,})
    else:
        return redirect('/')

