# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Upload Your Own Dataset',
        help_text='MAX 40 MB'
    )
