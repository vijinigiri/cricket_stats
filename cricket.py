import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import numpy as np
import os
from datetime import date,datetime,timedelta



print("*"*20)
def stream_data(info):
    for word in info.split(" "):
        yield word + " "
        time.sleep(0.01) 
# ------------------------------------------------------------
def get_info(url):
    st.session_state.header = st.session_state.header+1
    # if st.session_state.header>(len(headers)-1):
    try:
        req = requests.get(url, headers=headers[st.session_state.header])
        if req.status_code != 200:
            print(st.session_state.header)
            get_info(url)
    except:
        if st.session_state.api_val:
            with open(r"general\api_val.txt", "w") as file:
                file.write(str(datetime.today()+timedelta(hours=1)))
            st.session_state.api_val = 0
            req = 0
        print("api limit reached")
    return req

def check_val(country_val,country_id,days):
    if (not country_val.get(country_id)) or (date.today() - datetime.strptime(country_val.get(country_id),"%Y-%m-%d").date()).days>=days:
        return 1
    return 0

def remove_keys(players_id,a,b):
    try:
        players_id.pop(a)
        players_id.pop(b)
    except:
        pass
    return players_id
try:
    headers =[
            {
                "x-rapidapi-key": "2b8ae4a5b8msh30e1bddbe325be3p198900jsna26953e54a55",
                "x-rapidapi-host": "crickbuzz-official-apis.p.rapidapi.com"},
            {
                "x-rapidapi-key": "635725eaebmshf9e7e4347e216adp14034bjsn8fddb20e0349", 
                "x-rapidapi-host": "crickbuzz-official-apis.p.rapidapi.com"},
            {   
                "x-rapidapi-key": "55ecf0254dmshf0b4ab050e05a88p1c79a9jsnf1b21755a950",
                "x-rapidapi-host": "crickbuzz-official-apis.p.rapidapi.com"}
            ]
    if "player" not in st.session_state:
        st.session_state.player = ""
    if "player_id" not in st.session_state:
        st.session_state.player_id = ""
    if "header" not in st.session_state:
        st.session_state.header=0
    if "val" not in st.session_state:
        st.session_state.val=0
    if 'info' not in st.session_state :
        st.session_state.info = 0
    if 'batting_stats' not in st.session_state :
        st.session_state.batting_stats=0
    if 'bowling_stats' not in st.session_state :
        st.session_state.bowling_stats=0
    if "prev_country_id" not in st.session_state:
        st.session_state.prev_country_id = 0
    if 'players_id' not in st.session_state:
        st.session_state.players_id = 0
    if 'abc' not in st.session_state:
        st.session_state.abc = 0
    if "player_val" not in st.session_state:
        with open(r"general\player_val.json", "r") as file:
            st.session_state.player_val = json.load(file)
    if "country_val" not in st.session_state:
        with open(r"general\country_val.json", "r") as file:
            st.session_state.country_val = json.load(file)
    if "team_id" not in st.session_state:
        with open (r"general\teams_id.json","r") as file:
            st.session_state.team_id = json.load(file)
    if "api_val" not in st.session_state:
        with open(r"general\api_val.txt", "r") as file:
            st.session_state.api_val = file.read()
        if (datetime.today() - datetime.strptime(st.session_state.api_val,"%Y-%m-%d %H:%M:%S.%f")).days>=1:
            st.session_state.api_val = 1
        else : 
            st.session_state.api_val = 0

    st.session_state.country_name = st.sidebar.selectbox("select country:", st.session_state.team_id.keys())
    st.session_state.country_id = st.session_state.team_id[st.session_state.country_name]

    today = date.today()
    if st.session_state.country_id != st.session_state.prev_country_id:
        st.session_state.c_val = check_val(st.session_state.country_val,st.session_state.country_id,10)

    # playe id 
    a = 0
    if  st.session_state.api_val and st.session_state.c_val: 
        try:  
            url = f"https://crickbuzz-official-apis.p.rapidapi.com/team/{st.session_state.country_id}/players"
            response_player_id = requests.get(url, headers=headers[st.session_state.header])
            if response_player_id.status_code != 200:
                response_player_id = get_info(url)
            st.session_state.players_id = {i.get("name"):i.get('id') for i in response_player_id.json()["player"]}
            st.session_state.players_id = remove_keys(st.session_state.players_id,"ALL ROUNDER","WICKET KEEPER")
            st.session_state.player = st.sidebar.selectbox("select Player:", st.session_state.players_id.keys())
            st.session_state.player_id = st.session_state.players_id[st.session_state.player]
            st.session_state.country_val[st.session_state.country_id] = str(date.today())
            with open(r"general/country_val.json", "w") as file:
                json.dump(st.session_state.country_val, file, indent=4)
            with open(r"general/team_players_id.json","r") as file:
                ab = json.load(file)
            ab[st.session_state.country_name] = st.session_state.players_id 
            with open(r"general/team_players_id.json","w") as f:
                json.dump(ab,f,indent=4)
        except:
            a = 1
    elif (not (st.session_state.api_val and st.session_state.c_val)) or a:
        with open(r"general/team_players_id.json","r") as file:
            ab = json.load(file)
        st.session_state.players_id = ab[st.session_state.country_name]
        st.session_state.player = st.sidebar.selectbox("select Player:",st.session_state.players_id.keys())
        st.session_state.player_id = str(st.session_state.players_id[st.session_state.player])
        # st.write(type(st.session_state.player_id))
    st.session_state.val = check_val(st.session_state.player_val,st.session_state.player_id,3)

    st.session_state.prev_country_id = st.session_state.country_id
    # ------------------------------------------------------------------
    a = 0
    print("country_val :",st.session_state.c_val)
    print("palyer :",st.session_state.player)
    print("player_id :",st.session_state.player_id)
    print("palyer val:",st.session_state.val)
    print("api_val:",st.session_state.api_val)
    if st.sidebar.button("get information")  and  st.session_state.player_id is not None:    
        # -----------------------------------------------------------------
        if st.session_state.api_val and st.session_state.val:
            # players info
            try:
                url = f"https://crickbuzz-official-apis.p.rapidapi.com/browse/player/{ st.session_state.player_id}"
                response_player_info = requests.get(url, headers=headers[st.session_state.header])
                if response_player_info.status_code != 200:
                    response_player_info = get_info(url)
                st.session_state.info = pd.json_normalize(response_player_info.json())
                file_name = fr"information/{st.session_state.country_name}info.xlsx"
                sheet_name = st.session_state.player_id
                if os.path.exists(file_name):
                    with pd.ExcelWriter(file_name, mode='a', engine='openpyxl',if_sheet_exists = "replace") as writer:
                        st.session_state.info.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                        st.session_state.info.to_excel(writer, sheet_name=sheet_name, index=False)
            except:
                a=0
            print(f"{st.session_state.player} batting information")
            # ------------------------------------------------------------------------ 
            # batting stats
            try:
                url = f"https://crickbuzz-official-apis.p.rapidapi.com/browse/player/{ st.session_state.player_id}/batting"
                response_batting_info = requests.get(url, headers=headers[st.session_state.header])
                if response_batting_info.status_code != 200:
                    response_batting_info = get_info(url)
                st.session_state.batting_stats = pd.DataFrame([row['values'] for row in response_batting_info.json()['values']], columns=response_batting_info.json()['headers'])
                st.session_state.batting_stats = st.session_state.batting_stats.set_index("ROWHEADER")
                st.session_state.batting_stats = st.session_state.batting_stats.T.reset_index()
                st.session_state.batting_stats.rename({"index":"match"},axis = 1 ,inplace=True)

                file_name = fr"batting/{st.session_state.country_name}batting.xlsx"
                sheet_name = st.session_state.player_id
                if os.path.exists(file_name):
                    with pd.ExcelWriter(file_name, mode='a', engine='openpyxl',if_sheet_exists = "replace") as writer:
                        st.session_state.batting_stats.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                        st.session_state.batting_stats.to_excel(writer, sheet_name=sheet_name, index=False)
            except:
                a=0
            print(f"{st.session_state.player} batting information")
            # ---------------------------------------------------------------------------
            # bowling stats
            try:
                url = f"https://crickbuzz-official-apis.p.rapidapi.com/browse/player/{ st.session_state.player_id}/bowling"
                response_bowling_info = requests.get(url, headers=headers[st.session_state.header])
                if response_bowling_info.status_code != 200:
                    response_bowling_info = get_info(url)
                st.session_state.bowling_stats = pd.DataFrame([row['values'] for row in response_bowling_info.json()['values']], columns=response_bowling_info.json()['headers'])
                st.session_state.bowling_stats = st.session_state.bowling_stats.set_index("ROWHEADER")
                st.session_state.bowling_stats = st.session_state.bowling_stats.T.reset_index()
                st.session_state.bowling_stats.rename({"index":"match"},axis = 1 ,inplace=True)

                file_name = fr"bowling/{st.session_state.country_name}bowling.xlsx"
                sheet_name = st.session_state.player_id
                if os.path.exists(file_name):
                    with pd.ExcelWriter(file_name, mode='a', engine='openpyxl',if_sheet_exists = "replace") as writer:
                        st.session_state.bowling_stats.to_excel(writer, sheet_name=sheet_name, index=False)
                else:
                    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                        st.session_state.bowling_stats.to_excel(writer, sheet_name=sheet_name, index=False)
            except:
                pass
            print(f"{st.session_state.player} batting information")
            # -----------------------------------------------
            st.session_state.player_val[st.session_state.player_id] = str(date.today())
            with open(r"general\player_val.json", "w") as file:
                json.dump(st.session_state.player_val, file, indent=4)

        elif (not (st.session_state.api_val and st.session_state.val)) or a: 
            try:
                st.session_state.batting_stats = pd.read_excel(fr"batting/{st.session_state.country_name}batting.xlsx",sheet_name=None)
                st.session_state.batting_stats = st.session_state.batting_stats[st.session_state.player_id]
                st.session_state.bowling_stats = pd.read_excel(fr"bowling/{st.session_state.country_name}bowling.xlsx",sheet_name=None)
                st.session_state.bowling_stats = st.session_state.bowling_stats[st.session_state.player_id]
                st.session_state.info = pd.read_excel(fr"information/{st.session_state.country_name}info.xlsx",sheet_name=None)
                st.session_state.info = st.session_state.info[st.session_state.player_id]
                print("information loaded")
            except Exception as e:
                print("exc ",e)
        st.session_state.abc=1
        # -------------------------------------------------------------
    if st.session_state.abc:
        st.markdown(f" <span style='font-size: 40px;'> {st.session_state.info.loc[0,'name']}<span> <small style='font-size: 20px;'>{st.session_state.info.loc[0,"role"]}<small>",unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

            
        lst = ["bat","bowl","height","DoB"] 
        col_lst = [col1,col2,col3,col4]
        col = 0
        for i in lst:
            try:
                s = f"**{i}:** {st.session_state.info.loc[0, i]}"
                col_lst[col].write_stream(stream_data(s))
                col = col+1
            except :
                pass

        col5,_ = st.columns(2)
        col6, col7, col8 = st.columns(3)

        col5.write_stream(stream_data("ICC RANKINGS"))

        lst = ["rankings.bat.testRank","rankings.bat.odiRank","rankings.bat.t20Rank"] 
        col_lst = [col6,col7,col8]
        col = 0
        for i in lst:
            try:
                s = f"**{i.split('.')[2]}:** {st.session_state.info.loc[0, i]}"
                col_lst[col].write_stream(stream_data(s))
                col = col+1
            except :
                pass

        st.write_stream(stream_data(("-- -- "*20)))
        # --------------------------------------------------------------------
        st.markdown(f"<span style='font-size: 40px;'> Bowing Information <span>",unsafe_allow_html=True)
        # --------------------------------------------------------------------
        plt1,plt2 = st.columns(2)
        plt3,plt4 = st.columns(2)

        fig1 = px.bar(st.session_state.batting_stats,x = st.session_state.batting_stats["match"] ,y=st.session_state.batting_stats["Matches"],text_auto=True)
        fig1.update_layout(yaxis=dict(title = "No of Mathces",side="left"),title = "Total Mathces Played")
        plt1.plotly_chart(fig1,key="fig1")
        # ---------------------------------------------------
        fig2 = px.bar(st.session_state.batting_stats,x = st.session_state.batting_stats["match"] ,y=st.session_state.batting_stats["Runs"],text_auto=True)
        fig2.update_layout(title = "Total Runs")
        plt2.plotly_chart(fig2,key="fig2")
        # ---------------------------------------------------
        ab = (st.session_state.batting_stats["Fours"].astype(int)/(st.session_state.batting_stats["Balls"].astype(int)/6))*100
        ac = (st.session_state.batting_stats["Sixes"].astype(int)/(st.session_state.batting_stats["Balls"].astype(int)/6))*100
        df_melted = st.session_state.batting_stats[["match","Fours","Sixes"]].melt(id_vars=['match'], var_name='Type', value_name='Value %')
        df_melted["Value %"] = pd.concat([ab,ac]).values
        fig3 = px.bar(df_melted,x = "match" ,y = "Value %" ,color = "Type",barmode="group" ,text_auto=True)
        fig3.update_layout(
            yaxis=dict(range=[0, 100]),
            title = "Chances of Hitting Fours and Sixes Per Over"
        )
        plt3.plotly_chart(fig3,key="fig3")
        # ---------------------------------------------------
        df_melted = st.session_state.batting_stats[["match","Average","SR"]].melt(id_vars=['match'], var_name='Type', value_name='Value')
        fig4 = px.bar(df_melted,x = "match" ,y = "Value" ,color = "Type",barmode="group" ,text_auto=True)
        fig4.update_layout(title = "Total Average and Strike Rate")
        plt4.plotly_chart(fig4,key="fig4")
        # ---------------------------------------------------
        col9,col10 = st.columns(2)
        feature1 = col9.selectbox("feature1",st.session_state.batting_stats.columns.values[1:]) 
        bat_col = np.concatenate(([None],st.session_state.batting_stats.columns.values[1:]))
        feature2 = col10.selectbox("feature2",bat_col[bat_col!=feature1])
        if feature2 is not None:
            fig5 = go.Figure()
            fig5.add_trace(go.Bar(
                x=st.session_state.batting_stats["match"],y=st.session_state.batting_stats[feature1],
                name=feature1,yaxis="y1",offsetgroup=1 
            ))
            fig5.add_trace(go.Bar(
                x=st.session_state.batting_stats["match"],y=st.session_state.batting_stats[feature2],
                name=feature2,yaxis="y2",offsetgroup=2 
            ))
            fig5.update_layout(
                barmode="group",
                yaxis=dict(title = feature1,side="left"),
                yaxis2=dict(title=feature2,overlaying="y",side="right",showgrid=False
                ))
        else:
            fig5 = px.bar(x = st.session_state.batting_stats["match"] ,y=st.session_state.batting_stats[feature1],text_auto=True)
        st.plotly_chart(fig5,key="fig5")
        # ------------------------------------------------------------------------------------------
        st.markdown("---")
        st.markdown(f"<span style='font-size: 40px;'> Batting Information <span>",unsafe_allow_html=True)
        # ------------------------------------------------------------------------------------------

        plt5,plt6 = st.columns(2)
        plt7,plt8 = st.columns(2)

        fig6 = px.bar(x = st.session_state.bowling_stats["match"] ,y=st.session_state.bowling_stats["Wickets"],text_auto=True)
        fig6.update_layout(yaxis=dict(title = "Total No of Wickets Taken",side="left"),title = "Total Wickets Taken")
        plt5.plotly_chart(fig6,key="fig6")
        # ----------------------------------
        fig7 = px.bar(x = st.session_state.bowling_stats["match"] ,y=(st.session_state.bowling_stats["Balls"].astype(int)/6).astype(int),text_auto=True)
        fig7.update_layout(title = "Total Overs",yaxis=(dict(title="No Of Overs")),xaxis=(dict(title="Match")))
        plt6.plotly_chart(fig7,key="fig7")
        # ---------------------------------
        ab = (st.session_state.bowling_stats["Wickets"].astype(int)/st.session_state.bowling_stats["Balls"].astype(int)/6)*100
        fig8 = px.bar(x = st.session_state.bowling_stats["match"] ,y = ab ,text_auto=True)
        fig8.update_layout(
            yaxis=dict(range=[0, 100])   # Y-axis from 0 to 100
        )
        fig8.update_layout(title = "Chances of Taking Wickets Per Over",yaxis=(dict(title="value %")),xaxis=(dict(title="Match")))

        plt7.plotly_chart(fig8,key="fig8")
        # ---------------------------------
        fig9 = go.Figure()
        fig9.add_trace(go.Bar(
            x=st.session_state.bowling_stats["match"],y=st.session_state.bowling_stats["Eco"],
            name=feature1,yaxis="y1",offsetgroup=1 
        ))
        fig9.add_trace(go.Bar(
            x=st.session_state.bowling_stats["match"],y=st.session_state.bowling_stats["SR"],
            name=feature2,yaxis="y2",offsetgroup=2 
        ))
        fig9.update_layout(
            title = "Total Economy and Strike Rate",
            barmode="group",
            yaxis=dict(title = feature1,side="left"),
            yaxis2=dict(title=feature2,overlaying="y",side="right",showgrid=False
            ))
        plt8.plotly_chart(fig9,key="fig9")
        # -----------------------------------
        col9,col10 = st.columns(2)
        feature1 = col9.selectbox("select feature1",st.session_state.bowling_stats.columns.values[1:]) 
        bow_col = np.concatenate(([None],st.session_state.bowling_stats.columns.values[1:]))
        feature2 = col10.selectbox("select feature2",bow_col[bow_col!=feature1])
        if feature2 is not None:
            fig10 = go.Figure()
            fig10.add_trace(go.Bar(
                x=st.session_state.bowling_stats["match"],y=st.session_state.bowling_stats[feature1],
                name=feature1,yaxis="y1",offsetgroup=1 
            ))
            fig10.add_trace(go.Bar(
                x=st.session_state.bowling_stats["match"],y=st.session_state.bowling_stats[feature2],
                name=feature2,yaxis="y2",offsetgroup=2 
            ))
            fig10.update_layout(
                barmode="group",
                yaxis=dict(title = feature1,side="left"),
                yaxis2=dict(title=feature2,overlaying="y",side="right",showgrid=False
                ))
        else:
            fig10 = px.bar(x = st.session_state.bowling_stats["match"] ,y=st.session_state.bowling_stats[feature1],text_auto=True)
        st.plotly_chart(fig10,key="fig10")

        st.write("---")
        st.write(st.session_state.batting_stats)
        st.write(st.session_state.bowling_stats)
except:
    st.write("api limit reached")