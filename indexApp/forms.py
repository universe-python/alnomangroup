from django import forms 
from .models import *



from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Name',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Your Email',
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Phone',
    }))

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Subject',
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Your Message',
        'rows': 4
    }))

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'subject', 'message', 'status', 'captcha']




class JobApplicationForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Full Name',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Your Email',
    }))
    phone = forms.CharField(widget=forms.NumberInput(attrs={
        'class':'form-control',
        'maxlength': 15,
        'type': 'number',
        'placeholder':'Your Phone',
    }))

    expected_salary = forms.CharField(widget=forms.NumberInput(attrs={
        'class':'form-control',
        'type': 'number',
        'placeholder':'Expected salary',
    }))

    cv  = forms.FileField(label="Cardholder Name",widget=forms.ClearableFileInput(attrs={
        'class':'form-control',
        'placeholder':'Upload your cv',
        })
        )
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Your Message',
        'rows': 4
    }))
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'expected_salary','cv','message','status']


class UserFeedbackForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Name',     
    }))

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Write a short descripton',
        'rows':3,
    }))

    class Meta:
        model = FeedBack
        fields =['name','description','status','captcha']


class BookingNowForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Name',     
    }))


    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Your Email',     
    }))


    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Your Phone',          
    }
    ))
    def clean(self):
        data  = self.cleaned_data.get('phone')

        if len(data)<10:
            self._errors['phone']=self.error_class([
                "At least 11 digit user in this field"
            ])

        if not data.isdigit():
            self._errors['phone']=self.error_class([
                "Please provide your valid phone number"
            ])

        return self.cleaned_data



    job_designation = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Designation',     
    }))


    property_type = forms.ModelChoiceField(queryset=BookingPropertyType.objects.all(),empty_label='Select Property', widget=forms.Select(attrs={
        'class':'form-select prt',
        'placeholder':'Select Property',
    }))

    property_size = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Property Size',
    }))

    property_location = forms.ModelChoiceField(queryset=Location.objects.all(),empty_label='Property location',widget=forms.Select(attrs={
        'class':'form-select prt',
        'placeholder':'Property location',
    }))

    roperty_description = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'Write a short descripton',
        'rows':5,
    }))

    class Meta:
        model = BookingNow
        fields ='__all__'


#dependency Dropdown
class AreaForm(forms.ModelForm):
    division  = forms.ModelChoiceField(queryset=Division.objects.all(), empty_label='- select a division -',
required=False, widget=forms.Select(attrs={
        'class':'form-control custom-form-control',
        'data-filter': 'division'
    }))

    district  = forms.ModelChoiceField(queryset=District.objects.all(), empty_label='- select a district -',required=False, widget=forms.Select(attrs={
        'class':'form-control custom-form-control'
    }))

    sub_district  = forms.ModelChoiceField(queryset=SubDistrict.objects.all(), empty_label='- select a area -',
    required=False, widget=forms.Select(attrs={
        'class':'form-control custom-form-control'
    }))

    class Meta:
        model = Area
        fields = ('division', 'district', 'sub_district')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()
        self.fields['sub_district'].queryset = SubDistrict.objects.none()

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['district'].queryset = District.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.division.district_set.order_by('name')


        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['sub_district'].queryset = SubDistrict.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sub_district'].queryset = self.instance.district.sub_district_set.order_by('name')


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields ='__all__'


from django import forms
from .models import RealEstateApplication

class RealEstateApplicationForm(forms.ModelForm):
    class Meta:
        model = RealEstateApplication
        exclude = ['submitted_on']
        widgets = {
            # Date Inputs
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),

            # Textareas
            'permanent_address': forms.Textarea(attrs={'rows': 2}),
            'project_location': forms.Textarea(attrs={'rows': 2}),
            'instruction': forms.Textarea(attrs={'rows': 3}),

            # Select Inputs
            'residence_type': forms.Select(),
            
            # Checkbox
            'agree_terms': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            # Personal Info
            'applicant_full_name': 'Full name as per NID/Passport',
            'mother_name': "Mother's full name",
            'permanent_address': 'Permanent address (e.g. House No. 45, Road No. 7)',
            'date_of_birth': 'YYYY-MM-DD',
            'nationality': 'Your nationality (e.g. Bangladeshi)',
            'religion': 'Your religion (e.g. Islam)',
            'email': 'Email address (e.g. yourname@example.com)',

            # Profession Info
            'profession': 'Your profession (e.g. Engineer)',
            'designation': 'Your designation (e.g. Senior Developer)',
            'organization': 'Your organization (e.g. ABC Ltd.)',

            # Project Info
            'project_location': 'Specify project location',
            'total_price': 'Total project price (e.g. 5000000)',
            'per_share_price': 'Price per share (e.g. 50000)',
            'total_project_area': 'Total area (e.g. 1500 sq ft)',
            'number_of_share': 'Number of shares',
            'instruction': 'Additional instructions (optional)',

        }

        for name, field in self.fields.items():
            # Set placeholder if defined
            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]

            # Styling
            if not isinstance(field.widget, (forms.CheckboxInput, forms.Select, forms.RadioSelect)):
                field.widget.attrs.setdefault('class', 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-2 focus:ring-blue-500')




