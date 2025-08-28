from django.db import models
from decimal import Decimal

class Fund(models.Model):
    STRATEGY_CHOICES = [
        ('Long/Short Equity', 'Long/Short Equity'),
        ('Global Macro', 'Global Macro'),
        ('Arbitrage', 'Arbitrage'),
    ]
    
    name = models.CharField(max_length=200)
    strategy = models.CharField(max_length=50, choices=STRATEGY_CHOICES)
    aum = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    inception_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
