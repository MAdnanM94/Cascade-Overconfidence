from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Initialization(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'initialization'


class ScoreReveal(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        accuracy = self.player.accuracy
        return dict(
            ball_A=round(accuracy*100),
            ball_B=round(100 - accuracy*100),
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


class PostDecision(Page):
    form_model = 'player'

    def vars_for_template(self):
        return self.player.vars_for_template_history()

    def get_form_fields(self):
        return [
            ['Red_post_red1', 'Red_post_blue1'],
            ['Red_post_red2', 'Red_post_blue2'],
            ['Red_post_red3', 'Red_post_blue3'],
            ['Red_post_red4', 'Red_post_blue4'],
            ['Red_post_red5', 'Red_post_blue5'],
            ['Red_post_red6', 'Red_post_blue6'],
        ][self.group.order - 1]
    # the form depends on the order

    def before_next_page(self):
        current_sequence = self.player.participant.vars['sequences_order_1'][self.group.order - 1]
        true_state = self.session.vars['true_state_Red_1'][current_sequence - 1]

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
            if signal == "Red":
                self.player.Red_post1 = self.player.Red_post_red1
            else:
                self.player.Red_post1 = self.player.Red_post_blue1
        elif self.group.order == 2:
            self.player.signal2 = signal
            if signal == "Red":
                self.player.Red_post2 = self.player.Red_post_red2
            else:
                self.player.Red_post2 = self.player.Red_post_blue2
        elif self.group.order == 3:
            self.player.signal3 = signal
            if signal == "Red":
                self.player.Red_post3 = self.player.Red_post_red3
            else:
                self.player.Red_post3 = self.player.Red_post_blue3
        elif self.group.order == 4:
            self.player.signal4 = signal
            if signal == "Red":
                self.player.Red_post4 = self.player.Red_post_red4
            else:
                self.player.Red_post4 = self.player.Red_post_blue4
        elif self.group.order == 5:
            self.player.signal5 = signal
            if signal == "Red":
                self.player.Red_post5 = self.player.Red_post_red5
            else:
                self.player.Red_post5 = self.player.Red_post_blue5
        elif self.group.order == 6:
            self.player.signal6 = signal
            if signal == "Red":
                self.player.Red_post6 = self.player.Red_post_red6
            else:
                self.player.Red_post6 = self.player.Red_post_blue6


class PostFinal(WaitPage):
    def vars_for_template(self):
        return self.player.vars_for_template_history()

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
            self.group.red_hist_dump = str(self.session.vars['Red_hist_1_1'])
        else:
            self.group.red_hist_dump = str(self.session.vars['Red_hist_1_2'])


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
                 PostFinal,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 PostFinal,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 PostFinal,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 PostFinal,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 PostFinal,
                 OrderFinish,
                 PreDecision,
                 PostDecision,
                 PostFinal,
                 OrderFinish,
                 BlockEnd
                 ]
