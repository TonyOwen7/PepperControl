from django import forms
from .models import Speech

class SpeechForm(forms.ModelForm):
    class Meta:
        model = Speech
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }