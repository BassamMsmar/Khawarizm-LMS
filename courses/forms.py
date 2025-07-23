from django import forms
from .models import Review

from django import forms
from .models import Review
class ReviewForm(forms.ModelForm):
    rate = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating-input'}),
        label="Your Rating"
    )

    class Meta:
        model = Review
        fields = ['rate', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Write your review here...'
            }),
        }

