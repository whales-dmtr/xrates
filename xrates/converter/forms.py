from django.forms import Form, FloatField, ChoiceField

CURRENCY_CHOICES = {
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'PLN': 'Polish Zloty',
    'GBP': 'British Pound',
    'CHF': 'Swiss Franc',
    'JPY': 'Japanese Yen',
    'CZK': 'Czech Koruna',
}


class ConverterForm(Form):
    hryvnias_amount = FloatField(min_value=0)
    currency = ChoiceField(choices=CURRENCY_CHOICES)