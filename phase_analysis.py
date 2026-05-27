import pandas as pd

def run_analysis():
    print("Loading data...")
    df = pd.read_csv(r'c:\Users\VICTUS\Downloads\att_0_1778303821_c3a907.csv', low_memory=False)
    
    # 1. Clean seasons
    def clean_season(x):
        x = str(x).strip()
        if '/' in x:
            return int(x[:4])
        try:
            return int(float(x))
        except:
            return x

    df['season_clean'] = df['season'].apply(clean_season)
    
    # Define phases
    def get_phase(over):
        if over <= 5: return 'Powerplay'
        elif over <= 14: return 'Middle Overs'
        else: return 'Death Overs'

    df['phase'] = df['over'].apply(get_phase)

    # Filter out matches with no clear winner
    matches = df[['match_id', 'winner', 'team1', 'team2']].drop_duplicates()
    matches = matches[matches['winner'].notna() & (~matches['winner'].isin(['No Result', 'tie', 'abandoned']))]
    valid_match_ids = matches['match_id'].unique()
    
    df_valid = df[df['match_id'].isin(valid_match_ids)]
    
    # Calculate runs for each team in each match and phase
    team_phase_runs = df_valid.groupby(['match_id', 'batting_team', 'phase'])['runs_total'].sum().reset_index()
    
    # Join with matches to get team1/team2 and winner
    team_phase_runs = team_phase_runs.merge(matches, on='match_id')
    
    # Let's map team1 runs and team2 runs.
    t1_runs = team_phase_runs[team_phase_runs['batting_team'] == team_phase_runs['team1']]
    t2_runs = team_phase_runs[team_phase_runs['batting_team'] == team_phase_runs['team2']]
    
    merged_runs = pd.merge(
        t1_runs[['match_id', 'phase', 'runs_total', 'winner', 'team1', 'team2']],
        t2_runs[['match_id', 'phase', 'runs_total']],
        on=['match_id', 'phase'],
        suffixes=('_team1', '_team2')
    )
    
    # Determine the winner of each phase
    def get_winner_of_phase(row):
        if row['runs_total_team1'] > row['runs_total_team2']:
            return row['team1']
        elif row['runs_total_team2'] > row['runs_total_team1']:
            return row['team2']
        else:
            return 'Tie'
            
    merged_runs['phase_winner'] = merged_runs.apply(get_winner_of_phase, axis=1)
    
    # Check if phase winner is the match winner
    merged_runs['phase_winner_won_match'] = merged_runs['phase_winner'] == merged_runs['winner']
    
    print("\n--- PHASE WIN CORRELATION WITH MATCH WIN ---")
    for phase in ['Powerplay', 'Middle Overs', 'Death Overs']:
        phase_data = merged_runs[merged_runs['phase'] == phase]
        # Exclude Ties for clean comparison
        phase_no_ties = phase_data[phase_data['phase_winner'] != 'Tie']
        win_pct = (phase_no_ties['phase_winner_won_match'].sum() / len(phase_no_ties)) * 100
        print(f"{phase}: out of {len(phase_no_ties)} matches with a phase winner, "
              f"the phase winner won the match {phase_no_ties['phase_winner_won_match'].sum()} times ({win_pct:.2f}%)")

if __name__ == "__main__":
    run_analysis()
