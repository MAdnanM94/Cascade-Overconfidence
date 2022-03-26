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
import pandas as pd
from scipy import stats

author = 'Mir Adnan Mahmood'

doc = """
This app is contains code for the Second Quiz Block treatment for the Overconfidence with Cascades experiment. Players are
assigned a score based on a 10 item quiz. The score determines their accuracy. There are two phases:
Phase 1 - Unknown Phase - Players don't know their own score and thus don't know their own accuracy.
Phase 2 - Known Phase - Players know their own score and accuracy
Each Phase has 6 cascade sequences/decisions where players make two guesses about the probability that the color assigned
to their group is Red.
Groups are fixed for this block - 6 members per group.
"""


class Constants(BaseConstants):
    name_in_url = 'quiz_block_2'
    players_per_group = 6
    num_rounds = 2
    spell_length = 6

    # Prior of jar being Red
    prior_red = 0.5

    # Payout for Quiz Score
    score_payoff = 10
    # Payoff for score elicitation
    belief_payoff = 2
    # Payout for pre and post decision
    decision_payoff = 12


class Subsession(BaseSubsession):
    q_sequence = models.IntegerField()

    def creating_session(self):
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
                p.participant.vars['paying_round_3'] = paying_round
                p.participant.vars['paying_decision_3'] = paying_decision

        for p in self.get_players():
            p.paying_round = p.participant.vars['paying_round_3']
            p.paying_decision = p.participant.vars['paying_decision_3']

        # Code for setting the state
        # Generating a list of 6 random numbers - one for each sequence per group
        state_r = [random.random() for i in range(Constants.players_per_group)]
        # Generating boolean values for state being Red (if prior < 0.5, red)
        self.session.vars['true_state_Red_3'] = [r <= Constants.prior_red for r in state_r]

        # Initializing the histories for this round - one for each group
        # each history var is a matrix - rows represent the order, columns represent the sequence
        self.session.vars['Red_hist_3_1'] = [[False for i in range(Constants.players_per_group)] for j in
                                             range(Constants.spell_length)]
        self.session.vars['Red_hist_3_2'] = [[False for i in range(Constants.players_per_group)] for j in
                                             range(Constants.spell_length)]

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
            g.true_state_red_dump = str(self.session.vars['true_state_Red_3'])
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
            p.participant.vars['sequences_order_3'] = [row[j] for row in sequences]

            [p.sequence1, p.sequence2, p.sequence3, p.sequence4, p.sequence5, p.sequence6,
             ] = p.participant.vars['sequences_order_3']

            j = j + 1

            # this block records the sequence in which each agent acts in the prescribed order - so sequence(i) is the sequence
            # in which agent acts in the ith order/position

    def set_IS(self):
        # Structuring the information structure for each subject
        # (in main blocks, this will take the form of scores from quizzes)
        for p in self.get_players():
            if self.subsession.round_number == 2:
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
            psequence = p.participant.vars['sequences_order_3'][self.order - 1]
            # this player's current sequence
            # pRed = [p.Red_post1, p.Red_post2, p.Red_post3, p.Red_post4, p.Red_post5, p.Red_post6,
            #          ]
            pRed = [p.Red_hist1, p.Red_hist2, p.Red_hist3, p.Red_hist4, p.Red_hist5, p.Red_hist6]
            current_hist[psequence - 1] = pRed[self.order - 1]
            # construct a list of history within this order

        if self.id_in_subsession == 1:
            self.session.vars['Red_hist_3_1'][self.order - 1] = current_hist
        else:
            self.session.vars['Red_hist_3_2'][self.order - 1] = current_hist
        # add the history of this order into the round history
        # note that each row represents an order and each column represents a sequence


