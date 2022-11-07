from django.core.mail import send_mail

from .models import Profile


def send():
    users = Profile.objects.prefetch_related('transaction').only('email')
    for user in users:
        statistics = {}
        transactions = user.transaction.filter(user=user.id)
        for transaction in transactions:
            statistics[transaction.id] = [transaction.summa, transaction.action]
        send_mail(
            'Statistics',
            f'There were {len(transactions)} transactions: {statistics}',
            'some_mail',
            [user.email]
        )
