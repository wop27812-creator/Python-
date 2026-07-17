"""
Football Game Statistics Simulator

This script simulates a football match between two teams, generates player and team 
statistics, and presents them using pandas DataFrames. This can serve as a foundation 
for building more complex sports analytics applications.
"""

import random
import pandas as pd
from typing import List, Dict, Tuple


# --- Configuration --- #
TOTAL_GAME_EVENTS = 100  # Number of events in a game


# --- Helper Functions --- #

def get_weighted_random_player(players: List['Player'], attribute_key: str) -> 'Player':
    """Selects a player based on a weighted random attribute."""
    # Use getattr to access player attributes dynamically
    weights = [getattr(player, attribute_key) for player in players]
    total_weight = sum(weights)
    if total_weight == 0:  # Handle case where all weights are zero
        return random.choice(players)
    normalized_weights = [w / total_weight for w in weights]
    return random.choices(players, weights=normalized_weights, k=1)[0]


class Player:
    """Represents a football player with attributes and statistics."""
    
    def __init__(self, name: str, offense: int, defense: int, stamina: int):
        self.name = name
        self.offense = offense
        self.defense = defense
        self.stamina = stamina
        self.stats = {
            'goals': 0,
            'assists': 0,
            'shots': 0,
            'passes': 0,
            'tackles': 0,
            'interceptions': 0,
            'fouls_committed': 0,
            'fouls_suffered': 0,
            'possession_time': 0  # in arbitrary units
        }

    def __repr__(self) -> str:
        return f"Player(name='{self.name}', offense={self.offense}, defense={self.defense})"

    def to_dict(self) -> Dict:
        """Convert player stats to dictionary for DataFrame."""
        return {
            'Player': self.name,
            'Goals': self.stats['goals'],
            'Assists': self.stats['assists'],
            'Shots': self.stats['shots'],
            'Passes': self.stats['passes'],
            'Tackles': self.stats['tackles'],
            'Interceptions': self.stats['interceptions'],
            'Fouls Committed': self.stats['fouls_committed'],
            'Fouls Suffered': self.stats['fouls_suffered'],
            'Possession Time': self.stats['possession_time']
        }


class Team:
    """Represents a football team with players and match statistics."""
    
    def __init__(self, name: str, players: List[Player]):
        self.name = name
        self.players = players
        self.score = 0
        self.possession = 0  # in arbitrary units
        self.stats = {
            'goals_scored': 0,
            'shots_on_target': 0,
            'shots_off_target': 0,
            'passes_completed': 0,
            'passes_attempted': 0,
            'tackles_won': 0,
            'interceptions_made': 0,
            'fouls_committed': 0,
            'fouls_suffered': 0,
            'possession_percentage': 0.0
        }

    def get_offensive_players(self) -> List[Player]:
        """Get players sorted by offensive ability."""
        return sorted(self.players, key=lambda p: p.offense, reverse=True)

    def get_defensive_players(self) -> List[Player]:
        """Get players sorted by defensive ability."""
        return sorted(self.players, key=lambda p: p.defense, reverse=True)

    def __repr__(self) -> str:
        return f"Team(name='{self.name}', score={self.score})"

    def to_dict(self) -> Dict:
        """Convert team stats to dictionary for DataFrame."""
        return {
            'Team': self.name,
            'Goals Scored': self.stats['goals_scored'],
            'Shots on Target': self.stats['shots_on_target'],
            'Shots off Target': self.stats['shots_off_target'],
            'Passes Completed': self.stats['passes_completed'],
            'Passes Attempted': self.stats['passes_attempted'],
            'Tackles Won': self.stats['tackles_won'],
            'Interceptions Made': self.stats['interceptions_made'],
            'Fouls Committed': self.stats['fouls_committed'],
            'Fouls Suffered': self.stats['fouls_suffered'],
            'Possession %': f"{self.stats['possession_percentage']:.2f}%"
        }


