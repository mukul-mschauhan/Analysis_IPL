
from types import CodeType
import pandas as pd
import numpy as np
import streamlit as st
st.set_page_config(layout="wide")
import altair as alt
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly as pl
import plotly.express as px # Used for reading the dataset
import plotly.graph_objects as go # Used for plotting the Graphs
from plotly.offline import plot # Use plot function to generate the HTML Output of the plots

# Containers
header = st.container()
dataset = st.container()
about_data = st.container()
empty = st.container()
wins = st.container()
chennaiwins = st.container()
codebutton = st.container()
cskwinbutton = st.container()
missbutton = st.container()
toss = st.container()
venue = st.container()
miss =st.container()
player = st.container()
teams = st.container()
difficult_teams = st.container()
analysis = st.container()


with header:
    st.title("Understanding Data Science using IPL Case Study")
    st.markdown("Here, we will try to derive meaningful insights from the IPL Data")
    #list_actions = ["Dataset", "Impact of Toss", 
                    #"Impact of Cities","Most Impactful Players",
                    #"Top 3 Difficult Teams", "Analysis & Conclusion"]
    #option_data = st.sidebar.checkbox("Dataset")
    #option_toss = st.sidebar.checkbox("Impact of Toss")
    #option_cities = st.sidebar.checkbox("Impact of Cities")
    #option_player = st.sidebar.checkbox("Most Impactful Players")
    #option_teams = st.sidebar.checkbox("Top 3 Difficult Teams")
    #option_analysis= st.sidebar.checkbox("Analysis & Conclusion")
    #check_boxes = [st.sidebar.checkbox(i, key=i) for i in list_actions]
    
def callingdata():
    st.header("Analyising Patterns Using CSK IPL Data ")
    st.text("Here we will see the...")
    match = pd.read_csv("data/Matches.csv") 
    return(st.write(match.head(10)))
    
with dataset:
    match = pd.read_csv("data/Matches.csv")
    if st.sidebar.checkbox("Dataset"):
        callingdata()


with about_data: # Checking the Shape and Size of the Data
    if st.sidebar.checkbox("Shape & Info"):
        st.header("Lets Check the Info of the Dataset")
        st.write("The IPL Dataset has: ", 
                 match.shape[0], "Rows & ", match.shape[1], "columns")
        st.write(match.describe())


with wins: # Summary of the Games won by each time per season
    if st.sidebar.checkbox("Summary of Wins"):    
        st.header("Summary of the Games Won in every Season")
        summary_df = match.groupby(['season',
                                    'winner']).size().reset_index(name = "No of Games Won")
        st.write(summary_df)
        st.markdown("**Note - ** This is the Summary of Games Won by All Teams across Different Seasons.")

# Creating BarChart Function
def barcharts(headertext, df, x, y):
    st.header(headertext)
    fig = go.Figure([go.Bar(x = df[x], y = df[y],
                            marker_color = "#ff7f50")]).update_layout(xaxis_title = x, yaxis_title = y)
    st.write(fig)
    
def bar_chart():
    st.header("No of Matches Won by CSK")
    fig = go.Figure([go.Bar(x = chennai_wins["season"], 
                            y= chennai_wins["No of Games Won"],
                            marker_color = "indianred")]).update_layout(xaxis_title = "Season", 
                                                                        yaxis_title="Matches Won")
    st.write(fig)
    

with chennaiwins:
    if st.sidebar.checkbox("Games Won by CSK"):
        st.header("Summary of Wins by Chennai Super Kings")
        chennai_wins = summary_df[summary_df['winner']=='Chennai Super Kings']
        st.write(chennai_wins.head(15))
        total_wins = chennai_wins["No of Games Won"].sum()
        st.write("The Total No of Matches Won by CSK are", total_wins)
        barcharts("No of Matches Won by CSK", chennai_wins, "season", "No of Games Won")

