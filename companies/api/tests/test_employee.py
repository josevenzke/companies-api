import pytest
import json

from django.urls import reverse
from api.models import Company, Employee


employees_url = reverse("employees-list")


#------------------ Test GET Companies ------------------------

@pytest.mark.django_db
def test_zero_employees_should_return_empty_list(client) -> None:
    response = client.get(employees_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []

@pytest.mark.django_db
def test_one_employee_exists(client) -> None:
    test_employee = Employee.objects.create(name="João",cpf='12345678910')
    response = client.get(employees_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_employee.name
    assert response_content.get("cpf") == test_employee.cpf

@pytest.mark.django_db
def test_get_one_employee_by_id(client) -> None:
    test_employee = Employee.objects.create(name="João",cpf='12345678910')
    response = client.get(employees_url+f'{test_employee.id}/')
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("name") == test_employee.name
    assert response_content.get("cpf") == test_employee.cpf


#------------------ Test POST Companies ------------------------

@pytest.mark.django_db
def test_create_employee_without_name(client) -> None:
    response = client.post(employees_url,data={"cpf":"12345678910"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}

@pytest.mark.django_db
def test_create_employee_without_cpf(client) -> None:
    response = client.post(employees_url,data={"name":"João"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"cpf": ["This field is required."]}

@pytest.mark.django_db
def test_create_employee_with_wrong_cpf_length(client) -> None:
    response = client.post(employees_url,data={"name":"João","cpf":"1234567891"})
    assert response.status_code == 400
    assert json.loads(response.content) == {'cpf': ['CPF length should be 11 not 10']}

@pytest.mark.django_db
def test_create_employee_with_not_numeric_cpf(client) -> None:
    response = client.post(employees_url,data={"name":"João","cpf":"12abc678910"})
    assert response.status_code == 400
    assert json.loads(response.content) == {'cpf': ['CPF value should include only numbers']}

@pytest.mark.django_db
def test_create_employee(client) -> None:
    response = client.post(employees_url,data={"name":"João","cpf":"12345678910"})
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content.get("name") == "João"
    assert response_content.get("cpf") == "12345678910"

#------------------ Test PATCH Companies ------------------------

@pytest.mark.django_db
def test_patch_one_company_employees_list(client) -> None:
    test_company = Company.objects.create(name="Amazon",cnpj='12345678910111')
    test_employee = Employee.objects.create(name="Joao",cpf="12345678910")
    response = client.patch(employees_url+f'{test_employee.id}/',data=json.dumps({'companies': [test_company.id]}), content_type='application/json')
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("name") == test_employee.name
    assert response_content.get("cpf") == test_employee.cpf
    assert response_content.get("companies")[0] == test_company.id


@pytest.mark.django_db
def test_patch_one_company_withou_employee_id(client) -> None:
    test_employee = Employee.objects.create(name="Joao",cpf="12345678910")
    response = client.patch(employees_url+f'{test_employee.id}/', content_type='application/json')
    assert response.status_code == 400
    assert json.loads(response.content) == {"companies":["No companies value found"]}
