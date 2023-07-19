#!/usr/bin/python3
# -*- coding: UTF-8 -*-

 # Author   : JasonHung
 # Date     : 20221102
 # Update   : 202230421
 # Function : kedge web cloud platform

from argparse import Namespace
from dataclasses import dataclass
from distutils.log import debug
from email import charset
from hashlib import md5
import hashlib , time , logging , random , pymysql
#import socketio
from tabnanny import check
from flask import Flask,render_template,request,session,url_for,redirect,escape
from flask_socketio import SocketIO , emit 

from control.config import *
from control.web_cloud_dao import web_cloud_dao 

db = web_cloud_dao()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret' 
socketio = SocketIO(app)  

########
# log
########
log_format = "%(asctime)s %(message)s"
logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")

##############
# variables
##############
title  = parm['title']


############################
# /load_alter_sensor_form
############################
@app.route("/load_alter_sensor_form",methods=['POST','GET'])
def load_alter_sensor_form():
    if 'user' in session:
        
        ### operation record title
        form_name = request.form['form']
        operation_record_title = '載入 ' + form_name + ' 處理動作表'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                a_total    = db.account_total()
                a_list     = db.account_list()
                
                return render_template('ajax/load_sensor_action_form.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list)  
                
        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

####################################
# /submit_alter_sensor_form_value
####################################
@app.route("/submit_alter_sensor_form_value",methods=['POST','GET'])
def submit_alter_sensor_form_value():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '送出修改感測器表格資料'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                dB = request.form['db']
                pm10 = request.form['pm10']
                pm25 = request.form['pm25']
                a_position = request.form['a_position']

                db.alter_sensor_setup_val(a_position , dB , pm10 , pm25)

                a_total = db.account_total()
                s_total = db.sensor_total(user)
                
                s1_val  = db.sensor_detail_data('南門市場')
                s1_date  = db.sensor_final_date('南門市場')
                s1_setup_voice = db.sensor_final_setup('s_p_南門市場' , '噪音')
                s1_setup_pm10 = db.sensor_final_setup('s_p_南門市場' , 'pm10')
                s1_setup_pm25 = db.sensor_final_setup('s_p_南門市場' , 'pm25')
                s1_g_pm25_val = db.government_aqi('臺北市' , '萬華' , 'pm25')
                s1_g_pm10_val = db.government_aqi('臺北市' , '萬華' , 'pm10')

                s2_val  = db.sensor_detail_data('桃園會展')
                s2_date  = db.sensor_final_date('桃園會展')
                s2_setup_voice = db.sensor_final_setup('s_p_桃園會展' , '噪音')
                s2_setup_pm10 = db.sensor_final_setup('s_p_桃園會展' , 'pm10')
                s2_setup_pm25 = db.sensor_final_setup('s_p_桃園會展' , 'pm25')
                s2_g_pm25_val = db.government_aqi('桃園市' , '中壢' , 'pm25')
                s2_g_pm10_val = db.government_aqi('桃園市' , '中壢' , 'pm10')

                s3_val  = db.sensor_detail_data('泰山社宅')
                s3_date  = db.sensor_final_date('泰山社宅')
                s3_setup_voice = db.sensor_final_setup('s_p_泰山社宅' , '噪音')
                s3_setup_pm10 = db.sensor_final_setup('s_p_泰山社宅' , 'pm10')
                s3_setup_pm25 = db.sensor_final_setup('s_p_泰山社宅' , 'pm25')
                s3_g_pm25_val = db.government_aqi('新北市' , '林口' , 'pm25')
                s3_g_pm10_val = db.government_aqi('新北市' , '林口' , 'pm10')

                s4_val  = db.sensor_detail_data('二重埔')
                s4_date  = db.sensor_final_date('二重埔')
                s4_setup_voice = db.sensor_final_setup('s_p_二重埔' , '噪音')
                s4_setup_pm10 = db.sensor_final_setup('s_p_二重埔' , 'pm10')
                s4_setup_pm25 = db.sensor_final_setup('s_p_二重埔' , 'pm25')
                s4_g_pm25_val = db.government_aqi('新北市' , '新莊' , 'pm25')
                s4_g_pm10_val = db.government_aqi('新北市' , '新莊' , 'pm10')

                s5_val  = db.sensor_detail_data('民權東路案')
                s5_date  = db.sensor_final_date('民權東路案')
                s5_setup_voice = db.sensor_final_setup('s_p_民權東路案' , '噪音')
                s5_setup_pm10 = db.sensor_final_setup('s_p_民權東路案' , 'pm10')
                s5_setup_pm25 = db.sensor_final_setup('s_p_民權東路案' , 'pm25')
                s5_g_pm25_val = db.government_aqi('臺北市' , '松山' , 'pm25')
                s5_g_pm10_val = db.government_aqi('臺北市' , '松山' , 'pm10')

                s6_val  = db.sensor_detail_data('秀朗橋案')
                s6_date  = db.sensor_final_date('秀朗橋案')
                s6_setup_voice = db.sensor_final_setup('s_p_秀朗橋案' , '噪音')
                s6_setup_pm10 = db.sensor_final_setup('s_p_秀朗橋案' , 'pm10')
                s6_setup_pm25 = db.sensor_final_setup('s_p_秀朗橋案' , 'pm25')
                s6_g_pm25_val = db.government_aqi('新北市' , '永和' , 'pm25')
                s6_g_pm10_val = db.government_aqi('新北市' , '永和' , 'pm10')

                s7_val  = db.sensor_detail_data('裕毛屋')
                s7_date  = db.sensor_final_date('裕毛屋')
                s7_setup_voice = db.sensor_final_setup('s_p_裕毛屋' , '噪音')
                s7_setup_pm10 = db.sensor_final_setup('s_p_裕毛屋' , 'pm10')
                s7_setup_pm25 = db.sensor_final_setup('s_p_裕毛屋' , 'pm25')
                s7_g_pm25_val = db.government_aqi('臺中市' , '忠明' , 'pm25')
                s7_g_pm10_val = db.government_aqi('臺中市' , '忠明' , 'pm10')

                s8_val  = db.sensor_detail_data('後龍大橋')
                s8_date  = db.sensor_final_date('後龍大橋')
                s8_setup_voice = db.sensor_final_setup('s_p_後龍大橋' , '噪音')
                s8_setup_pm10 = db.sensor_final_setup('s_p_後龍大橋' , 'pm10')
                s8_setup_pm25 = db.sensor_final_setup('s_p_後龍大橋' , 'pm25')
                s8_g_pm25_val = db.government_aqi('苗栗縣' , '苗栗' , 'pm25')
                s8_g_pm10_val = db.government_aqi('苗栗縣' , '苗栗' , 'pm10')

                s9_val  = db.sensor_detail_data('嘉義車站C611世賢南')
                s9_date  = db.sensor_final_date('嘉義車站C611世賢南')
                s9_setup_voice = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , '噪音')
                s9_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , 'pm10')
                s9_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , 'pm25')
                s9_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
                s9_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

                s10_val = db.sensor_detail_data('嘉義車站C611宏仁女中')
                s10_date = db.sensor_final_date('嘉義車站C611宏仁女中')
                s10_setup_voice = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , '噪音')
                s10_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , 'pm10')
                s10_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , 'pm25')
                s10_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
                s10_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

                s11_val = db.sensor_detail_data('嘉義車站C612嘉北車站')
                s11_date = db.sensor_final_date('嘉義車站C612嘉北車站')
                s11_setup_voice = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , '噪音')
                s11_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , 'pm10')
                s11_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , 'pm25')
                s11_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
                s11_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

                s12_val = db.sensor_detail_data('嘉義車站C612北興')
                s12_date = db.sensor_final_date('嘉義車站C612北興')
                s12_setup_voice = db.sensor_final_setup('s_p_嘉義車站C612北興' , '噪音')
                s12_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C612北興' , 'pm10')
                s12_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C612北興' , 'pm25')
                s12_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
                s12_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

                s13_val = db.sensor_detail_data('台南車站一號口')
                s13_date = db.sensor_final_date('台南車站一號口')
                s13_setup_voice = db.sensor_final_setup('s_p_台南車站一號口' , '噪音')
                s13_setup_pm10 = db.sensor_final_setup('s_p_台南車站一號口' , 'pm10')
                s13_setup_pm25 = db.sensor_final_setup('s_p_台南車站一號口' , 'pm25')
                s13_g_pm25_val = db.government_aqi('臺南市' , '臺南' , 'pm25')
                s13_g_pm10_val = db.government_aqi('臺南市' , '臺南' , 'pm10')

                s14_val = db.sensor_detail_data('台南車站四號口')
                s14_date = db.sensor_final_date('台南車站四號口')
                s14_setup_voice = db.sensor_final_setup('s_p_台南車站四號口' , '噪音')
                s14_setup_pm10 = db.sensor_final_setup('s_p_台南車站四號口' , 'pm10')
                s14_setup_pm25 = db.sensor_final_setup('s_p_台南車站四號口' , 'pm25')
                s14_g_pm25_val = db.government_aqi('臺南市' , '臺南' , 'pm25')
                s14_g_pm10_val = db.government_aqi('臺南市' , '臺南' , 'pm10')

                return render_template('index.html' , user=user , lv=lv , title=title , a_total=a_total , s_total=s_total , s1_val=s1_val , s2_val=s2_val , 
                                        s3_val=s3_val , s4_val=s4_val , s5_val=s5_val , s6_val=s6_val , s7_val=s7_val , s8_val=s8_val , s9_val=s9_val , 
                                        s10_val=s10_val , s11_val=s11_val , s12_val=s12_val , s13_val=s13_val , s14_val=s14_val , s1_date=s1_date , 
                                        s2_date=s2_date , s3_date=s3_date , s4_date=s4_date , s5_date=s5_date , s6_date=s6_date , s7_date=s7_date ,
                                        s8_date=s8_date , s9_date=s9_date , s10_date=s10_date , s11_date=s11_date , s12_date=s12_date , s13_date=s13_date ,
                                        s14_date=s14_date , s1_g_pm25_val=s1_g_pm25_val , s1_g_pm10_val=s1_g_pm10_val , s2_g_pm25_val=s2_g_pm25_val , s2_g_pm10_val=s2_g_pm10_val ,
                                        s3_g_pm25_val=s3_g_pm25_val , s3_g_pm10_val=s3_g_pm10_val , s4_g_pm25_val=s4_g_pm25_val , s4_g_pm10_val=s4_g_pm10_val ,
                                        s5_g_pm25_val=s5_g_pm25_val , s5_g_pm10_val=s5_g_pm10_val , s6_g_pm25_val=s6_g_pm25_val , s6_g_pm10_val=s6_g_pm10_val ,
                                        s7_g_pm25_val=s7_g_pm25_val , s7_g_pm10_val=s7_g_pm10_val , s8_g_pm25_val=s8_g_pm25_val , s8_g_pm10_val=s8_g_pm10_val ,
                                        s9_g_pm25_val=s9_g_pm25_val , s9_g_pm10_val=s9_g_pm10_val , s10_g_pm25_val=s10_g_pm25_val , s10_g_pm10_val=s10_g_pm10_val ,
                                        s11_g_pm25_val=s11_g_pm25_val , s11_g_pm10_val=s11_g_pm10_val , s12_g_pm25_val=s12_g_pm25_val , s12_g_pm10_val=s12_g_pm10_val ,
                                        s13_g_pm25_val=s13_g_pm25_val , s13_g_pm10_val=s13_g_pm10_val , s14_g_pm25_val=s14_g_pm25_val , s14_g_pm10_val=s14_g_pm10_val ,
                                        s1_setup_voice=s1_setup_voice , s1_setup_pm10=s1_setup_pm10 , s1_setup_pm25=s1_setup_pm25 , 
                                        s2_setup_voice=s2_setup_voice , s2_setup_pm10=s2_setup_pm10 , s2_setup_pm25=s2_setup_pm25 , 
                                        s3_setup_voice=s3_setup_voice , s3_setup_pm10=s3_setup_pm10 , s3_setup_pm25=s3_setup_pm25 , 
                                        s4_setup_voice=s4_setup_voice , s4_setup_pm10=s4_setup_pm10 , s4_setup_pm25=s4_setup_pm25 , 
                                        s5_setup_voice=s5_setup_voice , s5_setup_pm10=s5_setup_pm10 , s5_setup_pm25=s5_setup_pm25 , 
                                        s6_setup_voice=s6_setup_voice , s6_setup_pm10=s6_setup_pm10 , s6_setup_pm25=s6_setup_pm25 , 
                                        s7_setup_voice=s7_setup_voice , s7_setup_pm10=s7_setup_pm10 , s7_setup_pm25=s7_setup_pm25 , 
                                        s8_setup_voice=s8_setup_voice , s8_setup_pm10=s8_setup_pm10 , s8_setup_pm25=s8_setup_pm25 , 
                                        s9_setup_voice=s9_setup_voice , s9_setup_pm10=s9_setup_pm10 , s9_setup_pm25=s9_setup_pm25 , 
                                        s10_setup_voice=s10_setup_voice , s10_setup_pm10=s10_setup_pm10 , s10_setup_pm25=s10_setup_pm25 , 
                                        s11_setup_voice=s11_setup_voice , s11_setup_pm10=s11_setup_pm10 , s11_setup_pm25=s11_setup_pm25 , 
                                        s12_setup_voice=s12_setup_voice , s12_setup_pm10=s12_setup_pm10 , s12_setup_pm25=s12_setup_pm25 , 
                                        s13_setup_voice=s13_setup_voice , s13_setup_pm10=s13_setup_pm10 , s13_setup_pm25=s13_setup_pm25 , 
                                        s14_setup_voice=s14_setup_voice , s14_setup_pm10=s14_setup_pm10 , s14_setup_pm25=s14_setup_pm25
                                        )
                    
        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

