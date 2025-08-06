from django import forms
from courses.models import Course
from college.models import College

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['slug']  # نستبعد السلاج لأنه بيتولد تلقائي
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'
            elif field.widget.__class__.__name__ == 'ClearableFileInput':
                field.widget.attrs['class'] = 'form-control-file'
            elif field.widget.__class__.__name__ == 'SelectMultiple':
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ == 'Select':
                field.widget.attrs['class'] = 'form-select'
            elif field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['rows'] = 3
            else:
                field.widget.attrs['class'] = 'form-control'


from department.models import Department

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['slug']
        widgets = {
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(CollegeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ == 'CheckboxInput':
                field.widget.attrs['class'] = 'form-check-input'
            elif field.widget.__class__.__name__ == 'ClearableFileInput':
                field.widget.attrs['class'] = 'form-control-file'
            elif field.widget.__class__.__name__ == 'Textarea':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['rows'] = 3
            else:
                field.widget.attrs['class'] = 'form-control'


from django.contrib.auth import get_user_model

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ['slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'college': forms.Select(attrs={'class': 'form-select'}),
            'admin': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for college and admin fields
        self.fields['college'].queryset = College.objects.all()
        self.fields['admin'].queryset = get_user_model().objects.all()
        self.fields['college'].empty_label = "Select College"
        self.fields['admin'].empty_label = "Select Admin"
        self.fields['admin'].required = False
