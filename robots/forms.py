from django import forms
from .models import Robot

class RobotForm(forms.ModelForm):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
    ]
    
    DIRECTION_CHOICES = [
        ('up', 'Up'),
        ('right', 'Right'),
        ('down', 'Down'),
        ('left', 'Left'),
    ]

    language = forms.ChoiceField(choices=LANGUAGE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    direction = forms.ChoiceField(choices=DIRECTION_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    floor = forms.IntegerField( initial=0, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    row = forms.IntegerField( initial=0, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    column = forms.IntegerField( initial=0, min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Robot
        fields = ['name', 'nao_ip', 'network_interface', 'language', 'floor', 'row', 'column', 'direction']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['nao_ip'].widget.attrs.update({'class': 'form-control'})
        self.fields['network_interface'].widget.attrs.update({'class': 'form-control'})
