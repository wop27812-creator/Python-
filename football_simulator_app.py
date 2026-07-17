import streamlit as st
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Football Game Simulator", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .score-display {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        color: #ff7f0e;
        margin: 20px 0;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>⚽ Football Game Statistics Simulator</h1>", unsafe_allow_html=True)

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

def get_player_statistics_df(team):
    """Returns player statistics as a DataFrame."""
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

def get_team_statistics_df(team):
    """Returns team statistics as a DataFrame."""
    return pd.DataFrame([{
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
    }])

# --- Sidebar Configuration --- #
st.sidebar.header("⚙️ Game Configuration")

# Team A customization
st.sidebar.subheader("Team A Setup")
team_a_name = st.sidebar.text_input("Team A Name", "FC Alpha")
team_a_formation = st.sidebar.selectbox("Team A Formation", ["4-3-3", "3-5-2", "5-3-2", "4-2-3-1"])

# Team B customization
st.sidebar.subheader("Team B Setup")
team_b_name = st.sidebar.text_input("Team B Name", "Sporting Beta")
team_b_formation = st.sidebar.selectbox("Team B Formation", ["4-3-3", "3-5-2", "5-3-2", "4-2-3-1"])

# Game events
game_events = st.sidebar.slider("Total Game Events", min_value=10, max_value=500, value=100, step=10)

# Random seed for reproducibility
use_seed = st.sidebar.checkbox("Use Random Seed (for reproducible results)")
if use_seed:
    seed_value = st.sidebar.number_input("Seed Value", value=42)
    random.seed(seed_value)

# --- Create Default Players --- #
team_a_players = [
    Player("Leo Messi", 95, 30, 85),
    Player("Kylian Mbappe", 90, 40, 90),
    Player("Sergio Ramos", 60, 90, 75),
    Player("Kevin De Bruyne", 88, 55, 88),
    Player("Virgil van Dijk", 50, 92, 80)
]

team_b_players = [
    Player("Cristiano Ronaldo", 92, 35, 88),
    Player("Erling Haaland", 90, 30, 87),
    Player("Ruben Dias", 55, 91, 78),
    Player("Luka Modric", 85, 60, 85),
    Player("Achraf Hakimi", 75, 80, 92)
]

# --- Create Teams --- #
team_a = Team(team_a_name, team_a_players)
team_b = Team(team_b_name, team_b_players)

# --- Run Simulation Button --- #
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("⚽ START SIMULATION", key="simulate", use_container_width=True):
        st.session_state.simulation_run = True
        run_simulation(team_a, team_b, game_events)

