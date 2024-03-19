from django import forms
from .models import Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class CreateCourse(forms.ModelForm):
    
    class Meta: 
        model = Course 
        fields = '__all__'
        labels = {
            "code": "",
            "cadre": "",
            "cadre_acronym": "",
            "position": "",
            "position_acronym": "",
            "ptb_course": "PTB course",
            "dhs_comp": "DHS competencies"
        }
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Course code (e.g., 7111 or 0823)"}),
            'cadre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Cadre (e.g., Public Assistance)"}),
            'cadre_acronym': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Cadre Acronym (e.g., PA)"}),
            'position': forms.TextInput(attrs={'class': 'form-control',  'placeholder': "Position or Course Title (e.g., Manager, Task Force Lead)"}),
            'position_acronym': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Position or Course Title Acronym (e.g., MGR, TFL)"}),
            'ptb_course' : forms.CheckboxInput(attrs={'class': 'form-check-input', 'input_type': 'checkbox'}),   
        }

        # def __init__(self, *args, **kwargs):
        #     super(CreateCourse, self).__init__(*args, **kwargs)
        #     for field in iter(self.fields):
        #         self.fields[field].widget.update({
        #             'class': 'form-control me-2'
        #     })

class UploadFileForm(forms.Form):

    # class Meta: 
    #     model = Course 
    #     fields = ['code']
        
        

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['code'].empty_label = "Course ID"
        
    code = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        to_field_name='code',
        required=True,  
        label = '',
        empty_label="Select course",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    file = forms.FileField(label = "",
        widget=forms.FileInput(attrs={'class': 'form-control'}))
    module = forms.CharField(
        max_length= 20,
        label = "",
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Module number (e.g., 0, 1.5, 1, etc.)"}))
    module_title = forms.CharField(max_length = 200, label = '',
                                   widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Name of module"}))
    minutes_to_complete = forms.IntegerField(label = '', widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Number of minutes"}))
    number_of_slides = forms.IntegerField(label = '', widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Number of slides"}))
    number_of_activities = forms.IntegerField(label = '', widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Number of activities"}))

class CreateIG(forms.Form):
    slides = MultipleFileField()
    
class MainHeadingOptions(forms.Form):
    pass

class ELAHeadingOptions(forms.Form):
    pass

class AdditionalOptions(forms.Form):
    pass

class SaveDirectory(forms.Form):
    pass


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    first_name = forms.CharField(label="", max_length = 100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="", max_length = 100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	
