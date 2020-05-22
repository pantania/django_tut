from django import forms
from .models import Post, Account, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('accounts',)


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('name',)
