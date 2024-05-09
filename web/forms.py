from django import forms

class RansomFile(forms.Form):
    file_name = forms.CharField()
    file_content = forms.CharField()



