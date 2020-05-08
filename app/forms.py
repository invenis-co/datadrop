from django import forms


class UploadForm(forms.Form):
    """Main app form: upload one or more files"""
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
