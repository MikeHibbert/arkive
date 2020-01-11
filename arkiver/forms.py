from django import forms


class URLForm(forms.Form):
    url = forms.URLField()


class PublishOptionsForm(forms.Form):
    url = forms.URLField()
    publish_as = forms.Select()
    include_images = forms.CheckboxInput()