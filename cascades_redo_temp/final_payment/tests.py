from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Payment
        yield pages.Demographics, dict(
            age=1,
            gender=1,
            major='blah',
            educ_year=1,
            past_experiments=False,
            game_theory=True,
            experiment=False
        )
