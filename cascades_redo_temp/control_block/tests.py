from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield pages.BlockStart

        if self.round_number == 2:
            yield pages.ScoreReveal

        yield Submission(pages.PreDecision, dict(Red_pre1=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PostDecision, dict(Red_post1=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PreDecision, dict(Red_pre2=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PostDecision, dict(Red_post2=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PreDecision, dict(Red_pre3=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PostDecision, dict(Red_post3=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PreDecision, dict(Red_pre4=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PostDecision, dict(Red_post4=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PreDecision, dict(Red_pre5=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PostDecision, dict(Red_post5=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PreDecision, dict(Red_pre6=random.randint(0, 100)), check_html=False)
        yield Submission(pages.PostDecision, dict(Red_post6=random.randint(0, 100)), check_html=False)

        if self.round_number == 2:
            yield pages.DecisionPayoff
            yield pages.BlockEnd
