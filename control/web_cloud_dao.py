#!/usr/bin/python3
# -*- coding: UTF-8 -*-

 # Author   : JasonHung
 # Date     : 20221102
 # Update   : 202230421
 # Function : kedge web cloud platform

import pymysql , logging , time , re , requests , json

from control.config import *

########################################################################################################################################
#
# web_cloud_dao
#
########################################################################################################################################
class web_cloud_dao:

    ########
    # log
    ########
    log_format = "%(asctime)s %(message)s"
    logging.basicConfig(format=log_format , level=logging.INFO , datefmt="%Y-%m-%d %H:%M:%S")
    #logging.disable(logging.INFO)

    ###########################
    # alter_sensor_setup_val
    ###########################
    def alter_sensor_setup_val(self , s_position , db_val , pm10_val , pm25_val):
        
        self.__connect__()
        try:
            sql1 = "update `sensor_setup` set s_tag_high_val='{1}' where s_position='{0}' and s_tag_name='噪音'".format(s_position, db_val)
            self.curr.execute(sql1)

            sql2 = "update `sensor_setup` set s_tag_high_val='{1}' where s_position='{0}' and s_tag_name='pm10'".format(s_position, pm10_val)
            self.curr.execute(sql2)
    
            sql3 = "update `sensor_setup` set s_tag_high_val='{1}' where s_position='{0}' and s_tag_name='pm25'".format(s_position, pm25_val)
            self.curr.execute(sql3)
                    
        except Exception as e:
            logging.info("< Error > alter_sensor_setup_val : " + str(e))
        finally:
            self.__disconnect__()

    #####################
    # sensor_setup_val
    #####################
    def sensor_setup_val(self , s_position , s_tag_name):
        
        self.__connect__()
        try:
            sql = "select s_tag_high_val from `sensor_setup` where s_position='{0}' and s_tag_name='{1}'".format(s_position , s_tag_name)
            self.curr.execute(sql)
            res = self.curr.fetchone()

            return res[0]

        except Exception as e:
            logging.info("< Error > sensor_setup_val : " + str(e))
        finally:
            self.__disconnect__()
    
    ###################
    # government_aqi
    ###################
    def government_aqi(self , county , site_name , item):
        
        self.__connect_government__()
        try:
            sql = "SELECT publish_time , {0} FROM `2023_04_aqi` WHERE county='{1}' and site_name='{2}' order by no desc limit 0,1".format(item , county , site_name)
            self.g_curr.execute(sql)
            res = self.g_curr.fetchall()

            return res

        except Exception as e:
            logging.info("< Error > government_aqi : " + str(e))
        finally:
            self.__disconnect_government__()

    ###########################
    # submit_add_new_account
    ###########################
    def submit_add_new_account(self , a_user , a_pwd , a_lv , a_position , a_comment):
        
        self.__connect__()
        try:
            r_year = time.strftime("%Y" , time.localtime())
            r_month = time.strftime("%m" , time.localtime())
            r_day = time.strftime("%d" , time.localtime())
            r_time = time.strftime("%H:%M:%S" , time.localtime())
            
            sql = "select count(*) from account where a_user='{0}' and a_status='run' ".format(a_user)
            self.curr.execute(sql)
            res = self.curr.fetchone()
            
            if res[0] == 0:
                sql2 = "insert into account (a_user , a_pwd , a_lv , a_position , a_comment , a_status , r_year , r_month , r_day , r_time) value('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}')".format(a_user , a_pwd , a_lv , a_position , a_comment , 'run' , r_year , r_month , r_day , r_time)
                res2 = self.curr.execute(sql2)
                
                if res2:
                    return 'ok'
                
            elif res[0] == 1:
                pass

        except Exception as e:
            logging.info("< Error > submit_add_new_account : " + str(e))
            
        finally:
            self.__disconnect__()
    
    #######################
    # submit_del_account
    #######################
    def submit_del_account(self , a_user , a_pwd):
        
        self.__connect__()
        try:
            #sql = "update account set a_status='stop' where a_user='{0}' and a_pwd='{1}'".format(a_user , a_pwd)
            sql = "delete from account where a_user='{0}' and a_pwd='{1}'".format(a_user , a_pwd)
            res = self.curr.execute(sql)
            
            if res:
                return 'ok'

        except Exception as e:
            logging.info("< Error > submit_del_account : " + str(e))
            
        finally:
            self.__disconnect__()
    
    #########################
    # submit_alter_account
    #########################
    def submit_alter_account(self , a_user , a_pwd , a_position , a_comment):
        
        self.__connect__()
        try:
            sql = "update account set a_pwd='{0}' , a_position='{1}' , a_comment='{3}' where a_user='{2}'".format(a_pwd , a_position , a_user , a_comment)
            res = self.curr.execute(sql)
            
            if res:
                return 'ok'

        except Exception as e:
            logging.info("< Error > submit_alter_account : " + str(e))
            
        finally:
            self.__disconnect__()
    
    ##################
    # account_alter
    ##################
    def account_alter(self , user):
        
        self.__connect__()
        try:
            sql = "select a_user , a_pwd , a_lv , a_position , a_comment from account where a_lv='3' and a_user='{0}'".format(user)
            self.curr.execute(sql)
            res = self.curr.fetchall()

            return res

        except Exception as e:
            logging.info("< Error > account_alter : " + str(e))

        finally:
            self.__disconnect__()

    #################
    # account_list
    #################
    def account_list(self):
        
        self.__connect__()
        try:
            sql = "select a_user , a_pwd , a_position from account where a_lv='3' and  a_status='run' order by no desc"
            self.curr.execute(sql)
            res = self.curr.fetchall()

            return res

        except Exception as e:
            logging.info("< Error > account_list : " + str(e))
        finally:
            self.__disconnect__()
    
    #######################
    # sensor_final_setup
    #######################
    def sensor_final_setup(self , position , item):
        
        self.__connect__()
        try:
            r_month = time.strftime("%Y_%m" , time.localtime())
            
            sql = "select s_tag_high_val from sensor_setup where s_position='{0}' and s_tag_name='{1}'  order by no desc limit 0,1".format(position , item)
            self.curr.execute(sql)
            res = self.curr.fetchone()   
            return res[0]
            
        except Exception as e:
            logging.info('< Error > sensor_final_setup : ' + str(e))
        finally:
            self.__disconnect__()
    
    ######################
    # sensor_final_date
    ######################
    def sensor_final_date(self , position):
        
        self.__connect__()
        try:
            r_month = time.strftime("%Y_%m" , time.localtime())
            
            sql = "select r_year , r_month , r_day , r_time from {0} where s_content='{1}' order by no desc limit 3,1".format(r_month , position)
            self.curr.execute(sql)
            res = self.curr.fetchall()   
            return res
            
        except Exception as e:
            logging.info('< Error > sensor_final_date : ' + str(e))
        finally:
            self.__disconnect__()
    
    #######################
    # sensor_detail_data
    #######################
    def sensor_detail_data(self , position):
        
        self.__connect__()
        try:
            r_month = time.strftime("%Y_%m" , time.localtime())
            
            sql = "select s_content , tag_name , val , unit , r_status , r_year , r_month , r_day , r_time from {0} where s_content='{1}' order by no desc limit 3,3".format(r_month , position)
            self.curr.execute(sql)
            res = self.curr.fetchall()   
            return res
            
        except Exception as e:
            logging.info('< Error > sensor_detail_data : ' + str(e))
        finally:
            self.__disconnect__()
    
    #################
    # sensor_total
    #################
    def sensor_total(self , user):
        
        self.__connect__()
        try:
            r_time = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime())
            r_month = time.strftime("%Y_%m" , time.localtime())
            
            sql2 = "select a_position from account where a_user='{0}'".format(user)
            self.curr.execute(sql2)
            res2 = self.curr.fetchone()

            if res2[0] == 'all':
                sql = "select distinct s_content from {0}".format(r_month)
                self.curr.execute(sql)
                res = self.curr.fetchall()
                
                return res
            else:
                return res2[0]

        except Exception as e:
            logging.info("< Error > sensor_total : " + str(e))
        finally:
            self.__disconnect__()

    ##################
    # account_total
    ##################
    def account_total(self):
        
        self.__connect__()
        try:
            sql = "select count(*) from account where a_lv='3' and a_status='run' order by no desc"
            self.curr.execute(sql)
            res = self.curr.fetchone()

            return res[0]

        except Exception as e:
            logging.info("< Error > account_manager_list : " + str(e))
        finally:
            self.__disconnect__()

    #####################
    # check_login_code
    #####################
    def check_login_code(self,user,login_code):
        
        try:
            self.user = user
            self.login_code = login_code

            self.__connect__()

            sql = "select login_code from login_out_record where a_user='{0}' order by no desc limit 0,1".format(self.user)
            self.curr.execute(sql)
            self.res = self.curr.fetchone()

            if self.res[0] == self.login_code:
                return 'ok'

        except Exception as e:
            logging.info("< Error > check login code : " + str(e))

        finally:
            self.__disconnect__()

    ##########
    # login
    ##########
    def login(self,user,pwd):
        
        try:
            self.user = user
            self.pwd  = pwd

            self.__connect__()

            self.sql = "select a_lv from account where a_user='{0}' and a_pwd='{1}' and a_status='run'".format(self.user , self.pwd)
            self.curr.execute(self.sql)
            self.res = self.curr.fetchone()

            return self.res

        except Exception as e:
            logging.info("< Error > login : " + str(e))

        finally:
            self.__disconnect__()
        
    #################
    # login_record   
    ################# 
    def login_record(self,user,login_code,r_time,ip):
        
        try:
            self.user       = user
            self.login_code = login_code
            self.r_time     = r_time
            self.ip         = ip

            self.__connect__()

            self.sql2 = "insert into login_out_record(a_user,login_code,login_time,login_ip) value('{0}','{1}','{2}','{3}')".format(self.user , self.login_code , self.r_time , self.ip)
            self.curr.execute(self.sql2)

        except Exception as e:
            logging.info("< Error > login record : " + str(e))

        finally:
            self.__disconnect__()
    
    #####################
    # operation_record
    #####################
    def operation_record(self,r_time,user,login_code,item):
        
        try:
            self.r_time     = r_time
            self.user       = user
            self.item       = item
            self.login_code = login_code

            self.__connect__()
            self.sql = "insert into operation_record(r_time,a_user,item,login_code) value('{0}','{1}','{2}','{3}')".format(self.r_time , self.user , self.item , self.login_code)
            self.curr.execute(self.sql)

        except Exception as e:
            logging.info("< Error > operation record : " + str(e))

        finally:
            self.__disconnect__()
    
    ##################
    # logout_record
    ##################
    def logout_record(self,user,login_code,r_time):
        
        try:
            self.user = user
            self.login_code = login_code
            self.r_time = r_time

            self.__connect__()    

            self.sql = "update login_out_record set logout_time='{0}' where login_code='{1}' and a_user='{2}'".format(self.r_time , self.login_code , self.user)
            self.curr.execute(self.sql)

        except Exception as e:
            logging.info("< Error > logout record : " + str(e))

        finally:
            self.__disconnect__()

    ###########################
    # __connect_government__ 
    ###########################
    def __connect_government__ (self):
        
        try:
            self.g_conn = pymysql.connect(host=government_db['host'],port=government_db['port'],user=government_db['user'],password=government_db['pwd'],database=government_db['db'],charset=government_db['charset'])
            self.g_curr = self.g_conn.cursor()
        except Exception as e:
            logging.info("< ERROR > __connect_government__ " + str(e))
        finally:
            pass

    ##############################
    # __disconnect_government__
    ##############################
    def __disconnect_government__(self):
        
        try:
            self.g_conn.commit()
            self.g_conn.close()
        except Exception as e:
            logging.info("< ERROR > __disconnect__ : " + str(e))
        finally:
            pass
    
    ################
    # __connect__ 
    ################
    def __connect__(self):
        
        try:
            self.conn = pymysql.connect(host=kedge_db['host'],port=kedge_db['port'],user=kedge_db['user'],password=kedge_db['pwd'],database=kedge_db['db'],charset=kedge_db['charset'])
            self.curr = self.conn.cursor()
        except Exception as e:
            logging.info("< ERROR > __connect__ " + str(e))
        finally:
            pass

    ###################
    # __disconnect__
    ###################
    def __disconnect__(self):
        
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            logging.info("< ERROR > __disconnect__ : " + str(e))
        finally:
            pass

