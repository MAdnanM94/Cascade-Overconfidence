from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Block1(Page):
    pass


class Instructions(Page):
    pass


page_sequence = [Instructions, Block1]