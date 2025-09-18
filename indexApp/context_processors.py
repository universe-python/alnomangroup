from .models import SocialMediaLink,ServiceType,ProjectTypeFilter,PropertyTypeFilter,SubDistrict,Cup_of_Coffee
from dashboard.models import Admin

def socialmedia(request):
    social_link = SocialMediaLink.objects.all().order_by('-id')[0:1]
    con_website_logo = Admin.objects.last()
    return {
        'social_link':social_link,
        'con_website_logo':con_website_logo,
        'projecttype': ProjectTypeFilter.objects.all(),
        'propertytype': PropertyTypeFilter.objects.all(),
        'subdistrict': SubDistrict.objects.all(),
        'cupofcoffeee': Cup_of_Coffee.objects.all()[:6]  
    }

def service_cat(request):
    service_type = ServiceType.objects.all()
    return {
        'service_type':service_type
    }
