from django import forms
from .models import MyModel, Category

class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['category', 'title', 'content']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)