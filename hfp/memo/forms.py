from django import forms

class MemoForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea,
        required=True,
        label="Note"
    )
    photo = forms.ImageField(
        required=False,
        label="Attach Photo"
    )


