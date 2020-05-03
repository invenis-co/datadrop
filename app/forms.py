from django import forms


class UploadForm(forms.Form):
    """Main app form: upload one or more files"""
    company = forms.CharField(max_length=64, help_text='Optional', required=False)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
