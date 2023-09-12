import pymssql
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import animation

# mssql로 부터 20개 데이터 SELECT
def getData() :
    conn = pymssql.connect(server='10.1.55.174', user='dlitdb', password='dlitdb', database='SensorDataDB')
    cursor = conn.cursor()
    query = '''
                SELECT TOP(20) humid1.DateAndTime AS '1번 장비 시간',
                       humid1.Humidity, 
                       temp1.Temperature, 
                       part31.Particle03,
                       part51.Particle05
                FROM DEV_HUMID_1 humid1
                JOIN DEV_TEMP_1 temp1 ON humid1.DateAndTime = temp1.DateAndTime 
                JOIN DEV_PART03_1 part31 ON humid1.DateAndTime = part31.DateAndTime
                JOIN DEV_PART05_1 part51 ON humid1.DateAndTime = part51.DateAndTime	
                ORDER BY humid1.DateAndTime DESC;
               '''
    cursor.execute(query)
    row = cursor.fetchall()
    return row

# SELECT 해온 데이터 pandas.DataFrame 형태로 변환
def dataToDF() :
    row = getData()
    sensor_df = pd.DataFrame(row)
    sensor_df = sensor_df.rename(columns={0:'datetime',1:'humid',2:'temp',3:'part3',4:'part5'})
    sensor_df = sensor_df.astype({'datetime':'datetime64','humid':'float','temp':'float','part3':'float','part5':'float'})
    return sensor_df

#그래프 한글 폰트 깨짐 방지를 위한 코드입니다
fm.get_fontconfig_fonts()
font_location = 'C:/Windows/Fonts/gulim.ttc' # 한글 폰트 파일 위치 확인하여 입력해줍니다.
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)
#코드 참고 : https://m.blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221225208497&proxyReferer=https:%2F%2Fwww.google.com%2F

# subplot 설정
fig = plt.figure(figsize=(17,17))

ax_humid = plt.subplot(221)
ax_humid.set_title('1번 장비 습도')
ax_humid.set_xlabel('시간')
ax_humid.set_ylabel('습도')

ax_temp = plt.subplot(222)
ax_temp.set_title('1번 장비 온도')
ax_temp.set_xlabel('시간')
ax_temp.set_ylabel('온도')

ax_part3 = plt.subplot(223)
ax_part3.set_title('1번 장비 Particle 0.3')
ax_part3.set_xlabel('시간')
ax_part3.set_ylabel('Particle 0.3')

ax_part5 = plt.subplot(224)
ax_part5.set_title('1번 장비 Particle 0.5')
ax_part5.set_xlabel('시간')
ax_part5.set_ylabel('Particle 0.5')

# 애니메이션 효과를 줄 함수 정의
def animate(i) :
    df_sensor1 = dataToDF() # 센서값 변수에 저장
    # 컬럼에 해당하는 값 numpy ndarray 형태로 변수에 저장
    datetime = df_sensor1['datetime'].values
    humid = df_sensor1['humid'].values
    temp = df_sensor1['temp'].values
    part3 = df_sensor1['part3'].values
    part5 = df_sensor1['part5'].values
    # subplot에 값 배치 ~ (시간, 값)
    ax_humid.plot(datetime,humid)
    ax_temp.plot(datetime,temp)
    ax_part3.plot(datetime,part3)
    ax_part5.plot(datetime,part5)

ani = animation.FuncAnimation(fig, animate)
plt.show()
