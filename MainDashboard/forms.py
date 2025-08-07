from django import forms
from courses.models import Course
from college.models import College
from department.models import Department # Import the Department model

from django.contrib.auth import get_user_model


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


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ['slug']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        # Populate choices for 'college' and 'admin' fields
        self.fields['college'].queryset = College.objects.all()
        self.fields['admin'].queryset = get_user_model().objects.all()

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


class StudentForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email','department', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user