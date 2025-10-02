from django import forms

class MemoForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
        label="Title"
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False,
        label="Content"
    )
    photo = forms.ImageField(
        required=False,
        label="Attach Photo"
    )