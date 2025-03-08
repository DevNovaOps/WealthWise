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
from random import choice


def home(request):
    return render(request, 'WW/home.html')

def security(request):
    return render(request,'WW/security.html')

def terms(request):
    return render(request,'WW/terms.html')

def privacy(request):
    return render(request,'WW/privacy.html')

def faq(request):
    return render(request, 'WW/FAQ.html')

def support(request):
    return render(request,'WW/support.html')

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
    progress_percentage = (savings / total_amount) * 100 if total_amount > 0 else 0

    pending_amount = total_amount - completed_amount
    if savings >= total_amount:
        goals.delete()
        messages.success(request, "All goals achieved! Your goals have been cleared.")

    if request.method == 'POST':
        form = goalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = user
            goal.save()
            
            message = f'Dear user, your new goal "{goal.goal_name}" of {goal.amount} has been added successfully!\n\nGoal Details:\n- Goal Name: {goal.goal_name}\n- Amount: {goal.amount}\n- Due Date: {goal.due_date}'
            
            send_mail(
                'Your New Goal',
                message,
                'wealthwise200@gmail.com',
                [user.email],
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
        'progress_percentage':progress_percentage,
        'savings': savings,
        'all_goals_achieved': savings >= total_amount
    }
    
    return render(request, 'WW/G.html', context)


def m_g(request, goal_id):
    """ Mark goal as achieved """
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    goal = get_object_or_404(Goal, id=goal_id, user=user)
    
    goal.is_done = True
    goal.save()

    message = f'Dear user, congratulations on achieving your goal "{goal.goal_name}" of {goal.amount}!\nWe have marked this goal as completed.'
    send_mail(
        'Goal Achieved',
        message,
        'wealthwise200@gmail.com',
        [user.email],
        fail_silently=False,
    )

    return redirect('g1')


def d_g(request, goal_id):
    """ Delete a goal """
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    goal = get_object_or_404(Goal, id=goal_id, user=user)
    goal.delete()
    return redirect('g1')

def check_goal_progress(request):
    """ Check goal progress and send motivational emails """
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "You must be logged in.")
        return redirect('signup')

    user = User.objects.get(id=user_id)
    goals = Goal.objects.filter(user=user, is_done=True)
    total_amount = sum(goal.amount for goal in Goal.objects.filter(user=user))
    total_income = sum(income.amount for income in Income.objects.filter(user=user))
    total_expense = sum(expense.amount for expense in Expense.objects.filter(user=user))
    savings = total_income - total_expense  


    if total_amount == 0:
        messages.error(request, "No financial goals found.")
        return redirect('g1')

    progress_percentage = (savings/ total_amount) * 100
    
    if progress_percentage < 25:
        motivation = "You're off to a great start! Keep pushing towards your financial goals. Every small step counts!"
    elif progress_percentage < 50:
        motivation = "You're making good progress! Stay consistent, and you'll achieve your goals soon."
    elif progress_percentage < 75:
        motivation = "You're over halfway there! Keep saving and investing wisely."
    elif progress_percentage < 100:
        motivation = "Almost there! Stay focused, and soon you'll reach your financial target."
    else:
        motivation = "Congratulations! You've successfully achieved your goal. Time to set new financial milestones!"

    message = f"Dear {user.name},\n\nYou have completed {progress_percentage:.2f}% of your financial goal. {motivation}\n\nKeep up the good work!\n\nBest,\nWealth-Wise Team"

    send_mail(
        'Goal Progress Update',
        message,
        'wealthwise200@gmail.com',
        [user.email],
        fail_silently=False,
    )

    messages.success(request, f'Email sent for achieving {progress_percentage:.2f}% of your goal.')

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
        completed_amount = sum(goal.amount for goal in Goal.objects.filter(user=user, is_done=True))
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
            'pie_chart': pie_chart,
        })