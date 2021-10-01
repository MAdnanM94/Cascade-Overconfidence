from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.PaymentInfo, dict(
            name='botttt',
            venmo='b0t@2',
            phone='1234'
        )
        yield pages.End