##########################
# /load_add_sensor_form
##########################
@app.route("/load_add_sensor_form",methods=['POST','GET'])
def load_add_sensor_form():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '新增感測器資料表格'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                a_s_form = request.form['position']

                a_total    = db.account_total()
                a_list     = db.account_list()

                s1_sensor_db = db.sensor_setup_val("s_p_南門市場" , "噪音")
                s1_sensor_pm10 = db.sensor_setup_val("s_p_南門市場" , "pm10")
                s1_sensor_pm25 = db.sensor_setup_val("s_p_南門市場" , "pm25")

                s2_sensor_db = db.sensor_setup_val("s_p_桃園會展" , "噪音")
                s2_sensor_pm10 = db.sensor_setup_val("s_p_桃園會展" , "pm10")
                s2_sensor_pm25 = db.sensor_setup_val("s_p_桃園會展" , "pm25")
                
                s3_sensor_db = db.sensor_setup_val("s_p_泰山社宅" , "噪音")
                s3_sensor_pm10 = db.sensor_setup_val("s_p_泰山社宅" , "pm10")
                s3_sensor_pm25 = db.sensor_setup_val("s_p_泰山社宅" , "pm25")
                
                s4_sensor_db = db.sensor_setup_val("s_p_二重埔" , "噪音")
                s4_sensor_pm10 = db.sensor_setup_val("s_p_二重埔" , "pm10")
                s4_sensor_pm25 = db.sensor_setup_val("s_p_二重埔" , "pm25")

                s5_sensor_db = db.sensor_setup_val("s_p_民權東路案" , "噪音")
                s5_sensor_pm10 = db.sensor_setup_val("s_p_民權東路案" , "pm10")
                s5_sensor_pm25 = db.sensor_setup_val("s_p_民權東路案" , "pm25")

                s6_sensor_db = db.sensor_setup_val("s_p_秀朗橋案" , "噪音")
                s6_sensor_pm10 = db.sensor_setup_val("s_p_秀朗橋案" , "pm10")
                s6_sensor_pm25 = db.sensor_setup_val("s_p_秀朗橋案" , "pm25")
                
                s7_sensor_db = db.sensor_setup_val("s_p_裕毛屋" , "噪音")
                s7_sensor_pm10 = db.sensor_setup_val("s_p_裕毛屋" , "pm10")
                s7_sensor_pm25 = db.sensor_setup_val("s_p_裕毛屋" , "pm25")

                s8_sensor_db = db.sensor_setup_val("s_p_後龍大橋" , "噪音")
                s8_sensor_pm10 = db.sensor_setup_val("s_p_後龍大橋" , "pm10")
                s8_sensor_pm25 = db.sensor_setup_val("s_p_後龍大橋" , "pm25")

                s9_sensor_db = db.sensor_setup_val("s_p_嘉義車站C611世賢南" , "噪音")
                s9_sensor_pm10 = db.sensor_setup_val("s_p_嘉義車站C611世賢南" , "pm10")
                s9_sensor_pm25 = db.sensor_setup_val("s_p_嘉義車站C611世賢南" , "pm25")

                s10_sensor_db = db.sensor_setup_val("s_p_嘉義車站C611宏仁女中" , "噪音")
                s10_sensor_pm10 = db.sensor_setup_val("s_p_嘉義車站C611宏仁女中" , "pm10")
                s10_sensor_pm25 = db.sensor_setup_val("s_p_嘉義車站C611宏仁女中" , "pm25")

                s11_sensor_db = db.sensor_setup_val("s_p_嘉義車站C612嘉北車站" , "噪音")
                s11_sensor_pm10 = db.sensor_setup_val("s_p_嘉義車站C612嘉北車站" , "pm10")
                s11_sensor_pm25 = db.sensor_setup_val("s_p_嘉義車站C612嘉北車站" , "pm25")

                s12_sensor_db = db.sensor_setup_val("s_p_嘉義車站C612北興" , "噪音")
                s12_sensor_pm10 = db.sensor_setup_val("s_p_嘉義車站C612北興" , "pm10")
                s12_sensor_pm25 = db.sensor_setup_val("s_p_嘉義車站C612北興" , "pm25")

                s13_sensor_db = db.sensor_setup_val("s_p_台南車站一號口" , "噪音")
                s13_sensor_pm10 = db.sensor_setup_val("s_p_台南車站一號口" , "pm10")
                s13_sensor_pm25 = db.sensor_setup_val("s_p_台南車站一號口" , "pm25")

                s14_sensor_db = db.sensor_setup_val("s_p_台南車站四號口" , "噪音")
                s14_sensor_pm10 = db.sensor_setup_val("s_p_台南車站四號口" , "pm10")
                s14_sensor_pm25 = db.sensor_setup_val("s_p_台南車站四號口" , "pm25")
                
                return render_template('ajax/load_add_sensor_form.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list , a_s_form=a_s_form , 
                                       s1_sensor_db=s1_sensor_db , s1_sensor_pm10=s1_sensor_pm10 , s1_sensor_pm25=s1_sensor_pm25 ,
                                       s2_sensor_db=s2_sensor_db , s2_sensor_pm10=s2_sensor_pm10 , s2_sensor_pm25=s2_sensor_pm25 , 
                                       s3_sensor_db=s3_sensor_db , s3_sensor_pm10=s3_sensor_pm10 , s3_sensor_pm25=s3_sensor_pm25 , 
                                       s4_sensor_db=s4_sensor_db , s4_sensor_pm10=s4_sensor_pm10 , s4_sensor_pm25=s4_sensor_pm25 , 
                                       s5_sensor_db=s5_sensor_db , s5_sensor_pm10=s5_sensor_pm10 , s5_sensor_pm25=s5_sensor_pm25 , 
                                       s6_sensor_db=s6_sensor_db , s6_sensor_pm10=s6_sensor_pm10 , s6_sensor_pm25=s6_sensor_pm25 , 
                                       s7_sensor_db=s7_sensor_db , s7_sensor_pm10=s7_sensor_pm10 , s7_sensor_pm25=s7_sensor_pm25 , 
                                       s8_sensor_db=s8_sensor_db , s8_sensor_pm10=s8_sensor_pm10 , s8_sensor_pm25=s8_sensor_pm25 , 
                                       s9_sensor_db=s9_sensor_db , s9_sensor_pm10=s9_sensor_pm10 , s9_sensor_pm25=s9_sensor_pm25 , 
                                       s10_sensor_db=s10_sensor_db , s10_sensor_pm10=s10_sensor_pm10 , s10_sensor_pm25=s10_sensor_pm25 , 
                                       s11_sensor_db=s11_sensor_db , s11_sensor_pm10=s11_sensor_pm10 , s11_sensor_pm25=s11_sensor_pm25 , 
                                       s12_sensor_db=s12_sensor_db , s12_sensor_pm10=s12_sensor_pm10 , s12_sensor_pm25=s12_sensor_pm25 , 
                                       s13_sensor_db=s13_sensor_db , s13_sensor_pm10=s13_sensor_pm10 , s13_sensor_pm25=s13_sensor_pm25 , 
                                       s14_sensor_db=s14_sensor_db , s14_sensor_pm10=s14_sensor_pm10 , s14_sensor_pm25=s14_sensor_pm25
                                       )  
                
        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