with toss:
    chennai = match.loc[match["team1"]=="Chennai Super Kings",]
    
    if st.sidebar.checkbox("Impact of Toss"):
        st.header("Impact of Toss on Win %Age of CSK")
        st.markdown("Now we will Filter the Team by CSK and Create a \
            DataFrame where the **Team 1** will bs **CSK**.\
            Here is the DataFrame with Team 1 as CSK.\
                Here we want to know **what is Win %Age** when \
                    CSK **wins the Toss & the Match**")
        
        #with codebutton:
            #pressed = st.button("See the Code", key="chennai")
        #if pressed:
        with st.echo():
            chennai = match.loc[match["team1"]=="Chennai Super Kings",]
        st.write(chennai.head())
        
        st.markdown("Now in order to know the Impact of the Toss, \
            We will Find the Instances where **CSK Won the Toss & the Match**")
        
        chennai_wtm = chennai[(chennai["toss_winner"]=="Chennai Super Kings")\
            & (chennai["winner"]=="Chennai Super Kings")]
        wtm = np.round((chennai_wtm.shape[0]/chennai.shape[0])*100, 2)
        
        with cskwinbutton:
            pressed = st.button("See the Code", key = "cskwin")
        if pressed:
            with st.echo():
                chennai_wtm = chennai[(chennai["toss_winner"]=="Chennai Super Kings")\
                    & (chennai["winner"]=="Chennai Super Kings")]
                wtm = np.round((chennai_wtm.shape[0]/chennai.shape[0])*100, 2)
            
        chennai_ltm = chennai[(chennai["toss_winner"]!="Chennai Super Kings")\
            & (chennai["winner"]=="Chennai Super Kings")]
        ltm = np.round((chennai_ltm.shape[0]/chennai.shape[0])*100, 2)
        
        st.write("The Win Percentage (Won Toss & Match) is ", wtm)
        st.write("The Win Percentage (Lost Toss & But Won Match) is ", ltm)
    # Venue
    if st.sidebar.checkbox("Impact of Venue"):
        st.header("Impact of Venue on Win %Age of CSK")
        st.markdown("Here we want to know if there is **any Impact of City on the  \
                    Performance of CSK**")
        venue = chennai.city.value_counts().rename_axis("Venue").reset_index(name = "Matches Played")
        st.write(venue.head())
        barcharts("Total no. of games played by CSK in each City", 
                  venue, "Venue", "Matches Played")
        # Cities where Chennai has Won the Matches
        venue_win = chennai.loc[chennai["winner"]
                                =="Chennai Super Kings"].city.value_counts().\
                                    rename_axis("Winning_Venue").\
                                        reset_index(name = "Win_Matches")
        st.write(venue_win)
        barcharts("Total no. of Games Won by CSK in each City", 
                  venue_win, "Winning_Venue", "Win_Matches")
        st.markdown("Now we will create a Table that will show the Matches Played in a City vs Won")
        # Merging the Cities where Chennai Played vs Won
        chennai_win = pd.merge(venue, venue_win,
            left_on= ["Venue"],\
                right_on=["Winning_Venue"], how = "left")
        st.write(chennai_win)
 
        
with miss:
    if st.sidebar.checkbox("Missing Values"):
        st.markdown("**We will Impute Zeros in Place of NAs \
            as they represent that the matches were not Played**")
        chennai_win["Win_Matches"].fillna(0, inplace = True)
        chennai_win["Win_Percent"] = np.round((chennai_win["Win_Matches"]\
            /chennai_win["Matches Played"])*100,2)
        st.write(chennai_win)
    
