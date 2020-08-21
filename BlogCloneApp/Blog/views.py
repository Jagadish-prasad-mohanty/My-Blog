from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView,ListView,DetailView,
                                CreateView,UpdateView,DeleteView)
from Blog.forms import PostForm,CommentsForm
from Blog.models import Post,Comments
from django.utils import timezone
from django.urls import reverse_lazy

# Create your views here.

class PostAboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    model=Post

    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')


class PostDetailView(DetailView):
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):
    login_url="/login/"
    redirect_field_name='Blog/post_detail.html'
    form_class=PostForm
    model=Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url="/login/"
    redirect_field_name="Blog/post_detail.html"
    form_class=PostForm
    model=Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url="/login/"
    redirect_field_name="Blog/post_list.html"
    model=Post

    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by("create_date")
    
######################################
#####################################
@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=post.pk)

@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentsForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
        return redirect('post_detail',pk=post.pk)

    else:
        form=CommentsForm()
    return render(request,"Blog/comment_form.html",{'form':form})

@login_required
def approve_comment(request,pk):
    comment=get_object_or_404(Comments,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def remove_comment(request,pk):
    comment=get_object_or_404(Comments,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

