function sensor_alarm_form(val){
        var data = val;

        $.ajax({
                type:"POST",
                url:"/load_alter_sensor_form",
                data:{
                        "form":data
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        alert(xhr.status);
                        alert(xhr.responseText);
                        alert(throwError);
                        alert(ajaxError)
                },
                success:function(res){
                        
                        var action_form = "#" + data + "_form";
                        $(action_form).show(1000).html(res);

                        // scroll page bottom to page top
                        //goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("載入 " + data + " 處理動作表格資料 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
}

function submit_alter_sensor_setup(val){
        var val1 = "#"+val+"_db";
        var val2 = "#"+val+"_pm10";
        var val3 = "#"+val+"_pm25";
        var val4 = "#"+val+"_position";
        
        var db   = $(val1).val();
        var pm10 = $(val2).val();
        var pm25 = $(val3).val();
        var a_position = $(val4).val();

        $.ajax({
                type:"POST",
                url:"/submit_alter_sensor_form_value",
                data:{
                        'db':db,
                        'pm10':pm10,
                        'pm25':pm25,
                        'a_position':a_position
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        alert(xhr.status);
                        alert(xhr.responseText);
                        alert(throwError);
                        alert(ajaxError)
                },
                success:function(res){
                        
                        $("#main_sensor_content").show(1000).html(res);

                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("送出修改 " + a_position + " 數值表格資料 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
}

function add_sensor_form(val){
        var position = val;

        $.ajax({
                type:"POST",
                url:"/load_add_sensor_form",
                data:{
                        'position':position
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        alert(xhr.status);
                        alert(xhr.responseText);
                        alert(throwError);
                        alert(ajaxError)
                },
                success:function(res){
                        
                        var s_position = "#"+position+"_form"
                        $(s_position).show(1000).html(res);

                        // scroll page bottom to page top
                        //goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("新增 " + position + " 數值資料表格 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
}
function kedge_cancel_sensor_form(val){
        var data = val
        var hide_form = "#"+data
        $(hide_form).hide(1000);     
}

function submit_add_new_account(){
        var a_user     = $("#a_account_user").val();
        var a_pwd      = $("#a_account_pwd").val();
        var a_lv       = $("#a_account_lv").val();
        var a_position = $("#a_account_position").val();
        var a_comment  = $("#a_account_comment").val();

        // check submit data
        if(a_user.length == 0){
                alert("帳號不能空白 !");
                exit();
        }else if(a_pwd.length == 0){
                alert("密碼不能空白 !");
                exit();
        }else if(a_position.length == 0){
                alert("位置不能空白 !");
                exit();
        }
        else{
                $.ajax({
                        type:"POST",
                        url:"/submit_add_new_account",
                        data:{
                                'a_user':a_user,
                                'a_pwd':a_pwd,
                                'a_lv':a_lv,
                                'a_position':a_position,
                                'a_comment':a_comment
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                alert('帳號 ' + a_user + ' , 新增完成.');
                                $("#kedge_alter_account_form").hide(1000);
                                $("#main_content").show(1000).html(res);

                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("送出新增 " + a_user + " 帳號資料 ...").css({'color':'blue'});
                        },
                        complete:function(){
                                $('#status').css({'color':'white'});
                        }
                });
        }
        
}

function submit_add_account(){

        $.ajax({
                type:"POST",
                url:"/submit_add_account",
                data:{
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        alert(xhr.status);
                        alert(xhr.responseText);
                        alert(throwError);
                        alert(ajaxError)
                },
                success:function(res){
                        
                        $("#kedge_alter_account").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("新增 帳號資料 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
        
}

function kedge_del_alter(){
        var a_user     = $("#a_account_user").val();
        var a_pwd      = $("#a_account_pwd").val();

        var check_del = prompt("刪除 " + a_user + " 帳號 , 確定刪除 , 再按一次 y ");
        
	if(check_del == 'y'){	
                $.ajax({
                        type:"POST",
                        url:"/submit_del_account",
                        data:{
                                'a_user':a_user,
                                'a_pwd':a_pwd
                        },
                        datatype:"html",
                                error:function(xhr , ajaxError , throwError){
                                alert(xhr.status);
                                alert(xhr.responseText);
                                alert(throwError);
                                alert(ajaxError)
                        },
                        success:function(res){
                                
                                alert('帳號 ' + a_user + ' , 刪除完成.');
                                $("#main_content").show(1000).html(res);
                                $("#kedge_alter_account_form").hide(1000);
                                
                                // scroll page bottom to page top
                                goto_top();
                                
                                //location.reload(true);
                        },
                        beforeSend:function(){
                                $('#status').html("送出刪除 " + a_user + " 帳號資料 ...").css({'color':'blue'});
                        },
                        complete:function(){
                                $('#status').css({'color':'white'});
                        }
                });
        }else{
                exit();
        }
        
}

function submit_alter_account(){
        var a_user     = $("#a_account_user").val();
        var a_pwd      = $("#a_account_pwd").val();
        var a_position = $("#a_account_position").val();
        var a_comment  = $("#a_account_comment").val();

        $.ajax({
                type:"POST",
                url:"/submit_alter_account",
                data:{
                        'a_user':a_user,
                        'a_pwd':a_pwd,
                        'a_position':a_position,
                        'a_comment':a_comment
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        alert(xhr.status);
                        alert(xhr.responseText);
                        alert(throwError);
                        alert(ajaxError)
                },
                success:function(res){
                        
                        $("#kedge_alter_account_form").hide(1000);
                        alert('帳號 ' + a_user + ' , 修改完成.');
                        $("#main_content").show(1000).html(res);

                        //kedge_account_manager();
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("送出修改 " + a_user + " 帳號資料 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
        
}

function alter_account_position(){
        var data = $("#change_account_position").val();
        $("#a_account_position").val(data);
}

function kedge_cancel_alter(){
        $("#kedge_alter_account_form").hide(1000);     
}

function kedge_account_manager(){

        $.ajax({
                type:"POST",
                url:"/account_manager",
                data:{
                        
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        alert(xhr.status);
                        alert(xhr.responseText);
                        alert(throwError);
                        alert(ajaxError)
                },
                success:function(res){
                        
                        //$("#kedge_alter_account").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        //goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("載入帳號清單 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
}

function kedge_alter_account(val){
        var account = val;

        $.ajax({
                type:"POST",
                url:"/load_alter_account",
                data:{
                        'account':account
                },
                datatype:"html",
                        error:function(xhr , ajaxError , throwError){
                        alert(xhr.status);
                        alert(xhr.responseText);
                        alert(throwError);
                        alert(ajaxError)
                },
                success:function(res){
                        
                        $("#kedge_alter_account").show(1000).html(res);
                        
                        // scroll page bottom to page top
                        goto_top();
                        
                        //location.reload(true);
                },
                beforeSend:function(){
                        $('#status').html("loading " + account + " 帳號資料 ...").css({'color':'blue'});
                },
                complete:function(){
                        $('#status').css({'color':'white'});
                }
        });
}

function goto_top(){
        
        // scroll page bottom to page top
        jQuery("html,body").animate({scrollTop:0},1000);
        $('#goto_top').css({'cursor':'pointer'});

}

