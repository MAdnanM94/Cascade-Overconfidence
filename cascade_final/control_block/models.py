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
import itertools

author = 'Mir Adnan Mahmood'

doc = """
This app is contains code for the Control Block treatment for the Overconfidence with Cascades experiment. Players are
assigned a score from a random distribution - the score determines their accuracy. There are two phases,
Phase 1 - Unknown Phase - Players don't know their own score and thus don't know their own accuracy.
Phase 2 - Known Phase - Players know their own score and accuracy
Each Phase has 6 cascade sequences/decisions where players make two guesses about the probability that the color assigned
to their group is Red.
Groups are fixed for this block - 6 members per group.
"""


class Constants(BaseConstants):
    name_in_url = 'control_block'
    players_per_group = 6
    num_rounds = 2
    spell_length = 6

    # Prior of jar being Red
    prior_red = 0.5

    # Payout for Quiz Score
    score_payoff = 10
    # Payoff for score elicitation
    belief_payoff = 2
    # Payout for pre and post decisions
    decision_payoff = 12


class Subsession(BaseSubsession):
    q_sequence = models.IntegerField()    # The sequence variable here indicates sequence of quizzes for quiz blocks

    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)

        self.q_sequence = self.session.config['q_sequence']

    def initialization(self):
        # This function initializes the round
        # First it records the random round/phase and sequence for payment purposes
        # Then it sets the states for the sequences and dumps them into the relevant history variables for the groups
        # For each group it then sets the order and group sequence

        # Participant code for payoffs
        if self.round_number == 1:
            # Recording for each player, the randomly chosen round and decision for payment
            for p in self.get_players():
                paying_round = random.randint(1, Constants.num_rounds)
                paying_decision = random.randint(1, Constants.spell_length)
                p.participant.vars['paying_round_1'] = paying_round
                p.participant.vars['paying_decision_1'] = paying_decision

        for p in self.get_players():
            p.paying_round = p.participant.vars['paying_round_1']
            p.paying_decision = p.participant.vars['paying_decision_1']

        # Code for setting the state
        # Generating a list of 6 random numbers - one for each sequence per group
        state_r = [random.random() for i in range(Constants.players_per_group)]
        # Generating boolean values for state being Red (if prior < 0.5, red)
        self.session.vars['true_state_Red_1'] = [r <= Constants.prior_red for r in state_r]

        # Initializing the histories for this round - one for each group
        # each history var is a matrix - rows represent the order, columns represent the sequence
        self.session.vars['Red_hist_1_1'] = [[False for i in range(Constants.players_per_group)] for j in range(Constants.spell_length)]
        self.session.vars['Red_hist_1_2'] = [[False for i in range(Constants.players_per_group)] for j in range(Constants.spell_length)]

        # Code for groups
        for g in self.get_groups():
            g.prior_red = Constants.prior_red
            # set the prior
            g.set_IS()
            # set the information structure
            g.set_sequence()
            # set the sequence matrix and the sequence variables
            g.order = 1
            # set order = 1
            g.true_state_red_dump = str(self.session.vars['true_state_Red_1'])
            # dumping the states into a long string field


