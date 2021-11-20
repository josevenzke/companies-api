from rest_framework import serializers
from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['id','name','cpf','companies']
    
    def update(self,instance, validated_data):
        company = validated_data.pop('companies')[0]

        company = Company.objects.get(pk=company.id)
        employee = Employee.objects.get(pk=instance.id)

        employee.companies.add(company)
        employee.save()
        return employee

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id','name','cnpj','employees']
    
    def update(self,instance, validated_data):
        employees = validated_data.pop('employees')[0]

        employee = Employee.objects.get(pk=employees.id)
        company = Company.objects.get(pk=instance.id)

        company.employees.add(employee)
        company.save()
        return company