class Player(BasePlayer):
    paying_round = models.IntegerField()
    paying_decision = models.IntegerField()
    score = models.IntegerField(initial=0)
    other_score = models.IntegerField()
    accuracy = models.FloatField()

    # Variables for quiz questions - Q1 to Q10 (one for each quiz)
    Q1 = models.StringField()
    Q1_correct = models.BooleanField(initial=False)

    Q2 = models.StringField()
    Q2_correct = models.BooleanField(initial=False)

    Q3 = models.StringField()
    Q3_correct = models.BooleanField(initial=False)

    Q4 = models.StringField()
    Q4_correct = models.BooleanField(initial=False)

    Q5 = models.StringField()
    Q5_correct = models.BooleanField(initial=False)

    Q6 = models.StringField()
    Q6_correct = models.BooleanField(initial=False)

    Q7 = models.StringField()
    Q7_correct = models.BooleanField(initial=False)

    Q8 = models.StringField()
    Q8_correct = models.BooleanField(initial=False)

    Q9 = models.StringField()
    Q9_correct = models.BooleanField(initial=False)

    Q10 = models.StringField()
    Q10_correct = models.BooleanField(initial=False)

    # Variables for guesses of own scores - using BDM
    own_score0 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 0",
                                     widget=widgets.Slider)
    own_score1 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 1",
                                     widget=widgets.Slider)
    own_score2 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 2",
                                     widget=widgets.Slider)
    own_score3 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 3",
                                     widget=widgets.Slider)
    own_score4 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 4",
                                     widget=widgets.Slider)
    own_score5 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 5",
                                     widget=widgets.Slider)
    own_score6 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 6",
                                     widget=widgets.Slider)
    own_score7 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 7",
                                     widget=widgets.Slider)
    own_score8 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 8",
                                     widget=widgets.Slider)
    own_score9 = models.IntegerField(min=0, max=100,
                                     label="What do you think is the probability (0-100%) that your own score is 9",
                                     widget=widgets.Slider)
    own_score10 = models.IntegerField(min=0, max=100,
                                      label="What do you think is the probability (0-100%) that your own score is 10",
                                      widget=widgets.Slider)

    # Variables for guesses of other persons' scores - using BDM
    other_score0 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 0",
                                       widget=widgets.Slider)
    other_score1 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 1",
                                       widget=widgets.Slider)
    other_score2 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 2",
                                       widget=widgets.Slider)
    other_score3 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 3",
                                       widget=widgets.Slider)
    other_score4 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 4",
                                       widget=widgets.Slider)
    other_score5 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 5",
                                       widget=widgets.Slider)
    other_score6 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 6",
                                       widget=widgets.Slider)
    other_score7 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 7",
                                       widget=widgets.Slider)
    other_score8 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 8",
                                       widget=widgets.Slider)
    other_score9 = models.IntegerField(min=0, max=100,
                                       label="What do you think is the probability (0-100%) that the other person's score is 9",
                                       widget=widgets.Slider)
    other_score10 = models.IntegerField(min=0, max=100,
                                        label="What do you think is the probability (0-100%) that the other person's score is 10",
                                        widget=widgets.Slider)

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

    # Final profit for quiz score and elicitations
    quiz_profit = models.FloatField(initial=0)

    # Profit vars
    # profit from the pre and post decisions - used in the final profit calculation per block
    profit_pre = models.FloatField(initial=0)
    profit_post = models.FloatField(initial=0)
    random_pre = models.IntegerField()
    random_post = models.IntegerField()

    # profit from score, own elicitation and other elicitation
    other_round = models.IntegerField()  # which random round chosen for other score elicitation
    profit_score = models.FloatField(initial=0)  # profit from quiz
    profit_own = models.FloatField(initial=0)  # profit from own score elicitation
    profit_other = models.FloatField(initial=0)  # profit from other score elicitation
    question_own = models.IntegerField()  # which question chosen at random for own score elicitation
    question_other = models.IntegerField()  # which question chosen at random for other score elicitation
    random_own = models.IntegerField()
    random_other = models.IntegerField()

    def record_state(self):
        if self.group.order == 1:
            self.stateR1 = self.session.vars['true_state_Red_3'][self.sequence1 - 1]
        if self.group.order == 2:
            self.stateR2 = self.session.vars['true_state_Red_3'][self.sequence2 - 1]
        if self.group.order == 3:
            self.stateR3 = self.session.vars['true_state_Red_3'][self.sequence3 - 1]
        if self.group.order == 4:
            self.stateR4 = self.session.vars['true_state_Red_3'][self.sequence4 - 1]
        if self.group.order == 5:
            self.stateR5 = self.session.vars['true_state_Red_3'][self.sequence5 - 1]
        if self.group.order == 6:
            self.stateR6 = self.session.vars['true_state_Red_3'][self.sequence6 - 1]

    def vars_for_template_history(self):
        # These are the variables used in the HTML template
        current_sequence = [
                            self.sequence1, self.sequence2, self.sequence3, self.sequence4, self.sequence5, self.sequence6,
                        ][self.group.order - 1] - 1

        if self.group.id_in_subsession == 1:
            current_hist = self.session.vars['Red_hist_3_1']
        else:
            current_hist = self.session.vars['Red_hist_3_2']

        return dict(

            current_signal=[
                self.signal1, self.signal2, self.signal3, self.signal4, self.signal5, self.signal6,
            ][self.group.order - 1],

            current_guessR_pre=[
                self.Red_pre1, self.Red_pre2, self.Red_pre3, self.Red_pre4, self.Red_pre5, self.Red_pre6,
            ][self.group.order - 1],

            current_guessR_post=[
                self.Red_post1, self.Red_post2, self.Red_post3, self.Red_post4, self.Red_post5, self.Red_post6,
            ][self.group.order - 1],

            current_stateR=[
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
        self.participant.vars['guess_profit_3'] = self.guess_profit

    def quiz_profit_calc(self):
        # This function computes the profit for the quiz taken in this block -
        # contains profit from score, own score elicitation and other score elicitation

        # Profit from quiz score
        # Loading the dataset
        data = pd.read_csv('_static/quiz.csv')
        if self.subsession.q_sequence == 2:
            scores = data['easy1'].copy()

        else:
            scores = data['hard1'].copy()

        # appending the participant's score to the data
        score_list = scores.values.tolist()
        score_list.append(self.score)

        # Computing the percentile rank
        percentile = round(stats.percentileofscore(score_list, self.score) / 100, 2)

        self.profit_score = Constants.score_payoff * percentile

        # Profit from score elicitation
        self.other_round = random.randint(1, 2)
        in_round_1 = self.in_round(1)  # Getting player values in round 1

        own_guesses = [in_round_1.own_score0, in_round_1.own_score1, in_round_1.own_score2,
                       in_round_1.own_score3, in_round_1.own_score4, in_round_1.own_score5,
                       in_round_1.own_score6, in_round_1.own_score7, in_round_1.own_score8,
                       in_round_1.own_score9, in_round_1.own_score10]

        in_other_round = self.in_round(self.other_round)  # getting player values in the round chosen for other score
        other_guesses = [in_other_round.other_score0, in_other_round.other_score1, in_other_round.other_score2,
                         in_other_round.other_score3, in_other_round.other_score4, in_other_round.other_score5,
                         in_other_round.other_score6, in_other_round.other_score7, in_other_round.other_score8,
                         in_other_round.other_score9, in_other_round.other_score10]

        # Getting the other player in the group.
        other_list = self.get_others_in_group()
        r = random.randint(1, len(other_list))
        self.other_score = other_list[r - 1].score

        in_round_1.other_score = self.other_score

        # random selection for the questions
        self.question_own = random.randint(0, 10)  # which question to pay for own score
        self.question_other = random.randint(0, 10)  # which question to pay for other score

        self.random_own = random.randint(0, 100)  # which choice to pay for for given own score questions
        self.random_other = random.randint(0, 100)  # which choice to pay for for given other score questions

        # Payoffs
        if self.random_own <= own_guesses[self.question_own]:
            self.profit_own += Constants.belief_payoff * (self.score == self.question_own)
        else:
            r1 = random.randint(0, 100)
            self.profit_own += Constants.belief_payoff * (r1 <= self.random_own)

        if self.random_other <= other_guesses[self.question_other]:
            self.profit_other += Constants.belief_payoff * (self.other_score == self.question_other)
        else:
            r2 = random.randint(0, 100)
            self.profit_other += Constants.belief_payoff * (r2 <= self.random_other)

        # Adding it all up
        self.quiz_profit = self.profit_score + self.profit_own + self.profit_other
        # Setting these as participant vars
        self.participant.vars['quiz_profit_3'] = self.quiz_profit  # payoff from quiz
        self.participant.vars['own_score_3'] = self.score  # own score
        self.participant.vars['other_score_3'] = self.other_score  # random participant's score
        self.participant.vars['own_question_3'] = self.question_own  # question chosen for belief elicitation payment
        self.participant.vars[
            'other_question_3'] = self.question_other  # question chosen for belief elicitation payment
