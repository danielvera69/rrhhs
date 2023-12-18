import json
from django.db import models
from django.forms import model_to_dict
from rrhhs import utils

class Country(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    state = models.BooleanField(verbose_name='Activo', default=True)
  
    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Pais'
        verbose_name_plural = 'Paises'
        ordering = ['-name']

class City(models.Model):
    country = models.ForeignKey(Country,on_delete=models.PROTECT,verbose_name="Pais")
    name = models.CharField('Descripcion',max_length=100)
 
    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['-name']

class Organization(models.Model):
    name = models.CharField(
        verbose_name='Nombre de la organización',
        max_length=100,
        unique=True
    )
    country = models.ForeignKey(Country,on_delete=models.PROTECT,verbose_name='Pais')
    city = models.ForeignKey(City,on_delete=models.PROTECT,verbose_name='Ciudad')
    image = models.ImageField(
        verbose_name='Logo',
        upload_to='organization',
        max_length=500,
        null=True,
        blank=True
    )
    ruc = models.CharField("Ruc Empresa", max_length=15)
    direction = models.CharField("Dirección", max_length=100)
    phone = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    fax = models.CharField("Fax", max_length=50, blank=True, null=True)
    email = models.CharField("Correo", max_length=100)
    web = models.CharField("Página Web", max_length=100, blank=True, null=True)
    slogan = models.CharField("Eslogan", max_length=100, blank=True, null=True)
    ruc_representative = models.CharField(
        'Ruc Representante',
        max_length=15,
        blank=True,
        null=True
    )
    latitude = models.CharField("Latitud", max_length=100, blank=True, null=True)
    longitude = models.CharField("Longitud", max_length=100, blank=True, null=True)
    matriz = models.BooleanField(default=False)
  
    @staticmethod
    def get_organization_first():
        return Organization.objects.filter(matriz=True).order_by('id').first()

    def of_json_pure_to_dumps(self):
        return json.dumps(self.get_model_dict())

    def get_model_dict(self):
        item = model_to_dict(self)
        item['image_url'] = self.get_image_url()
        return item

    def get_image_url(self):
        return utils.get_image(self.image)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ('-id',)


