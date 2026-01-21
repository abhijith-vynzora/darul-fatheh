from django import forms
from .models import (
    
    Category,
    GalleryImage,
    DonationDetails,
    StudentRegistration,
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class GalleryImageForm(forms.ModelForm):  # no need
    class Meta:
        model = GalleryImage
        fields = ["category", "title", "image"]





class DonationForm(forms.ModelForm):
    class Meta:
        model = DonationDetails
        fields = [
            'donor_name', 
            'phone', 
            'email', 
            'amount', 
            # 'transaction_id', 
            'message'
        ]
        


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentRegistration
        fields = ['first_name', 'last_name', 'dob', 'email', 'mobile', 'course', 'program_name']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Mobile Number'}),
            'course': forms.Select(attrs={'class': 'custom-select-box'}),
            
            'program_name': forms.TextInput(attrs={'placeholder': 'Enter Program Name (e.g., MA English)'}),
        }