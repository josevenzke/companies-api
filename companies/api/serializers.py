from rest_framework import serializers
from django.core.exceptions import ValidationError

from .models import Company, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "name", "cpf", "companies"]

    def update(self, instance, validated_data):
        company = validated_data.pop("companies",None)
        if not company:
            raise serializers.ValidationError({"companies":["No companies value found"]})

        company = Company.objects.get(pk=company[0].id)
        employee = Employee.objects.get(pk=instance.id)

        employee.companies.add(company)
        employee.save()
        return employee


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "cnpj", "employees"]

    def update(self, instance, validated_data):
        employees = validated_data.pop("employees",None)
        if not employees:
            raise serializers.ValidationError({"employees":["No employees value found"]})

        employee = Employee.objects.get(pk=employees[0].id)
        company = Company.objects.get(pk=instance.id)

        company.employees.add(employee)
        company.save()
        return company
