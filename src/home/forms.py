from django import forms
from django.utils.translation import ugettext as _

from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': _('News content must be less than 300 characters'),
               'cols': '60', 'rows': '3', 'required': 'required', 'maxlength':'300',
               'title': _('News content is required')}))
    tags = forms.CharField(required=True, label=_('Tags'), widget=forms.TextInput(
        attrs={'class': 'form-control col-sm-7', 'placeholder': _('Separate tags with comma'),
               'required': 'required', 'title': _('Tags are required')}))

    class Meta:
        model = Post
        fields = ['content', 'tags']
        exclude = ('user', )