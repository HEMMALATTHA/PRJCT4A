from django import forms
from .models import Post, Comment

class SearchForm(forms.Form):
    q = forms.CharField(label="Search", required=False)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "image", "categories", "is_published"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3})
        }
