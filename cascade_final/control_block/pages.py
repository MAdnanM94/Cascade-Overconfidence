from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Initialization(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'initialization'


class ScoreReveal(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self):
        return dict(
            ball_A=50 + 5*self.player.score,
            ball_B=50 - 5*self.player.score
        )


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
        current_chain = self.player.participant.vars['chains_order_1'][self.group.order - 1]
        true_state = self.session.vars['true_state_Red_1'][current_chain - 1]

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
            if self.player.Red_post1 >= 50:
                self.player.Red_hist1 = True
            else:
                self.player.Red_hist1 = False
        elif self.group.order == 2:
            if self.player.Red_post2 >= 50:
                self.player.Red_hist2 = True
            else:
                self.player.Red_hist2 = False
        if self.group.order == 3:
            if self.player.Red_post3 >= 50:
                self.player.Red_hist3 = True
            else:
                self.player.Red_hist3 = False
        if self.group.order == 4:
            if self.player.Red_post4 >= 50:
                self.player.Red_hist4 = True
            else:
                self.player.Red_hist4 = False
        if self.group.order == 5:
            if self.player.Red_post5 >= 50:
                self.player.Red_hist5 = True
            else:
                self.player.Red_hist5 = False
        if self.group.order == 6:
            if self.player.Red_post6 >= 50:
                self.player.Red_hist6 = True
            else:
                self.player.Red_hist6 = False


class OrderFinish(WaitPage):
    def after_all_players_arrive(self):
        self.group.record_history()

        for p in self.group.get_players():
            p.record_state()

        self.group.order += 1
        if self.group.id_in_subsession == 1:
            self.group.red_hist_dump = str(self.session.vars['Red_hist_1_1'])
        else:
            self.group.red_hist_dump = str(self.session.vars['Red_hist_1_2'])


class PayoffCalc(WaitPage):
    def is_displayed(self):
        return self.round_number == 2

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.decision_profit()


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
            pre = guesses_pre[self.player.paying_decision - 1],
            post=guesses_post[self.player.paying_decision - 1]
        )


class BlockStart(Page):
    def is_displayed(self):
        return self.round_number == 1


class BlockEnd(Page):
    def is_displayed(self):
        return self.round_number == 2


page_sequence = [Initialization,
                 BlockStart,
                 ScoreReveal,
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
                 DecisionPayoff,
                 BlockEnd
                 ]
