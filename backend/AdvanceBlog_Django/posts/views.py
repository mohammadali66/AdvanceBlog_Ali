from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q

from .models import Post
from .forms import PostForm


class PostListView(View):
    
    template_name = 'post_list.html'
    
    def get(self, request, *args, **kwargs):
        
        today = timezone.now().date()
        
        if request.user.is_staff or request.user.is_superuser:
            postList = Post.objects.all()
        else:
            #active() function has defined in PostManager
            postList = Post.objects.active() #.all() #.order_by('-timestamp')
        
        #Searching
        query = request.GET.get('q')
        if query:
            postList = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        
        paginator = Paginator(postList, 3) # Show 25 posts per page

        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)
        
        context = {
            'posts': posts,
            'today': today,
        }
        return render(request, self.template_name, context)

#............................................................................................................
class PostDetailView(View):
    
    template_name = 'post_detail.html'
    
    def get(self, request, slug, *args, **kwargs):
        
        post = get_object_or_404(Post, slug=slug)
        if post.draft or post.publish > timezone.now().date():
            if not request.user.is_staff or not request.user.is_superuser:
                raise Http404
            
        context = {
            'post': post,
        }
        return render(request, self.template_name, context)

#............................................................................................................
def postCreateView(request):
    template_name = 'post_form.html'
    
    
#     if not request.user.is_staff or not request.user.is_superuser:
#         raise Http404
    
    if not request.user.is_authenticated():
        raise Http404
        
    form = PostForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, 'Successfully Created!')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, 'Failed')
        
    context = {'form': form}
    return render(request, template_name, context)
    
#............................................................................................................
class PostUpdateView(View):
    template_name = 'post_form.html'
    
    def get(self, request, slug, *args, **kwargs):
        
        post = get_object_or_404(Post, slug=slug)
        
        if post.draft or post.publish > timezone.now().date():
            if not request.user.is_staff or not request.user.is_superuser:
                raise Http404
                
        form = PostForm(instance=post)
        
        context = {
            'post': post,
            'form': form,
            }
        return render(request, self.template_name, context)
    
    
    def post(self, request, slug):
        
        post = get_object_or_404(Post, slug=slug)
        form = PostForm(request.POST or None, request.FILES or None, instance=post)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Successfully Edited!')
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            messages.error(request, 'Failed')
            
        context = {'form': form}
        return render(request, self.template_name, context)
        
#............................................................................................................
class PostDeleteView(View):
    
    def get(self, request, slug, *args, **kwargs):
        
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
        
        post = get_object_or_404(Post, slug=slug)
        post.delete()
        messages.success(request, 'Deleted')
        return redirect('posts:postlist')






