from django import forms
from .models import User, Income, Expense,Currency

class SignupForm(forms.ModelForm):
    currency=forms.ModelChoiceField(queryset=Currency.objects.all(),empty_label='Select Currency',required= True)
    class Meta:
        model = User
        fields = ['name', 'email', 'password','currency']
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class IncomeForm(forms.ModelForm):
    INCOME_CATEGORIES = [
        ('💰 Salary', '💰 Salary'),
        ('💼 Business', '💼 Business'),
        ('💻 Freelance', '💻 Freelance'),
        ('📈 Investments', '📈 Investments'),
        ('🏠 Rental', '🏠 Rental'),
        ('🎁 Other', '🎁 Other')
    ]
    
    source = forms.ChoiceField(choices=INCOME_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))
    
    class Meta:
        model = Income
        fields = ['source', 'amount']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.emoji = self.cleaned_data['source'].split()[0]  
        instance.source = self.cleaned_data['source'] 
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance


class ExpenseForm(forms.ModelForm):
    EXPENSE_CATEGORIES = [
        ('🍕 Food', '🍕 Food'),
        ('🚗 Transportation', '🚗 Transportation'),
        ('💡 Utilities', '💡 Utilities'),
        ('🏠 Rent', '🏠 Rent'),
        ('🛍 Shopping', '🛍 Shopping'),
        ('🎬 Entertainment', '🎬 Entertainment'),
        ('⚕ Healthcare', '⚕ Healthcare'),
        ('📚 Education', '📚 Education'),
        ('📦 Other', '📦 Other')
    ]
    
    category = forms.ChoiceField(choices=EXPENSE_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))
    
    class Meta:
        model = Expense
        fields = ['category', 'amount']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.emoji = self.cleaned_data['category'].split()[0]  # Extract emoji
        instance.category = self.cleaned_data['category']  # Store full text (emoji + name)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance