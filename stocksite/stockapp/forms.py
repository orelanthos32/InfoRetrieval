from django import forms

class SearchForm(forms.Form):
    searchtext = forms.CharField(label = 'Search', widget = forms.TextInput(attrs= {'border-radius': '12px','font-size' : '50','size': '100', 'placeholder': 'Input Query'}))


class DataForm(forms.Form):
    source = forms.ChoiceField(choices = [('',''),('reddit', 'Reddit'), ('twitter', 'Twitter')], 
    widget=forms.Select(attrs={"onChange":'this.form.submit();'}))
