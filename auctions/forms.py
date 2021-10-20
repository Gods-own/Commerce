from django import forms

categories = (
    ('Fashion', 'Fashion'),
    ('Electronics', 'Electronics'),
    ('Toys', 'Toys'),
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Children', 'Children'),
    ('Shoes', 'Shoes'),
    ('Furniture', 'Furniture'),
    ('Clothing', 'Clothing'),
    ('Hair', 'Hair'),
    ('Watches', 'Watches'),
)


class AddListings(forms.Form):
    titl = forms.CharField(max_length=100, label="Title", widget=forms.TextInput 
    (attrs={'class':'inputs', 'id':'input5'}))
    prod = forms.URLField(max_length=599, label="Image URL", required=False, widget=forms.URLInput 
    (attrs={'class':'inputs', 'id':'input1'}))
    desc = forms.CharField(max_length=599, label="Description", widget=forms.TextInput 
    (attrs={'class':'inputs', 'id':'input3'}))
    amount = forms.DecimalField(label="Price", widget=forms.NumberInput 
    (attrs={'class':'inputs', 'id':'input4'}))

class AddCategory(forms.Form):
    cat = forms.MultipleChoiceField(label="", choices=categories,
    widget=forms.CheckboxSelectMultiple (attrs={'id':'input2'}))

class PlaceBid(forms.Form):
    curPrice = forms.DecimalField(label="", widget=forms.NumberInput 
    (attrs={'class':'inputs', 'id':'input6'}))

class AddComment(forms.Form):
    comments = forms.CharField(label="Comment", widget=forms.Textarea
    (attrs={'class':'inputs', 'id':'input8'}))
