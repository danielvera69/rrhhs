import datetime
from django.db import models
from django.forms import model_to_dict
from apps.core.models import City, Country, ModelBase, Organization
from rrhhs import utils
from rrhhs.const import EMPLOYEE_CLASS, FREQUENCY_ROL
from django.utils.timezone import now

class Post(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    profile = models.TextField(verbose_name='Perfil')
    studies = models.TextField(verbose_name='Estudios', max_length=200)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['-name']

class Category(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    salary = models.DecimalField(verbose_name="Sueldo", decimal_places=2,max_digits=18)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-name']

class TypeEmployee(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
 
    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Tipo Empleado'
        verbose_name_plural = 'Tipo Empelados'
        ordering = ['-name']

class TypeContract(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo Contrato'
        verbose_name_plural = 'Tipo Contratos'
        ordering = ['-name']

class TypeRegime(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo Regimen'
        verbose_name_plural = 'Tipo Regimens'
        ordering = ['-name']

class TypeArea(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def __str__(self):
        return self.name

    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo Area'
        verbose_name_plural = 'Tipo Areas'
        ordering = ['-name']

class Area(ModelBase):
    name = models.CharField(verbose_name='Nombre', max_length=50, unique=True)
    type_area=models.ForeignKey(TypeArea,on_delete=models.PROTECT,verbose_name='type_area')
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal')
    predecessor = models.ForeignKey("self",on_delete=models.PROTECT,verbose_name='Predecesor',blank=True,null=True)
    active = models.BooleanField(verbose_name='Activo', default=True)
    
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['-name']

class Employee(ModelBase):
    firts_name = models.CharField(verbose_name='Nombres',max_length=50,)
    last_name = models.CharField(verbose_name='Apellidos',max_length=50,)
    image = models.ImageField(verbose_name='Foto',upload_to='empleado',max_length=500,null=True,blank=True)
    dni = models.CharField(verbose_name="Dni", max_length=50)
    phone = models.CharField(verbose_name="Teléfono", max_length=50, blank=True, null=True)
    email = models.CharField(verbose_name="Correo", max_length=100)
    country = models.ForeignKey(Country,on_delete=models.PROTECT,verbose_name='Pais')
    city = models.ForeignKey(City,on_delete=models.PROTECT,verbose_name='Ciudad', blank=True, null=True)
    direction = models.CharField(verbose_name="Dirección", max_length=100)
    latitude = models.CharField(verbose_name="Latitud", max_length=100, blank=True, null=True)
    longitude = models.CharField(verbose_name="Longitud", max_length=100, blank=True, null=True)
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal', blank=True, null=True)
    date_admission = models.DateTimeField(verbose_name="Fecha Ingreso",default=now)
    post = models.ForeignKey(Post,on_delete=models.PROTECT,verbose_name='Cargo', blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='Categoria', blank=True, null=True)
    area = models.ForeignKey(Area,on_delete=models.PROTECT,verbose_name='Area', blank=True, null=True)
    employee_class = models.IntegerField(verbose_name="Clase Empleado", choices=EMPLOYEE_CLASS,default=EMPLOYEE_CLASS[1][0])
    type_regime = models.ForeignKey(TypeRegime,on_delete=models.PROTECT,verbose_name='Tipo Regimen', blank=True, null=True)
    type_employee = models.ForeignKey(TypeEmployee,on_delete=models.PROTECT,verbose_name='Tipo Empleado', blank=True, null=True)
    type_contract = models.ForeignKey(TypeContract,on_delete=models.PROTECT,verbose_name='Tipo Contrato', blank=True, null=True)
    number_iess = models.CharField(verbose_name="Numero Iess", max_length=50,blank=True,null=True)
    date_membership = models.DateField(verbose_name="Fecha Iess",default=now)
    sueldo = models.DecimalField(verbose_name="Sueldo", decimal_places=2,max_digits=18)
    rol= models.BooleanField(verbose_name="Pago Rol", default=True)
    frequency_rol = models.IntegerField(verbose_name="Frecuencia Rol", choices=FREQUENCY_ROL,default=FREQUENCY_ROL[1][0],blank=True,null=True)
    active = models.BooleanField(verbose_name="Activo", default=False)
  
    def get_full_name(self):
        return f'{self.last_name} {self.firts_name}'

    def get_model_dict(self):
        item = model_to_dict(self)
        item['image_url'] = self.get_image_url()
        return item

    def get_image_url(self):
        return utils.get_image(self.image)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ('-id',)
        
