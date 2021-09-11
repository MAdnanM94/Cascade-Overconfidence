from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random

author = 'Mir Adnan Mahmood'

doc = """
This app computes the final payment for the Overconfidence and Cascades experiment. It randomly chooses one block
for the payments for guesses of the state and one quiz for the payments for the quizzes. This app also contains a survey
on demographic information (age, gender, college major, college year etc).
"""


class Constants(BaseConstants):
    name_in_url = 'final_payment'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def final_payoffs(self):
        # Choosing the blocks for payment
        guess_block = random.randint(1, 5)
        quiz_block = random.randint(2, 5)
        for p in self.get_players():
            # Getting the payment for the guesses
            p.payment_block = guess_block
            if p.payment_block == 1:
                p.payment_phase = p.participant.vars['paying_round_1']
                p.payment_decision = p.participant.vars['paying_decision_1']
                p.profit_decisions = p.participant.vars['guess_profit_1']
            elif p.payment_block == 2:
                p.payment_phase = p.participant.vars['paying_round_2']
                p.payment_decision = p.participant.vars['paying_decision_2']
                p.profit_decisions = p.participant.vars['guess_profit_2']
            elif p.payment_block == 3:
                p.payment_phase = p.participant.vars['paying_round_3']
                p.payment_decision = p.participant.vars['paying_decision_3']
                p.profit_decisions = p.participant.vars['guess_profit_3']
            elif p.payment_block == 4:
                p.payment_phase = p.participant.vars['paying_round_4']
                p.payment_decision = p.participant.vars['paying_decision_4']
                p.profit_decisions = p.participant.vars['guess_profit_4']
            elif p.payment_block == 5:
                p.payment_phase = p.participant.vars['paying_round_5']
                p.payment_decision = p.participant.vars['paying_decision_5']
                p.profit_decisions = p.participant.vars['guess_profit_5']

            # Getting payment for the quizzes
            p.payment_quiz_block = quiz_block
            if p.payment_quiz_block == 2:
                p.profit_quiz = p.participant.vars['quiz_profit_2']
                p.own_score = p.participant.vars['own_score_2']
                p.other_score = p.participant.vars['other_score_2']
                p.own_question = p.participant.vars['own_question_2']
                p.other_question = p.participant.vars['other_question_2']
            elif p.payment_quiz_block == 3:
                p.profit_quiz = p.participant.vars['quiz_profit_3']
                p.own_score = p.participant.vars['own_score_3']
                p.other_score = p.participant.vars['other_score_3']
                p.own_question = p.participant.vars['own_question_3']
                p.other_question = p.participant.vars['other_question_3']
            if p.payment_quiz_block == 4:
                p.profit_quiz = p.participant.vars['quiz_profit_4']
                p.own_score = p.participant.vars['own_score_4']
                p.other_score = p.participant.vars['other_score_4']
                p.own_question = p.participant.vars['own_question_4']
                p.other_question = p.participant.vars['other_question_4']
            if p.payment_quiz_block == 5:
                p.profit_quiz = p.participant.vars['quiz_profit_5']
                p.own_score = p.participant.vars['own_score_5']
                p.other_score = p.participant.vars['other_score_5']
                p.own_question = p.participant.vars['own_question_5']
                p.other_question = p.participant.vars['other_question_5']

            # Total payoff for the experiment
            p.payoff = round(p.profit_decisions + p.profit_quiz, 1)


class Player(BasePlayer):
    # Payment vars for cascade sequences
    payment_block = models.IntegerField()
    payment_phase = models.IntegerField()
    payment_decision = models.IntegerField()
    profit_decisions = models.FloatField()
    # Payment vars for quizzes
    payment_quiz_block = models.IntegerField()
    profit_quiz = models.FloatField()
    own_score = models.IntegerField()
    other_score = models.IntegerField()
    own_question = models.IntegerField()
    other_question = models.IntegerField()

    # Variables for demographics
    age = models.IntegerField(label="What is your age (in years)?")
    gender = models.IntegerField(label="What is your gender?",
                                 choices=[
                                     [1, 'Male'], [2, 'Female'], [3, 'Non-binary']
                                 ],
                                 widget=widgets.RadioSelect)
    major = models.StringField(label='What is your major?')
    educ_year = models.IntegerField(label='What year of college are you in?',
                                    choices=[
                                        [1, 'Freshman'], [2, 'Sophomore'], [3, 'Junior'],
                                        [4, 'Senior'], [5, 'Graduate Student'], [6, 'Not Applicable/Graduated']
                                    ],
                                    widget=widgets.RadioSelect)
    past_experiments = models.BooleanField(label='Have you taken part in previous Economics Experiments?',
                                           choices = [
                                               [False, 'No'], [True, 'Yes']
                                           ],
                                           widget=widgets.RadioSelect)
    game_theory = models.BooleanField(label='Have you taken a course in Game Theory?',
                                      choices=[
                                          [False, 'No'], [True, 'Yes']
                                      ],
                                      widget=widgets.RadioSelect)

    experiment = models.BooleanField(label='Have you taken a course in Experimental Economics?',
                                     choices=[
                                         [False, 'No'], [True, 'Yes']
                                     ],
                                     widget=widgets.RadioSelect
                                     )




