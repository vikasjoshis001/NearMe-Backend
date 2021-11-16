from django.db import models

# Create your models here.


class ShopInfo(models.Model):
    """ A custom shop """

    shop_id = models.AutoField(primary_key=True)

    shop_name = models.CharField(max_length=50, blank=True, null=True)
    shop_contact = models.CharField(max_length=10, blank=True, null=True)
    shop_email = models.CharField(max_length=50, blank=True, null=True)
    shop_address = models.CharField(max_length=50, blank=True, null=True)
    shop_type = models.CharField(max_length=50, blank=True, null=True)
    shop_description = models.TextField(max_length=500)
    shop_image = models.FileField(
        upload_to='images/', null=True, blank=True, default="media/images/logo.png")

    owner_name = models.CharField(max_length=50, blank=True, null=True)
    owner_contact = models.CharField(max_length=10, blank=True, null=True)
    owner_email = models.CharField(max_length=50, blank=True, null=True)
    owner_address = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.shop_name


class ContactUs(models.Model):
    """ contact us """

    contact_id = models.AutoField(primary_key=True)

    fname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return self.fname
