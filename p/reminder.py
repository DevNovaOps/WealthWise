import time
import django
import os
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from WW.models import Bill

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "p.settings")  
django.setup()

def bill_reminder_service():
    User = get_user_model()
    while True:
        today = now().date()
        users = User.objects.all()

        for user in users:
            bills = Bill.objects.filter(user=user, is_paid=False)

            for bill in bills:
                days_left = (bill.due_date - today).days

                if days_left in [5, 2, 1]: 
                    message = f"""
                    Dear {user.username},

                    This is a reminder that your bill "{bill.bill_name}" of ${bill.amount} is due in {days_left} day(s) on {bill.due_date}.

                    Please make the payment on time to avoid any penalties.

                    Regards,
                    Wealth-Wise Team
                    """

                    send_mail(
                        'Bill Payment Reminder',
                        message,
                        'wealthwise200@gmail.com',
                        [user.email],
                        fail_silently=False,
                    )
        print("Checked for bill reminders. Sleeping for 24 hours...")
        time.sleep(86400)  
        
if __name__ == "__main__":
    bill_reminder_service()