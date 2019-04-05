

from django.contrib.auth.decorators import login_required
import datetime as dt
from django.urls import reverse
from django.shortcuts import render
from .models import Project,Profile
from django.http import HttpResponse,Http404,HttpResponseRedirect
from . forms import PhotosLetterForm,PhotoImageForm,ProfileUploadForm,VoteForm
from .models import PhotosLetterRecipients
from .email import send_welcome_email
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer


  
def photos_today(request):
    date = dt.date.today()
    form = PhotosLetterForm()
    photos=Project.todays_photos()
   
    if request.method == 'POST':
        form = PhotosLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']

            recipient = PhotosLetterRecipients(name = name,email =email)
            recipient.save()
            send_welcome_email(name,email)

            HttpResponseRedirect('photos_today')
    else:
        form = PhotosLetterForm()
    return render(request, 'all-photos/index.html', {"date": date,"OK":photos,"letterForm":form})


       
def search_project(request):
    try:
        if 'project' in request.GET and request.GET['project']:
            searched_term = (request.GET.get('project')).title()
            searched_project = Project.objects.get(project_title__icontains = searched_term.title())
            return render(request,'search.html',{'project':searched_project})
    except (ValueError,Project.DoesNotExist):
        raise Http404()

    return render(request,'search.html')
@login_required(login_url='/accounts/login/')
def image(request, image_id):      

    try:
        image = image.objects.get(id = image_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all-photos/index.html", {"image":image})        
@login_required(login_url='/accounts/login/')
def photo_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = PhotoImageForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('photosToday')

    else:
        form = PhotoImageForm()
    return render(request, 'photo_image.html', {"form": form})   

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile2 = Profile.objects.all()
    prof =None
    images=None
    for image in profile2:
        images=image.profile_pic
       
    return render(request, 'profile.html', {"current_user": current_user,'image':images})   

@login_required(login_url='/accounts/login/')
def upload_profile(request):
    current_user = request.user 
    title = 'Upload Profile'
    # try:
    # requested_profile = Profile.objects.get(user_id = current_user.id)
    if request.method == 'POST':
        form = ProfileUploadForm(request.POST,request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileUploadForm()
    # # except:
    # #     if request.method == 'POST':
    # #         form = ProfileUploadForm(request.POST,request.FILES)

    # #         if form.is_valid():
    # #             new_profile = Profile(profile_pic = form.cleaned_data['profile_pic'],bio = form.cleaned_data['bio'],username = form.cleaned_data['username'])
    # #             new_profile.save_profile()
    # #             return redirect( profile )
    #     else:
    #         form = ProfileUploadForm()


    return render(request,'upload_profile.html',{"title":title,"current_user":current_user,"form":form})


@login_required(login_url='/accounts/login/')
def project(request,project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid:
            project.vote_submissions += 1
            if project.design == 0:
                project.design = int(request.POST['design'])
            else:
                project.design = (project.design + int(request.POST['design']))/2
            if project.usability == 0:
                project.usability = int(request.POST['usability'])
            else:
                project.usability = (project.design + int(request.POST['usability']))/2
            if project.content == 0:
                project.content = int(request.POST['content'])
            else:
                project.content = (project.design + int(request.POST['content']))/2
            project.save()
            return redirect(reverse('project',args=[project.id]))
    else:
        form = VoteForm()
    return render(request,'project.html',{'form':form,'project':project})

class ProfileList(APIView):
    def get(self,request,format=None):
        all_users = UserProfile.objects.all()
        serializers = ProfileSerializer(all_users,many=True)
        return Response(serializers.data)

class ProjectList(APIView):
    def get(self,request,format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects,many=True)
        return Response(serializers.data)


@login_required(login_url='/accounts/login/')
def submit_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewProjectForm(request.POST,request.FILES)

        if form.is_valid():
            project = Project(project_title=request.POST['project_title'],landing_page=request.FILES['landing_page'],project_description=request.POST['project_description'],live_site=request.POST['live_site'],user=request.user)
            project.save()
            return redirect(reverse('index'))
    else:
        form = NewProjectForm()

    return render(request,'submit_project.html',{'form':form}) 






@login_required(login_url='/accounts/login/')    
def add_comment(request, image_id):
 
    form = CommentForm(request.POST)
    image = get_object_or_404(image, id=image_id)
 
    if form.is_valid():
        comment = Comment()
        comment.path = []
        comment.image_id = image
        comment.user_id = auth.get_user(request)
        comment.content = form.cleaned_data['comment_area']
        comment.save()
 
        # Django does not allow to see the comments on the ID, we do not save it,
        # Although PostgreSQL has the tools in its arsenal, but it is not going to
        # work with raw SQL queries, so form the path after the first save
        # And resave a comment
        try:
            comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
            comment.path.append(comment.id)
        except ObjectDoesNotExist:
            comment.path.append(comment.id)
 
        comment.save()
 
    return redirect(image.get_absolute_url())    
    return render(request,'new-comment.html',{"image":image,"form":form})