############################
# /submit_add_new_account
############################
@app.route("/submit_add_new_account",methods=['POST','GET'])
def submit_add_new_account():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '送出新增帳號資料'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                a_user = request.form['a_user']
                a_pwd = request.form['a_pwd']
                a_lv = request.form['a_lv']
                a_position = request.form['a_position']
                a_comment = request.form['a_comment']

                res = db.submit_add_new_account(a_user , a_pwd , a_lv , a_position , a_comment)

                a_total    = db.account_total()
                a_list     = db.account_list()

                if res == "ok":
                    return render_template('ajax/reload_account_manager.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list)  
                
        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

########################
# /submit_add_account
########################
@app.route("/submit_add_account",methods=['POST','GET'])
def submit_add_account():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '新增帳號資料'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                a_total    = db.account_total()
                a_list     = db.account_list()
                a_position = db.sensor_total(user)

                return render_template('ajax/load_add_account.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list , a_position=a_position) 
                
        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

########################
# /submit_del_account
########################
@app.route("/submit_del_account",methods=['POST','GET'])
def submit_del_account():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '送出刪除帳號資料'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                a_user     = request.form['a_user']
                a_pwd      = request.form['a_pwd']

                res = db.submit_del_account(a_user , a_pwd)
                
                a_total = db.account_total()
                a_list = db.account_list()

                if res == 'ok':
                    return render_template('ajax/reload_account_manager.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list)  
                
        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

##########################
# /submit_alter_account
##########################
@app.route("/submit_alter_account",methods=['POST','GET'])
def submit_alter_account():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '送出修改帳號資料'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                a_user     = request.form['a_user']
                a_pwd      = request.form['a_pwd']
                a_position = request.form['a_position']
                a_comment  = request.form['a_comment']

                res = db.submit_alter_account(a_user , a_pwd , a_position , a_comment)
                
                a_total    = db.account_total()
                a_list     = db.account_list()

                if res == 'ok':
                    return render_template('ajax/reload_account_manager.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list)  
                
        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

########################
# /load_alter_account
########################
@app.route("/load_alter_account",methods=['POST','GET'])
def load_alter_account():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '修改帳號'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            if request.method == 'POST':
                
                a_alter = request.form['account']

                a_total    = db.account_total()
                a_list     = db.account_list()
                a_data     = db.account_alter(a_alter)
                a_position = db.sensor_total(user)

                return render_template('ajax/load_alter_account.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list , a_alter=a_alter , a_data=a_data , a_position=a_position)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

######
# /
######
@app.route("/")
def index():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '主頁'    

        ### session 
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)

        if check_repeat_login == 'ok':
            
            ### operation record
            db.operation_record(r_time,user,login_code,operation_record_title)    
            
            #################
            # main content 
            #################
            a_total = db.account_total()
            s_total = db.sensor_total(user)

            s1_val  = db.sensor_detail_data('南門市場')
            s1_date  = db.sensor_final_date('南門市場')
            s1_setup_voice = db.sensor_final_setup('s_p_南門市場' , '噪音')
            s1_setup_pm10 = db.sensor_final_setup('s_p_南門市場' , 'pm10')
            s1_setup_pm25 = db.sensor_final_setup('s_p_南門市場' , 'pm25')
            s1_g_pm25_val = db.government_aqi('臺北市' , '萬華' , 'pm25')
            s1_g_pm10_val = db.government_aqi('臺北市' , '萬華' , 'pm10')

            s2_val  = db.sensor_detail_data('桃園會展')
            s2_date  = db.sensor_final_date('桃園會展')
            s2_setup_voice = db.sensor_final_setup('s_p_桃園會展' , '噪音')
            s2_setup_pm10 = db.sensor_final_setup('s_p_桃園會展' , 'pm10')
            s2_setup_pm25 = db.sensor_final_setup('s_p_桃園會展' , 'pm25')
            s2_g_pm25_val = db.government_aqi('桃園市' , '中壢' , 'pm25')
            s2_g_pm10_val = db.government_aqi('桃園市' , '中壢' , 'pm10')

            s3_val  = db.sensor_detail_data('泰山社宅')
            s3_date  = db.sensor_final_date('泰山社宅')
            s3_setup_voice = db.sensor_final_setup('s_p_泰山社宅' , '噪音')
            s3_setup_pm10 = db.sensor_final_setup('s_p_泰山社宅' , 'pm10')
            s3_setup_pm25 = db.sensor_final_setup('s_p_泰山社宅' , 'pm25')
            s3_g_pm25_val = db.government_aqi('新北市' , '林口' , 'pm25')
            s3_g_pm10_val = db.government_aqi('新北市' , '林口' , 'pm10')

            s4_val  = db.sensor_detail_data('二重埔')
            s4_date  = db.sensor_final_date('二重埔')
            s4_setup_voice = db.sensor_final_setup('s_p_二重埔' , '噪音')
            s4_setup_pm10 = db.sensor_final_setup('s_p_二重埔' , 'pm10')
            s4_setup_pm25 = db.sensor_final_setup('s_p_二重埔' , 'pm25')
            s4_g_pm25_val = db.government_aqi('新北市' , '新莊' , 'pm25')
            s4_g_pm10_val = db.government_aqi('新北市' , '新莊' , 'pm10')

            s5_val  = db.sensor_detail_data('民權東路案')
            s5_date  = db.sensor_final_date('民權東路案')
            s5_setup_voice = db.sensor_final_setup('s_p_民權東路案' , '噪音')
            s5_setup_pm10 = db.sensor_final_setup('s_p_民權東路案' , 'pm10')
            s5_setup_pm25 = db.sensor_final_setup('s_p_民權東路案' , 'pm25')
            s5_g_pm25_val = db.government_aqi('臺北市' , '松山' , 'pm25')
            s5_g_pm10_val = db.government_aqi('臺北市' , '松山' , 'pm10')

            s6_val  = db.sensor_detail_data('秀朗橋案')
            s6_date  = db.sensor_final_date('秀朗橋案')
            s6_setup_voice = db.sensor_final_setup('s_p_秀朗橋案' , '噪音')
            s6_setup_pm10 = db.sensor_final_setup('s_p_秀朗橋案' , 'pm10')
            s6_setup_pm25 = db.sensor_final_setup('s_p_秀朗橋案' , 'pm25')
            s6_g_pm25_val = db.government_aqi('新北市' , '永和' , 'pm25')
            s6_g_pm10_val = db.government_aqi('新北市' , '永和' , 'pm10')

            s7_val  = db.sensor_detail_data('裕毛屋')
            s7_date  = db.sensor_final_date('裕毛屋')
            s7_setup_voice = db.sensor_final_setup('s_p_裕毛屋' , '噪音')
            s7_setup_pm10 = db.sensor_final_setup('s_p_裕毛屋' , 'pm10')
            s7_setup_pm25 = db.sensor_final_setup('s_p_裕毛屋' , 'pm25')
            s7_g_pm25_val = db.government_aqi('臺中市' , '忠明' , 'pm25')
            s7_g_pm10_val = db.government_aqi('臺中市' , '忠明' , 'pm10')

            s8_val  = db.sensor_detail_data('後龍大橋')
            s8_date  = db.sensor_final_date('後龍大橋')
            s8_setup_voice = db.sensor_final_setup('後龍大橋' , '噪音')
            s8_setup_pm10 = db.sensor_final_setup('後龍大橋' , 'pm10')
            s8_setup_pm25 = db.sensor_final_setup('後龍大橋' , 'pm25')
            s8_g_pm25_val = db.government_aqi('苗栗縣' , '苗栗' , 'pm25')
            s8_g_pm10_val = db.government_aqi('苗栗縣' , '苗栗' , 'pm10')

            s9_val  = db.sensor_detail_data('嘉義車站C611世賢南')
            s9_date  = db.sensor_final_date('嘉義車站C611世賢南')
            s9_setup_voice = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , '噪音')
            s9_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , 'pm10')
            s9_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , 'pm25')
            s9_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s9_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s10_val = db.sensor_detail_data('嘉義車站C611宏仁女中')
            s10_date = db.sensor_final_date('嘉義車站C611宏仁女中')
            s10_setup_voice = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , '噪音')
            s10_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , 'pm10')
            s10_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , 'pm25')
            s10_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s10_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s11_val = db.sensor_detail_data('嘉義車站C612嘉北車站')
            s11_date = db.sensor_final_date('嘉義車站C612嘉北車站')
            s11_setup_voice = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , '噪音')
            s11_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , 'pm10')
            s11_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , 'pm25')
            s11_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s11_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s12_val = db.sensor_detail_data('嘉義車站C612北興')
            s12_date = db.sensor_final_date('嘉義車站C612北興')
            s12_setup_voice = db.sensor_final_setup('s_p_嘉義車站C612北興' , '噪音')
            s12_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C612北興' , 'pm10')
            s12_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C612北興' , 'pm25')
            s12_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s12_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s13_val = db.sensor_detail_data('台南車站一號口')
            s13_date = db.sensor_final_date('台南車站一號口')
            s13_setup_voice = db.sensor_final_setup('s_p_台南車站一號口' , '噪音')
            s13_setup_pm10 = db.sensor_final_setup('s_p_台南車站一號口' , 'pm10')
            s13_setup_pm25 = db.sensor_final_setup('s_p_台南車站一號口' , 'pm25')
            s13_g_pm25_val = db.government_aqi('臺南市' , '臺南' , 'pm25')
            s13_g_pm10_val = db.government_aqi('臺南市' , '臺南' , 'pm10')

            s14_val = db.sensor_detail_data('台南車站四號口')
            s14_date = db.sensor_final_date('台南車站四號口')
            s14_setup_voice = db.sensor_final_setup('s_p_台南車站四號口' , '噪音')
            s14_setup_pm10 = db.sensor_final_setup('s_p_台南車站四號口' , 'pm10')
            s14_setup_pm25 = db.sensor_final_setup('s_p_台南車站四號口' , 'pm25')
            s14_g_pm25_val = db.government_aqi('臺南市' , '臺南' , 'pm25')
            s14_g_pm10_val = db.government_aqi('臺南市' , '臺南' , 'pm10')

            return render_template('index.html' , user=user , lv=lv , title=title , a_total=a_total , s_total=s_total , s1_val=s1_val , s2_val=s2_val , 
                                   s3_val=s3_val , s4_val=s4_val , s5_val=s5_val , s6_val=s6_val , s7_val=s7_val , s8_val=s8_val , s9_val=s9_val , 
                                   s10_val=s10_val , s11_val=s11_val , s12_val=s12_val , s13_val=s13_val , s14_val=s14_val , s1_date=s1_date , 
                                   s2_date=s2_date , s3_date=s3_date , s4_date=s4_date , s5_date=s5_date , s6_date=s6_date , s7_date=s7_date ,
                                   s8_date=s8_date , s9_date=s9_date , s10_date=s10_date , s11_date=s11_date , s12_date=s12_date , s13_date=s13_date ,
                                   s14_date=s14_date , s1_g_pm25_val=s1_g_pm25_val , s1_g_pm10_val=s1_g_pm10_val , s2_g_pm25_val=s2_g_pm25_val , s2_g_pm10_val=s2_g_pm10_val ,
                                   s3_g_pm25_val=s3_g_pm25_val , s3_g_pm10_val=s3_g_pm10_val , s4_g_pm25_val=s4_g_pm25_val , s4_g_pm10_val=s4_g_pm10_val ,
                                   s5_g_pm25_val=s5_g_pm25_val , s5_g_pm10_val=s5_g_pm10_val , s6_g_pm25_val=s6_g_pm25_val , s6_g_pm10_val=s6_g_pm10_val ,
                                   s7_g_pm25_val=s7_g_pm25_val , s7_g_pm10_val=s7_g_pm10_val , s8_g_pm25_val=s8_g_pm25_val , s8_g_pm10_val=s8_g_pm10_val ,
                                   s9_g_pm25_val=s9_g_pm25_val , s9_g_pm10_val=s9_g_pm10_val , s10_g_pm25_val=s10_g_pm25_val , s10_g_pm10_val=s10_g_pm10_val ,
                                   s11_g_pm25_val=s11_g_pm25_val , s11_g_pm10_val=s11_g_pm10_val , s12_g_pm25_val=s12_g_pm25_val , s12_g_pm10_val=s12_g_pm10_val ,
                                   s13_g_pm25_val=s13_g_pm25_val , s13_g_pm10_val=s13_g_pm10_val , s14_g_pm25_val=s14_g_pm25_val , s14_g_pm10_val=s14_g_pm10_val ,
                                   s1_setup_voice=s1_setup_voice , s1_setup_pm10=s1_setup_pm10 , s1_setup_pm25=s1_setup_pm25 , 
                                   s2_setup_voice=s2_setup_voice , s2_setup_pm10=s2_setup_pm10 , s2_setup_pm25=s2_setup_pm25 , 
                                   s3_setup_voice=s3_setup_voice , s3_setup_pm10=s3_setup_pm10 , s3_setup_pm25=s3_setup_pm25 , 
                                   s4_setup_voice=s4_setup_voice , s4_setup_pm10=s4_setup_pm10 , s4_setup_pm25=s4_setup_pm25 , 
                                   s5_setup_voice=s5_setup_voice , s5_setup_pm10=s5_setup_pm10 , s5_setup_pm25=s5_setup_pm25 , 
                                   s6_setup_voice=s6_setup_voice , s6_setup_pm10=s6_setup_pm10 , s6_setup_pm25=s6_setup_pm25 , 
                                   s7_setup_voice=s7_setup_voice , s7_setup_pm10=s7_setup_pm10 , s7_setup_pm25=s7_setup_pm25 , 
                                   s8_setup_voice=s8_setup_voice , s8_setup_pm10=s8_setup_pm10 , s8_setup_pm25=s8_setup_pm25 , 
                                   s9_setup_voice=s9_setup_voice , s9_setup_pm10=s9_setup_pm10 , s9_setup_pm25=s9_setup_pm25 , 
                                   s10_setup_voice=s10_setup_voice , s10_setup_pm10=s10_setup_pm10 , s10_setup_pm25=s10_setup_pm25 , 
                                   s11_setup_voice=s11_setup_voice , s11_setup_pm10=s11_setup_pm10 , s11_setup_pm25=s11_setup_pm25 , 
                                   s12_setup_voice=s12_setup_voice , s12_setup_pm10=s12_setup_pm10 , s12_setup_pm25=s12_setup_pm25 , 
                                   s13_setup_voice=s13_setup_voice , s13_setup_pm10=s13_setup_pm10 , s13_setup_pm25=s13_setup_pm25 , 
                                   s14_setup_voice=s14_setup_voice , s14_setup_pm10=s14_setup_pm10 , s14_setup_pm25=s14_setup_pm25
                                   )

        else:
            return redirect(url_for('logout'))

    return redirect(url_for('login')) 

