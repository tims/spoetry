from django.shortcuts import render_to_response
from django import forms
from lib import spotify

class PoetryForm(forms.Form):
    text = forms.CharField(max_length=300, widget=forms.Textarea)
    maxngram = forms.IntegerField()

def index(request):
    text = None
    queries = None
    results = None
    if request.method == 'POST': # If the form has been submitted...
        form = PoetryForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            text = form.cleaned_data['text']
            form = PoetryForm()
    else:
        form = PoetryForm() # An unbound form
    
    if text:
        results = spotify.searchForLargestNgrams(text.split(), 4)

    return render_to_response('spoetry/index.html', \
       {'queries': queries, 'text': text, 'form': form, 'results': results})

