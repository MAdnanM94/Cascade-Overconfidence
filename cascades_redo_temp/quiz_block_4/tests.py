from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield pages.BlockStart
            yield pages.Q1, dict(Q1='titanic')
            yield pages.Q2, dict(Q2='disney')
            yield pages.Q3, dict(Q3='beatles')
            yield pages.Q4, dict(Q4='madonna')
            yield pages.Q5, dict(Q5='2019')
            yield pages.Q6, dict(Q6='quentin tarantino')
            yield pages.Q7, dict(Q7='halle berry')
            yield pages.Q8, dict(Q8='elvis')
            yield pages.Q9, dict(Q9='mtv')
            yield pages.Q10, dict(Q10='1')

        if self.round_number == 2:
            yield pages.ScoreReveal

        if self.round_number == 1:
            yield pages.OwnScore, dict(
                own_score0=100,
                own_score1=0,
                own_score2=0,
                own_score3=0,
                own_score4=0,
                own_score5=0,
                own_score6=0,
                own_score7=0,
                own_score8=0,
                own_score9=0,
                own_score10=0,
            )

        yield pages.OtherScore, dict(
            other_score0=100,
            other_score1=0,
            other_score2=0,
            other_score3=0,
            other_score4=0,
            other_score5=0,
            other_score6=0,
            other_score7=0,
            other_score8=0,
            other_score9=0,
            other_score10=0,
        )
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
            yield pages.QuizPayoff
            yield pages.DecisionPayoff
            yield pages.BlockEnd