from django import forms
from .models import User, Income, Expense,Currency,Bill,Goal

class SignupForm(forms.ModelForm):
    currency = forms.ModelChoiceField(
        queryset=Currency.objects.all(),
        empty_label='Select Currency',
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'style': (
                'background: #121212; '
                'color: #00ff41; '
                'border: 1px solid #00ff41; '
                'border-radius: 5px; '
                'box-shadow: 0 0 15px rgba(0, 255, 65, 0.2); '
                'scrollbar-width: thin; '
                'scrollbar-color: #00ff41 #000000; '
            ) 
           } )
            
        )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'password1', 'placeholder': 'Enter Password'}))
    class Meta:
        model = User
        fields = ['name', 'email', 'password','currency']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter OTP'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

class IncomeForm(forms.ModelForm):
    INCOME_CATEGORIES = [
        ('💰 Salary', '💰 Salary'),
        ('💼 Business', '💼 Business'),
        ('💻 Freelance', '💻 Freelance'),
        ('📈 Investments', '📈 Investments'),
        ('🏠 Rental', '🏠 Rental'),
        ('🎁 Other', '🎁 Other'),
    ]
    
    source = forms.ChoiceField(choices=INCOME_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control'}))
    other_source = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter source if "Other" selected'})
    )
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))

    class Meta:
        model = Income
        fields = ['source', 'amount']

    def clean_source(self):
        """ Ensure 'Other' source has a valid name entered """
        source = self.cleaned_data.get('source')
        other_source = self.cleaned_data.get('other_source')
        if source == "🎁 Other" and not other_source:
            raise forms.ValidationError("Please provide a source name for 'Other'.")
        return other_source if source == "🎁 Other" else source

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

    category = forms.ChoiceField(choices=EXPENSE_CATEGORIES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'category-select'}))
    other_category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter other category', 'id': 'other-category-input'}), required=False)
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}))

    class Meta:
        model = Expense
        fields = ['category', 'other_category', 'amount']

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        other_category = cleaned_data.get('other_category')

        if category == '📦 Other' and not other_category:
            self.add_error('other_category', 'This field is required when "Other" is selected.')

        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        category = self.cleaned_data['category']
        other_category = self.cleaned_data['other_category']

        if category == '📦 Other':
            instance.emoji = '📦'
            instance.category = other_category
        else:
            instance.emoji = category.split()[0]
            instance.category = category

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