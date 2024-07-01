from django import forms


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback = forms.ChoiceField(choices=FEEDBACK_CHOICES)


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Science&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other'),
    ]

    name = forms.CharField(label='Your Name', required=False)
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        label='Select a category:',
        required=False,
        widget=forms.RadioSelect
    )
    max_price = forms.IntegerField(
        label='Maximum Price',
        min_value=0
    )