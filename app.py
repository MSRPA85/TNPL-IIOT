import streamlit as st
from opcua import Client
import sqlite3
import time
from datetime import datetime

import pickle
from pathlib import Path

import streamlit_authenticator as stauth


def add_db(time1, pm2gsm, pm2speed, pm2moist, papbrk, ashiftprod, bshiftprod, cshiftprod, totdayprod, dt):
    conn = sqlite3.connect('ST_TAG.db')
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS data
    (Time TEXT, gsm TEXT, Speed TEXT, Moisture TEXT, Paper_Status TEXT, A TEXT, B TEXT, C TEXT, Total TEXT, Date Text)""")

    c.execute(""" INSERT INTO data
    (Time, gsm, Speed, Moisture, Paper_Status, A, B, C, Total, Date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (time1, pm2gsm, pm2speed, pm2moist, papbrk, ashiftprod, bshiftprod, cshiftprod, totdayprod, dt))

    conn.commit()
    c.close()
    conn.close()


url = "opc.tcp://192.168.0.5:4845"
client = Client(url)
client.connect()
data = dict()

st.set_page_config(page_title="IIOT", layout="wide")

names = ["Peter Parker", "Rebecca Miller"]
usernames = ["pparker", "rmiller"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "IIOT", "abcdef", cookie_expiry_days=0)
name, authentication_status, username = authenticator.login("Login", "main")

if not authentication_status:
    st.error("Username or Password is incorrect")
if authentication_status is None:
    st.warning("Please enter username & password to login")
if authentication_status:

    st.markdown(
        "<h1 style= 'text-align: center;text-size: 40px;background-color: #06a4ec;border-radius: 15px;font-weight: bolder;'>IIOT_TNPL</h1>",
        unsafe_allow_html=True)

    st.subheader("Hi, This is M.Suthan")
    st.markdown("an automation engineer")
    st.markdown("this is a test web page")
    st.markdown("[Learn more >](https://google.com)")
    st.markdown("Website under development......")
    st.markdown("<h5 style= 'text-align: left;font-size: 28px;color: brown;font-weight: bolder;'>PM2 LIVE Datas:</h5>",
                unsafe_allow_html=True)
    st.markdown("---")


    def function():

        while True:
            try:
                agsm = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.PM2_GSM_Value")
                aspeed = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.PM2_Machine_Speed_Value")
                amoist = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.PM2_Moisture_Value")
                apap = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.Paper_Break")
                aashift = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.PM2_A_SHIFT_PROD")
                abshift = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.PM2_B_SHIFT_PROD")
                acshift = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.PM2_C_SHIFT_PROD")
                atotday = client.get_node("ns=7;s=SIMATIC 300(1).CPU 317-2 PNDP.PM2_TOT_DAY_PROD")
                pm2gsm1 = agsm.get_value()
                pm2speed1 = aspeed.get_value()
                pm2moist1 = amoist.get_value()
                papbrk1 = apap.get_value()
                if papbrk1:
                    a = "PAPER BROKEN"
                    # print(a)
                else:
                    a = "PAPER OK"
                    # print(b)
                pm2ashiftprod1 = aashift.get_value()
                pm2bshiftprod1 = abshift.get_value()
                pm2cshiftprod1 = acshift.get_value()
                pm2totaldayprod1 = atotday.get_value()
                pm2gsm1 = round(pm2gsm1, 2)
                pm2speed1 = round(pm2speed1, 2)
                pm2moist1 = round(pm2moist1, 2)
                pm2ashiftprod1 = round(pm2ashiftprod1, 2)
                pm2bshiftprod1 = round(pm2bshiftprod1, 2)
                pm2cshiftprod1 = round(pm2cshiftprod1, 2)
                pm2totaldayprod1 = round(pm2totaldayprod1, 2)
                data["PM2_GSM"] = float(pm2gsm1)
                data["PM2_SPEED"] = float(pm2speed1)
                data["PM2_MOIST"] = float(pm2moist1)
                data["WEB_STATUS"] = str(a)
                data["A SHIFT_PROD"] = float(pm2ashiftprod1)
                data["B SHIFT_PROD"] = float(pm2bshiftprod1)
                data["C SHIFT_PROD"] = float(pm2cshiftprod1)
                data["TOTAL_DAY_PROD"] = float(pm2totaldayprod1)
                gh(data)

            except Exception as e:
                print(e)


    p = st.empty()
    p1 = st.empty()
    p2 = st.empty()


    def gh(data1):
        x1 = data1.get('PM2_GSM')
        x2 = data1.get('PM2_SPEED')
        x3 = data1.get('PM2_MOIST')
        x4 = data1.get('WEB_STATUS')
        x5 = data1.get('A SHIFT_PROD')
        x6 = data1.get('B SHIFT_PROD')
        x7 = data1.get('C SHIFT_PROD')
        x8 = data1.get('TOTAL_DAY_PROD')

        mytime = datetime.now()
        tm = '{}:{}:{}'.format(mytime.hour, mytime.minute, mytime.second)
        dt = '{}/{}/{}'.format(mytime.month, mytime.day, mytime.year)

        # print(tm, str(x1), str(x2), str(x3), str(x4), str(x5), str(x6), str(x7), str(x8), str(dt))
        add_db(tm, str(x1), str(x2), str(x3), str(x4), str(x5), str(x6), str(x7), str(x8), str(dt))

        a1, a2, a3, a4 = p.columns(4)

        a1.metric("GSM", x1)
        a2.metric("SPEED", x2)
        a3.metric("MOIST", x3)
        a4.metric("WEB_STATUS", x4)
        a5, a6, a7, a8 = p1.columns(4)
        a5.metric("A_SHIFT_PROD", x5)
        a6.metric("B_SHIFT_PROD", x6)
        a7.metric("C_SHIFT_PROD", x7)
        a8.metric("TOTAL_DAY_PROD", x8)

        time.sleep(1)


    function()
