from django import forms


class URLForm(forms.Form):
    url = forms.URLField()


class PublishOptionsForm(forms.Form):
    url = forms.URLField()
    publish_as = forms.CharField(widget=forms.Select)
    include_images = forms.BooleanField(widget=forms.CheckboxInput)
    tags = forms.CharField(widget=forms.TextInput)