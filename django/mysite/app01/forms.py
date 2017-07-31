from django import forms
from app01 import models

class BookForm(forms.Form):
    name = forms.CharField(max_length=10)
    publisher_id = forms.IntegerField(widget=forms.Select)
    # author_id = forms.IntegerField(widget=forms.SelectMultiple)
    publish_date = forms.DateField()


class BookModelForm(forms.ModelForm):

    class Meta:
        model = models.Book
        exclude = ()

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'})
        }