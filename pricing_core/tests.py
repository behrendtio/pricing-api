import json
import pytest
from django.contrib.auth.models import User

from rest_framework.test import RequestsClient

from pricing_core.models import Order, Product


@pytest.mark.django_db(transaction=False)
def test_requests():
    client = RequestsClient()
    response = client.get('http://testserverapi/api/orders/')
    assert response.status_code == 200


@pytest.mark.django_db(transaction=False)
def test_the_endpoint_creates_order(client, django_user_model):

    # Creating the products that will be used in the tests
    Product.objects.create(name="Book", price=599, vat_band="st")
    Product.objects.create(name="White Bread", price=250, vat_band="ze")
    Product.objects.create(name="Wholegrain Bread", price=250, vat_band="ze")
    Product.objects.create(name="Computer", price=1000, vat_band="ze")
    Product.objects.create(name="Car", price=1250, vat_band="st")

    # Creating the customer
    user = User.objects.create(username="user", email='test@test.com', is_active=True)
    user.set_password('test')
    user.save()

    # Testing
    assert Order.objects.exists() is False
    #client = RequestsClient()

    #client, _ = get_logged_in_client(client, django_user_model)
    payload = {"customer": 1, "items": [{"id": 3, "quantity": 1}, {"id": 4, "quantity": 2}]}

    response = client.post("http://testserverapi/api/orders/", data=json.dumps(payload), content_type="application/json")

    assert response.status_code == 201
    response_json = response.json()

    # checking if the order was created
    assert Order.objects.filter(id=response_json["id"]).exists()
    assert Order.objects.all().count() == 1

    # checking if the order belongs to the right customer
    assert response_json["customer"] == payload["customer"]

    # checking if the same number of items were added to the order
    assert len(response_json["items"]) == len(payload["items"])


# def get_logged_in_client(client, django_user_model):
#     username = "user1"
#     password = "pass1"
#     user = django_user_model.objects.create_user(username=username, password=password)
#     client.login(username=username, password=password)
#     return client, user
