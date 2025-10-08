from django import forms
from .models import YipForm, AdminModel

class YipFormForm(forms.ModelForm):
    class Meta:
        model = YipForm
        fields = ['full_name', 'email', 'phone', 'gender', 'dob', 'short_bio', 'resume_upload']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'short_bio': forms.Textarea(attrs={'rows': 4}),
            'gender': forms.RadioSelect(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'resume_upload': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }

    def clean_resume_upload(self):
        resume = self.cleaned_data.get('resume_upload')
        if resume and resume.size > 2 * 1024 * 1024:
            raise forms.ValidationError("File size should not exceed 2 MB.")
        return resume


class AdminModelForm(forms.ModelForm):
    class Meta:
        model = AdminModel
        fields = ['full_name', 'email', 'phone']




class AdminLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)





