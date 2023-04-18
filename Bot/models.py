from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

SUBSCRIPTION_CHOICES = [
    ('Free', 'Free'),
    # ('Basic', 'Basic'),
    # ('Standard', 'Standard'),
    ('VIP', 'VIP'),
]

LANGUAGE_CHOICES = [
    ('ru', 'ru'),
    ('en', 'en'),
]

BINANCE = 'Binance'
BYBIT = 'Bybit'
not_con = 'Not_connect'

EXCHANGE_CHOICES = [
    (not_con, 'Not_connect'),
    (BINANCE, 'Binance'),
    (BYBIT, 'Bybit'),
]


# class UserFollowing(models.Model):
#     trader_f = models.ForeignKey('Traders', on_delete=models.CASCADE)
#     user_f = models.ForeignKey('Users', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.trader_f}/{self.user_f}'


class Traders(models.Model):
    name = models.CharField(max_length=35, verbose_name='Name')
    link = models.CharField(max_length=255, verbose_name='LINK TO PROFILE')
    is_active = models.BooleanField(default=True,
                                    verbose_name='Active',
                                    help_text='If the check box is active, the trader"s trades are copied ')

    def __str__(self):
        return self.name


class Users(models.Model):
    user_name = models.CharField(max_length=25, verbose_name='Name User')
    user_id = models.CharField(max_length=30, verbose_name='User ID in Telegram', unique=True)

    # balance = models.FloatField(default=0, verbose_name='User balance {cashback}')
    subs_date_end = models.DateField(null=True, verbose_name='Subscription end', blank=True)
    subs_active = models.BooleanField(default=False,
                                      verbose_name='If the subscription is active then true if not false')
    leverage = models.PositiveIntegerField(verbose_name='default leverage', default=10)

    percent_balance = models.PositiveIntegerField(
        verbose_name='Percent allocated for order',
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ]
    )

    # referral = models.ForeignKey('Users', on_delete=models.CASCADE, blank=True, default=None, null=True)

    api_key = models.CharField(max_length=350, verbose_name='Exchange api key', blank=True)
    api_secret = models.CharField(max_length=350, verbose_name='Exchange api secret', blank=True)
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en',
        verbose_name='language'
    )
    subscription_type = models.CharField(
        max_length=25,
        choices=SUBSCRIPTION_CHOICES,
        default='Free',
        verbose_name='Subscription type'
    )
    exchange = models.CharField(
        max_length=25,
        choices=EXCHANGE_CHOICES,
        default=not_con,
        verbose_name='Exchange'
    )

    def __str__(self):
        return self.user_name


class Admin(models.Model):
    user_name = models.CharField(max_length=30, verbose_name='Name', blank=True, default='Admin')
    user_id = models.CharField(max_length=30, verbose_name='User or Channel ID in Telegram', unique=True)
    subs_active = models.BooleanField(default=True, verbose_name='Active', help_text='If user admin true/else false')
    leverage = models.PositiveIntegerField(verbose_name='Admin default leverage', default=10)

    percent_balance = models.PositiveIntegerField(
        verbose_name='Percent allocated for order',
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ]
    )
    api_key = models.CharField(max_length=265, verbose_name='api_key', blank=True)
    api_secret = models.CharField(max_length=265, verbose_name='api_secret', blank=True)
    bot_token = models.CharField(max_length=255, verbose_name='Token bot telegram')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admins'


class Signal(models.Model):
    name_trader = models.ForeignKey('Traders', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=15, verbose_name='Symbol')
    side = models.CharField(max_length=55, verbose_name='SIDE', default='none')
    size = models.CharField(max_length=55, verbose_name='Size')
    entry_price = models.CharField(max_length=55, verbose_name='Entry Price')
    mark_price = models.CharField(max_length=55, verbose_name='Mark Price')
    pnl = models.CharField(max_length=55, verbose_name='PNL (ROE %)')
    roe = models.CharField(max_length=55, verbose_name='ROE')
    date = models.CharField(max_length=55, verbose_name='TIME')
    is_active = models.BooleanField(default=True)
    upd = models.CharField(max_length=86, verbose_name='Update time order')
    status = models.BooleanField(default=False)
    message = models.CharField(max_length=3000, verbose_name='Message')

    def __str__(self):
        return self.name_trader.name + '/' + self.symbol
