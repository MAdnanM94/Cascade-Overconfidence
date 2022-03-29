from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class FinalPayoff(WaitPage):
    after_all_players_arrive = 'final_payoffs'


class Payment(Page):
    pass


class Demographics(Page):
    form_model = 'player'
    form_fields=['age', 'gender', 'major', 'educ_year', 'past_experiments', 'game_theory', 'experiment']


page_sequence = [FinalPayoff, Payment, Demographics]
