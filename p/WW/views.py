from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail 
from django.contrib import messages
from .forms import SignupForm, LoginForm, ForgotPasswordForm, IncomeForm, ExpenseForm,billForm,goalForm
from .models import User, Income, Expense,Bill,Goal
from django.urls import reverse
import re
import plotly.graph_objs as go
import plotly.io as pio


def home(request):
    return render(request, 'WW/home.html')

def faq(request):
    return render(request, 'WW/FAQ.html')

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
                        return redirect('home')
                    else:
                        login_form.add_error('password', 'Incorrect password.')
                except User.DoesNotExist:
                    login_form.add_error('email', 'User does not exist.')
            else:
                for field in login_form.errors:
                    messages.error(request, f"{field}: {login_form.errors[field]}")

        elif 'signup' in request.POST:
            signup_form = SignupForm(request.POST)
            if signup_form.is_valid():
                password = signup_form.cleaned_data['password']
                if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
                    signup_form.add_error('password', 'Password must be at least 8 characters long, contain one uppercase letter, one lowercase letter, one number, and one special character.')
                    return render(request,'WW/error.html')
                else:
                    user = signup_form.save(commit=False)
                    user.password = make_password(password)
                    user.save()
                    messages.success(request, "Account created successfully. Please log in.")
                    return redirect('home')
            else:
                for field in signup_form.errors:
                    messages.error(request, f"{field}: {signup_form.errors[field]}")

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
    
  
    selected_month = request.POST.get('month', 'January')
    return redirect(reverse('i1') + f'?month={selected_month}')

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
    
    selected_month = request.POST.get('month', 'January')
    return redirect(reverse('i1') + f'?month={selected_month}')

def logout(request):
    if request.session.get('user_id'):
        del request.session['user_id']
        messages.success(request, 'You have been logged out.')  
    return redirect('home')

def g1(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('signup')
    goals = Goal.objects.filter(user=user)
    total_goals = goals.count()
    total_amount = sum(goal.amount for goal in goals)
    completed_amount = sum(goal.amount for goal in goals if goal.is_done)
    total_income = sum(income.amount for income in Income.objects.filter(user=user))
    total_expense = sum(expense.amount for expense in Expense.objects.filter(user=user))
    savings = total_income - total_expense  

    pending_amount = total_amount - completed_amount
    if request.method == 'POST':
        form = goalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user
            goal.save()
            email = goal.user.email
            user = User.objects.get(email=email)
            user.save()
            message = f'Dear user, your new goal {goal.goal_name} of {goal.amount} has been added successfully!\n\nBelow are the goal details:\n\nGoal Name: {goal.goal_name}\nAmount: {goal.amount}\nDue Date: {goal.due_date}\n'
            send_mail(
                    'Your New Goal',
                    message,
                    'wealthwise200@gmail.com',
                    [email],
                    fail_silently=False,
                )
            return redirect('g1')  
    else:
        form = goalForm()  
    context = {
        'user': user,
        'currency': user.currency,
        'goals': goals,
        'goal_form': form,
        'total_goals': total_goals,
        'total_amount': total_amount,
        'completed_amount': completed_amount,
        'pending_amount': pending_amount,
        'savings': savings,
    }
    return render(request, 'WW/G.html', context)
    
def m_g(request, goal_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    goal = get_object_or_404(Goal, id=goal_id, user=user)
    goal.is_done = True
    goal.save()
    email = goal.user.email
    message = f'Dear user, congratulations on achieving your goal {goal.goal_name} of {goal.amount}! \n\nKindly note that we are closing the goal from our side.'
    send_mail(
        'Goal Achieved',
        message,
        'wealthwise200@gmail.com',
        [email],
        fail_silently=False,
    )
    return redirect('g1')

def d_g(request, goal_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    goal = get_object_or_404(Goal, id=goal_id, user=user)
    goal.delete()
    return redirect('g1')

def lock_goals(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')
    user = User.objects.get(id=user_id)
    goals = Goal.objects.filter(user=user, is_done=False)
    total_amount = sum(goal.amount for goal in goals)
    request.session['locked_amount'] = float(total_amount)
    messages.success(request, f'Goals locked with a total amount of ${total_amount}.')
    return redirect('g1')

def check_goal_progress(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')

    user = User.objects.get(id=user_id)
    completed_amount = sum(goal.amount for goal in Goal.objects.filter(user=user, is_done=True))
    
    total_income = sum(income.amount for income in Income.objects.filter(user=user))
    total_expense = sum(expense.amount for expense in Expense.objects.filter(user=user))
    savings = total_income - total_expense

    if savings >= 0.5 * completed_amount:
        email = user.email
        message = f'''
        🎉 Congratulations {user.name}! 🎉  

        You have successfully saved {user.currency.symbol}{completed_amount}, which is 50% of your goal! Keep going strong!  

        Every step brings you closer to financial freedom. 🚀  

        Regards,  
        Wealth-Wise Team
        '''
        send_mail(
            '50% Goal Achieved 🎯',
            message,
            'wealthwise200@gmail.com',
            [email],
            fail_silently=False,
        )
        messages.success(request, 'Motivational email sent for achieving 50% of the goal.')
    
    return redirect('g1')
    
def b1(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')
    user = User.objects.get(id=user_id)
    bills = Bill.objects.filter(user=user)
    total_bills = bills.count()
    total_amount = sum(bill.amount for bill in bills)
    paid_amount = sum(bill.amount for bill in bills if bill.is_paid)
    pending_amount = total_amount - paid_amount
    form = billForm()
    return render(request, 'WW/b1.html', {
        'user': user,
        'currency': user.currency,
        'bill_form': form,
        'bills': bills,
        'total_bills': total_bills,
        'total_amount':  sum(bill.amount for bill in bills),
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
    })

def add_bill(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = billForm(request.POST) 
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = user
            bill.save()
            messages.success(request, 'Bill added successfully!')
            return redirect('b1')
    return redirect('b1')

def delete_bill(request, bill_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')
    user = User.objects.get(id=user_id)
    bill = get_object_or_404(Bill, id=bill_id, user=user)
    bill.delete()
    return redirect('b1')

def mark_bill(request, bill_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')
    user = User.objects.get(id=user_id)
    bill = get_object_or_404(Bill, id=bill_id, user=user)
    if request.method == 'GET':
        # is_paid = request.GET.get('is_paid', True)
        
        # # Update the bill's paid status
        # bill.is_paid = is_paid
        # bill.save()
        
        # Recalculate the paid amount
        bills = Bill.objects.filter(user=user)
        bill.is_paid = True
        paid_amount = sum(bill.amount for bill in bills if bill.is_paid)
        total_amount = sum(bill.amount for bill in bills)
        pending_amount = total_amount - paid_amount
        bill.save()
        return redirect('b1')
    

def report(request):
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "You must be logged in.")
            return redirect('signup')

        user = User.objects.get(id=user_id)
        currency = getattr(user, 'currency', 'USD')

        incomes = Income.objects.filter(user=user)
        expenses = Expense.objects.filter(user=user)

        total_income = sum(income.amount for income in incomes)
        total_expense = sum(expense.amount for expense in expenses)
        savings = total_income - total_expense

        months = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
        income_values = [sum(i.amount for i in incomes if i.month == month) for month in months]
        expense_values = [sum(e.amount for e in expenses if e.month == month) for month in months]

        # 📊 Generate Graphs
        bar_graph = pio.to_json({
            "data": [
                go.Bar(x=months, y=income_values, name="Income", marker=dict(color="green")),
                go.Bar(x=months, y=expense_values, name="Expenses", marker=dict(color="red"))
            ],
            "layout": go.Layout(title="Monthly Income vs Expenses", barmode="group")
        })

        line_graph = pio.to_json({
            "data": [
                go.Scatter(x=months, y=income_values, mode="lines+markers", name="Income", line=dict(color="green")),
                go.Scatter(x=months, y=expense_values, mode="lines+markers", name="Expenses", line=dict(color="red"))
            ],
            "layout": go.Layout(title="Income & Expense Trends")
        })

        categories = list(set(expense.category for expense in expenses))
        category_values = [sum(e.amount for e in expenses if e.category == category) for category in categories]

        pie_chart = pio.to_json({
            "data": [go.Pie(labels=categories, values=category_values, hole=0.4)],
            "layout": go.Layout(title="Yearly Expense Breakdown by Category")
        })

        return render(request, 'WW/report.html', {
            'user': user,
            'currency': currency,
            'total_income': total_income,
            'total_expense': total_expense,
            'savings': savings,
            'bar_graph': bar_graph,
            'line_graph': line_graph,
            'pie_chart': pie_chart
        })