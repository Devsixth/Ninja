# import sqlite3
import requests
import pandas as pd
import streamlit as st
from sqlalchemy import update
from datetime import datetime, date
from RecDB_Integrated import StockManager, Stock, NinjaCalls, NinjaManager

st.markdown("<h1 style='text-align: center; color: blue;'>Ninja Telegram</h1>", unsafe_allow_html=True)


def to_group(call):
    callg = {'chat_id': "-1001750224466", 'text': call}
    requests.post(url, data=callg).json()


def to_channel(call):
    callc = {'chat_id': "-1001542839898", 'text': call}
    requests.post(url, data=callc).json()


def news():
    # with col3:
        st.header("NEWS")
        news = st.text_input("Enter the News", )
        if st.button("SendNews"):
            st.write(news)
            # to_channel(news)
            # to_group(news)


# sending closure part to Telegram

def call_closure():
    with col2:
        st.header("Call Closure")
        type = st.selectbox("TypeOfClosure", ['<select>', "TSL", "TGT", "SL", "Exit"], 0)
        if type == 'Exit':
            exitrate = st.number_input("ExitRate")
        elif type == 'TSL':
            newsl = st.number_input("NewSLRate")

        stock = st.selectbox("SelectStock", names)
        stock1 = stock.upper()

        nm = NinjaManager()
        qs = nm.get_session().query(NinjaCalls)
        qs0 = qs.where((NinjaCalls.Symbol == stock1) & (NinjaCalls.Date == date.today()))
        qsd = pd.read_sql(qs0.statement, nm.get_session().bind)
        nm.get_session().close()

        if st.button("SendClosure"):
            for i in range(qsd.shape[0]):
                segmt = qsd.iloc[i, 3]
                signal = qsd.iloc[i, 4]
                tgtval = qsd.iloc[i, 7]
                slval = qsd.iloc[i, 6]
                limit = qsd.iloc[i, 5]
                qty = qsd.iloc[i, 13]

                if stock:
                    if type == "TSL":
                        alert = f"{stock1} \n Alert for TSL. Move SL to {newsl}"
                        if segmt == 'Cash':
                            st.write(alert)
                            # to_group(alert)
                            # to_channel(alert)
                        elif (segmt == 'Future') or (segmt == 'Idx'):
                            pass
                            # to_channel(call)
                        ninja_closure_db(stock1, newsl, type, 0)

                    if type == "TGT":
                        if signal == 'BUY':
                            pl = (tgtval - limit) * qty
                        elif signal == 'SELL':
                            pl = (limit - tgtval) * qty
                        call = f"{stock1} \n TGT {tgtval} Achvd. Book Profits {pl}"
                        st.write(call)
                        if segmt == 'Cash':
                            pass
                            # to_group(call)
                            # to_channel(call)
                        elif (segmt == 'Future') or (segmt == 'Idx'):
                            pass
                            # to_channel(call)
                        ninja_closure_db(stock1, pl, type, 0)

                    elif type == "SL":
                        if signal == 'BUY':
                            pl = (slval - limit) * qty
                        elif signal == 'SELL':
                            pl = (limit - slval) * qty
                        call = f"{stock1} \n SL {slval} Hit. Book Loss {pl}"
                        st.write(call)
                        if segmt == 'Cash':
                            pass
                            # to_group(call)
                            # to_channel(call)
                        elif (segmt == 'Future') or (segmt == 'Idx'):
                            pass
                            # to_channel(call)
                        ninja_closure_db(stock1, pl, type, 0)

                    elif type == 'Exit':
                        if signal == 'BUY':
                            pl = (exitrate - limit) * qty
                        elif signal == 'SELL':
                            pl = (limit - exitrate) * qty
                        call = f"{stock1} \n Exit at {exitrate}. Book P/L {pl}"
                        st.write(call)
                        if segmt == 'Cash':
                            pass
                            # to_group(call)
                            # to_channel(call)
                        elif (segmt == 'Future') or (segmt == 'Idx'):
                            pass
                            # to_channel(call)
                        ninja_closure_db(stock1, pl, type, exitrate)


# saving closure part in the table

