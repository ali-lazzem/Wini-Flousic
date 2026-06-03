import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from transactions.models import Transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Import old transaction data from transactions.json and finance.json (Tunisian dialect support)'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Existing username to assign transactions to')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return

        self.import_transactions_json(user)
        self.import_finance_json(user)

        self.stdout.write(self.style.SUCCESS('Import completed.'))

    # -------------------- transactions.json --------------------
    def import_transactions_json(self, user):
        try:
            with open('transactions.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.WARNING('transactions.json not found, skipping.'))
            return

        transactions = data.get('transactions', [])
        created = 0
        skipped = 0

        for item in transactions:
            amount = float(item.get('amount', 0))
            if amount <= 0:
                continue

            category = item.get('category', 'others')
            description = item.get('description', '')
            date_str = item.get('date', '')
            try:
                trans_date = datetime.fromisoformat(date_str).date()
            except (ValueError, TypeError):
                self.stderr.write(f"Skipping invalid date: {date_str}")
                skipped += 1
                continue

            # Avoid duplicates
            if Transaction.objects.filter(
                user=user, date=trans_date, amount=amount,
                category=category, description=description
            ).exists():
                skipped += 1
                continue

            Transaction.objects.create(
                user=user,
                type='expense',
                amount=amount,
                category=category,
                description=description,
                date=trans_date,
                payment_method='cash'   # default, old data didn't specify
            )
            created += 1

        self.stdout.write(f'transactions.json: {created} created, {skipped} skipped.')

    # -------------------- finance.json --------------------
    def import_finance_json(self, user):
        try:
            with open('finance.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.WARNING('finance.json not found, skipping.'))
            return

        transactions = data.get('transactions', [])
        created = 0
        skipped = 0

        # Tunisian -> English category mapping
        tunisian_map = {
            # Drinks
            'cofe': 'drinks',
            'gazouza': 'drinks',
            'the': 'drinks',
            'capu': 'drinks',
            'cafe': 'drinks',
            'chay': 'drinks',
            'lben': 'drinks',
            # Food
            'malfouf': 'food',
            'makloub': 'food',
            'mlewi': 'food',
            'fricace': 'food',
            'chapati': 'food',
            'sandwich': 'food',
            'pizza': 'food',
            'mlawi': 'food',
            'frite': 'food',
            'kaskrout': 'food',
            # Snacks
            'zare3a': 'snacks',
            'choklata': 'snacks',
            'biscuit': 'snacks',
            'batata': 'snacks',
            'cacahuetes': 'snacks',
            # Transport
            'metro': 'transport',
            'louage': 'transport',
            'taxi': 'transport',
            'train': 'transport',
            'carhba': 'transport',
            'essence': 'transport',
            # Fun / outings
            'da3ou': 'fun',
            'date': 'fun',
            'cinema': 'fun',
            'sortie': 'fun',
            # University
            'hacathon': 'university',
            'bootcamp': 'university',
            'membership': 'university',
            'inscription': 'university',
            'cours': 'university',
            # Groceries
            'baguette': 'groceries',
            'eggs': 'groceries',
            'jbin': 'groceries',
            'pates': 'groceries',
            'riz': 'groceries',
            'lait': 'groceries',
            'tomate': 'groceries',
            'oignon': 'groceries',
            # Others
            '5 ticket resto': 'food',
            'masrouf': 'income',  # special: treated as income
            'rja3': 'income',
        }

        for item in transactions:
            amount = float(item.get('amount', 0))
            if amount == 0:
                continue

            trans_type = 'expense' if amount < 0 else 'income'
            absolute_amount = abs(amount)

            description = item.get('description', '').lower()
            # Map account to payment_method
            account = item.get('account', 'cash')
            payment_method = 'cash' if account == 'cash' else 'bank'

            timestamp_str = item.get('timestamp', '')
            try:
                trans_date = datetime.fromisoformat(timestamp_str).date()
            except (ValueError, TypeError):
                self.stderr.write(f"Skipping invalid timestamp: {timestamp_str}")
                skipped += 1
                continue

            # Determine category based on Tunisian keywords
            category = 'others'   # default
            if trans_type == 'income':
                category = 'income'   # but Transaction model does not have category for income; we'll set to None
                # For income, category is not used in the model – we can leave blank.
                pass
            else:
                # Search for known keywords in description
                found = False
                for keyword, cat in tunisian_map.items():
                    if keyword in description:
                        if cat == 'income':
                            # If we accidentally map an expense to income, ignore this mapping
                            continue
                        category = cat
                        found = True
                        break
                # If not found, keep 'others'

            # Skip duplicates: use a combination of fields
            if Transaction.objects.filter(
                user=user,
                date=trans_date,
                amount=absolute_amount,
                type=trans_type,
                payment_method=payment_method
            ).exists():
                skipped += 1
                continue

            # For income, category should be None (or empty string)
            if trans_type == 'income':
                category = None

            Transaction.objects.create(
                user=user,
                type=trans_type,
                amount=absolute_amount,
                category=category,
                description=description,
                date=trans_date,
                payment_method=payment_method
            )
            created += 1

        self.stdout.write(f'finance.json: {created} created, {skipped} skipped.')