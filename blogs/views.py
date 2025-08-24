from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm, CommentForm, SearchForm
from .models import Post, Comment, Category

# Posts visible only to logged-in users
class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blogs/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        qs = Post.objects.select_related("author").prefetch_related("categories").filter(is_published=True)
        q = self.request.GET.get("q")
        cat = self.request.GET.get("category")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q))
        if cat:
            qs = qs.filter(categories__slug=cat)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = SearchForm(self.request.GET or None)
        ctx["categories"] = Category.objects.all()
        ctx["active_cat"] = self.request.GET.get("category", "")
        return ctx


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "blogs/post_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        ctx["approved_comments"] = self.object.comments.filter(is_approved=True).select_related("user")
        return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blogs/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"slug": self.object.slug})


class IsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class PostUpdateView(LoginRequiredMixin, IsAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blogs/post_form.html"

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"slug": self.object.slug})


class PostDeleteView(LoginRequiredMixin, IsAuthorMixin, DeleteView):
    model = Post
    template_name = "blogs/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=post, user=request.user, text=form.cleaned_data["text"], is_approved=False
            )
    return redirect("post-detail", slug=slug)


# Moderation: staff-only list & approve
@login_required
def moderation_queue(request):
    if not request.user.is_staff:
        return redirect("post-list")
    comments = Comment.objects.filter(is_approved=False).select_related("post", "user")
    return render(request, "blogs/moderation_queue.html", {"comments": comments})

@login_required
def approve_comment(request, pk):
    if not request.user.is_staff:
        return redirect("post-list")
    c = get_object_or_404(Comment, pk=pk)
    c.is_approved = True
    c.save()
    return redirect("moderation-queue")
