from django.conf import settings


PAYMENT_METHOD = (
    ('stripe', 'Stripe'),
    ('check', 'Check'),
    ('non-cash', 'Non cash')
)

APP_NAME = settings.APP_NAME
FROM_TO = (
    (f'client-to-{APP_NAME}', f'Client to {APP_NAME}'),
    (f'{APP_NAME}-to-client', f'{APP_NAME} to Client'),
    (f'{APP_NAME}-to-agent', f'{APP_NAME} to Agent')
)
