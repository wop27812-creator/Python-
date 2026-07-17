import streamlit as st
import random
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Football Game Simulator",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚽ Football Game Statistics Simulator")
st.markdown("Simulate a football match between two teams and analyze detailed player and team statistics.")

# --- Helper Functions --- #

def get_weighted_random_player(players, attribute_key):
    """Selects a player based on a weighted random attribute."""
    weights = [getattr(player, attribute_key) for player in players]
    total_weight = sum(weights)
    if total_weight == 0:
        return random.choice(players)
    normalized_weights = [w / total_weight for w in weights]
    return random.choices(players, weights=normalized_weights, k=1)[0]

class Player:
    def __init__(self, name, offense, defense, stamina):
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
            'possession_time': 0
        }

    def __repr__(self):
        return f"Player(name='{self.name}', offense={self.offense}, defense={self.defense})"

class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.score = 0
        self.possession = 0
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

    def get_offensive_players(self):
        return sorted(self.players, key=lambda p: p.offense, reverse=True)

    def get_defensive_players(self):
        return sorted(self.players, key=lambda p: p.defense, reverse=True)

    def __repr__(self):
        return f"Team(name='{self.name}', score={self.score})"


def simulate_game_event(team_a, team_b):
    """Simulates a single event within the game."""
    if team_a.possession >= team_b.possession:
        current_possessor = random.choices([team_a, team_b], weights=[0.4, 0.6], k=1)[0]
    else:
        current_possessor = random.choices([team_a, team_b], weights=[0.6, 0.4], k=1)[0]

    opponent_team = team_a if current_possessor == team_b else team_b

    possession_duration = random.randint(1, 10)
    current_possessor.possession += possession_duration

    action_player = get_weighted_random_player(current_possessor.players, 'offense')
    action_player.stats['possession_time'] += possession_duration

    event_type = random.choices(
        ['pass', 'shot', 'tackle', 'foul', 'interception'],
        weights=[0.4, 0.3, 0.15, 0.1, 0.05], k=1)[0]

    if event_type == 'pass':
        action_player.stats['passes'] += 1
        current_possessor.stats['passes_attempted'] += 1
        if random.random() < 0.75:
            current_possessor.stats['passes_completed'] += 1
            if random.random() < 0.3:
                receiver = get_weighted_random_player(current_possessor.players, 'offense')
                if receiver != action_player and random.random() < 0.5:
                    receiver.stats['assists'] += 1

    elif event_type == 'shot':
        action_player.stats['shots'] += 1
        defensive_player = get_weighted_random_player(opponent_team.players, 'defense')
        shot_chance = action_player.offense * 0.1 - defensive_player.defense * 0.05 + random.uniform(0.1, 0.5)

        if shot_chance > 0.6:
            current_possessor.score += 1
            current_possessor.stats['goals_scored'] += 1
            action_player.stats['goals'] += 1
            current_possessor.stats['shots_on_target'] += 1
        elif shot_chance > 0.3:
            current_possessor.stats['shots_on_target'] += 1
        else:
            current_possessor.stats['shots_off_target'] += 1

    elif event_type == 'tackle':
        tackler = get_weighted_random_player(opponent_team.players, 'defense')
        action_player.stats['fouls_suffered'] += 1
        tackler.stats['tackles'] += 1

        if random.random() < 0.6:
            opponent_team.stats['tackles_won'] += 1
        else:
            if random.random() < 0.4:
                tackler.stats['fouls_committed'] += 1
                opponent_team.stats['fouls_committed'] += 1

    elif event_type == 'interception':
        interceptor = get_weighted_random_player(opponent_team.players, 'defense')
        interceptor.stats['interceptions'] += 1
        opponent_team.stats['interceptions_made'] += 1
        current_possessor.possession -= possession_duration
        opponent_team.possession += possession_duration

    elif event_type == 'foul':
        fouler = get_weighted_random_player(current_possessor.players, 'defense')
        fouler.stats['fouls_committed'] += 1
        current_possessor.stats['fouls_committed'] += 1
        fouled_player = get_weighted_random_player(opponent_team.players, 'offense')
        fouled_player.stats['fouls_suffered'] += 1
        opponent_team.stats['fouls_suffered'] += 1


