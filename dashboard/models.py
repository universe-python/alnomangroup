from django.db import models

# Create your models here.

class Admin(models.Model):
    admin_name = models.CharField(max_length=50,blank=True,null=True)
    admin_image = models.ImageField(upload_to="admin_images/",blank=True,null=True)
    navbar_color = models.CharField(max_length=50, default="transparent")
    navbar_textcolor = models.CharField(max_length=50, default="black")
    navbar_texthovercolor = models.CharField(max_length=50, default="red")
    navbar_textactivecolor = models.CharField(max_length=50, default="red")
    logo = models.ImageField(upload_to="admin_logos/",blank=True,null=True)
    footer_logo = models.ImageField(upload_to="footer_logos/",blank=True,null=True)
    favicon = models.ImageField(upload_to="admin_favicons/",blank=True,null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    phone3 = models.CharField(max_length=15, blank=True, null=True)
    phone4 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.admin_name

    class Meta:
        ordering = ['-id']