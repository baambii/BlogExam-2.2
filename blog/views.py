from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm, CommentForm
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from django.views import View
from django.http import HttpResponseRedirect

def homepage(request):
    return render(request, "homepage.html")

def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    context = {
        'posts': 
            Post.objects.all()
    }

    return render(request, 'home.html', context)

def base(request):
    return render(request, 'base.html')


def welcomeback(request):
    posts = Post.objects.all()
    return render(request, 'welcomeback.html', {'object_list': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    author_profile = Profile.objects.get(user=post.author)
    likes_count = post.number_of_likes()
    return render(request, 'post_detail.html', {'post': post, 'author_profile': author_profile})


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('postdetail', args=[str(pk)]))

@login_required
def CommentView(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        comment = CommentForm(data=request.POST)
        if comment.is_valid():
            comment = comment.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('postdetail', pk=post.pk)
    else:
        comment = CommentForm()
    return render(request, 'comment.html', {'comment': comment})

# CRUD Class-based views
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm  

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'editpost.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        post = form.save(commit=False)

        if form.has_changed():
            post.updated_on = timezone.now()

        
        if self.request.POST.get('remove_image'):
            post.image.delete()
            post.image = None

        if self.request.POST.get('remove_video'):
            post.video.delete()
            post.video = None
    

        post.save()
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


