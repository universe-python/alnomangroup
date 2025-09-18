from django import forms 
from django.forms import ModelForm
from indexApp.models import *
from dashboard.models import *
from ckeditor.widgets import CKEditorWidget

from ckeditor_uploader.widgets import CKEditorUploadingWidget

############ start related image inlineformset form ##########
from django.forms import ModelForm, inlineformset_factory


class PropertyPostForm(ModelForm):
    class Meta:
        model = PropertyPost
        exclude = ()


class RelatedImageForm(ModelForm):
    class Meta:
        model = Post_related_images
        exclude = ()


RelatedImageFormSet = inlineformset_factory(PropertyPost, Post_related_images,
                                            form=RelatedImageForm, extra=1)

############ end related image inlineformset form ##########

class BannerForm(forms.ModelForm):
    
    class Meta:
        model = Banner
        fields ='__all__'
        
class WhyChooseUsForm(forms.ModelForm):
    class Meta:
        model = Why_chosse_us
        fields ='__all__'

class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields ='__all__'

class CountersForm(forms.ModelForm):
    class Meta:
        model = Counters
        fields ='__all__'

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields ='__all__'

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields ='__all__'
        
class ServicePostForm(forms.ModelForm):
    class Meta:
        model = ServicePost
        fields ='__all__'
        
class GalleryPostForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields ='__all__'
class AlbumPostForm(forms.ModelForm):
    class Meta:
        model = Album
        fields ='__all__'


# class CareerAdmin(forms.ModelForm):
#     prepopulated_fields ={'slug': ('title',)}

class CareerForm(forms.ModelForm):
    # job_description = forms.CharField(widget=CKEditorWidget())

    title = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',  
    }))

    post_date = forms.CharField(widget=forms.TextInput(attrs={
        'type':'date',  
    }))
    
    end_date = forms.CharField(widget=forms.TextInput(attrs={
        'type':'date', 
    }))

    class Meta:
        model = Career
        fields = ['title','job_description','post_date','end_date']

class OurTeamForm(forms.ModelForm):
    class Meta:
        model = OurTeam
        fields ='__all__'
        exclude = ['ordering']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields ='__all__'

class AboutHeadForm(forms.ModelForm):
    class Meta:
        model = AboutUs
        fields ='__all__'

class AboutLookingSectionForm(forms.ModelForm):
    class Meta:
        model = AboutLookingSection
        fields ='__all__'

class AboutTestimotialForm(forms.ModelForm):
    class Meta:
        model = AboutTestimotial
        fields ='__all__'

class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = '__all__'

class FeedBackApprovedForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = '__all__'
        exclude = ('status',)

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        
class Video_GalaryForm(forms.ModelForm):
    class Meta:
        model = Video_Galary
        fields = '__all__'


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = '__all__'


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = '__all__'


class ProjectTypeFilterForm(forms.ModelForm):
    class Meta:
        model = ProjectTypeFilter
        fields = '__all__'

class PropertyTypeFilterForm(forms.ModelForm):
    class Meta:
        model = PropertyTypeFilter
        fields = '__all__'

class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = '__all__'
        
class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'

class SubDistrictForm(forms.ModelForm):
    class Meta:
        model = SubDistrict
        fields = '__all__'

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = '__all__'

class SocialMediaLinkForm(forms.ModelForm):
    class Meta:
        model = SocialMediaLink
        fields = '__all__'
        
class CsrForm(forms.ModelForm):
    class Meta:
        model = CSR
        fields = '__all__'

class MissionVisionForm(forms.ModelForm):
    class Meta:
        model = MissionVision
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))
class MD_MessageForm(forms.ModelForm):
    class Meta:
        model = MD_Message
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))


class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Privacy
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))



class Social_ResponsibilityForm(forms.ModelForm):
    class Meta:
        model = Social_Responsibility
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))

class AwardsForm(forms.ModelForm):
    class Meta:
        model = Awards
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))

class Land_WantedForm(forms.ModelForm):
    class Meta:
        model = Land_Wanted
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))

class Land_WantedForm(forms.ModelForm):
    class Meta:
        model = Land_Wanted
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))

class Corparate_StructureForm(forms.ModelForm):
    class Meta:
        model = Corparate_Structure
        fields = '__all__'
    
  
class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = '__all__'

class Cup_of_CoffeeForm(forms.ModelForm):
    class Meta:
        model = Cup_of_Coffee
        fields = '__all__'
    
  

class Our_CertificateForm(forms.ModelForm):
    class Meta:
        model = Our_Certificate
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))
    
class Our_CertificateForm(forms.ModelForm):
    class Meta:
        model = Our_Certificate
        fields = '__all__'
    
    details = forms.CharField(error_messages={'required': 'This description field is required.'},widget=CKEditorUploadingWidget(attrs={
        'class': 'form-control p-20',
        'rows': "4"
    }))



class SisterConcernForm(forms.ModelForm):
    class Meta:
        model = SisterConcern
        fields = '__all__'

class RealstateTermsForm(forms.ModelForm):
    class Meta:
        model = RealstateTerms
        fields = ['terms']
        widgets = {
            'terms': CKEditorWidget(),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['pdf']

class CampingBannerForm(forms.ModelForm):
    class Meta:
        model = CampingBanner
        fields = '__all__'


class SisterConcernBannerForm(forms.ModelForm):
    class Meta:
        model = SisterConcernBanner
        fields = '__all__'