# Who is their most impactful player against each team (man of the match).    
with player:
    if st.sidebar.checkbox("Impactful Player(s)"):
        team_chennai = chennai.loc[chennai["winner"]=="Chennai Super Kings",] # Chennai Data
        # Here we will find out CSK as Winner with Team2, Player of Match & Win By Runs
        csk_win_t1 =  team_chennai[team_chennai['team1']
                        =='Chennai Super Kings'].groupby(['team2',
                                                          'player_of_match','win_by_runs'])\
                                                              .size().reset_index()
        # Passing the Column Name to the Data Frame
        csk_win_t1.columns = ['opposite_team','player_of_match','win_by_runs','no_times_won_as_player_of_match']
        st.header("Who is their Most Impactful Player against each team (Man of the Match).")
        st.write(csk_win_t1)
        st.markdown("**Conclusion** - On the Looks of It, It is clear that MS Dhoni is the most Powerful Player of CSK and a Powerful Captain in the entire Tournament.")
        man_of_match = csk_win_t1.copy()
        man_of_match = man_of_match.groupby(['opposite_team',
                                             'player_of_match','win_by_runs'])\
                                                 .no_times_won_as_player_of_match.agg\
                                                     (["sum"]).reset_index()
        man_of_match.sort_values(by=['sum'],ascending=False, inplace=True)
        man_of_match.reset_index(inplace=True,drop=True)
        man_of_match.columns = ['opposite_team','player_of_match',
                                'win_by_runs','No.of times won MOM']
        man_of_match = man_of_match.groupby(["player_of_match"])\
            .aggregate("sum").reset_index().sort_values("No.of times won MOM", \
                ascending = False)
        man_of_match = csk_win_t1.copy()
        man_of_match = man_of_match.groupby(['opposite_team',
                                             'player_of_match','win_by_runs'])\
                                                 .no_times_won_as_player_of_match.agg(["sum"]).reset_index()
        man_of_match.sort_values(by=['sum'],ascending=False, inplace=True)
        man_of_match.reset_index(inplace=True,drop=True)
        man_of_match.columns = ['opposite_team','player_of_match','win_by_runs','No.of times won MOM']
        man_of_match = man_of_match.groupby(["player_of_match"]).aggregate("sum").reset_index().sort_values("No.of times won MOM", ascending = False)
        barcharts("Top Impactful players of CSK", man_of_match, 'player_of_match', 'No.of times won MOM')
        st.markdown("**It is clearly evident that the SK Raina, MS Dhoni & Hussey are the Top 3 Players of CSK**")

# Code for Impactful Player against All Teams
with teams:
    if st.sidebar.checkbox("Teams"):
        st.markdown("---")
        # Against Kings XI Punjab Player and Max Runs
        st.header("Most Impactful Player Against Kings XI Punjab")
        punjab_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Kings XI Punjab",]\
                        .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Kings XI Punjab",]\
                        .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
        with st.echo():
            st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Kings XI Punjab",]\
                        .sort_values("win_by_runs", ascending = False))
        
        results = f" The Man of The Match Against **Kings XI Punjab** was **{punjab_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        
        st.markdown("---")
        # Against Delhi Dare-Devils
        st.header("Most Impactful Player Against Delhi Daredevils")
        delhi_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Delhi Daredevils",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Delhi Daredevils",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
        with st.echo():
            st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Delhi Daredevils",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **Delhi Daredevils** was **{delhi_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against KT Kerala
        st.header("Most Impactful Player Against KT Kerala")
        kerala_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Kochi Tuskers Kerala",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Kochi Tuskers Kerala",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Kochi Tuskers Kerala",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **Kochi Tuskers Kerala** was **{kerala_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against Deccan Chargers
        st.header("Most Impactful Player Against Deccan Chargers")
        dc_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Deccan Chargers",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Deccan Chargers",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Deccan Chargers",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **Deccan Chargers** was **{dc_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against Mumbai Indians
        st.header("Most Impactful Player Against Mumbai Indians")
        mumbai_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Mumbai Indians",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Mumbai Indians",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Mumbai Indians",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **Mumbai Indians** was **{mumbai_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against KKR
        st.header("Most Impactful Player Against KKR")
        kkr_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Kolkata Knight Riders",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Kolkata Knight Riders",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Kolkata Knight Riders",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **KKR** was **{kkr_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against Pune Warriors
        st.header("Most Impactful Player Against Pune Warriors")
        pune_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Pune Warriors",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Pune Warriors",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Pune Warriors",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **Pune Warriors** was **{pune_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against Rajasthan Royals
        st.header("Most Impactful Player Against RR")
        rr_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Rajasthan Royals",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Rajasthan Royals",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Rajasthan Royals",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **Rajasthan Royals** was **{rr_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against Royal Challengers Blore
        st.header("Most Impactful Player Against RCB")
        blore_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Royal Challengers Bangalore",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Royal Challengers Bangalore",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Royal Challengers Bangalore",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **RCB** was **{blore_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
        # Against Sunrisers Hyderabad
        st.header("Most Impactful Player Against SRH")
        hyd_mom = list(csk_win_t1.loc[csk_win_t1.opposite_team=="Sunrisers Hyderabad",]\
            .sort_values("win_by_runs", ascending = False).player_of_match)[0]

        max_runs = csk_win_t1.loc[csk_win_t1.opposite_team=="Sunrisers Hyderabad",]\
            .sort_values("win_by_runs", ascending = False)["win_by_runs"].max()
            
        st.write(csk_win_t1.loc[csk_win_t1.opposite_team=="Sunrisers Hyderabad",]\
                        .sort_values("win_by_runs", ascending = False))
        results = f" The Man of The Match Against **Sunrisers Hyderabad** was **{hyd_mom}\
            **& the **Max Runs** were **{max_runs}**."
        st.markdown(results)
        st.markdown("---")
        