class Group(BaseGroup):
    prior_red = models.FloatField()
    # String field containing the true states for each sequence
    true_state_red_dump = models.LongStringField()
    # Order variable signifying the "position" of each decision
    order = models.IntegerField(initial=1)
    # History variables - string field containing history of actions
    red_hist_dump = models.LongStringField()

    def set_sequence(self):
        def create_matrix(inList, n, k):
            # This function creates a sequence matrix - it's an nxn matrix
            firstrow = random.sample(inList, k)
            permutes = random.sample(inList, k)
            return list(firstrow[i:] + firstrow[:i] for i in permutes[:n])

        n = Constants.players_per_group
        subjects = list(range(1, n + 1))
        sequences = create_matrix(subjects, Constants.spell_length, n)
        # sequences: each row corresponds to an sequence, each column corresponds to a subject
        # each cell is an integer from 1 to n

        j = 0
        for p in self.get_players():
            p.participant.vars['sequences_order_1'] = [row[j] for row in sequences]

            [p.sequence1, p.sequence2, p.sequence3, p.sequence4, p.sequence5, p.sequence6,
             ] = p.participant.vars['sequences_order_1']

            j = j + 1

            # this block records the sequence in which each agent acts in the prescribed order - so sequence(i) is the sequence
            # in which agent acts in the ith order/position

    def set_IS(self):
        # Structuring the information structure for each subject
        # (in main blocks, this will take the form of scores from quizzes)
        for p in self.get_players():
            if self.subsession.round_number == 1:
                r = random.random()
                if r <= 1/11:
                    p.score = 0
                elif r <= 2/11:
                    p.score = 1
                elif r <= 3/11:
                    p.score = 2
                elif r <= 4/11:
                    p.score = 3
                elif r <= 5/11:
                    p.score = 4
                elif r <= 6/11:
                    p.score = 5
                elif r <= 7/11:
                    p.score = 6
                elif r <= 8/11:
                    p.score = 7
                elif r <= 9/11:
                    p.score = 8
                elif r <= 10/11:
                    p.score = 9
                else:
                    p.score = 10
            else:
                p.score = p.in_round(1).score

            if p.score <= 3:
                p.accuracy = 0.55
            elif p.score <= 7:
                p.accuracy = 0.65
            else:
                p.accuracy = 0.9

    def record_history(self):
        current_hist = ['' for i in range(Constants.players_per_group)]
        # set empty current history

        for p in self.get_players():
            psequence = p.participant.vars['sequences_order_1'][self.order - 1]
            # this player's current sequence
            # pRed = [p.Red_post1, p.Red_post2, p.Red_post3, p.Red_post4, p.Red_post5, p.Red_post6,
            #          ]
            pRed = [p.Red_hist1, p.Red_hist2, p.Red_hist3, p.Red_hist4, p.Red_hist5, p.Red_hist6]
            current_hist[psequence - 1] = pRed[self.order - 1]
            # construct a list of history within this order

        if self.id_in_subsession == 1:
            self.session.vars['Red_hist_1_1'][self.order - 1] = current_hist
        else:
            self.session.vars['Red_hist_1_2'][self.order - 1] = current_hist
        # add the history of this order into the round history
        # note that each row represents an order and each column represents a sequence


