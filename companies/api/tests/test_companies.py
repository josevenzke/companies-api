import pytest
import json

from django.urls import reverse
from api.models import Company, Employee


companies_url = reverse("companies-list")


# ------------------ Test GET Companies ------------------------


@pytest.mark.django_db
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.django_db
def test_one_company_exists(client) -> None:
    test_company = Company.objects.create(name="Amazon", cnpj="12345678910111")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("cnpj") == test_company.cnpj


@pytest.mark.django_db
def test_get_one_company_by_id(client) -> None:
    test_company = Company.objects.create(name="Amazon", cnpj="12345678910111")
    response = client.get(companies_url + f"{test_company.id}/")
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("cnpj") == test_company.cnpj


# ------------------ Test POST Companies ------------------------


@pytest.mark.django_db
def test_create_company_without_name(client) -> None:
    response = client.post(companies_url, data={"cnpj": "12345678910111"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


@pytest.mark.django_db
def test_create_company_without_cnpj(client) -> None:
    response = client.post(companies_url, data={"name": "Amazon"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"cnpj": ["This field is required."]}


@pytest.mark.django_db
def test_create_company_with_wrong_cnpj_length(client) -> None:
    response = client.post(companies_url, data={"name": "Amazon", "cnpj": "123456789"})
    assert response.status_code == 400
    assert json.loads(response.content) == {"cnpj": ["CNPJ length should be 14 not 9"]}


@pytest.mark.django_db
def test_create_company_with_not_numeric_cnpj(client) -> None:
    response = client.post(
        companies_url, data={"name": "Amazon", "cnpj": "128asdf910111a"}
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "cnpj": ["CNPJ value should include only numbers"]
    }


@pytest.mark.django_db
def test_create_company(client) -> None:
    response = client.post(
        companies_url, data={"name": "Amazon", "cnpj": "12345678910111"}
    )
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content.get("name") == "Amazon"
    assert response_content.get("cnpj") == "12345678910111"


# ------------------ Test PATCH Companies ------------------------


@pytest.mark.django_db
def test_patch_one_company_employees_list(client) -> None:
    test_company = Company.objects.create(name="Amazon", cnpj="12345678910111")
    test_employee = Employee.objects.create(name="Joao", cpf="12345678910")
    response = client.patch(
        companies_url + f"{test_company.id}/",
        data=json.dumps({"employees": [test_employee.id]}),
        content_type="application/json",
    )
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("cnpj") == test_company.cnpj
    assert response_content.get("employees")[0] == test_employee.id


@pytest.mark.django_db
def test_patch_one_company_withou_employee_id(client) -> None:
    test_company = Company.objects.create(name="Amazon", cnpj="12345678910111")
    response = client.patch(
        companies_url + f"{test_company.id}/", content_type="application/json"
    )
    assert response.status_code == 400
    assert json.loads(response.content) == {"employees": ["No employees value found"]}
