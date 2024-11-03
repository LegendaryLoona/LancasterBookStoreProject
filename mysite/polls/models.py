from django.db import models

class Investment(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    years = models.IntegerField(default=30)
    monthly_contribution = models.IntegerField(default=0)
    def projected_revenue(self):
        total_amount = self.amount
        r = self.percentage / 100
        for i in range(1, self.years+1):
            total_amount = total_amount*(1+r)
            total_amount+= self.monthly_contribution*12
        return round(total_amount, 1)
    
class Expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    years = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    def projected_loss(self):
        if self.years != 0:
            return round(self.amount * self.years, 1)
        else:
            return round(self.amount, 1)