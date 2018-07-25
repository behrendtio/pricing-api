from django.contrib.auth.models import User
from django.db import models
from pricing_core.services import get_currency_rate


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(editable=False, default=False,
                                     verbose_name='Deleted')

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField(max_length=128)  # name of the task
    price = models.PositiveIntegerField(default=0)

    ZERO = "ze"
    STANDARD = "st"
    VAT_CHOICES = ((ZERO, "Zero"), (STANDARD, "Standard"))

    vat_band = models.CharField(max_length=2, choices=VAT_CHOICES, default="st")

    # More fields can also be added such as short_description or tag etc but it would not demonstrate any different skills

    @property
    def vat(self):
        if self.vat_band == self.ZERO:
            return 0
        else:
            return round(self.price * 0.2)
        # per country

    def __str__(self):
        return self.name


class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='ItemQuantity', blank=True)

    @property
    def vat_total(self):
        vat_total = 0
        quantity = item.itemquantity_set.get(order=self.id).quantity
        for item in self.items.all():
            vat_total += item.vat * quantity
        return round(vat_total)

    @property
    def order_total(self):
        total = 0
        for item in self.items.all():
            quantity = item.itemquantity_set.get(order=self.id).quantity
            total += item.price * quantity + item.vat * quantity
        return round(total)

    def get_converted_order_total(self, user_currency="GBP", org_currency="GBP"):
        if user_currency == org_currency:
            return self.order_total
        rate = get_currency_rate(org_currency, user_currency)
        rate = rate.get(org_currency + "_" + user_currency)  # the format of the currency API
        converted_order_total = round(rate * self.order_total)
        return converted_order_total

    def __str__(self):
        return "Order # %i" % self.id


class ItemQuantity(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s - %s x %s " % (self.order, self.item, self.quantity)
