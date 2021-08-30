from django import forms
from django.forms import ValidationError


class CommentForm(forms.Form):

    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    content = forms.CharField(label='Comment', widget=forms.Textarea)

    def clean_name(self):
        name = self.cleaned_data['name']
        if ' ' in name:
            raise ValidationError('The name cannot contain whitespaces!')

        return name