##########
# /login
##########
@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        check_account = db.login(request.form['user'] , request.form['pwd'])

        if type(check_account) == tuple:
            
            ### r_time
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            
            ### operation record title
            operation_record_title = '登入成功'    
            
            ### session  
            session['user'] = request.form['user']
            
            ### for python3 md5 use method
            m = hashlib.md5()
            m.update(r_time.encode('utf-8'))
            h = m.hexdigest()
            session['login_code'] = h
            session['ip'] = request.remote_addr
            session['lv'] = check_account[0]
            user = session['user']
            lv = session['lv']
            
            ### login record
            db.login_record(session['user'],session['login_code'],r_time,session['ip'])
            
            ### operation record
            db.operation_record(r_time , session['user'] , session['login_code'] , operation_record_title)    

            #################
            # main content
            #################
            a_total = db.account_total()
            s_total = db.sensor_total(user)

            s1_val  = db.sensor_detail_data('南門市場')
            s1_date  = db.sensor_final_date('南門市場')
            s1_setup_voice = db.sensor_final_setup('s_p_南門市場' , '噪音')
            s1_setup_pm10 = db.sensor_final_setup('s_p_南門市場' , 'pm10')
            s1_setup_pm25 = db.sensor_final_setup('s_p_南門市場' , 'pm25')
            s1_g_pm25_val = db.government_aqi('臺北市' , '萬華' , 'pm25')
            s1_g_pm10_val = db.government_aqi('臺北市' , '萬華' , 'pm10')

            s2_val  = db.sensor_detail_data('桃園會展')
            s2_date  = db.sensor_final_date('桃園會展')
            s2_setup_voice = db.sensor_final_setup('s_p_桃園會展' , '噪音')
            s2_setup_pm10 = db.sensor_final_setup('s_p_桃園會展' , 'pm10')
            s2_setup_pm25 = db.sensor_final_setup('s_p_桃園會展' , 'pm25')
            s2_g_pm25_val = db.government_aqi('桃園市' , '中壢' , 'pm25')
            s2_g_pm10_val = db.government_aqi('桃園市' , '中壢' , 'pm10')

            s3_val  = db.sensor_detail_data('泰山社宅')
            s3_date  = db.sensor_final_date('泰山社宅')
            s3_setup_voice = db.sensor_final_setup('s_p_泰山社宅' , '噪音')
            s3_setup_pm10 = db.sensor_final_setup('s_p_泰山社宅' , 'pm10')
            s3_setup_pm25 = db.sensor_final_setup('s_p_泰山社宅' , 'pm25')
            s3_g_pm25_val = db.government_aqi('新北市' , '林口' , 'pm25')
            s3_g_pm10_val = db.government_aqi('新北市' , '林口' , 'pm10')

            s4_val  = db.sensor_detail_data('二重埔')
            s4_date  = db.sensor_final_date('二重埔')
            s4_setup_voice = db.sensor_final_setup('s_p_二重埔' , '噪音')
            s4_setup_pm10 = db.sensor_final_setup('s_p_二重埔' , 'pm10')
            s4_setup_pm25 = db.sensor_final_setup('s_p_二重埔' , 'pm25')
            s4_g_pm25_val = db.government_aqi('新北市' , '新莊' , 'pm25')
            s4_g_pm10_val = db.government_aqi('新北市' , '新莊' , 'pm10')

            s5_val  = db.sensor_detail_data('民權東路案')
            s5_date  = db.sensor_final_date('民權東路案')
            s5_setup_voice = db.sensor_final_setup('s_p_民權東路案' , '噪音')
            s5_setup_pm10 = db.sensor_final_setup('s_p_民權東路案' , 'pm10')
            s5_setup_pm25 = db.sensor_final_setup('s_p_民權東路案' , 'pm25')
            s5_g_pm25_val = db.government_aqi('臺北市' , '松山' , 'pm25')
            s5_g_pm10_val = db.government_aqi('臺北市' , '松山' , 'pm10')

            s6_val  = db.sensor_detail_data('秀朗橋案')
            s6_date  = db.sensor_final_date('秀朗橋案')
            s6_setup_voice = db.sensor_final_setup('s_p_秀朗橋案' , '噪音')
            s6_setup_pm10 = db.sensor_final_setup('s_p_秀朗橋案' , 'pm10')
            s6_setup_pm25 = db.sensor_final_setup('s_p_秀朗橋案' , 'pm25')
            s6_g_pm25_val = db.government_aqi('新北市' , '永和' , 'pm25')
            s6_g_pm10_val = db.government_aqi('新北市' , '永和' , 'pm10')

            s7_val  = db.sensor_detail_data('裕毛屋')
            s7_date  = db.sensor_final_date('裕毛屋')
            s7_setup_voice = db.sensor_final_setup('s_p_裕毛屋' , '噪音')
            s7_setup_pm10 = db.sensor_final_setup('s_p_裕毛屋' , 'pm10')
            s7_setup_pm25 = db.sensor_final_setup('s_p_裕毛屋' , 'pm25')
            s7_g_pm25_val = db.government_aqi('臺中市' , '忠明' , 'pm25')
            s7_g_pm10_val = db.government_aqi('臺中市' , '忠明' , 'pm10')

            s8_val  = db.sensor_detail_data('後龍大橋')
            s8_date  = db.sensor_final_date('後龍大橋')
            s8_setup_voice = db.sensor_final_setup('s_p_後龍大橋' , '噪音')
            s8_setup_pm10 = db.sensor_final_setup('s_p_後龍大橋' , 'pm10')
            s8_setup_pm25 = db.sensor_final_setup('s_p_後龍大橋' , 'pm25')
            s8_g_pm25_val = db.government_aqi('苗栗縣' , '苗栗' , 'pm25')
            s8_g_pm10_val = db.government_aqi('苗栗縣' , '苗栗' , 'pm10')

            s9_val  = db.sensor_detail_data('嘉義車站C611世賢南')
            s9_date  = db.sensor_final_date('嘉義車站C611世賢南')
            s9_setup_voice = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , '噪音')
            s9_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , 'pm10')
            s9_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C611世賢南' , 'pm25')
            s9_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s9_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s10_val = db.sensor_detail_data('嘉義車站C611宏仁女中')
            s10_date = db.sensor_final_date('嘉義車站C611宏仁女中')
            s10_setup_voice = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , '噪音')
            s10_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , 'pm10')
            s10_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C611宏仁女中' , 'pm25')
            s10_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s10_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s11_val = db.sensor_detail_data('嘉義車站C612嘉北車站')
            s11_date = db.sensor_final_date('嘉義車站C612嘉北車站')
            s11_setup_voice = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , '噪音')
            s11_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , 'pm10')
            s11_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C612嘉北車站' , 'pm25')
            s11_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s11_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s12_val = db.sensor_detail_data('嘉義車站C612北興')
            s12_date = db.sensor_final_date('嘉義車站C612北興')
            s12_setup_voice = db.sensor_final_setup('s_p_嘉義車站C612北興' , '噪音')
            s12_setup_pm10 = db.sensor_final_setup('s_p_嘉義車站C612北興' , 'pm10')
            s12_setup_pm25 = db.sensor_final_setup('s_p_嘉義車站C612北興' , 'pm25')
            s12_g_pm25_val = db.government_aqi('嘉義市' , '嘉義' , 'pm25')
            s12_g_pm10_val = db.government_aqi('嘉義市' , '嘉義' , 'pm10')

            s13_val = db.sensor_detail_data('台南車站一號口')
            s13_date = db.sensor_final_date('台南車站一號口')
            s13_setup_voice = db.sensor_final_setup('s_p_台南車站一號口' , '噪音')
            s13_setup_pm10 = db.sensor_final_setup('s_p_台南車站一號口' , 'pm10')
            s13_setup_pm25 = db.sensor_final_setup('s_p_台南車站一號口' , 'pm25')
            s13_g_pm25_val = db.government_aqi('臺南市' , '臺南' , 'pm25')
            s13_g_pm10_val = db.government_aqi('臺南市' , '臺南' , 'pm10')

            s14_val = db.sensor_detail_data('台南車站四號口')
            s14_date = db.sensor_final_date('台南車站四號口')
            s14_setup_voice = db.sensor_final_setup('s_p_台南車站四號口' , '噪音')
            s14_setup_pm10 = db.sensor_final_setup('s_p_台南車站四號口' , 'pm10')
            s14_setup_pm25 = db.sensor_final_setup('s_p_台南車站四號口' , 'pm25')
            s14_g_pm25_val = db.government_aqi('臺南市' , '臺南' , 'pm25')
            s14_g_pm10_val = db.government_aqi('臺南市' , '臺南' , 'pm10')

            return render_template('index.html' , user=user , lv=lv , title=title , a_total=a_total , s_total=s_total , s1_val=s1_val , s2_val=s2_val , 
                                   s3_val=s3_val , s4_val=s4_val , s5_val=s5_val , s6_val=s6_val , s7_val=s7_val , s8_val=s8_val , s9_val=s9_val , 
                                   s10_val=s10_val , s11_val=s11_val , s12_val=s12_val , s13_val=s13_val , s14_val=s14_val , s1_date=s1_date , 
                                   s2_date=s2_date , s3_date=s3_date , s4_date=s4_date , s5_date=s5_date , s6_date=s6_date , s7_date=s7_date ,
                                   s8_date=s8_date , s9_date=s9_date , s10_date=s10_date , s11_date=s11_date , s12_date=s12_date , s13_date=s13_date ,
                                   s14_date=s14_date , s1_g_pm25_val=s1_g_pm25_val , s1_g_pm10_val=s1_g_pm10_val , s2_g_pm25_val=s2_g_pm25_val , s2_g_pm10_val=s2_g_pm10_val ,
                                   s3_g_pm25_val=s3_g_pm25_val , s3_g_pm10_val=s3_g_pm10_val , s4_g_pm25_val=s4_g_pm25_val , s4_g_pm10_val=s4_g_pm10_val ,
                                   s5_g_pm25_val=s5_g_pm25_val , s5_g_pm10_val=s5_g_pm10_val , s6_g_pm25_val=s6_g_pm25_val , s6_g_pm10_val=s6_g_pm10_val ,
                                   s7_g_pm25_val=s7_g_pm25_val , s7_g_pm10_val=s7_g_pm10_val , s8_g_pm25_val=s8_g_pm25_val , s8_g_pm10_val=s8_g_pm10_val ,
                                   s9_g_pm25_val=s9_g_pm25_val , s9_g_pm10_val=s9_g_pm10_val , s10_g_pm25_val=s10_g_pm25_val , s10_g_pm10_val=s10_g_pm10_val ,
                                   s11_g_pm25_val=s11_g_pm25_val , s11_g_pm10_val=s11_g_pm10_val , s12_g_pm25_val=s12_g_pm25_val , s12_g_pm10_val=s12_g_pm10_val ,
                                   s13_g_pm25_val=s13_g_pm25_val , s13_g_pm10_val=s13_g_pm10_val , s14_g_pm25_val=s14_g_pm25_val , s14_g_pm10_val=s14_g_pm10_val ,
                                   s1_setup_voice=s1_setup_voice , s1_setup_pm10=s1_setup_pm10 , s1_setup_pm25=s1_setup_pm25 , 
                                   s2_setup_voice=s2_setup_voice , s2_setup_pm10=s2_setup_pm10 , s2_setup_pm25=s2_setup_pm25 , 
                                   s3_setup_voice=s3_setup_voice , s3_setup_pm10=s3_setup_pm10 , s3_setup_pm25=s3_setup_pm25 , 
                                   s4_setup_voice=s4_setup_voice , s4_setup_pm10=s4_setup_pm10 , s4_setup_pm25=s4_setup_pm25 , 
                                   s5_setup_voice=s5_setup_voice , s5_setup_pm10=s5_setup_pm10 , s5_setup_pm25=s5_setup_pm25 , 
                                   s6_setup_voice=s6_setup_voice , s6_setup_pm10=s6_setup_pm10 , s6_setup_pm25=s6_setup_pm25 , 
                                   s7_setup_voice=s7_setup_voice , s7_setup_pm10=s7_setup_pm10 , s7_setup_pm25=s7_setup_pm25 , 
                                   s8_setup_voice=s8_setup_voice , s8_setup_pm10=s8_setup_pm10 , s8_setup_pm25=s8_setup_pm25 , 
                                   s9_setup_voice=s9_setup_voice , s9_setup_pm10=s9_setup_pm10 , s9_setup_pm25=s9_setup_pm25 , 
                                   s10_setup_voice=s10_setup_voice , s10_setup_pm10=s10_setup_pm10 , s10_setup_pm25=s10_setup_pm25 , 
                                   s11_setup_voice=s11_setup_voice , s11_setup_pm10=s11_setup_pm10 , s11_setup_pm25=s11_setup_pm25 , 
                                   s12_setup_voice=s12_setup_voice , s12_setup_pm10=s12_setup_pm10 , s12_setup_pm25=s12_setup_pm25 , 
                                   s13_setup_voice=s13_setup_voice , s13_setup_pm10=s13_setup_pm10 , s13_setup_pm25=s13_setup_pm25 , 
                                   s14_setup_voice=s14_setup_voice , s14_setup_pm10=s14_setup_pm10 , s14_setup_pm25=s14_setup_pm25
                                   )

        else:
            res_data = "<登入失敗> 帳密有錯，重新輸入 !!!"
            return render_template('login.html' , login_msg=res_data , title=title)

    else:
        return render_template('login.html' , title=title)

