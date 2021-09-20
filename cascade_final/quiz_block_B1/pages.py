from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


# Start wait page for block
class StartBlock(WaitPage):
    wait_for_all_groups=True


# Quiz Question Pages
class Q1(Page):
    form_model = 'player'
    form_fields = ['Q1']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "titanic" in self.player.Q1.lower():
                self.player.score += 1
                self.player.Q1_correct = True
        else:
            if "washington" in self.player.Q1.lower() and ("d.c" in self.player.Q1.lower() or "dc" in self.player.Q1.lower()):
                self.player.score += 1
                self.player.Q1_correct = True


class Q2(Page):
    form_model = 'player'
    form_fields = ['Q2']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "heart" in self.player.Q2.lower():
                self.player.score += 1
                self.player.Q2_correct = True
        else:
            if "sun" in self.player.Q2.lower():
                self.player.score += 1
                self.player.Q2_correct = True


class Q3(Page):
    form_model = 'player'
    form_fields = ['Q3']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if ("september" in self.player.Q3.lower() or "9" in self.player.Q3.lower()) and "11" in self.player.Q3.lower():
                self.player.score += 1
                self.player.Q3_correct = True
        else:
            if "himalaya" in self.player.Q3.lower():
                self.player.score += 1
                self.player.Q3_correct = True


class Q4(Page):
    form_model = 'player'
    form_fields = ['Q4']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "2000" == self.player.Q4.lower():
                self.player.score += 1
                self.player.Q4_correct = True
        else:
            if "baltic" in self.player.Q4.lower():
                self.player.score += 1
                self.player.Q4_correct = True


class Q5(Page):
    form_model = 'player'
    form_fields = ['Q5']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "jordan" in self.player.Q5.lower():
                self.player.score += 1
                self.player.Q5_correct = True
        else:
            if "waterloo" in self.player.Q5.lower():
                self.player.score += 1
                self.player.Q5_correct = True


class Q6(Page):
    form_model = 'player'
    form_fields = ['Q6']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "blue" in self.player.Q6.lower():
                self.player.score += 1
                self.player.Q6_correct = True
        else:
            if "ankara" in self.player.Q6.lower():
                self.player.score += 1
                self.player.Q6_correct = True


class Q7(Page):
    form_model = 'player'
    form_fields = ['Q7']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "turkey" in self.player.Q7.lower():
                self.player.score += 1
                self.player.Q7_correct = True
        else:
            if self.player.Q7.lower() == "6" or self.player.Q7.lower() == "six":
                self.player.score += 1
                self.player.Q7_correct = True


class Q8(Page):
    form_model = 'player'
    form_fields = ['Q8']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "gold" in self.player.Q8.lower():
                self.player.score += 1
                self.player.Q8_correct = True
        else:
            if "black" in self.player.Q8.lower() and "tuesday" in self.player.Q8.lower():
                self.player.score += 1
                self.player.Q8_correct = True


class Q9(Page):
    form_model = 'player'
    form_fields = ['Q9']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "bangladesh" in self.player.Q9.lower():
                self.player.score += 1
                self.player.Q9_correct = True
        else:
            if "marvin gaye" in self.player.Q9.lower() and ("senior" in self.player.Q9.lower() or "sr" in self.player.Q9.lower()):
                self.player.score += 1
                self.player.Q9_correct = True


class Q10(Page):
    form_model = 'player'
    form_fields = ['Q10']

    timeout_seconds = 20

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        if self.subsession.q_sequence == 1:
            if "liechtenstein" in self.player.Q10.lower():
                self.player.score += 1
                self.player.Q10_correct = True
        else:
            if "stephen jay gould" in self.player.Q10.lower() or "stephen gould" in self.player.Q10.lower():
                self.player.score += 1
                self.player.Q10_correct = True