with difficult_teams:
    if st.sidebar.checkbox("Top 3 Teams"):
        st.header("Top 3 Difficult Teams to Beat...")
        st.markdown("**As per our analysis, \
            CSK has lost a total of 38 matches. \
                They have won for the most number of times \
                    (7 times) against MI and KKR, followed by RR (5 times).**")
        with st.echo():
            lost = chennai.loc[chennai['winner']!='Chennai Super Kings']
        summary = lost.groupby("winner").size().reset_index(name = "No_of_Times_Lost")
        summary.columns = ["Rival Team", "No of Times Lost"]
        sort_summary = summary.sort_values("No of Times Lost", ascending = False)
        st.write(sort_summary)
        top_3 =list(summary.sort_values("No of Times Lost", ascending = False)\
            ["Rival Team"].head(3))
        results = f" The Top **03 Difficult Teams** are **{top_3}**."
        st.markdown(results)
        with st.echo(code_location="below"):
            barcharts("Tough Competitors", 
                      sort_summary, "Rival Team", "No of Times Lost")
        st.markdown("---")
        
        # Mumbai Indians
        st.header("Strategy Against Mumbai Indians")
        toss_win = chennai.groupby(['team1','team2','toss_winner','toss_decision','winner']).size().reset_index()
        toss_win.columns = ['team1', 'team2', 'toss_winner', 'toss_decision', 'winner', 'no_of_matches']
        with st.echo(code_location="above"):
            st.table(toss_win.loc[toss_win['team2'] =='Mumbai Indians'])
        #st.table(toss_win.loc[toss_win['team2'] =='Mumbai Indians'])
        
        st.markdown("**Out of the 12 times CSK has played against MI, \
            they have Won the Toss 5 times, all 5 times they chose to Bat First \
                and Won. Hence, CSK should always choose to Bat First if\
                they Win a toss against MI.**")
        st.markdown("---")
        
        # KKR
        st.header("Strategy Against KKR")
        with st.echo():
            st.table(toss_win.loc[toss_win['team2'] =='Kolkata Knight Riders'])
        st.markdown("**Its clearly evident that When KKR wins the Toss, they have a bigger chance of Winning\.\
            By looking at the Data, KKR's USP is strong fielding that has made it win the Matches.\
                Here the Correct Strategy for CSK would be to have strong Fielding.**")
        st.markdown("---")
        # RR
        st.header("Strategy Against RR")
        with st.echo():
            st.table(toss_win.loc[toss_win['team2'] =='Rajasthan Royals'])
        st.markdown("**When CSK wins the toss,\
            then chances of losing the match increase as CSK has won toss 5/12 \
                times and out of these 5 times, CSK has lost the match 3 times.**")
        st.markdown("---")
        
        # Delhi DareDevils
        st.header("Strategy Against Delhi DareDevils")
        with st.echo():
            st.table(toss_win.loc[toss_win['team2'] =='Delhi Daredevils'])
        st.markdown("**CSK should choose to bat\
            (4 times CSK has won the match by choosing to bat, out of 7 toss wins)**")
        st.markdown("---")
        
        # Kings XI Punjab
        st.header("Strategy Against Kings XI Punjab")
        with st.echo():
            st.table(toss_win.loc[toss_win['team2'] =='Kings XI Punjab'])
        st.markdown("**CSK should choose to bat\
            (6 times CSK has won the match by choosing to bat, out of 7 toss wins)**")
        st.button("This ends the Case Study")     