###########
# /logout 
###########
@app.route("/logout")
def logout():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '登出成功'

        ### session 
        user = session['user']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
    
        ### logout record
        try:
            db.logout_record(session['user'] , session['login_code'] , r_time)
        except Exception as e:
            logging.info("< Error > logout record : " + str(e))
        finally:
            pass
        
        ### operation record
        db.operation_record(r_time , user , session['login_code'] , operation_record_title)    

        ### clean up session param
        session.pop('user',None)
        session.pop('login_code',None)
        session.pop('ip',None)
        session.pop('lv',None)

    return redirect(url_for('index'))


#####################
# /account_manager
#####################
@app.route("/account_manager",methods=['POST','GET'])
def account_manager():
    if 'user' in session:
        
        ### operation record title
        operation_record_title = '帳號管理'    

        ### session
        user = session['user']
        lv   = session['lv']
        login_code = session['login_code']

        ### r_time
        r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())

        ### check repeat login
        check_repeat_login = db.check_login_code(user,login_code)
        
        if check_repeat_login == 'ok':

            ### operation record
            db.operation_record(r_time , user , login_code , operation_record_title)    

            #################
            # main content
            #################
            a_total = db.account_total()
            a_list = db.account_list()

            return render_template('account_manager.html' , user=user , lv=lv , title=title , a_total=a_total , a_list=a_list)    

        else:
            return redirect(url_for('logout'))
    
    return redirect(url_for('login'))

########################################################################################################################################
#
# socketIO - WebSocket - Flask-SocketIO 
#
########################################################################################################################################

@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    logging.info('Client disconnected')

'''
@socketio.on('connect', namespace='/')
def test_connect():
    while True:
        socketio.sleep(5)
        t = random_int_list(1, 100, 10)
        emit('server_response',{'data': t},namespace='/')
 
def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list
  
@socketio.on('disconnect', namespace='/')  
def test_disconnect():  
    logging.info('Client disconnected')  
'''


########################################################################################################################################
#
# start
#
########################################################################################################################################
if __name__ == "__main__":
    
    ##########
    # Flask
    ##########
    #app.run(host="0.0.0.0" , port=8080 , debug=True)
    
    ###################
    # Flask-SocketIO
    ###################
    socketio.run(app , host="0.0.0.0" , port=9095 , debug=True)