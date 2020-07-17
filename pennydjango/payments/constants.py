from django.conf import settings


PAYMENT_METHOD = (
    ('payment_processor', 'Payment Processor'),
    ('check', 'Check'),
    ('non-cash', 'Non cash'),
    ('bank', 'Bank'),
    ('cash', 'Cash')
)
DEFAULT_PAYMENT_METHOD = 'payment_processor'
BANK_TRANSFER = 'bank'

APP_NAME = settings.APP_NAME

CLIENT_TO_APP = f'client-to-{APP_NAME}'
APP_TO_CLIENT = f'{APP_NAME}-to-client'
APP_TO_AGENT = f'{APP_NAME}-to-agent'
OWNER_PAYOUT = 'owner_payout'
FROM_TO = (
    (CLIENT_TO_APP, f'Client to {APP_NAME}'),
    (APP_TO_CLIENT, f'{APP_NAME} to Client'),
    (APP_TO_AGENT, f'{APP_NAME} to Agent'),
    (OWNER_PAYOUT, 'Owner Payout')
)
MANUAL_TRANSACTION_CHOICES = (
    (CLIENT_TO_APP, f'Client to {APP_NAME}'),
    (APP_TO_CLIENT, f'{APP_NAME} to Client'),
    (OWNER_PAYOUT, 'Owner Payout')
)

# Transaction Status
FAILED = 'failed'
APPROVED = 'approved'
PENDING = 'pending'
TRANSACTION_STATUS = (
    (FAILED, 'failed'),
    (APPROVED, 'Approved'),
    (PENDING, 'Pending')
)
