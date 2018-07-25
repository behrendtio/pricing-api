import json
import pytest

from pricing_core.models import Order


@pytest.mark.django_db(transaction=False)
def test_the_endpoint_creates_order(client, django_user_model):
    assert Order.objects.exists() is False
    client, _ = get_logged_in_client(client, django_user_model)
    headers = {'content-type': 'application/json'}
    payload = {'customer': 3, 'items': [{'id': 3, 'quantity': 1}, {'id': 4, 'quantity': 2}]}

    response = client.post("http://127.0.0.1:9000/api/orders/", data=json.dumps(payload), headers=headers)

    assert response.status_code == 201
    response_json = response.json()
    for item in payload.items():
        assert response_json[item] == item

    assert Order.objects.filter(id=response_json["id"]).exists()
    assert Order.objects.all().count() == 1


def get_logged_in_client(client, django_user_model):
    username = "user1"
    password = "pass1"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.login(username=username, password=password)
    return client, user