class Player(BasePlayer):
    paying_round = models.IntegerField()
    paying_decision = models.IntegerField()
    score = models.IntegerField()
    accuracy = models.FloatField()

    # sequence identifiers and decision variables
    # sequence(i) identifies the sequence in which agent makes ith decision
    # signal(i) identifies the signal received in the ith decision
    # stateR(i) is the state in decision i
    # Red_pre(i) - pre guess of probability of state being Red in ith decision
    # Red_post(i) - post guess of probability of state being Red in ith decision
    # Red_hist(i) - recorded state in ith decision (True/Red if greater than 50%, False/Blue otherwise)
    sequence1 = models.IntegerField()
    signal1 = models.StringField(initial='')
    stateR1 = models.BooleanField()
    Red_pre1 = models.IntegerField(min=0, max=100,
                                   label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_post1 = models.IntegerField(min=0, max=100,
                                    label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_hist1 = models.BooleanField()

    sequence2 = models.IntegerField()
    signal2 = models.StringField(initial='')
    stateR2 = models.BooleanField()
    Red_pre2 = models.IntegerField(min=0, max=100,
                                   label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_post2 = models.IntegerField(min=0, max=100,
                                    label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_hist2 = models.BooleanField()

    sequence3 = models.IntegerField()
    signal3 = models.StringField(initial='')
    stateR3 = models.BooleanField()
    Red_pre3 = models.IntegerField(min=0, max=100,
                                   label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_post3 = models.IntegerField(min=0, max=100,
                                    label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_hist3 = models.BooleanField()

    sequence4 = models.IntegerField()
    signal4 = models.StringField(initial='')
    stateR4 = models.BooleanField()
    Red_pre4 = models.IntegerField(min=0, max=100,
                                   label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_post4 = models.IntegerField(min=0, max=100,
                                    label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_hist4 = models.BooleanField()

    sequence5 = models.IntegerField()
    signal5 = models.StringField(initial='')
    stateR5 = models.BooleanField()
    Red_pre5 = models.IntegerField(min=0, max=100,
                                   label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_post5 = models.IntegerField(min=0, max=100,
                                    label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_hist5 = models.BooleanField()

    sequence6 = models.IntegerField()
    signal6 = models.StringField(initial='')
    stateR6 = models.BooleanField()
    Red_pre6 = models.IntegerField(min=0, max=100,
                                   label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_post6 = models.IntegerField(min=0, max=100,
                                    label="What do you think is the probability (0 to 100%) that the color is Red for this sequence?")
    Red_hist6 = models.BooleanField()

    # Final profit-chosen at random for guesses made for this block
    guess_profit = models.FloatField(initial=0)

    # Profit vars - profit from the pre and post guesses - used in the final profit calculation per block
    profit_pre = models.FloatField(initial=0)
    profit_post = models.FloatField(initial=0)
    random_pre = models.IntegerField()
    random_post = models.IntegerField()

    def record_state(self):
        if self.group.order == 1:
            self.stateR1 = self.session.vars['true_state_Red_1'][self.sequence1 - 1]
        if self.group.order == 2:
            self.stateR2 = self.session.vars['true_state_Red_1'][self.sequence2 - 1]
        if self.group.order == 3:
            self.stateR3 = self.session.vars['true_state_Red_1'][self.sequence3 - 1]
        if self.group.order == 4:
            self.stateR4 = self.session.vars['true_state_Red_1'][self.sequence4 - 1]
        if self.group.order == 5:
            self.stateR5 = self.session.vars['true_state_Red_1'][self.sequence5 - 1]
        if self.group.order == 6:
            self.stateR6 = self.session.vars['true_state_Red_1'][self.sequence6 - 1]

    def vars_for_template_history(self):
        # These are the variables used in the HTML template
        current_sequence = [
            self.sequence1, self.sequence2, self.sequence3, self.sequence4, self.sequence5, self.sequence6,
        ][self.group.order - 1] - 1

        if self.group.id_in_subsession == 1:
            current_hist = self.session.vars['Red_hist_1_1']
        else:
            current_hist = self.session.vars['Red_hist_1_2']

        return dict(

            current_signal=[
                self.signal1, self.signal2, self.signal3, self.signal4, self.signal5, self.signal6,
            ][self.group.order - 1],

            current_guessR_pre = [
                self.Red_pre1, self.Red_pre2, self.Red_pre3, self.Red_pre4, self.Red_pre5, self.Red_pre6,
            ][self.group.order - 1],

            current_guessR_post = [
                self.Red_post1, self.Red_post2, self.Red_post3, self.Red_post4, self.Red_post5, self.Red_post6,
            ][self.group.order - 1],

            current_stateR = [
                self.stateR1, self.stateR2, self.stateR3, self.stateR4, self.stateR5, self.stateR6,
            ][self.group.order - 1],

            # Histories about the current sequence
            Red_his1=current_hist[0][current_sequence],

            Red_his2=current_hist[1][current_sequence],

            Red_his3=current_hist[2][current_sequence],

            Red_his4=current_hist[3][current_sequence],

            Red_his5=current_hist[4][current_sequence],

            Red_his6=current_hist[5][current_sequence],

            # number of balls in a jar
            ball_A=round(self.accuracy*100),
            ball_B=round(100 - self.accuracy*100),
        )

    def decision_profit(self):
        # This function computes the profits for the guesses for this block - takes one round at random and one sequence at random
        # and pays for that.

        in_paying_round = self.in_round(self.paying_round)
        guesses_pre = [in_paying_round.Red_pre1, in_paying_round.Red_pre2, in_paying_round.Red_pre3,
                       in_paying_round.Red_pre4, in_paying_round.Red_pre5, in_paying_round.Red_pre6]

        guesses_post = [in_paying_round.Red_post1, in_paying_round.Red_post2, in_paying_round.Red_post3,
                        in_paying_round.Red_post4, in_paying_round.Red_post5, in_paying_round.Red_post6]

        states = [in_paying_round.stateR1, in_paying_round.stateR2, in_paying_round.stateR3,
                  in_paying_round.stateR4, in_paying_round.stateR5, in_paying_round.stateR6]

        # Generating random questions for each pre-and post decision
        self.random_pre = random.randint(0, 100)
        self.random_post = random.randint(0, 100)

        # Generating profits
        if self.random_pre <= guesses_pre[self.paying_decision - 1]:
            self.profit_pre += Constants.decision_payoff * states[self.paying_decision - 1]
        else:
            r1 = random.randint(0, 100)
            self.profit_pre += Constants.decision_payoff * (r1 <= self.random_pre)

        if self.random_post <= guesses_post[self.paying_decision - 1]:
            self.profit_post += Constants.decision_payoff * states[self.paying_decision - 1]
        else:
            r2 = random.randint(0, 100)
            self.profit_post += Constants.decision_payoff * (r2 <= self.random_post)

        self.guess_profit = self.profit_pre + self.profit_post
        self.participant.vars['guess_profit_1'] = self.guess_profit


