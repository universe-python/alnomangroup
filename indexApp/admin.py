from django.contrib import admin
from .models import *


class relatedPostImageAdmin(admin.StackedInline):
    model = Post_related_images

class PostAdmin(admin.ModelAdmin):
    inlines = [relatedPostImageAdmin]
admin.site.register(PropertyPost,PostAdmin)


admin.site.register(Menu)
admin.site.register(Banner)
admin.site.register(Property_type)
admin.site.register(Counters)
admin.site.register(Location)
admin.site.register(Why_chosse_us)
admin.site.register(Gallery)
admin.site.register(ProjectTypeFilter)
admin.site.register(PropertyTypeFilter)
admin.site.register(Division)
admin.site.register(District)
admin.site.register(SubDistrict)
admin.site.register(Blog)
admin.site.register(AboutUs)
admin.site.register(AboutLookingSection)
admin.site.register(AboutTestimotial)
admin.site.register(OurTeam)
admin.site.register(Notice)
admin.site.register(Career)
admin.site.register(JobApplication)
admin.site.register(ContactUs)
admin.site.register(FeedBack) 
admin.site.register(ServiceType) 
admin.site.register(Faq)
admin.site.register(BookingNow)
admin.site.register(BookingPropertyType)
admin.site.register(SocialMediaLink)
admin.site.register(CSR)
admin.site.register(Privacy)
admin.site.register(Album)



admin.site.register(Awards)
admin.site.register(MissionVision)
admin.site.register(MD_Message)
admin.site.register(Corparate_Structure)
# admin.site.register(Social_Responsibility)
admin.site.register(Testimonial)
admin.site.register(Land_Wanted)
admin.site.register(Our_Certificate)
admin.site.register(Video_Galary)
admin.site.register(NewsLetter)
admin.site.register(Cup_of_Coffee)
class ServiceRelatedImageAdmin(admin.StackedInline):
    model = Service_related_images

class ServiceAdmin(admin.ModelAdmin):
    inlines = [ServiceRelatedImageAdmin]
admin.site.register(ServicePost,ServiceAdmin) 

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)

# @admin.register(SisterConcern)
# class SisterConcernAdmin(admin.ModelAdmin):
#     list_display = ("name", "country", "phone", "email")
#     prepopulated_fields = {"slug": ("name",)}

@admin.register(SisterConcern)
class SisterConcernAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'phone', 'email')
    prepopulated_fields = {"slug": ("name",)}

    

from django.contrib import admin
from .models import RealEstateApplication

@admin.register(RealEstateApplication)
class RealEstateApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'applicant_full_name',
        'email',
        'profession',
        'residence_type',
        'project_location',
        'total_price',
        'submitted_on',
    )

    list_filter = (
        'residence_type',
        'profession',
        'submitted_on',
    )

    search_fields = (
        'applicant_full_name',
        'email',
        'nid_or_passport',
        'nominee_name',
        'project_location',
    )

    readonly_fields = ('submitted_on',)

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'applicant_full_name',
                'mother_name',
                'date_of_birth',
                'nationality',
                'religion',
                'email',
                'permanent_address',
            )
        }),
        ('Professional Information', {
            'fields': (
                'profession',
                'designation',
                'organization',
            )
        }),
        ('Project Information', {
            'fields': (
                'residence_type',
                'project_location',
                'total_price',
                'per_share_price',
                'total_project_area',
                'number_of_share',
                'instruction',
            )
        }),
        ('Legal', {
            'fields': (
                'agree_terms',
                'submitted_on',
            )
        }),
    )


admin.site.register(RealstateTerms)
admin.site.register(Document)

class CampingBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'camping_banner')

admin.site.register(CampingBanner, CampingBannerAdmin)

admin.site.register(SisterConcernBanner)