def run_simulation(team_a, team_b, num_events):
    """Runs the full game simulation."""
    for _ in range(num_events):
        simulate_game_event(team_a, team_b)

    total_possession_time = team_a.possession + team_b.possession
    if total_possession_time > 0:
        team_a.stats['possession_percentage'] = (team_a.possession / total_possession_time) * 100
        team_b.stats['possession_percentage'] = (team_b.possession / total_possession_time) * 100


def display_player_statistics(team):
    """Returns player statistics DataFrame."""
    player_data = []
    for player in team.players:
        player_data.append({
            'Player': player.name,
            'Goals': player.stats['goals'],
            'Assists': player.stats['assists'],
            'Shots': player.stats['shots'],
            'Passes': player.stats['passes'],
            'Tackles': player.stats['tackles'],
            'Interceptions': player.stats['interceptions'],
            'Fouls Committed': player.stats['fouls_committed'],
            'Fouls Suffered': player.stats['fouls_suffered'],
            'Possession Time': player.stats['possession_time']
        })
    return pd.DataFrame(player_data)


def display_team_statistics(team):
    """Returns team statistics DataFrame."""
    team_data = [{
        'Team': team.name,
        'Goals Scored': team.stats['goals_scored'],
        'Shots on Target': team.stats['shots_on_target'],
        'Shots off Target': team.stats['shots_off_target'],
        'Passes Completed': team.stats['passes_completed'],
        'Passes Attempted': team.stats['passes_attempted'],
        'Tackles Won': team.stats['tackles_won'],
        'Interceptions Made': team.stats['interceptions_made'],
        'Fouls Committed': team.stats['fouls_committed'],
        'Fouls Suffered': team.stats['fouls_suffered'],
        'Possession %': f"{team.stats['possession_percentage']:.2f}%"
    }]
    return pd.DataFrame(team_data)


# --- Sidebar Configuration --- #
st.sidebar.header("⚙️ Simulation Settings")
num_events = st.sidebar.slider("Number of Game Events", min_value=50, max_value=200, value=100, step=10)

# --- Create Players --- #
player1_a = Player("Leo Messi", 95, 30, 85)
player2_a = Player("Kylian Mbappe", 90, 40, 90)
player3_a = Player("Sergio Ramos", 60, 90, 75)
player4_a = Player("Kevin De Bruyne", 88, 55, 88)
player5_a = Player("Virgil van Dijk", 50, 92, 80)

team_a_players = [player1_a, player2_a, player3_a, player4_a, player5_a]

player1_b = Player("Cristiano Ronaldo", 92, 35, 88)
player2_b = Player("Erling Haaland", 90, 30, 87)
player3_b = Player("Ruben Dias", 55, 91, 78)
player4_b = Player("Luka Modric", 85, 60, 85)
player5_b = Player("Achraf Hakimi", 75, 80, 92)

team_b_players = [player1_b, player2_b, player3_b, player4_b, player5_b]

# --- Create Teams --- #
team_a = Team("FC Alpha", team_a_players)
team_b = Team("Sporting Beta", team_b_players)

# --- Run Simulation --- #
if st.button("🎮 Run Simulation", use_container_width=True):
    st.info(f"Simulating match between {team_a.name} and {team_b.name} with {num_events} events...")
    
    run_simulation(team_a, team_b, num_events)
    
    # Display Match Result
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.metric(team_a.name, team_a.score)
    with col2:
        st.markdown(f"<h2 style='text-align: center'>Final Score</h2>", unsafe_allow_html=True)
    with col3:
        st.metric(team_b.name, team_b.score)
    
    st.success(f"✅ Match Complete: {team_a.name} {team_a.score} - {team_b.score} {team_b.name}")
    
    # Display Team Statistics
    st.markdown("---")
    st.subheader("📊 Team Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {team_a.name}")
        st.dataframe(display_team_statistics(team_a), use_container_width=True)
    with col2:
        st.markdown(f"### {team_b.name}")
        st.dataframe(display_team_statistics(team_b), use_container_width=True)
    
    # Display Player Statistics
    st.markdown("---")
    st.subheader("👥 Player Statistics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### {team_a.name} Players")
        st.dataframe(display_player_statistics(team_a), use_container_width=True)
    with col2:
        st.markdown(f"#### {team_b.name} Players")
        st.dataframe(display_player_statistics(team_b), use_container_width=True)
else:
    st.info("👈 Click the 'Run Simulation' button to start the match!")
