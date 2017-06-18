from django import forms
 
class MarkerForm(forms.Form):
    mark_loc  = forms.CharField(max_length=50)
    mark_time = forms.CharField(max_length=50)
    mark_type = forms.CharField(max_length=50)
    mark_name = forms.CharField(max_length=100)

class PostForm(forms.Form):
    post_mid  = forms.CharField(max_length=50)
    post_id = forms.CharField(max_length=50)
    post_content = forms.CharField(widget=forms.Textarea)