import time
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.core.mail import send_mail
from WW.models import Bill, User  

class Command(BaseCommand):
    help = "Send email reminders for due bills"

    def handle(self, *args, **kwargs):
        today = now().date()
        users = User.objects.all()

        for user in users:
            bills = Bill.objects.filter(user=user, is_paid=False)

            for bill in bills:
                days_left = (bill.due_date - today).days

                if days_left in [5, 2, 1]: 
                    message = f"""
                    Dear {user.name},
                    This is a reminder that your bill "{bill.bill_name}"amounting to {user.currency.symbol} {bill.amount} is due in {days_left} day(s) on {bill.due_date}.
                    We kindly request you to make the payment by the due date to avoid any late fees or service interruptions.
                    Thank you for your prompt attention to this matter.
                    Best regards,
                    The Wealth-Wise Team
                    """

                    try:
                        send_mail(
                            'Bill Payment Reminder',
                            message,
                            'wealthwise200@gmail.com',
                            [user.email],
                            fail_silently=False,
                        )
                        print(f"✅ Email sent to {user.email} for bill '{bill.bill_name}'.")
                    except Exception as e:
                        print(f"❌ Failed to send email to {user.email}: {e}")

        self.stdout.write("✅ Bill reminders process completed!")