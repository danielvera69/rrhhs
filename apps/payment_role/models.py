import datetime
from django.db import models
from django.forms import model_to_dict
from apps.core.models import ModelBase, Organization
from apps.personal_file.models import Employee
from rrhhs import utils
from rrhhs.const import TYPE_DISCOUNT, TYPE_ITEM

class RoleFrequency(ModelBase):
    description= models.CharField(verbose_name="Descripcion",max_length=20)
    
    def get_model_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return f'{self.description}'
    
    class Meta:
        verbose_name = 'Frecuencia Rol'
        verbose_name_plural = 'Frecuencia Roles'
        ordering = ('-id',)
    
  
class Item(ModelBase):
    code_item= models.CharField(verbose_name="Codigo Rubro",max_length=3)
    name_short= models.CharField(verbose_name="Nombre Corto",max_length=10)
    description= models.CharField(verbose_name="Descripcion",max_length=100)
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='sucursal')
    type_item=models.IntegerField(choices=TYPE_ITEM,default=TYPE_ITEM[0][0])
    collective = models.BooleanField(default=False)
    role_frequency=models.ManyToManyField(RoleFrequency,verbose_name='Frecuencia Rol')
    order=models.IntegerField(verbose_name="Orden")
    discount=models.IntegerField(choices=TYPE_DISCOUNT,default=TYPE_ITEM[0][0])
    value= models.DecimalField(verbose_name="Valor", decimal_places=2,max_digits=18)
    role_month=models.BooleanField(verbose_name="Rol mensual",default=False)
    thirteenth=models.BooleanField(verbose_name="Decimo Tercero",default=False)
    fourteenth=models.BooleanField(verbose_name="Decimo Cuarto",default=False)
    vacation=models.BooleanField(verbose_name="Vacacion",default=False)
    reserve_fund=models.BooleanField(verbose_name="Fondo Reserva",default=False)
    retirement = models.BooleanField(verbose_name="Renuncia",default=False)
    resignation= models.BooleanField(verbose_name="Jubilacion",default=False)
    employer_retirement = models.BooleanField(verbose_name="Liquidacion Patronal",default=False)
    Hours_extras = models.BooleanField(verbose_name="Horas Extras",default=False)
    active = models.BooleanField(verbose_name="Activo",default=False)
    
    def get_model_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return f'{self.code_item}-{self.name_short}'
    
    class Meta:
        verbose_name = 'Rubro'
        verbose_name_plural = 'Rubros'
        ordering = ('-id',)
    
    
class Calendar(ModelBase):
    year = models.IntegerField(verbose_name='Año',default=datetime.date.today().year)
    month = models.IntegerField(verbose_name='Mes',default=datetime.date.today().month)
    role_frequency = models.ForeignKey(RoleFrequency,on_delete=models.PROTECT, verbose_name='Frecuencia Rol')
    date_from = models.DateTimeField(verbose_name='Fecha desde')
    date_to = models.DateTimeField(verbose_name='Fecha hasta')
    active = models.BooleanField(default=False)
    
    @property
    def codigo_rol(self):
        return f'Rol#:{self.id} - {self.role_frequency.description} - {self.year} - {self.month}'
    
    def get_model_dict(self):
        item = model_to_dict(self)
        return item
        
        
    def __str__(self):
        return self.codigo_rol
    
    class Meta:
        verbose_name = 'Calendario'
        verbose_name_plural = 'Calendario Roles'
        ordering = ('id',)
        
class Overtime(ModelBase):
    calendar = models.ForeignKey(Calendar,on_delete=models.PROTECT,verbose_name='Calendario Rol')
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal')
    value_hour= models.DecimalField(verbose_name="Valor hora", decimal_places=2,max_digits=10)
    total=models.DecimalField(verbose_name="Total Sobretiempo", decimal_places=2,max_digits=10)
    processed = models.BooleanField(default=False)
    calendar_process = models.IntegerField("Calendario Procesado",blank=True,null=True)
      
    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.employee.get_full_name()}'
    
    class Meta:
        verbose_name = 'Sobretiempo'
        verbose_name_plural = 'Sobretiempos'
        ordering = ('-id',)
        
class OvertimeDetail(ModelBase):
    overtime = models.ForeignKey(Overtime,on_delete=models.CASCADE,verbose_name='Sobretiempo')
    item = models.ForeignKey(Item,on_delete=models.PROTECT,verbose_name='Tipo Horas',blank=True,null=True)
    number_hours=models.DecimalField(verbose_name="Numero horsa", decimal_places=2,max_digits=10)
    value=models.DecimalField(verbose_name="Valor", decimal_places=2,max_digits=10)

    
    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.value}'
    
    class Meta:
        verbose_name = 'Sobretiempo detalle'
        verbose_name_plural = 'Sobretiempo detalles'
        ordering = ('-id',)

class PayRoll(ModelBase):
    calendar = models.ForeignKey(Calendar,on_delete=models.PROTECT,verbose_name='Calendario Rol')
    sucursal = models.ForeignKey(Organization,on_delete=models.PROTECT,verbose_name='Sucursal')
    income=models.DecimalField(verbose_name="Total Ingresos", decimal_places=2,max_digits=18)
    discounts=models.DecimalField(verbose_name="Total Descuentos", decimal_places=2,max_digits=18)
    net=models.DecimalField(verbose_name="Neto Recibir", decimal_places=2,max_digits=18)
    processed = models.BooleanField(default=False)
    
    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.calendar.year}-{self.calendar.month}-{self.net}'
    
    class Meta:
        verbose_name = 'Nomina'
        verbose_name_plural = 'Nominas'
        ordering = ('-id',)
        

class PayRollDetail(ModelBase):
    payRoll = models.ForeignKey(PayRoll,on_delete=models.PROTECT,verbose_name='Nomina')
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    income=models.DecimalField(verbose_name="Total Ingresos", decimal_places=2,max_digits=10)
    discounts=models.DecimalField(verbose_name="Total Descuentos", decimal_places=2,max_digits=10)
    net=models.DecimalField(verbose_name="Neto Recibir", decimal_places=2,max_digits=10)
 
    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.employee.get_full_name()}-{self.net}'
    
    class Meta:
        verbose_name = 'Nomina detalle'
        verbose_name_plural = 'Nomina detalles'
        ordering = ('-id',)
 
class PayRollDetailItem(ModelBase):
    payRollDetail = models.ForeignKey(PayRollDetail,on_delete=models.PROTECT,verbose_name='Detalle Rubros')
    item = models.ForeignKey(Item,on_delete=models.PROTECT,verbose_name='Rubro')
    value=models.DecimalField(verbose_name="Valor", decimal_places=2,max_digits=10)
    balance=models.DecimalField(verbose_name="Saldo", decimal_places=2,max_digits=10)
   
    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.item}-{self.value}'
    
    class Meta:
        verbose_name = 'Detalle rubro'
        verbose_name_plural = 'Detalle Rubros'
        ordering = ('-id',)
 
class EmployeeItems(ModelBase):
    employee = models.ForeignKey(Employee,on_delete=models.PROTECT,verbose_name='Empleado')
    item = models.ManyToManyField(Item,verbose_name='Rubro')
  
    def get_model_to_dict(self):
        item = model_to_dict(self)
        return item
    
    def __str__(self):
        return f'{self.employee.get_full_name()}'

    class Meta:
        verbose_name = 'Empleado Rubro'
        verbose_name_plural = 'Empleado Rubros'
       
 