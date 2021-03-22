from django import forms

class SearchForm(forms.Form):
    searchtext = forms.CharField(label = 'Search')


class DataForm(forms.Form):
    source = forms.ChoiceField(choices = [('','----'),('reddit', 'Reddit'), ('twitter', 'Twitter')], 
    widget=forms.Select(attrs={"onChange":'this.form.submit();'}))
