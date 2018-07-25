from django.test import TestCase

from unittest import skip

from django.contrib.auth.models import User
# from django.urls import reverse

# from pricing_core.models import Order, Product

user = User.object.get(id=1)

from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/', {'user': user})
