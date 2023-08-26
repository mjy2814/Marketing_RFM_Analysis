import pymysql 
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import smtplib, ssl
from email.mime.text import MIMEText
# import my_naver_account as naver 
import datetime

# customer_list = pd.read_csv('./customer_list2.csv')
conn, curr = None, None
conn = pymysql.connect(host='localhost', user='root', password='1111', db='marketing', charset='utf8')
with conn.cursor() as curs:
    sql = f"SELECT * FROM `customer_list`"
    curs.execute(sql)
    result = curs.fetchall()
conn.commit()
conn.close()
customer_list = pd.DataFrame(result) # 열은 왜 같이 안불러지지..하하ㅏㅏ
customer_list.columns = ['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary',
       'recency_score', 'frequency_score', 'monetary_score', 'RFM_SCORE',
       'product_category_frequently']



st.set_page_config(page_title="뚜기뚜기마케터스", layout="wide")
st.title("RFM Analysis for Target Marketing Strategies")


row3_1, row3_space2, row3_2, row3_space3 = st.columns((1.5, 0.3, 1.5, 0.1))

customer_segmemts_stat = customer_list[["Segment", "Recency", "Frequency", "Monetary"]].groupby("Segment").agg(['mean','median', 'min', 'max', 'count'])
customer_segmemts_stat['Ratio']= (100*customer_segmemts_stat['Monetary']["count"]/customer_segmemts_stat['Monetary']["count"].sum()).round(2)
label_list = []
for i in range(len(customer_segmemts_stat)):
    label_list.append(customer_segmemts_stat.index[i] +' '+str(customer_segmemts_stat['Ratio'].values[i])+' %')
customer_segmemts_stat['label'] = label_list
customer_segmemts_stat = customer_segmemts_stat.droplevel(axis=1,level=0)
customer_segmemts_stat.columns = ['R_mean', 'R_median', 'R_min', 'R_max', 'R_count', 'F_mean', 'F_median', 'F_min', 'F_max', 'F_count', 'M_mean', 'M_median', 'M_min', 'M_max', 'M_count', 'Ration', 'label']

with row3_1:
    st.header("Customer Segmentation")
    tab1, tab2 = st.tabs(["Segments", "Sales"])
    with tab1:
        fig = px.treemap(customer_segmemts_stat, values='R_count', path=['label'])
        st.plotly_chart(fig)
    with tab2:
        fig, ax = plt.subplots()
        fig = px.bar(x=customer_segmemts_stat['M_mean'], y=customer_segmemts_stat.index, orientation='h', \
                     labels=dict(y="Average Sales", x="Segments"))
        st.plotly_chart(fig)

with row3_2:
    st.header("Distribution of RFM")
    tab1, tab2 = st.tabs(["Chart", "Data"])
    with tab1:
        fig = make_subplots(rows=3, cols=1, subplot_titles=("Recency", "Frequency", "Monetary"))            
        Recency = go.Histogram(x=customer_list['Recency'])
        Frequency = go.Histogram(x=customer_list['Frequency'])
        Monetary = go.Histogram(x=customer_list['Monetary'])
        fig.append_trace(Recency, 1, 1)
        fig.append_trace(Frequency, 2, 1)
        fig.append_trace(Monetary, 3, 1)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        tab2 = st.dataframe(customer_list[['Recency', 'Frequency', 'Monetary']].describe().T)

row1_1, row1_space2, row1_2, row1_space3 = st.columns((1, 1.3, 1, 0.1))
with row1_1:
    st.header("Customer List")
    option = st.multiselect(' ', options=('신규 고객', '충성 고객', '잠재적 충성고객', '관심 고객', '이탈 위험 고객', '이탈 고객'))

with row1_2:
    st.header("Ternary Plot")
    option2 = st.multiselect('  ', options=('신규 고객', '충성 고객', '잠재적 충성고객', '관심 고객', '이탈 위험 고객', '이탈 고객'))

row2_1, row2_space2, row2_2, row2_space3 = st.columns((2, 0.1, 1, 0.1))
with row2_1:
    if option != []:
        if len(option) == 1:
            temp = customer_list.loc[customer_list['Segment'] == option[0], \
                                     ['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary', 'RFM_SCORE', 'product_category_frequently']]
            st.dataframe(temp)
        elif len(option) == 2:
            temp = customer_list.loc[(customer_list['Segment'] == option[0])|(customer_list['Segment'] == option[1]), \
                                 ['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary', 'RFM_SCORE', 'product_category_frequently']]
            st.dataframe(temp)
        elif len(option) == 3:
            temp = customer_list.loc[(customer_list['Segment'] == option[0])|(customer_list['Segment'] == option[1])|(customer_list['Segment'] == option[2]), \
                                 ['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary', 'RFM_SCORE', 'product_category_frequently']]
            st.dataframe(temp)
        elif len(option) == 4:
            temp = customer_list.loc[(customer_list['Segment'] == option[0])|(customer_list['Segment'] == option[1])|(customer_list['Segment'] == option[2])|(customer_list['Segment'] == option[3]), \
                                 ['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary', 'RFM_SCORE', 'product_category_frequently']]
            st.dataframe(temp)
        elif len(option) == 5:
            temp = customer_list.loc[(customer_list['Segment'] == option[0])|(customer_list['Segment'] == option[1])|(customer_list['Segment'] == option[2])|(customer_list['Segment'] == option[3])|(customer_list['Segment'] == option[4]), \
                                 ['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary', 'RFM_SCORE', 'product_category_frequently']]
            st.dataframe(temp)
        elif len(option) == 6:
            st.dataframe(customer_list[['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary', 'RFM_SCORE', 'product_category_frequently']])
    else:
        st.dataframe(customer_list[['customer_unique_id', 'Segment', 'Recency', 'Frequency', 'Monetary', 'RFM_SCORE', 'product_category_frequently']])

