from django.shortcuts import render_to_response
from django import forms
from lib import spotify

class PoetryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, max_length=400)
    maxngram = forms.IntegerField(label="Maximum ngram size", initial=8)

def index(request):
    text = None
    queries = None
    results = None
    if request.method == 'POST': # If the form has been submitted...
        form = PoetryForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            text = form.cleaned_data['text']
            maxngram = form.cleaned_data['maxngram']
            form = PoetryForm()
            
    else:
        form = PoetryForm() # An unbound form
    print "text is: " + str(text)
    if text:
        results = spotify.poemToPlaylist(text, maxngram)

    return render_to_response('spoetry/index.html', \
       {'queries': queries, 'text': text, 'form': form, \
        'results': results, 'errors':form.errors})