def ninja_closure_db(stock1, pl, type, exitval):
    nm = NinjaManager()
    if (type == 'SL') or (type == 'TGT'):
        nm.get_session().execute(update(NinjaCalls).where((NinjaCalls.Symbol == stock1) &
                                                          (NinjaCalls.Date == date.today())).
                                 values(dict(Closure=type, PL=pl)))
    elif type == 'Exit':
        nm.get_session().execute(update(NinjaCalls).where((NinjaCalls.Symbol == stock1) &
                                                          (NinjaCalls.Date == date.today())).
                                 values(dict(Closure=type, PL=pl, ExitRate=exitval)))
    elif type == 'TSL':
        nm.get_session().execute(update(NinjaCalls).where((NinjaCalls.Symbol == stock1) &
                                                          (NinjaCalls.Date == date.today())).
                                 values(dict(StopPrice=pl)))

    nm.get_session().commit()
    nm.get_session().close()


# sending call to Telegram

def call_to_tele():
    with col1:
        st.header("Calls to Telegram")
        segment = st.selectbox("Segment", ['<select>', "Cash", "Future", "Idx"], 0)
        stoc = st.selectbox("Select Stock", names)
        stock1 = stoc.upper()
        signal = st.selectbox("OrderType", ['<select>', "BUY", "SELL"], 0)
        lp1 = st.number_input("LimitPrice")
        sp1 = st.number_input("StopPrice")
        tgt1 = st.number_input("Target", )
        if segment:
            if lp1:
                if segment == 'Cash':
                    qty1 = (round(100000 / lp1), 0)
                    qty = f"{qty1[0]} (1 Lakh)"
                elif (segment == 'Future') or (segment == 'Idx'):
                    sm = StockManager()
                    q0 = sm.get_session().query(Stock)
                    q = q0.where(Stock.Symbol == stock1)
                    det = pd.read_sql(q.statement, sm.get_session().bind)
                    lot1 = det['Lot'].tolist()
                    lot = lot1[0]
                    qty = f"{lot} Mar23"
                    sm.get_session().close()

        if st.button("SendCallToTelegram"):
            if segment == 'Cash':
                call = f"{stock1} \n{signal} at {round(lp1, 1)}, TGT - {tgt1}, SL - {sp1}, " \
                       f"QTY = {qty}"
                st.write(call)
                # sending calls to channel and group
                # to_channel(call)
                # to_group(call)
                call_to_db(stock1, signal, lp1, tgt1, sp1, qty1[0], segment)

            elif (segment == 'Future') or (segment == 'Idx'):
                call = f"{stock1} \n{signal} at {round(lp1, 1)}, TGT - {tgt1}, SL - {sp1}, " \
                       f"LOT = {qty}"
                # st.write(call)
                # to_channel(call)
                call_to_db(stock1, signal, lp1, tgt1, sp1, lot, segment)


# saving the call to NinjaCalls table
def call_to_db(stock1, signal, lp1, tgt1, sp1, qty1, segment):
    nm = NinjaManager()
    new_txn = NinjaCalls(Symbol=stock1, Segment=segment, Signal=signal,
                         LimitPrice=lp1, StopPrice=sp1, Target=tgt1, QTY=qty1,
                         Date=date.today(), EntryAt=datetime.now().strftime("%H:%M:%S"), OrderPlacement="No")
    nm.get_session().add(new_txn)
    nm.get_session().commit()
    nm.get_session().close()


if __name__ == "__main__":
    # dividing the streamlit app ino two columns
    col1, col2, col3 = st.columns(3)

    # url for telegram
    url = "https://api.telegram.org/bot5378660401:AAG6VvrbQY4c5Ph3dtIlRdy7E4mmcew67O8/sendmessage"

    # accessing the Symbol column from the table StockProfile
    # conn = sqlite3.connect('Data/DBEngine.db')
    # c = conn.cursor()
    # c.execute("SELECT Symbol FROM StockProfile")
    # results = c.fetchall()
    # names = [row[0] for row in results]
    # names[0] = '<select>'

    # calling the functions to run the app

    # call_to_tele()
    # call_closure()
    news()