with row2_2:
    if option2 != []:
        if len(option2) == 1:
            temp = customer_list[customer_list['Segment'] == option2[0]]
            fig = px.scatter_ternary(temp, a="recency_score", b="frequency_score", c="monetary_score")
            st.plotly_chart(fig, theme=None)
        elif len(option2) == 2:
            temp = customer_list[(customer_list['Segment'] == option2[0])|(customer_list['Segment'] == option2[1])]
            fig = px.scatter_ternary(temp, a="recency_score", b="frequency_score", c="monetary_score")
            st.plotly_chart(fig, theme=None)
        elif len(option2) == 3:
            temp = customer_list[(customer_list['Segment'] == option2[0])|(customer_list['Segment'] == option2[1])|(customer_list['Segment'] == option2[2])]
            fig = px.scatter_ternary(temp, a="recency_score", b="frequency_score", c="monetary_score")
            st.plotly_chart(fig, theme=None)
        elif len(option2) == 4:
            temp = customer_list[(customer_list['Segment'] == option2[0])|(customer_list['Segment'] == option2[1])|(customer_list['Segment'] == option2[2])|(customer_list['Segment'] == option2[3])]
            fig = px.scatter_ternary(temp, a="recency_score", b="frequency_score", c="monetary_score")
            st.plotly_chart(fig, theme=None)
        elif len(option2) == 5:
            temp = customer_list[(customer_list['Segment'] == option2[0])|(customer_list['Segment'] == option2[1])|(customer_list['Segment'] == option2[2])|(customer_list['Segment'] == option2[3])|(customer_list['Segment'] == option2[4])]
            fig = px.scatter_ternary(temp, a="recency_score", b="frequency_score", c="monetary_score")
            st.plotly_chart(fig, theme=None)
        elif len(option2) == 6:
            fig = px.scatter_ternary(customer_list, a="recency_score", b="frequency_score", c="monetary_score")
            st.plotly_chart(fig, theme=None)
    else:
        fig = px.scatter_ternary(customer_list, a="recency_score", b="frequency_score", c="monetary_score")
        st.plotly_chart(fig, theme=None)

row5_1, row5_space1 = st.columns((3, 0.1))
with row5_1:
    st.header("Email Target Marketing")

row4_1, row4_space1, row4_2, row1_space2, row4_3, row1_space3 = st.columns((1, 0.1, 2, 0.1, 0.5, 0.1))
with row4_1:
    option3 = st.multiselect('       ', options=('신규 고객', '충성 고객', '잠재적 충성고객', '관심 고객', '이탈 위험 고객', '이탈 고객'))

with row4_2:
    if option3 != []:
        if option3[0] == '신규 고객':
            email = st.text_area('                ', ' 🎉 오뚜기몰에 오신 것을 환영합니다! 🚂\n ooo님의 오뚜기몰 회원가입을 축하드립니다.\n항상 좋은 서비스로 고객님이 만족하실 수 있도록 노력하겠습니다.\n\
회원가입 감사 20% 쿠폰을 발급해 드렸으니,MY COUPON 페이지를 통해서 확인하시길 바랍니다.\n쿠폰 확인하기>(빨간색)')
        elif option3[0] == '충성 고객':
            email = st.text_area('                  ', '충성고객 타켓 메시지')
        elif option3[0] == '잠재적 충성고객':
            email = st.text_area('                     ', '잠재적 충성고객 타켓 메시지')
        elif option3[0] == '관심 고객':
            email = st.text_area('                            ', '관심 고객 타켓 메시지')
        elif option3[0] == '이탈 위험 고객':
            email = st.text_area('                           ', '이탈 위험 고객 타켓 메시지')
        elif option3[0] == '이탈 고객':
            email = st.text_area('                        ', '이탈 고객 타켓 메시지')
    else:
        st.text_area('         ', '마케팅 메시지')

def make_mime_text(mail_to, subjuct, body):
    msg = MIMEText(body, 'plane')
    msg['Subject'] = subjuct
    msg['To'] = mail_to 
    msg['From'] = naver.account 
    return msg

def send_naver_mail(msg):
    server = smtplib.SMTP('smtp.naver.com', 587)
    server.starttls()
    server.login(naver.account, naver.password)
    server.send_message(msg)

def send_test_email(email):
    msg = make_mime_text(mail_to=naver.account, subjuct='제목', body=email)
    send_naver_mail(msg)

with row4_3:
    st.write(' ')
    if st.button('Send Email'):
        # send_test_email(email) 
        st.write('Sending Time :', datetime.datetime.now())