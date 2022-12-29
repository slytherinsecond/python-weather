import streamlit as st
import datetime,requests
from plotly import graph_objects as go

st.set_page_config(page_title='Thesis UTE Weather', page_icon=":rainbow:")

st.title("DỰ BÁO THỜI TIẾT 🌧️🌥️")

city=st.text_input("NHẬP TÊN THÀNH PHỐ BẤT KỲ TRÊN THẾ GIỚI")

unit=st.selectbox("CHỌN ĐƠN VỊ NHIỆT ĐỘ ",["Độ C","Độ F"])

speed=st.selectbox("CHỌN ĐƠN VỊ TỐC ĐỘ GIÓ ",["M/s","Km/h"])

graph=st.radio("CHỌN LOẠI BIỂU ĐỒ ",["Bar Graph","Line Graph"])

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.shutterstock.com/image-photo/blue-sky-background-tiny-clouds-260nw-288947759.jpg")
    }
  
    </style>
    """,
    unsafe_allow_html=True
)

if unit=="Độ C":
    temp_unit=" °C"
else:
    temp_unit=" °F"
    
if speed=="Km/H":
    wind_unit=" km/h"
else:
    wind_unit=" m/s"

api="9b833c0ea6426b70902aa7a4b1da285c"
url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}"
response=requests.get(url)
x=response.json()
    
if(st.button("SUBMIT")):
    try:
        lon=x["coord"]["lon"]
        lat=x["coord"]["lat"]
        ex="current,minutely,hourly"
        url2=f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={ex}&appid={api}'
        res=requests.get(url2)
        y=res.json()

        maxtemp=[]
        mintemp=[]
        pres=[]
        humd=[]
        wspeed=[]
        desc=[]
        cloud=[]
        rain=[]
        dates=[]
        sunrise=[]
        sunset=[]
        cel=273.15
        
        for item in y["daily"]:
            
            if unit=="Độ C":
                maxtemp.append(round(item["temp"]["max"]-cel,2))
                mintemp.append(round(item["temp"]["min"]-cel,2))
            else:
                maxtemp.append(round((((item["temp"]["max"]-cel)*1.8)+32),2))
                mintemp.append(round((((item["temp"]["min"]-cel)*1.8)+32),2))

            if wind_unit=="m/s":
                wspeed.append(str(round(item["wind_speed"],1))+wind_unit)
            else:
                wspeed.append(str(round(item["wind_speed"]*3.6,1))+wind_unit)

            pres.append(item["pressure"])
            humd.append(str(item["humidity"])+' %')
            
            cloud.append(str(item["clouds"])+' %')
            rain.append(str(int(item["pop"]*100))+'%')

            desc.append(item["weather"][0]["description"].title())

            d1=datetime.date.fromtimestamp(item["dt"])
            dates.append(d1.strftime('%d %b'))
            
            sunrise.append( datetime.datetime.utcfromtimestamp(item["sunrise"]).strftime('%H:%M'))
            sunset.append( datetime.datetime.utcfromtimestamp(item["sunset"]).strftime('%H:%M'))

        def bargraph():
            fig=go.Figure(data=
                [
                go.Bar(name="Maximum",x=dates,y=maxtemp,marker_color='crimson'),
                go.Bar(name="Minimum",x=dates,y=mintemp,marker_color='navy')
                ])
            fig.update_layout(xaxis_title="Dates",yaxis_title="Temperature",barmode='group',margin=dict(l=70, r=10, t=80, b=80),font=dict(color="white"))
            st.plotly_chart(fig)
        
        def linegraph():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates, y=mintemp, name='Minimum '))
            fig.add_trace(go.Scatter(x=dates, y=maxtemp, name='Maximimum ',marker_color='crimson'))
            fig.update_layout(xaxis_title="Dates",yaxis_title="Temperature",font=dict(color="white"))
            st.plotly_chart(fig)
            
        icon=x["weather"][0]["icon"]
        current_weather=x["weather"][0]["description"].title()
        
        if unit=="Độ C":
            temp=str(round(x["main"]["temp"]-cel,2))
        else:
            temp=str(round((((x["main"]["temp"]-cel)*1.8)+32),2))
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("## Nhiệt độ hiện tại ")
        with col2:
            st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png",width=70)

        
        col1, col2= st.columns(2)
        col1.metric("NHIỆT ĐỘ",temp+temp_unit)
        col2.metric("THỜI TIẾT",current_weather)
        st.subheader(" ")
        
        if graph=="Bar Graph":
            bargraph()
            
        elif graph=="Line Graph":
            linegraph()

         
        table1=go.Figure(data=[go.Table(header=dict(
                  values = [
                  '<b>NGÀY</b>',
                  '<b>NHIỆT ĐỘ TỐI ĐA<br>(in'+temp_unit+')</b>',
                  '<b>NHIỆT ĐỘ TỐI THIỂU<br>(in'+temp_unit+')</b>',
                  '<b>TỈ LỆ THỜI TIẾT CÓ MƯA</b>',
                  '<b>PHẠM VI ĐÁM MÂY</b>',
                  '<b>ĐỘ ẨM</b>'],
                  line_color='black', fill_color='royalblue',  font=dict(color='white', size=14),height=32),
        cells=dict(values=[dates,maxtemp,mintemp,rain,cloud,humd],
        line_color='black',fill_color=['paleturquoise',['palegreen', '#fdbe72']*7], font_size=14,height=32
            ))])

        table1.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=328)
        st.write(table1)
        
        table2=go.Figure(data=[go.Table(columnwidth=[1,2,1,1,1,1],header=dict(values=['<b>NGÀY</b>','<b>TÌNH HÌNH THỜI TIẾT</b>','<b>TỐC ĐỘ GIÓ</b>','<b>ÁP SUẤT<br>(in hPa)</b>','<b>HOÀNG HÔN<br>(in UTC)</b>','<b>BÌNH MINH<br>(in UTC)</b>']
                  ,line_color='black', fill_color='royalblue',  font=dict(color='white', size=14),height=36),
        cells=dict(values=[dates,desc,wspeed,pres,sunrise,sunset],
        line_color='black',fill_color=['paleturquoise',['palegreen', '#fdbe72']*7], font_size=14,height=36))])
        
        table2.update_layout(margin=dict(l=10,r=10,b=10,t=10),height=360)
        st.write(table2)
        
        st.header(' ')
        st.header(' ')
        st.markdown(" ĐỒ ÁN ĐƯỢC THỰC HIỆN BỞI : ")
        st.markdown(" Front-end&Back-end : Phạm Thế Anh - 20610014")
        st.markdown(" UML Diagram : Hồ Trương Công Thắng - 20810007")
        st.markdown(" Design UX/UI : Phan Thị Quỳnh Giang - 20810016")
        st.markdown(" API Data Analyst : Nguyễn Xuân Quang - 208410014")
        st.markdown(" IT Support Environment : Trần Công Khánh - 20810010")
 
    except KeyError:
        st.error(" Invalid city!!  Please try again !!")

