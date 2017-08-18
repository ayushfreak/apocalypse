from django import forms
from .models import Post,UserProfile
from ckeditor.widgets import CKEditorWidget

#collecting additional information during SignupForm
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='first_name')
    last_name = forms.CharField(max_length=30, label='last_name')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

class EmailPostForm(forms.Form):
#forms.Form as we do not save anything in database
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('image','user_info')


class PostForm(forms.ModelForm):
    body =forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ('title','body','status','tags','image')

'''class PostUpdate(forms.ModelForm):
    body =forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ('body','status')'''


class SearchForm(forms.Form):
    query = forms.CharField()
