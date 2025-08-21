from django import forms
from .models import Quiz, Question, Choice, Review

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['unit', 'title', 'duration', 'is_active']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'text', 'is_correct']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rate', 'comment']
