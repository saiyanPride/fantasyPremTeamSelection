class PlayerScore:

    @staticmethod
    def compute_player_score_by_predicted_points_and_form(player_data):
        FORM_SCORE_CONTRIBUTION_PROPORTION = (
        0.3  # if too high, then there's a bias for players that played well recently
        )

        score = (
            player_data.avg_predicted_points # predicted points component
            * FORM_SCORE_CONTRIBUTION_PROPORTION
            * player_data.form # form component
        )
        return round(score, 1)
