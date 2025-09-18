from django.utils import timezone
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator

# Create your models here.

class Menu(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='children')

    def __str__(self):
        return self.name

class Banner(models.Model):
    image = models.ImageField(upload_to="banner_images/")
    title = models.CharField(max_length=250, blank=True, null=True)
    # title_color = models.CharField(max_length=50, default='white')
    # sub_title = models.CharField(max_length=250, blank=True, null=True)
    # sub_title_color = models.CharField(max_length=50, default='white')

    # description = models.TextField(blank=True, null=True)
    # description_color = models.CharField(max_length=50, default='white')

    # link = models.URLField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.title
class Location(models.Model):
    location_name = models.CharField(max_length=250)
    location_pic= models.ImageField(upload_to="location_img/",null=True)

    def __str__(self):
        return f'{self.location_name}'
    
    def total_property_count(self):
        total = self.location.all().count()
        return total
    
class Property_type(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class PropertyTypeFilter(models.Model):
    name = models.CharField(max_length = 100)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ProjectTypeFilter'
        verbose_name_plural = 'Property Type Filter'

class ProjectTypeFilter(models.Model):
    name = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ProjectTypeFilter'
        verbose_name_plural = 'Project Type Filter'


# class Division(models.Model):
#     name = models.CharField(max_length=50)
#     def __str__(self):
#         return self.name
      
# class District(models.Model):
#     country = models.ForeignKey(Division, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name

# class Area(models.Model):
#     city = models.ForeignKey(District, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


class Division(models.Model):
    name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Divisions'
      
class District(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Districts'

class SubDistrict(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Sub District'


class Area(models.Model):
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.division.name + ", " + self.district.name + ", " + self.sub_district.name
    
    class Meta:
        verbose_name_plural = 'Area'



class PropertyPost(models.Model):
    LIFT=(
        ('Yes','Yes'),
        ('No','No'),
    )
    post_pic = models.ImageField(upload_to='features_post_img/',blank=True,null=True)
    price = models.FloatField(default='0.00',blank=True,null=True)
    post_title = models.CharField(max_length=250,blank=True,null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    post_location = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='location',blank=True,null=True)
    # select_project_type = models.ForeignKey(ProjectTypeFilter,on_delete=models.CASCADE,blank=True,null=True)
    # select_property_type = models.ForeignKey(PropertyTypeFilter,on_delete=models.CASCADE,blank=True,null=True)
    # select_division = models.ForeignKey(Division,on_delete=models.CASCADE,blank=True,null=True)
    # select_district = models.ForeignKey(District,on_delete=models.CASCADE,blank=True,null=True)

    project_type_filter = models.ForeignKey(ProjectTypeFilter, on_delete=models.CASCADE, blank=True, null=True)
    property_type_filter = models.ForeignKey(PropertyTypeFilter, on_delete=models.CASCADE, blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE,blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE,blank=True, null=True)
    sub_district = models.ForeignKey(SubDistrict, on_delete=models.CASCADE,blank=True, null=True)
    post_type = models.ManyToManyField(Property_type, related_name='pro_type',blank=True)

    land_size = models.IntegerField(blank=True,null=True)
    bedrooms = models.IntegerField(blank=True,null=True)
    bathrooms = models.IntegerField(blank=True,null=True)
    apartment_size = models.CharField(max_length=255,blank=True,null=True)
    total_apartment = models.IntegerField(blank=True,null=True)
    parking_area = models.CharField(max_length=100,blank=True,null=True)
    parking_size = models.IntegerField(blank=True,null=True)
    facing = models.CharField(max_length=100,blank=True,null=True)
    lift = models.CharField(max_length=100,choices=LIFT,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    video_link = models.CharField(max_length=500,blank=True,null=True)
    broucher = models.FileField(upload_to='file/',max_length=500,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    floor_plan_image_or_land_layout_img = models.ImageField(upload_to='floor_plan_image/',blank=True, null=True)
    feature = models.TextField(blank=True,null=True)
    map_link = models.TextField(blank=True,null=True)

    developer_name = models.CharField(max_length=250,blank=True, null=True)
    created_date =models.DateTimeField(auto_now_add=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.post_title)
            slug = base_slug
            counter = 1
            while PropertyPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_date(self):
        return self.created_date.date()

    def __str__(self):
        return self.post_title

    class Meta:
        ordering= ['-created_date']

class Post_related_images(models.Model):
    post = models.ForeignKey(PropertyPost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Post_related_images')
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.post.post_title

class Recently_Properties(models.Model):
    images = models.ImageField(upload_to='Recently_Properties/')
    for_rent = models.CharField(max_length=250,blank=True, null=True)
    for_sale = models.CharField(max_length=250,blank=True, null=True)
    price = models.FloatField(default='0.00',blank=True, null=True)
    title = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    sqr_feet = models.CharField(max_length=250)
    bedrooms = models.CharField(max_length=250)
    bathrooms = models.CharField(max_length=250)
    created = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.title}"
    
    class Meta:
        ordering=['-created']

class Counters(models.Model):
    counter_for_sale = models.IntegerField(default='0')
    counter_for_rent = models.IntegerField(default='0')
    brokers = models.IntegerField(default='0')
    agents = models.IntegerField(default='0')

    def __str__(self):
        return f"Num_of_Counters: {self.counter_for_rent}"

class Agent(models.Model):
    images = models.ImageField(upload_to='Agent_img/')
    name = models.CharField(max_length=250)
    disignation = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    email = models.EmailField(max_length=250,null=True)
    mobile = models.CharField(max_length=250)
    fax = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"

 
    def __str__(self):
        return f"{self.option_name}"
    class Meta:
        verbose_name = 'Why_chosse_us_option'
        verbose_name_plural = 'Why_chosse_us_options'


class Why_chosse_us(models.Model):
    bg_color = models.CharField(max_length=100, default='#2E67AF')
    title = models.CharField(max_length=100,null=True)
    title_color = models.CharField(max_length=100, default='white')
    image = models.ImageField(upload_to="whychoose/image/", null=True, blank=True)
    description = models.TextField()
    description_color = models.CharField(max_length=100, default='white')
     
    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = 'Why Chosse US'
        verbose_name_plural = 'Why Chosse US'


class Album(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='album/',)     

    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

class Gallery(models.Model):
    # IMG_TYPE = (
    #     ('Management','Management'),
    #     ('Realstate Property','Realstate Property'),
    #     ('E-commerce','E-commerce'),
    #     ('Client Area','Client Area')
    # )   
    album = models.ForeignKey(Album, on_delete=models.CASCADE,blank=True,null=True)
    img = models.ImageField(upload_to='gallery/office/',blank=True,null=True)
    # img_type = models.CharField(max_length=100, choices=IMG_TYPE, blank=True, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Image type: {self.title}/{self.img}"

    class Meta:
        ordering= ['-id']

class Blog(models.Model):
    blog_img = models.ImageField(upload_to="blog_images")
    title = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)
    details = RichTextUploadingField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_date(self):
        return self.created.date()

    def get_month(self):
        return self.created.strftime("%B")


class AboutUs(models.Model):
    main_image =  models.ImageField(upload_to='about-us_img/')
    # shadow_image = models.ImageField(upload_to='about-us_img/')
    # experience_year = models.IntegerField()
    title = models.CharField(max_length=150,null=True)
    description = RichTextUploadingField(null=True)

    def __str__(self):
        return f'{self.experience_year} of year experience'

    class Meta:
        verbose_name = 'AboutUs'
        verbose_name_plural = 'About Us'

class AboutLookingSection(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'AboutLookingSection'
        verbose_name_plural = 'About looking section'

class AboutTestimotial(models.Model):
    title = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.ImageField(upload_to='about-us_img/')
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'AboutTestimotial'
        verbose_name_plural = 'About Testimotial'


class OurTeam(models.Model):
    name  = models.CharField(max_length = 150)
    designation = models.CharField(max_length = 150)
    image  = models.ImageField(upload_to='TeamImage')
    cover_image  = models.ImageField(upload_to='TeamImage')
    facebook_link = models.URLField(max_length = 500, blank=True,null=True)
    twitter_link = models.URLField(max_length = 500,blank=True,null=True)
    linkedin_link = models.URLField(max_length = 500,blank=True,null=True)
    instagram_link = models.URLField(max_length = 500,blank=True,null=True)
    ordering  = models.IntegerField(blank=True,null=True)
    
    class Meta:
        ordering =['ordering']
        verbose_name = 'OurTeam'
        verbose_name_plural = 'OurTeam'

    def __str__(self):
        return self.name

class Career(models.Model):
    title = models.CharField(max_length = 150)
    slug = models.SlugField(max_length = 50)
    active_status = models.BooleanField(default=True)
    job_description =RichTextUploadingField()
    post_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-id']


class Notice(models.Model):
    title  = models.CharField(max_length = 150)
    notice_file  = models.FileField(upload_to='Notice')
    
    class Meta:
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        return self.title

class ContactUs(models.Model):
    STATUS =(
        ('pending','pending'),
        ('read','read'),
    )
    name = models.CharField(max_length = 150)
    email = models.EmailField()
    phone = models.CharField(max_length = 150)
    subject = models.CharField(max_length = 150)
    message  = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS, null=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'ContactUs'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return self.email

class JobApplication(models.Model):
    STATUS =(
        ('pending','pending'),
        ('read','read'),
    )
    full_name= models.CharField(max_length = 150)
    email = models.EmailField()
    phone= models.CharField(max_length = 150)
    expected_salary= models.CharField(max_length = 150)
    cv= models.FileField(upload_to='ApplicationCV')
    message = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS, null=True)
    
    def __str__(self):
        return self.email

class FeedBack(models.Model):
    STATUS =(
        ('pending','pending'),
        ('read','read'),
    )
    name = models.CharField(max_length=50)
    property_id = models.IntegerField(blank=True,null=True)
    description = models.TextField()
    is_feedback_show = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']


class ServiceType(models.Model):
    name =  models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class ServicePost(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image =  models.ImageField(upload_to = 'services/')
    service_type = models.ManyToManyField(ServiceType,related_name='service')
    created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering= ['-created']



class Service_related_images(models.Model):
    service = models.ForeignKey(ServicePost, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Post_related_images')
    created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.service.title

class Faq(models.Model):
    queations = models.CharField(max_length=250)
    answers = models.TextField()

    def __str__(self):
        return self.queations

class BookingPropertyType(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural='Booking Property Types'

phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$", "The phone number provided is invalid")
class BookingNow(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField (max_length=15,validators=[phone_validator],null = False, blank = False)
    job_designation = models.CharField(max_length=50)
    property_type = models.ForeignKey(BookingPropertyType,on_delete=models.CASCADE, null=True)
    property_size = models.IntegerField()
    property_location = models.ForeignKey(Location,on_delete=models.CASCADE, null=True)
    roperty_description = models.TextField()
    read_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='BookingNow'
        verbose_name_plural='Booking Now'

class SocialMediaLink(models.Model):
    facebook_social_link = models.CharField(max_length=500,blank=True,null=True)
    twitter_social_link = models.CharField(max_length=500,blank=True,null=True)
    linkedin_social_link = models.CharField(max_length=500,blank=True,null=True)
    instagram_social_link = models.CharField(max_length=500,blank=True,null=True)
    youtube_social_link = models.CharField(max_length=500,blank=True,null=True)
    
    def __str__(self):
        return f'social link'
    
class CSR(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image =  models.ImageField(upload_to = 'CSR/')
    created = models.DateTimeField(auto_now_add=True,null=True)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='CSR'



# new add
class MissionVision(models.Model): #d
    title = models.CharField(max_length=150)      
    details = RichTextUploadingField()

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='Mission & Vision'
class Privacy(models.Model):
    title = models.CharField(max_length=150)      
    details = RichTextUploadingField()

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural='Privacy'

class MD_Message(models.Model): #d
    title = models.CharField(max_length=150) 
    image = models.ImageField(upload_to="md_message/images/", null=True)  
    is_center = models.BooleanField(default=True)   
    details = RichTextUploadingField()

    class Meta:
        verbose_name_plural='MD Message'



class Social_Responsibility(models.Model): #d
    title = models.CharField(max_length=150)
    banner = models.ImageField(upload_to="social_responsibility/images/", null=True)      
    details = RichTextUploadingField()

class Testimonial(models.Model): #d
    title = models.CharField(max_length=150) 
    image = models.ImageField(upload_to='testimonial/image/', null=True, blank=True)     
    details = RichTextUploadingField()
    
class Awards(models.Model): #d
    title = models.CharField(max_length=150)  
    image = models.ImageField(upload_to='awards/image/', null=True, blank=True)         
    details = RichTextUploadingField()


class Land_Wanted(models.Model): #d
    title = models.CharField(max_length=150) 
    image = models.ImageField(upload_to='land-wanted/image/', null=True, blank=True)     
    details = RichTextUploadingField()    
    
class Corparate_Structure(models.Model): #d
    title = models.CharField(max_length=150)      
    image = models.ImageField(upload_to='corparate_structure/image/', null=True, blank=True)  

class Our_Certificate(models.Model): #d
    title = models.CharField(max_length=150) 
    image = models.ImageField(upload_to='our-certificate/image/', null=True, blank=True)     
    details = RichTextUploadingField()    


class NewsLetter(models.Model): #d
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name}"
    

class Cup_of_Coffee(models.Model): #d
    title = models.CharField(max_length=100)
    number = models.CharField(max_length=150)
    
class Video_Galary(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField(max_length=250)
    published_by = models.CharField(max_length=100)

from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
from django.utils.text import slugify

class SisterConcernBanner(models.Model):
    image = models.ImageField(upload_to='sister_concerns/banners/', blank=True, null=True)

    def __str__(self):
        return f"Sister Concern Banner {self.id}"

class SisterConcern(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='sister_concerns/sister-concerns-image/', blank=True, null=True)

    # Contact info
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    map_embed_url = models.URLField( max_length=1000, blank=True, null=True, help_text="Google Maps embed URL")
    message = models.TextField(blank=True, null=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

from django.db import models

class RealEstateApplication(models.Model):


    RESIDENCE_TYPE = [
        ('Resident', 'Resident'),
        ('Non Resident', 'Non Resident'),
        ('Apartment', 'Apartment'),
        ('Floor', 'Floor'),
    ]

    # Personal Info
    applicant_full_name = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255, blank=True)
    permanent_address = models.TextField()
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    email = models.EmailField()

    # Profession Info
    profession = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)

    # Project Info
    residence_type = models.CharField(max_length=20, choices=RESIDENCE_TYPE)
    project_location = models.TextField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    per_share_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_project_area = models.CharField(max_length=100)
    number_of_share = models.PositiveIntegerField()
    instruction = models.TextField(blank=True)


    # Legal
    agree_terms = models.BooleanField(default=False)

    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_full_name} - {self.project_location}"
    
class RealstateTerms(models.Model):
    terms = RichTextField()



class Document(models.Model):
    pdf = models.FileField(upload_to='pdfs/')



class CampingBanner(models.Model):
    camping_banner = models.ImageField(upload_to="camping_banner/")
     

