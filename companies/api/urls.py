from rest_framework import routers
from .views import CompanyViewSet, EmployeeViewSet

companies_router = routers.DefaultRouter()

companies_router.register("companies", viewset=CompanyViewSet, basename="companies")
companies_router.register("employees", viewset=EmployeeViewSet, basename="employees")
