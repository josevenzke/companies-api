from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

def validates_cnpj(cnpj):
    if not cnpj.isdecimal():
        raise ValidationError('CNPJ value should include only numbers')
    if len(cnpj) !=14:
        raise ValidationError(f'CPF length should be 14 not {len(cnpj)}')

def validates_cpf(cpf):
    if not cpf.isdecimal():
        raise ValidationError('CPF value should include only numbers')
    if len(cpf) !=11:
        raise ValidationError(f'CPF length should be 11 not {len(cpf)}')


class Company(models.Model):
    name = models.CharField(max_length=50,unique=True)
    cnpj = models.CharField(max_length=14,unique=True,validators=[validates_cnpj])
    employees = models.ManyToManyField('Employee', through='Employee_companies', blank=True)
    
    class Meta:
        verbose_name_plural = 'Companies'
    
    def __str__(self)->str:
        return f"{self.name}"
    

class Employee(models.Model):
    name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11,unique=True,validators=[validates_cpf])
    companies = models.ManyToManyField('Company',blank=True)

    def __str__(self)->str:
        return f"{self.name}"

