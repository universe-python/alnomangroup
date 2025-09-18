from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news-letter', newsletter, name='newsletter'),
    path('location-post/<str:location_name>/', LocationView.as_view(), name='location'),

    #properties url
    path('landProject/', LandProjectView.as_view(), name='land_project'),
    path('land-Project/', landprojectpage , name='landproject'),
    path('apartment-Project/', apartmentprojectpage , name='apartmentproject'),
    path('land-details-property/<slug:slug>/', LandDetailsPropertyView.as_view(), name='land_details_property'),
    path('apnartmentProject/', ApartmentProject.as_view(), name='apartment_project'),
    path('details/property/<slug:slug>/', ApartmentPropertyDetailView.as_view(), name='details_property'),

    path('feature-details-property/<str:id>/', FeaturePropertyDetailView.as_view(), name='feature_details_property'),
    path('recent-details-property/<str:id>/', RecentPropertyDetailView.as_view(), name='recent_details_property'),
    path('choose-details-property/<str:id>/', ChooseTheBestDetailView.as_view(), name='choose_details_property'),

    # Service URLs
    path('service/details-page/<str:id>/', ServiceDetailView.as_view(), name='service_details'),

    # Blog URLs
    path('blog/', BlogListView.as_view(), name='blog'),
    path('read/more/<slug>/', BlogDetailView.as_view(), name='read-more'),

    # About URL
    path('about/', AboutView.as_view(), name='about'),

    # Gallery URLs
    # path('gallery/', GalleryView.as_view(), name='gallery'),
    # path('albums/', AlbumView.as_view(), name='album'),
    path('albums/', album, name='album'),
    # path('gallery/<int:album_id>/', GalleryView.as_view(), name='gallery'),
    path('gallery/<int:pk>/', gallery, name='gallerys'),
    path('video/', VideoView.as_view(), name='video'),
    path('video/gallery/', video_gallery, name='video_gallery'),

    # Get in touch
    path('contact/', ContactView.as_view(), name='contactus'),
    path('our_team/', OurTeamView.as_view(), name='ourteam'),
    path('notice/', NoticeView.as_view(), name='notice'),
    path('career/', CareerView.as_view(), name='career'),
    path('career-detail/<slug>-<str:id>/', CareerDetailView.as_view(), name='career-detail'),
    path('csr/', CSRView.as_view(), name='csr'),
    path('csr-detail/<str:id>/', CSRDetailView.as_view(), name='csr-detail'),

   # sister concerns 
    path('sister-concerns/', sister_concerns, name='sister_concerns'),
    path('sister-concerns/<slug:slug>/', sister_concerns_details, name='sister_concerns_details'),


    

    # Booking now
    path('booking-now/', BookingNowView.as_view(), name='booking_now'),

    # Load district and sub-district
    path('ajax/load_districts/', LoadDistrictsView.as_view(), name='ajax_load_districts'),
    path('ajax/load_subdistricts/', LoadSubDistrictsView.as_view(), name='ajax_load_subdistricts'),

    #filter data
    path('landProject/filter-data/', FilterLandProjectView.as_view(), name='filter_data'),
    path('apartmentProject/filter-data/', FilterApartmentProjectView.as_view(), name="apmntp_filter"),


    path("awards", awards, name="award"),
    path("awards/<int:pk>/", awards_details, name="awards_details"),
    path("our-certificate", our_certificate, name="our_certificate"),
    path("our-certificate/<int:pk>/", our_certificate_details, name="our_certificate_details"),
    path("testimonial", testimonial, name="testimonials"),


    path("mission-vision", mission_vission, name="mission_vission"),
    path("md-message", md_message, name="md_message"),
    path("corparate-structure", corparate_structure, name="corparate_structure"),
    path("social-responsibility", social_responsibility, name="social_responsibility"),
    path("land-wanted", land_wanted, name="land_wanted"),
    

    # booking Form
    path('apply/', realestate_apply, name='realestate_apply'),
    path('privacy_policy/', privacy_policy, name='privacy_policy'),


]