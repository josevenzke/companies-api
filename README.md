# Companies API 

Esse é um exemplo de aplicação provendo uma API REST para a manipulação de uma 
relação Many-To-Many(MTM), feita com Django/DRF e com a intenção de usar ao máximo
as vantagens que essas ferramentas trazem para um desenvolvimento eficaz.

### models.py
Feita a criação de modelos simples, com uma relação many-to-many nos dois lados, usando o método de referência a tabela intermediaria ao invés de usar um inline por conta da integração com o ModelViewSet

### serializers.py
Deixando o ModelSerializer fazer o trabalho pesado, e apenas sobrescrevendo o método de update para que as requests de path/put adicionem uma nova relação a tabela intermediaria ao invés de modificar uma. 

### views.py
Por conta da simplicidade dos modelos e suas relações, optei pelo uso do ModelViewSet, já que nesse caso a abstração e inflexibilidade que a classe proporciona não é um problema.

### urls.py
Como padrão junto ao uso dos viewsets, as urls são feitas dinamicamente através de routers.

### /tests
Implementação feita com pytest, fazendo simples testes de unidade para as operações possíveis, com uma cobertura razoável.



# Endpoints

Os endpoints da API estão descritos abaixo.

URL: `https://companies-test-api.herokuapp.com/`

# Companies:
## Get list of Companies

### Request

`GET /companies/`

    curl -i -H 'Accept: application/json' https://companies-test-api.herokuapp.com/companies/

### Response

    Status: 200 OK
    Connection: keep-alive
    Content-Type: application/json
    Content-Length: 200

    [{
        "id": 1,
        "name": "Facebook",
        "cnpj": "12345678910122",
        "employees": []
    }]

## Create a new Company

### Request

`POST /companies/`

    curl -i -H 'Accept: application/json' -d 'name=Netflix&cnpj=12345123451234' https://companies-test-api.herokuapp.com/companies/

### Response

    Status: 201 Created
    Connection: Connection: keep-alive
    Content-Type: application/json
    Location: /companies/1/
    Content-Length: 64

    {
    "id": 1,
    "name": "Netflix",
    "cnpj": "12345123451234",
    "employees": []
    }

## Get a specific Company

`GET /companies/{id}/`

    curl -i -H 'Accept: application/json' https://companies-test-api.herokuapp.com/companies/{id}/

### Response

    Status: 200 OK
    Connection: keep-alive
    Content-Type: application/json
    Content-Length: 64

    {
    "id": 1,
    "name": "Netflix",
    "cnpj": "12345123451234",
    "employees": []
    }

## Add employee to specific Company

`PATCH /companies/{id}/`

    curl -i -H 'Accept: application/json' -d 'employees=1' https://companies-test-api.herokuapp.com/companies/{id}/

No body envie um id de um employee através da key employees, como:
employees=1

### Response

    Status: 200 OK
    Connection: keep-alive
    Content-Type: application/json
    Content-Length: 64

    {
        "id": 1,
        "name": "Netflix",
        "cnpj": "12345123451234",
        "employees": [1]
    }

# Employees:
## Get list of Employees

### Request

`GET /employees/`

    curl -i -H 'Accept: application/json' https://companies-test-api.herokuapp.com/employees/

### Response

    Status: 200 OK
    Connection: keep-alive
    Content-Type: application/json
    Content-Length: 127

    [{
        "id": 1,
        "name": "João",
        "cpf": "12345678912",
        "companies": [2,3]
    }]

## Create a new Employee

### Request

`POST /employees/`

    curl -i -H 'Accept: application/json' -d 'name=Jorge&cpf=12345123451' https://companies-test-api.herokuapp.com/employees/

### Response

    Status: 201 Created
    Connection: Connection: keep-alive
    Content-Type: application/json
    Location: /companies/1/
    Content-Length: 64
    
    {
        "id": 1,
        "name": "Jorge",
        "cpf": "12345123451",
        "companies": []
    }


## Get a specific Employee

`GET /employees/{id}/`

    curl -i -H 'Accept: application/json' https://companies-test-api.herokuapp.com/employees/{id}/

### Response

    Status: 200 OK
    Connection: keep-alive
    Content-Type: application/json
    Content-Length: 64

    {
        "id": 1,
        "name": "Jorge",
        "cpf": "12345123451",
        "companies": []
    }

## Add company to specific Employee

`PATCH /employes/{id}/`

    curl -i -H 'Accept: application/json' -d 'companies=1' https://companies-test-api.herokuapp.com/employees/{id}/

No body envie um id de uma company através da key companies, como:
companies=1

### Response

    Status: 200 OK
    Connection: keep-alive
    Content-Type: application/json
    Content-Length: 64

    {
    "id": 1,
    "name": "Jorge",
    "cpf": "12345123451",
    "companies": [1]
    }
