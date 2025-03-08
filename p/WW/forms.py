from django import forms
from .models import User, Income, Expense,Currency,Bill,Goal

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
        ('✈ Travel', '✈ Travel'),
        ('🐾 Pets', '🐾 Pets'),
        ('🎁 Gifts', '🎁 Gifts'),
        ('💼 Business', '💼 Business'),
        ('🏦 Savings', '🏦 Savings'),
        ('🍽 Dining Out', '🍽 Dining Out'),
        ('🏋 Fitness', '🏋 Fitness'),
        ('🛠 Home Improvement', '🛠 Home Improvement'),
        ('🎨 Hobbies', '🎨 Hobbies'),
        ('🍼 Childcare', '🍼 Childcare'),
        ('💻 Subscriptions', '💻 Subscriptions'),
        ('🚿 Personal Care', '🚿 Personal Care'),
        ('🎓 Student Loans', '🎓 Student Loans'),
        ('🚑 Insurance', '🚑 Insurance'),
        ('💳 Credit Card Payments', '💳 Credit Card Payments'),
        ('🏖 Vacation', '🏖 Vacation'),
        ('📱 Mobile Phone', '📱 Mobile Phone'),
        ('💼 Professional Services', '💼 Professional Services'),
        ('🎉 Parties', '🎉 Parties'),
        ('🚰 Water', '🚰 Water'),
        ('🔌 Electricity', '🔌 Electricity'),
        ('📦 Other', '📦 Other')
    ]
    category = forms.ChoiceField(choices=EXPENSE_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))
    
    class Meta:
        model = Expense
        fields = ['category', 'amount']

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.emoji = self.cleaned_data['category'].split()[0]
        instance.category = self.cleaned_data['category']  
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
    
class billForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['bill_name', 'amount', 'due_date', 'is_paid']
        
class goalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal_name', 'amount', 'due_date', 'is_done']