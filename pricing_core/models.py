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
    name = models.CharField(max_length=128)
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

    def __str__(self):
        return self.name


class Order(BaseModel):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='ItemQuantity', blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)

    @property
    def vat_total(self):
        vat_total = 0
        for item in self.items.all():
            quantity = item.itemquantity_set.get(order=self.id).quantity
            vat_total += item.vat * quantity
        if self.currency:
            rate = get_currency_rate("GBP", self.currency)
            rate = rate.get("GBP" + "_" + self.currency)
            vat_total = vat_total * rate
            return round(vat_total)
        return round(vat_total)

    @property
    def order_total(self):
        total = 0
        for item in self.items.all():
            quantity = item.itemquantity_set.get(order=self.id).quantity
            total += item.price * quantity + item.vat * quantity
        if self.currency:
            rate = get_currency_rate("GBP", self.currency)
            rate = rate.get("GBP" + "_" + self.currency)
            total = total * rate
            return round(total)
        return round(total)

    # The amounts would change each time currecy fluxcuates.
    # For (real world) production uses, these values should also be kept in the database.

    def __str__(self):
        return "Order # %i" % self.id


class ItemQuantity(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "%s - %s x %s " % (self.order, self.item, self.quantity)
