from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name} ({self.code})"
    
class User(models.Model):
    currency= models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True,blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
    MONTH_CHOICES = [
        ('january', 'January'),
        ('february', 'February'),
        ('march', 'March'),
        ('april', 'April'),
        ('may', 'May'),
        ('june', 'June'),
        ('july', 'July'),
        ('august', 'August'),
        ('september', 'September'),
        ('october', 'October'),
        ('november', 'November'),
        ('december', 'December')
    ]

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency= models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True,blank=True)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month= models.CharField(max_length=100,choices=User.MONTH_CHOICES,default='january')
    emoji = models.CharField(max_length=100, default='💰')
    def __str__(self):
        return f"{self.source} - {self.currency.symbol}{self.amount}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency= models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True,blank=True)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month= models.CharField(max_length=100,choices=User.MONTH_CHOICES,default='january')
    emoji = models.CharField(max_length=100, default='🛒')
    
    def __str__(self):
        return f"{self.category} - {self.currency.symbol}{self.amount}"
    
class Bill(models.Model):
    currency= models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True,blank=True)
    bill_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    def _str_(self):
        return self.name
    
class Goal(models.Model):
    currency= models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True,blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    incomes= models.ForeignKey(Income, on_delete=models.SET_NULL, null=True,blank=True)
    expenses= models.ForeignKey(Expense,on_delete=models.SET_NULL, null=True,blank=True)
    goal_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_done = models.BooleanField(default=False)
    
