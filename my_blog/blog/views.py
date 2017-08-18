from urllib.parse   import quote
from django.shortcuts import render, get_object_or_404
from .models import Post,UserProfile
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from .forms import EmailPostForm,SearchForm,PostForm,ProfileForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count,Q
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.http import HttpResponseRedirect
#for class based views
from django.contrib.messages.views import SuccessMessageMixin
#for non class based views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
#http://www.effectivedjango.com/tutorial/additional-views.html

def profile_dispaly(request,my_list=None):
    object_list = Post.objects.all()
    object_list =object_list.filter(author__username=my_list)
    user = User.objects.get(username=my_list)
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    paginator = Paginator(object_list, 5) # 3 posts in each page
    page = request.GET.get('page')
    # 'page' is a number here
    #GET value from the ? mark in the url
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/profile.html',{'posts': posts,
                            'userprofile':userprofile})

class ProfileUpdate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    redirect_field_name = '/blog'
    model = UserProfile
    form_class = ProfileForm
    template_name = 'blog/post/profile_update_form.html'
    success_url = "/blog"
    success_message = " was updated successfully"


class PostCreate(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    redirect_field_name = '/blog'
    model = Post
    template_name = 'blog/post/post_form.html'
    #fields = ['title','body','status','tags']
    form_class = PostForm#use this instead of fields otherwise problem is created
    success_url = "/blog"
    success_message = "%(title)s was created successfully"
    def form_valid(self, form):#this part executed if form is valid
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostUpdate(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    redirect_field_name = '/blog'
    model = Post
    form_class = PostForm
    #if dont want to display all the fields then create a new from eg PostUpdate see froms.py
    #form_class = PostUpdate
    template_name = 'blog/post/post_update_form.html'
    success_url = "/blog"
    success_message = "%(title)s was updated successfully"



class DeletePost(LoginRequiredMixin,DeleteView):
    redirect_field_name = '/blog'
    model = Post
    template_name = 'blog/post/post_confirm_delete.html'
    success_url = "/blog"
    success_message = "%(title)s was deleted successfully"
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()#to retrive the current object
        #to automatically clean models
        for tag in obj.tags.all():
            if tag.taggit_taggeditem_items.count() == 1:
                tag.delete()
        viewed_posts =HitCount.objects.order_by('-hits')
        for posts in viewed_posts:
            if posts.content_object == None:
                posts.delete()
        #################################
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeletePost, self).delete(request, *args, **kwargs)



def post_list(request,tag_slug=None,my_list=None,num=None):
    request.session.set_test_cookie()
    #posts = Post.published.all()#return only the published posts not draft one
    object_list = Post.published.all()
    if num:
        object_list = Post.objects.all()
    results=None
    if my_list:
        if request.user.is_authenticated():
            object_list =object_list.filter(author=request.user)
    if request.method =='POST':
        query=request.POST.get('q')
        if query:
            results = object_list.filter(Q(title__icontains=query)|
             Q(body__icontains=query)|Q(author__username__icontains=query)|
             Q(author__first_name__icontains=query)|
             Q(tags__name__icontains=query)).distinct()
# if field connected to other database like author to user database and tags to tag
# database the use name or username or according to parent database otherwise takes pk and gives error
    if results:
        object_list=results
        # count total results
        total_results = results.count()
    else:
        total_results=None

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # orobject_list = Post.objects.filter(tags__name__in=[tag],status='published')## slower than below
        object_list = object_list.filter(tags__name__in=[tag])
        #tags__name__in is to handle a list of tags, if a single tag then can use tags=tag
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    # 'page' is a number here
    #GET value from the ? mark in the url
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts': posts,'tag': tag,
                 'total_results': total_results,'num':num})



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
        publish__year=year,publish__month=month,publish__day=day)
#__ are lookups or to extract field from ForeignKey as author__username gives
#username of corresponding user from USER database
#https://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups
    # first get the related HitCount object for your model object
    hit_count = HitCount.objects.get_for_object(post)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    # your response could look like this:
    # UpdateHitCountResponse(hit_counted=True, hit_message='Hit counted: session key')
    # UpdateHitCountResponse(hit_counted=False, hit_message='Not counted: session key has active hit')

    post_tags_ids = post.tags.values_list('id', flat=True)
    #https://docs.djangoproject.com/en/1.11/ref/models/querysets/#values-list
    #cant use tags__in=post.tags as a non iterable object is generated
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    #https://simpleisbetterthancomplex.com/tutorial/2016/12/06/how-to-create-group-by-queries.html
    for po in similar_posts:
        print(po.title)
        print(po.same_tags)
    share_content=quote(post.body)
    return render(request,'blog/post/detail.html',{'post': post,'similar_posts': similar_posts,
    'share_content':share_content})


def post_share(request,post_id):
    form = EmailPostForm()
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    cd=None
    if request.method=='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
    #to build a complete URL including HTTP schema and hostname.
            subject = '%s %s recommends you reading %s'%(cd['name'], cd['email'], post.title)
            message = 'Read %s at %s\n\n%s\'s comments: %s'%(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'ayushaggarwal.97@gmail.com',[cd['to']])
            sent = True
    return render(request, 'blog/post/share.html', {'post': post,'form': form,'sent': sent,'cd':cd})


def tinymce_form(request):
    form = EmailPostForm()
    cd=None
    if request.method=='POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    return render(request, 'blog/post/tiny.html', {'form': form,'cd':cd})
