from django import forms
from django.forms import ValidationError

from profanity_filter import ProfanityFilter
from bs4 import BeautifulSoup


class CommentForm(forms.Form):

    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Your Email')
    content = forms.CharField(label='Comment', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.pf = ProfanityFilter()
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']

        # The name can only have a certain size
        if len(name) > 80:
            raise ValidationError('The name cannot be longer than 80 characters')

        return name

    def clean_content(self):
        content = self.cleaned_data['content']

        # Profanity is not allowed
        if not self.pf.is_clean(content):
            raise ValidationError('Profanity is not allowed in the comments!')

        # TODO: Alternative is to use a html sanitizer
        # No html markup is allowed
        soup = BeautifulSoup(content, 'html.parser')
        if bool(soup.find()):
            raise ValidationError('No html markup allowed in the content of a comment! Please understand that '
                                  'permitting html markup in comments is risky and vulnerable to attacks.')

        return content
