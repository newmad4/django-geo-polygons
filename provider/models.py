from django.contrib.gis.db import models


class Provider(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    language = models.CharField(max_length=50, help_text="Language code")
    currency = models.CharField(max_length=20, help_text="Currency code")


class ServiceArea(models.Model):
    name = models.CharField(max_length=200)
    provider = models.ForeignKey(
        Provider,
        related_name="services_areas",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=18, decimal_places=2)
    geo_information = models.PolygonField()
