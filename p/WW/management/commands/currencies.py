from django.core.management.base import BaseCommand
from WW.models import Currency

class Command(BaseCommand):
    help = 'Populates the database with currency data'

    def handle(self, *args, **options):
        currencies = [
            ('USD', 'United States Dollar', '$'),
            ('EUR', 'Euro', '€'),
            ('GBP', 'British Pound', '£'),
            ('INR', 'Indian Rupee', '₹'),
            ('AUD', 'Australian Dollar', 'A$'),
            ('CAD', 'Canadian Dollar', 'C$'),
            ('SGD', 'Singapore Dollar', 'S$'),
            ('MYR', 'Malaysian Ringgit', 'RM'),
            ('JPY', 'Japanese Yen', '¥'),
            ('CNY', 'Chinese Yuan', '¥'),
            ('HKD', 'Hong Kong Dollar', 'HK$'),
            ('NZD', 'New Zealand Dollar', 'NZ$'),
            ('SEK', 'Swedish Krona', 'kr'),
            ('NOK', 'Norwegian Krone', 'kr'),
            ('CHF', 'Swiss Franc', 'CHF'),
            ('DKK', 'Danish Krone', 'kr'),
            ('RUB', 'Russian Ruble', '₽'),
            ('ZAR', 'South African Rand', 'R'),
            ('BRL', 'Brazilian Real', 'R$'),
            ('TRY', 'Turkish Lira', '₺'),
            ('KRW', 'South Korean Won', '₩'),
            ('AED', 'UAE Dirham', 'د.إ'),
            ('SAR', 'Saudi Riyal', 'ر.س'),
            ('QAR', 'Qatari Riyal', 'ر.ق'),
            ('KWD', 'Kuwaiti Dinar', 'د.ك'),
            ('OMR', 'Omani Rial', 'ر.ع.'),
            ('BHD', 'Bahraini Dinar', 'ب.د'),
            ('JOD', 'Jordanian Dinar', 'د.ا'),
            ('EGP', 'Egyptian Pound', 'ج.م'),
            ('THB', 'Thai Baht', '฿'),
            ('IDR', 'Indonesian Rupiah', 'Rp'),
            ('PHP', 'Philippine Peso', '₱'),
            ('PKR', 'Pakistani Rupee', '₨'),
            ('LKR', 'Sri Lankan Rupee', 'Rs'),
            ('BDT', 'Bangladeshi Taka', '৳'),
            ('NPR', 'Nepalese Rupee', 'रू'),
            ('MMK', 'Myanmar Kyat', 'K'),
            ('VND', 'Vietnamese Dong', '₫'),
            ('KHR', 'Cambodian Riel', '៛'),
            ('KZT', 'Kazakhstani Tenge', '₸'),
            ('UZS', 'Uzbekistani Som', 'лв'),
            ('TJS', 'Tajikistani Somoni', 'ЅМ'),
        ]

        for code, name, symbol in currencies:
            Currency.objects.get_or_create(code=code, defaults={'name': name, 'symbol': symbol})

        self.stdout.write(self.style.SUCCESS('Successfully added currencies.'))