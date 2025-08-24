from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    add_comment, moderation_queue, approve_comment
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("new/", PostCreateView.as_view(), name="post-create"),
    path("<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("<slug:slug>/edit/", PostUpdateView.as_view(), name="post-edit"),
    path("<slug:slug>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("<slug:slug>/comment/", add_comment, name="add-comment"),
    path("moderation/", moderation_queue, name="moderation-queue"),
    path("moderation/approve/<int:pk>/", approve_comment, name="approve-comment"),
]