# Score elicitation pages
class OwnScore(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['own_score0',
                   'own_score1',
                   'own_score2',
                   'own_score3',
                   'own_score4',
                   'own_score5',
                   'own_score6',
                   'own_score7',
                   'own_score8',
                   'own_score9',
                   'own_score10',
                   ]

    def error_message(self, values):
        print('values is', values)
        sum = values['own_score0'] + values['own_score1'] + values['own_score2'] + values['own_score3'] \
              + values['own_score4'] + values['own_score5'] + values['own_score6'] + values['own_score7'] \
              + values['own_score8'] + values['own_score9'] + values['own_score10']
        if sum != 100:
            return 'The total sum of all entries is ' + str(sum) + '. The numbers must add up to 100'


class OtherScore(Page):
    form_model = 'player'
    form_fields = ['other_score0',
                   'other_score1',
                   'other_score2',
                   'other_score3',
                   'other_score4',
                   'other_score5',
                   'other_score6',
                   'other_score7',
                   'other_score8',
                   'other_score9',
                   'other_score10',
                   ]

    def error_message(self, values):
        print('values is', values)
        sum = values['other_score0'] + values['other_score1'] + values['other_score2'] + values['other_score3'] \
              + values['other_score4'] + values['other_score5'] + values['other_score6'] + values['other_score7'] \
              + values['other_score8'] + values['other_score9'] + values['other_score10']
        if sum != 100:
            return 'The total sum of all entries is ' + str(sum) + '. The numbers must add up to 100'


# Initialization Wait Page - initializes everything
class Initialization(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'initialization'


class ScoreReveal(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        accuracy = self.player.accuracy
        return dict(
            ball_A=int(accuracy*100),
            ball_B=int(100 - accuracy*100),
        )


class CascadeWait(WaitPage):
    pass


class PreDecision(Page):
    form_model = 'player'

    def vars_for_template(self):
        return self.player.vars_for_template_history()

    def get_form_fields(self):
        return [
            ['Red_pre1'],
            ['Red_pre2'],
            ['Red_pre3'],
            ['Red_pre4'],
            ['Red_pre5'],
            ['Red_pre6'],
        ][self.group.order - 1]
    # the form depends on the order

    def before_next_page(self):
        current_sequence = self.player.participant.vars['sequences_order_2'][self.group.order - 1]
        true_state = self.session.vars['true_state_Red_2'][current_sequence - 1]

        r = random.random()
        accuracy = self.player.accuracy
        if true_state:
            if r <= accuracy:
                signal = 'Red'
            else:
                signal = 'Blue'
        else:
            if r <= accuracy:
                signal = 'Blue'
            else:
                signal = 'Red'

        if self.group.order == 1:
            self.player.signal1 = signal
        elif self.group.order == 2:
            self.player.signal2 = signal
        elif self.group.order == 3:
            self.player.signal3 = signal
        elif self.group.order == 4:
            self.player.signal4 = signal
        elif self.group.order == 5:
            self.player.signal5 = signal
        elif self.group.order == 6:
            self.player.signal6 = signal


class PostDecision(Page):
    form_model = 'player'

    def vars_for_template(self):
        return self.player.vars_for_template_history()

    def get_form_fields(self):
        return [
            ['Red_post1'],
            ['Red_post2'],
            ['Red_post3'],
            ['Red_post4'],
            ['Red_post5'],
            ['Red_post6'],
        ][self.group.order - 1]
    # the form depends on the order

    def before_next_page(self):
        if self.group.order == 1:
            if self.player.Red_post1 > 50:
                self.player.Red_hist1 = True
            elif self.player.Red_post1 < 50:
                self.player.Red_hist1 = False
            else:
                self.player.Red_hist1 = random.choice([True, False])
        elif self.group.order == 2:
            if self.player.Red_post2 > 50:
                self.player.Red_hist2 = True
            elif self.player.Red_post2 < 50:
                self.player.Red_hist2 = False
            else:
                self.player.Red_hist2 = random.choice([True, False])
        if self.group.order == 3:
            if self.player.Red_post3 > 50:
                self.player.Red_hist3 = True
            elif self.player.Red_post3 < 50:
                self.player.Red_hist3 = False
            else:
                self.player.Red_hist3 = random.choice([True, False])
        if self.group.order == 4:
            if self.player.Red_post4 > 50:
                self.player.Red_hist4 = True
            elif self.player.Red_post4 < 50:
                self.player.Red_hist4 = False
            else:
                self.player.Red_hist4 = random.choice([True, False])
        if self.group.order == 5:
            if self.player.Red_post5 > 50:
                self.player.Red_hist5 = True
            elif self.player.Red_post5 < 50:
                self.player.Red_hist5 = False
            else:
                self.player.Red_hist5 = random.choice([True, False])
        if self.group.order == 6:
            if self.player.Red_post6 > 50:
                self.player.Red_hist6 = True
            elif self.player.Red_post6 < 50:
                self.player.Red_hist6 = False
            else:
                self.player.Red_hist6 = random.choice([True, False])


class OrderFinish(WaitPage):
    def after_all_players_arrive(self):
        self.group.record_history()

        for p in self.group.get_players():
            p.record_state()

        self.group.order += 1
        if self.group.id_in_subsession == 1:
            self.group.red_hist_dump = str(self.session.vars['Red_hist_2_1'])
        else:
            self.group.red_hist_dump = str(self.session.vars['Red_hist_2_2'])


class PayoffCalc(WaitPage):
    def is_displayed(self):
        return self.round_number == 2

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.quiz_profit_calc()
            p.decision_profit()


class QuizPayoff(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        in_round_1 = self.player.in_round(1)
        in_other_round = self.player.in_round(self.player.other_round)

        own_guesses = [in_round_1.own_score0, in_round_1.own_score1, in_round_1.own_score2,
                       in_round_1.own_score3, in_round_1.own_score4, in_round_1.own_score5,
                       in_round_1.own_score6, in_round_1.own_score7, in_round_1.own_score8,
                       in_round_1.own_score9, in_round_1.own_score10]

        other_guesses = [in_other_round.other_score0, in_other_round.other_score1, in_other_round.other_score2,
                         in_other_round.other_score3, in_other_round.other_score4, in_other_round.other_score5,
                         in_other_round.other_score6, in_other_round.other_score7, in_other_round.other_score8,
                         in_other_round.other_score9, in_other_round.other_score10]

        return dict(
            own=own_guesses[self.player.question_own],
            other=other_guesses[self.player.question_other],
            percentile=self.player.profit_score / Constants.score_payoff * 100
        )


class DecisionPayoff(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        player_in_round = self.player.in_round(self.player.paying_round)
        states = [player_in_round.stateR1, player_in_round.stateR2, player_in_round.stateR3,
                  player_in_round.stateR4, player_in_round.stateR5, player_in_round.stateR6]

        guesses_pre = [player_in_round.Red_pre1, player_in_round.Red_pre2, player_in_round.Red_pre3,
                       player_in_round.Red_pre4, player_in_round.Red_pre5, player_in_round.Red_pre6]

        guesses_post = [player_in_round.Red_post1, player_in_round.Red_post2, player_in_round.Red_post3,
                        player_in_round.Red_post4, player_in_round.Red_post5, player_in_round.Red_post6]

        return dict(
            state=states[self.player.paying_decision - 1],
            pre=guesses_pre[self.player.paying_decision - 1],
            post=guesses_post[self.player.paying_decision - 1]
        )


# Pages for block start and end placeholders
class BlockStart(Page):
    def is_displayed(self):
        return self.round_number == 1


class BlockEnd(Page):
    def is_displayed(self):
        return self.round_number == 2


page_sequence = [StartBlock,
                 BlockStart,
                 Q1,
                 Q2,
                 Q3,
                 Q4,
                 Q5,
                 Q6,
                 Q7,
                 Q8,
                 Q9,
                 Q10,
                 Initialization,
                 ScoreReveal,
                 OwnScore,
                 OtherScore,
                 CascadeWait,
                 PreDecision,
                 PostDecision,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 OrderFinish,
                 PayoffCalc,
                 QuizPayoff,
                 DecisionPayoff,
                 BlockEnd
                 ]