def simulate_game_event(team_a: Team, team_b: Team) -> None:
    """Simulates a single event within the game."""

    # Determine which team has possession based on a rough probability
    if team_a.possession >= team_b.possession:
        current_possessor = random.choices([team_a, team_b], weights=[0.4, 0.6], k=1)[0]
    else:
        current_possessor = random.choices([team_a, team_b], weights=[0.6, 0.4], k=1)[0]

    opponent_team = team_a if current_possessor == team_b else team_b

    # Assign possession time (arbitrary unit)
    possession_duration = random.randint(1, 10)
    current_possessor.possession += possession_duration

    # Select a player for the action from the possessing team
    action_player = get_weighted_random_player(current_possessor.players, 'offense')
    action_player.stats['possession_time'] += possession_duration

    event_type = random.choices(
        ['pass', 'shot', 'tackle', 'foul', 'interception'],
        weights=[0.4, 0.3, 0.15, 0.1, 0.05], k=1)[0]

    if event_type == 'pass':
        action_player.stats['passes'] += 1
        current_possessor.stats['passes_attempted'] += 1
        if random.random() < 0.75:  # 75% pass completion rate
            current_possessor.stats['passes_completed'] += 1
            # Simulate another player receiving an assist chance
            if random.random() < 0.3:  # 30% chance for an assist opportunity
                receiver = get_weighted_random_player(current_possessor.players, 'offense')
                if receiver != action_player and random.random() < 0.5:  # 50% chance if different player
                    receiver.stats['assists'] += 1

    elif event_type == 'shot':
        action_player.stats['shots'] += 1

        # Select a defensive player from the opponent to contest the shot
        defensive_player = get_weighted_random_player(opponent_team.players, 'defense')

        # Shot success depends on offensive player's skill vs. defensive player's skill
        shot_chance = action_player.offense * 0.1 - defensive_player.defense * 0.05 + random.uniform(0.1, 0.5)

        if shot_chance > 0.6:  # Goal!
            current_possessor.score += 1
            current_possessor.stats['goals_scored'] += 1
            action_player.stats['goals'] += 1
            current_possessor.stats['shots_on_target'] += 1
        elif shot_chance > 0.3:  # Shot on target, but saved/missed by small margin
            current_possessor.stats['shots_on_target'] += 1
        else:  # Shot off target
            current_possessor.stats['shots_off_target'] += 1

    elif event_type == 'tackle':
        # An offensive player attempts to tackle an opposing player
        tackler = get_weighted_random_player(opponent_team.players, 'defense')
        action_player.stats['fouls_suffered'] += 1
        tackler.stats['tackles'] += 1

        if random.random() < 0.6:  # 60% chance tackle is successful
            opponent_team.stats['tackles_won'] += 1
        else:
            # Missed tackle, possibly a foul
            if random.random() < 0.4:  # 40% chance of foul on missed tackle
                tackler.stats['fouls_committed'] += 1
                opponent_team.stats['fouls_committed'] += 1

    elif event_type == 'interception':
        interceptor = get_weighted_random_player(opponent_team.players, 'defense')
        interceptor.stats['interceptions'] += 1
        opponent_team.stats['interceptions_made'] += 1
        # Possession changes
        current_possessor.possession -= possession_duration
        opponent_team.possession += possession_duration

    elif event_type == 'foul':
        fouler = get_weighted_random_player(current_possessor.players, 'defense')
        fouler.stats['fouls_committed'] += 1
        current_possessor.stats['fouls_committed'] += 1
        # Opponent suffers foul
        fouled_player = get_weighted_random_player(opponent_team.players, 'offense')
        fouled_player.stats['fouls_suffered'] += 1
        opponent_team.stats['fouls_suffered'] += 1


def run_simulation(team_a: Team, team_b: Team, num_events: int) -> Dict:
    """Runs the full game simulation and returns match results."""
    for _ in range(num_events):
        simulate_game_event(team_a, team_b)

    # Calculate possession percentage
    total_possession_time = team_a.possession + team_b.possession
    if total_possession_time > 0:
        team_a.stats['possession_percentage'] = (team_a.possession / total_possession_time) * 100
        team_b.stats['possession_percentage'] = (team_b.possession / total_possession_time) * 100

    return {
        'team_a_name': team_a.name,
        'team_a_score': team_a.score,
        'team_b_name': team_b.name,
        'team_b_score': team_b.score,
        'team_a': team_a,
        'team_b': team_b
    }


def display_player_statistics(team: Team) -> pd.DataFrame:
    """Returns player statistics as a DataFrame."""
    player_data = [player.to_dict() for player in team.players]
    df = pd.DataFrame(player_data)
    return df.set_index('Player')


def display_team_statistics(team: Team) -> pd.DataFrame:
    """Returns team statistics as a DataFrame."""
    team_data = [team.to_dict()]
    df = pd.DataFrame(team_data)
    return df.set_index('Team')


def create_teams() -> Tuple[Team, Team]:
    """Creates and returns two teams with players."""
    # Team A Players
    player1_a = Player("Leo Messi", 95, 30, 85)
    player2_a = Player("Kylian Mbappe", 90, 40, 90)
    player3_a = Player("Sergio Ramos", 60, 90, 75)
    player4_a = Player("Kevin De Bruyne", 88, 55, 88)
    player5_a = Player("Virgil van Dijk", 50, 92, 80)

    team_a_players = [player1_a, player2_a, player3_a, player4_a, player5_a]

    # Team B Players
    player1_b = Player("Cristiano Ronaldo", 92, 35, 88)
    player2_b = Player("Erling Haaland", 90, 30, 87)
    player3_b = Player("Ruben Dias", 55, 91, 78)
    player4_b = Player("Luka Modric", 85, 60, 85)
    player5_b = Player("Achraf Hakimi", 75, 80, 92)

    team_b_players = [player1_b, player2_b, player3_b, player4_b, player5_b]

    # Create Teams
    team_a = Team("FC Alpha", team_a_players)
    team_b = Team("Sporting Beta", team_b_players)

    return team_a, team_b


def print_match_result(team_a: Team, team_b: Team) -> None:
    """Prints the match result."""
    print(f"\n{'='*60}")
    print(f"MATCH RESULT: {team_a.name} {team_a.score} - {team_b.score} {team_b.name}")
    print(f"{'='*60}\n")


def print_all_statistics(team_a: Team, team_b: Team) -> None:
    """Prints all team and player statistics."""
    print(f"\n{'='*60}")
    print(f"{team_a.name} - Overall Team Statistics")
    print(f"{'='*60}")
    print(display_team_statistics(team_a))

    print(f"\n{'-'*60}")
    print(f"{team_a.name} - Player Statistics")
    print(f"{'-'*60}")
    print(display_player_statistics(team_a))

    print(f"\n{'='*60}")
    print(f"{team_b.name} - Overall Team Statistics")
    print(f"{'='*60}")
    print(display_team_statistics(team_b))

    print(f"\n{'-'*60}")
    print(f"{team_b.name} - Player Statistics")
    print(f"{'-'*60}")
    print(display_player_statistics(team_b))


def main():
    """Main function to run the simulation."""
    print("Starting football match simulation...")
    print(f"Total events: {TOTAL_GAME_EVENTS}\n")

    team_a, team_b = create_teams()
    result = run_simulation(team_a, team_b, TOTAL_GAME_EVENTS)

    print_match_result(team_a, team_b)
    print_all_statistics(team_a, team_b)


if __name__ == "__main__":
    main()