# --- Display Results --- #
if st.session_state.get('simulation_run', False):
    
    # Final Score
    st.markdown(f"<div class='score-display'>{team_a.name} {team_a.score} - {team_b.score} {team_b.name}</div>", unsafe_allow_html=True)
    
    # Determine Winner
    if team_a.score > team_b.score:
        winner = f"🏆 {team_a.name} WINS!"
        color = "green"
    elif team_b.score > team_a.score:
        winner = f"🏆 {team_b.name} WINS!"
        color = "green"
    else:
        winner = "🤝 IT'S A DRAW!"
        color = "blue"
    
    st.markdown(f"<h2 style='text-align: center; color: {color};'>{winner}</h2>", unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Team Stats", "👥 Player Stats", "📈 Charts", "🎯 Comparison", "📋 Detailed Stats"])
    
    with tab1:
        st.subheader(f"{team_a.name} - Overall Statistics")
        st.dataframe(get_team_statistics_df(team_a).set_index('Team'), use_container_width=True)
        
        st.subheader(f"{team_b.name} - Overall Statistics")
        st.dataframe(get_team_statistics_df(team_b).set_index('Team'), use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"{team_a.name} - Player Statistics")
            st.dataframe(get_player_statistics_df(team_a).set_index('Player'), use_container_width=True)
        
        with col2:
            st.subheader(f"{team_b.name} - Player Statistics")
            st.dataframe(get_player_statistics_df(team_b).set_index('Player'), use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            team_a_df = get_player_statistics_df(team_a)
            fig_goals_a = px.bar(team_a_df, x='Player', y='Goals', title=f"{team_a.name} - Goals by Player", color='Goals')
            st.plotly_chart(fig_goals_a, use_container_width=True)
        
        with col2:
            team_b_df = get_player_statistics_df(team_b)
            fig_goals_b = px.bar(team_b_df, x='Player', y='Goals', title=f"{team_b.name} - Goals by Player", color='Goals')
            st.plotly_chart(fig_goals_b, use_container_width=True)
        
        fig_possession = go.Figure(data=[go.Pie(labels=[team_a.name, team_b.name], 
                                                values=[team_a.stats['possession_percentage'], team_b.stats['possession_percentage']],
                                                marker=dict(colors=['#1f77b4', '#ff7f0e']))])
        fig_possession.update_layout(title="Possession Distribution")
        st.plotly_chart(fig_possession, use_container_width=True)
    
    with tab4:
        metrics_data = {
            'Metric': ['Goals Scored', 'Shots on Target', 'Passes Completed', 'Tackles Won', 'Possession %'],
            team_a.name: [
                team_a.stats['goals_scored'],
                team_a.stats['shots_on_target'],
                team_a.stats['passes_completed'],
                team_a.stats['tackles_won'],
                round(team_a.stats['possession_percentage'], 2)
            ],
            team_b.name: [
                team_b.stats['goals_scored'],
                team_b.stats['shots_on_target'],
                team_b.stats['passes_completed'],
                team_b.stats['tackles_won'],
                round(team_b.stats['possession_percentage'], 2)
            ]
        }
        
        comparison_df = pd.DataFrame(metrics_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        fig_comparison = px.bar(comparison_df, x='Metric', y=[team_a.name, team_b.name], barmode='group', title="Team Comparison")
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with tab5:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {team_a.name} - Detailed Statistics")
            st.markdown(f"**Shots:** {team_a.stats['shots_on_target']} on target, {team_a.stats['shots_off_target']} off target")
            st.markdown(f"**Pass Accuracy:** {team_a.stats['passes_completed']}/{team_a.stats['passes_attempted']} ({(team_a.stats['passes_completed']/team_a.stats['passes_attempted']*100 if team_a.stats['passes_attempted'] > 0 else 0):.1f}%)")
            st.markdown(f"**Defensive:** {team_a.stats['tackles_won']} tackles, {team_a.stats['interceptions_made']} interceptions")
            st.markdown(f"**Fouls:** {team_a.stats['fouls_committed']} committed, {team_a.stats['fouls_suffered']} suffered")
        
        with col2:
            st.markdown(f"### {team_b.name} - Detailed Statistics")
            st.markdown(f"**Shots:** {team_b.stats['shots_on_target']} on target, {team_b.stats['shots_off_target']} off target")
            st.markdown(f"**Pass Accuracy:** {team_b.stats['passes_completed']}/{team_b.stats['passes_attempted']} ({(team_b.stats['passes_completed']/team_b.stats['passes_attempted']*100 if team_b.stats['passes_attempted'] > 0 else 0):.1f}%)")
            st.markdown(f"**Defensive:** {team_b.stats['tackles_won']} tackles, {team_b.stats['interceptions_made']} interceptions")
            st.markdown(f"**Fouls:** {team_b.stats['fouls_committed']} committed, {team_b.stats['fouls_suffered']} suffered")

else:
    st.info("👈 Configure the game in the sidebar and click 'START SIMULATION' to begin!")
    
    st.subheader("Default Teams Preview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**FC Alpha Players**")
        for player in team_a_players:
            st.markdown(f"- {player.name} (OFF: {player.offense}, DEF: {player.defense})")
    
    with col2:
        st.markdown("**Sporting Beta Players**")
        for player in team_b_players:
            st.markdown(f"- {player.name} (OFF: {player.offense}, DEF: {player.defense})")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Football Game Statistics Simulator | Made with Streamlit ⚽</p>", unsafe_allow_html=True)