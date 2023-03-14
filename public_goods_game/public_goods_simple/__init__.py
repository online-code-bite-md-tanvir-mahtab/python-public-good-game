from otree.api import *
from .player_roles import PlayerRoles
import pandas as pd

class C(BaseConstants):
    NAME_IN_URL = 'public_goods_simple'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 20
    ENDOWMENT = cu(20)
    MULTIPLIER = 1.8
    CONTRIBUTER = 4
    JUDGE = 1
    PUNISHMENT_AMOUNT_1 = 5
    PUNISHMENT_AMOUNT_2 = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    # TODO: thsi part
    contributor_names = models.StringField()
    judge_name = models.StringField()
    

    def assign_roles(self):
        # Get the names of the contributors and judge from the participant vars
        contributors = self.participant.vars['contributor_names']
        judge = self.participant.vars['judge_name']

        # Set the roles for each player in the group
        for p in self.get_players():
            p.player_roles.set_roles(contributors, judge)

class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=C.ENDOWMENT, label="How much will you contribute?"
    )
    # TODO: thsi part
    name = models.StringField()
    amount_punished = models.CurrencyField(min=5,max=10,initial=0)
    # your player-level models here
    contribution = models.CurrencyField(min=0, max=C.ENDOWMENT, label="How much will you contribute?")
    punish_choice = models.BooleanField(choices=[[False, "Computer"], [True, "Human"]], label="Do you want to be punished by a human or a computer either way your earn will be cutt between 5 or 10?")

    # rating-related fields
    fairness_rating = models.PositiveIntegerField(min=0, max=10, label="How fair do you think the punishment was? (0 = completely unfair, 10 = completely fair)")
    punishment = models.CurrencyField(initial=0)
    
    def role(self):
        return self.id_in_group
    
# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players[:4]]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        # 0.5 * sum of contribution
        group.total_contribution * C.MULTIPLIER / C.CONTRIBUTER
    )
    for p in players[:4]:
        # 20 - contribution
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share
        
        
# another function
def set_punish_payoffs(group: Group):
    # i am going to get all the players
    players = group.get_players()
    contributions = [p.contribution for p in players[:4]]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        # 0.5 * sum of contribution
        group.total_contribution * C.MULTIPLIER / C.CONTRIBUTER
    )
    for p in players[:4]:
        # 20 - contribution
        p.payoff = (C.ENDOWMENT - p.contribution + group.individual_share) - p.amount_punished


# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

class Role(Page):
    
    def vars_for_template(self):
        # Define the player's role based on their ID
        role = ''
        
        if Player.role(self) == 5:
            role = 'Judge'
        else:
            role = 'Contributor'
        return {'role': role}




class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']
    
    def is_displayed(self):
        return Player.role(self) != 5


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    def vars_for_template(self):
        players = self.group.get_players()
        contributions = [p.contribution for p in players[:4]]
        share = [p.payoff for p in players[:4]]
        # Define the player's role based on their ID
        role = ''
        data = pd.DataFrame({
            'contributed':contributions,
            'earn':share
        })
        if Player.role(self) == 5:
            role = 'Judge'
        else:
            role = 'Contributor'
        return {
            'role': role,
            'data':players[:4]
            }





class Punishment(Page):
    form_model = 'player'
    form_fields = ['punish_choice']
    
    def vars_for_template(self):
        players = self.group.get_players()
        if Player.role(self) == 5:
            role = 'Judge'
        else:
            role = 'Contributor'
        # now i am going to get the choice of the player
        # who he want to get punished by
        if Player.punish_choice == 'Human':
            # # TODO: i will check it soon
            # if Player.role(self) == 5:

            #     return {
            #         'role': role,
            #         'data':players[:4]
            #         }
            # else:
            #     pass
            pass
        else:
            if C.NUM_ROUNDS % 2 == 0:
                Player.amount_punished = C.PUNISHMENT_AMOUNT_1
            else:
                Player.amount_punished = C.PUNISHMENT_AMOUNT_2
        return {
            'role': role,
            'data':players[:4]
            }
    def is_displayed(self):
        return Player.role(self) != 5

    
    
class PunishWaitPage(WaitPage):
    after_all_players_arrive = set_punish_payoffs


class Rating(Page):
    form_model = 'player'
    form_fields = ['fairness_rating']
    def vars_for_template(self):
        players = self.group.get_players()
        id = Player.role(self)
        return {
            'players':players[:4],
            'id':id
        }


class Human(Page):
    form_model = 'player'
    form_fields = ['amount_punished']
    def vars_for_template(self):
        players = self.group.get_players()

        return {
            'players': players[:4]
        }
        pass

    def is_displayed(self):
        return Player.role(self) == 5
    
    # def before_next_page(self, timeout_happened=False):
    #     Player.amount_punished = Player.amount_punished
    
    
                    
                    
page_sequence = [Introduction,Role,Contribute, ResultsWaitPage, Results,Punishment,Human,PunishWaitPage,Results,Rating]
