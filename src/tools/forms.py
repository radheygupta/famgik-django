from django import forms


class PrettyPrintForm(forms.Form):
    LANGUAGE_CHOICES = (('html', 'HTML'),
                        ('js', 'Java Script'),
                        ('css', 'CSS'))

    str = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)
