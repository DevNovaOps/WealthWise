from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail 
from django.contrib import messages
from .forms import SignupForm, LoginForm, ForgotPasswordForm, IncomeForm, ExpenseForm
from .models import User, Income, Expense

def home(request):
    return render(request, 'WW/home.html')

def signup(request):
    if request.session.get('user_id'): 
        messages.info(request, 'You are already logged in.')
        return redirect('home')
    login_form = LoginForm()
    signup_form = SignupForm()

    if request.method == 'POST':
        if 'login' in request.POST: 
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                try:
                    user = User.objects.get(email=email)
                  
                    if check_password(password, user.password):
                        request.session['user_id'] = user.id 
                        return redirect('signup') 
                    else:
                        login_form.add_error('password', 'Incorrect password.')
                except User.DoesNotExist:
                    login_form.add_error('email', 'User does not exist.')

        elif 'signup' in request.POST: 
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.password = make_password(signup_form.cleaned_data['password'])
                user.save()
                messages.success(request, "Account created successfully. Please log in.")
                return redirect('signup')  

    return render(request, 'WW/signup.html', {
        'login_form': login_form,
        'signup_form': signup_form,
    })

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                new_password = form.cleaned_data['password']
                user.password = make_password(new_password)
                user.save()
                send_mail(
                    'Your New Password',
                    f'Your new password is: {new_password}',
                    'wealthwise200@gmail.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'A new password has been sent to your email.')
                return redirect('signup')
            except User.DoesNotExist:
                form.add_error('email', 'User does not exist.')
    else:
        form = ForgotPasswordForm()

    return render(request, 'WW/forgot-password.html', {'forgot_password_form': form})

def i1(request):  
    user_id = request.session.get('user_id')  
    if not user_id:  
        messages.error(request, "You must be logged in.")  
        return redirect('signup') 
    
    user = User.objects.get(id=user_id)  
    selected_month = request.GET.get('month', 'January') 

    incomes = Income.objects.filter(user=user, month=selected_month)
    expenses = Expense.objects.filter(user=user, month=selected_month)

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    savings = total_income - total_expense

    total_expense_percentage = (total_expense / total_income * 100) if total_income else 0
    savings_percentage = (savings / total_income * 100) if total_income else 0

    return render(request, 'WW/i1.html', {
        'user': user,
        'selected_month': selected_month,
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
        'total_expense_percentage': total_expense_percentage,
        'savings_percentage': savings_percentage,
        'income_form': IncomeForm(),
        'expense_form': ExpenseForm(),
    })


def add_income(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')

    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = user
            income.month = request.POST.get('month', 'January')  
            income.save()
            messages.success(request, 'Income added successfully!')
        else:
            messages.error(request, 'Please correct the errors.')
    return redirect('i1')


def add_expense(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = user
            expense.month = request.POST.get('month', 'January') 
            expense.save()
            messages.success(request, 'Expense added successfully!')
        else:
            messages.error(request, 'Please correct the errors.')
    return redirect('i1')

def logout(request):
    if request.session.get('user_id'):
        del request.session['user_id']
        messages.success(request, 'You have been logged out.')  
    return redirect('home')

def G(request):
    return render(request, 'WW/G.html')