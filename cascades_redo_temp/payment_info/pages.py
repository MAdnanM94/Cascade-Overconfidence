from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class PaymentInfo(Page):
    form_model = 'player'
    form_fields = ['name', 'email', 'phone']

    def before_next_page(self):
        self.player.payment = round(float(self.participant.payoff_plus_participation_fee()), 2)


class End(Page):
    pass


page_sequence = [PaymentInfo, End]
