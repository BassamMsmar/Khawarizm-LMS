from django import forms
from courses.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'  # يمكنك تحديد الحقول يدويًا لو حبيت

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course title'
            }),
            'lecturer': forms.Select(attrs={
                'class': 'form-control'
            }),
            'academic_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 30'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Brief summary of the course...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control ckeditor',
                'placeholder': 'Full course description...'
            }),
            'what_youll_learn': forms.Textarea(attrs={
                'class': 'form-control ckeditor',
                'placeholder': 'What students will learn...'
            }),
            'who_this_course_is_for': forms.Textarea(attrs={
                'class': 'form-control ckeditor',
                'placeholder': 'Who this course is intended for...'
            }),
            'colleges': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'thumbnail': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
            'students_enrolled': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
