/*
* Author   : JasonHung
* Date     : 20220211
* Update   : 20230419
* Function : JNC CB and sensor value
*/

/*
 * database  tinfar_kedge
 */ 
create database tinfar_kedge DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
use tinfar_kedge;


/* 
 * sensor_setup
 */
create table sensor_setup(
no int not null primary key AUTO_INCREMENT,
r_time datetime null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
account varchar(50) null,
s_position varchar(50) null,
s_tag_name varchar(50) null,
s_tag_high_val varchar(50) null,
s_tag_low_val varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_南門市場','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_南門市場','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_南門市場','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_桃園會展','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_桃園會展','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_桃園會展','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_泰山社宅','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_泰山社宅','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_泰山社宅','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_二重埔','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_二重埔','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_二重埔','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_民權東路案','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_民權東路案','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_民權東路案','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_秀朗橋案','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_秀朗橋案','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_秀朗橋案','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_裕毛屋','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_裕毛屋','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_裕毛屋','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_後龍大橋','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_後龍大橋','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_後龍大橋','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C611世賢南','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C611世賢南','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C611世賢南','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C611宏仁女中','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C611宏仁女中','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C611宏仁女中','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C612嘉北車站','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C612嘉北車站','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C612嘉北車站','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C612北興','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C612北興','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_嘉義車站C612北興','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_台南車站一號口','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_台南車站一號口','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_台南車站一號口','pm25','10');

insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_台南車站四號口','噪音','70');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_台南車站四號口','pm10','20');
insert into `sensor_setup` (account , s_position , s_tag_name , s_tag_high_val) value('kedge','s_p_台南車站四號口','pm25','10');

/* 
 * sensor_alarm
 */
create table sensor_alarm(
no int not null primary key AUTO_INCREMENT,
r_time datetime null,
r_year varchar(10) null,
r_month varchar(10) null,
r_day varchar(10) null,
account varchar(50) null,
a_position varchar(50) null,
a_tag_name varchar(50) null,
a_tag_val varchar(50) null,
a_comment text null,
a_time datetime null,
sign_status varchar(50) null,
sign_time datetime null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/* 
 * operation_record
 */
create table operation_record(
no int not null primary key AUTO_INCREMENT,
a_user varchar(200) null,
login_code varchar(200) null,
r_time datetime null,
item varchar(50) null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/* 
 * login_out_record
 */
create table login_out_record(
no int not null primary key AUTO_INCREMENT,
a_user varchar(200) null,
login_code varchar(200) null,
login_ip varchar(100) null,
login_time datetime null,
logout_time datetime null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


/* 
 * account
 */
create table account(
no int not null primary key AUTO_INCREMENT,
r_year varchar(100) null,
r_month varchar(100) null,
r_day varchar(100) null,
r_time time null,
a_user varchar(200) null,
a_pwd varchar(200) null,
a_lv varchar(10) null,
a_position varchar(100) null,
a_status varchar(50) null,
a_comment text null
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

insert into account (a_user , a_pwd , a_lv , a_status , a_position) VALUES('admin','1qaz#123','1','run' , 'all');
insert into account (a_user , a_pwd , a_lv , a_status , a_position) VALUES('kedge','kedge#123','2','run' , 'all');