from django import forms
from .models import EmployeeDetail
from .models import EmployeeWorkDetail

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetail
        fields = [ 'fullName', 'phonenumber', 'dob', 'doj', 'empID', 'empDept', 'designation', 'email', 'gender', 'password' ]

class previewForm(forms.Form):

    name = forms.CharField(max_length=100)
    designation = forms.CharField(max_length=100)
    project = forms.CharField(max_length=100)
    assignedOn = forms.DateField()
    completionDate = forms.DateField()

class EmployeeWorkDetailForm(forms.ModelForm):
    class Meta:
        model = EmployeeWorkDetail
        fields = ['name', 'designation', 'project', 'assigned_on', 'completion_date']
        widgets = {
            'assigned_on': forms.DateInput(attrs={'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'type': 'date'}),
        }