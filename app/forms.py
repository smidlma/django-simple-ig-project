from django import forms
from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['location', 'image', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
        }


class CommentForm(forms.Form):
    comment = forms.CharField(label='Comment')
    widgets = {
        'comment': forms.Textarea(attrs={'class': 'form-control'}),
    }

class UserForm(forms.ModelForm):
     class Meta:
        model = User

        fields = ['username', 'avatar', 'email', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-select'}),
        }
# class CapacitySearchForm(forms.Form):
#     from_capacity = forms.IntegerField(label = 'from')
#     to_capacity = forms.IntegerField(label = 'to')
