from otree.api import *



class PlayerRoles(ExtraModel):
    # This model defines the role of each player in the game

    # Determine whether this player contributed less than the endowment
    is_contributor = models.BooleanField()

    # Determine whether this player is the judge
    is_judge = models.BooleanField()

    def set_roles(self, contributors, judge):
        # Set the roles for this player
        self.is_contributor = self.participant.vars['contributor_names'][self.id_in_group-1] in contributors
        self.is_judge = self.participant.vars['judge_name'] == judge
