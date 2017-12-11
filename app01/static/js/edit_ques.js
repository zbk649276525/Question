/**
 * Created by zbk on 2017/12/10.
 */

//绑定删除问题事件
$(".question_list").on("click",".fork",function () {
    $(this).parent().parent().remove()
})

//绑定添加问题事件
$(".add").click(function () {
    s = '<li><div pk ="" class = "pk"><div class = "form-group" ><label for= "id_caption" class = "col-md-2 control-label">问题名称：</label > <div class = "col-md-10"><textarea name = "caption" cols = "40" rows = "10" class = "form-control" style = "resize:none; width:500px; height:40px;"maxlength = "64"required = ""id = "id_caption" > </textarea > </div > </div > <hr > <div style = "height: 50px;" > </div > <div class = "form-group" > <label for= "id_tp" class = "col-md-2 control-label" > 问题类型：</label > <div class = "col-md-3 add_btn" > <select name = "tp"class = "form-control"id = "select_change"required = "" > <option value = ""selected = "" > --------- </option > <option value = "1" > 打分 </option > <option value = "2" > 单选 </option > <option value = "3" > 评价 </option > </select > </div > <div class = "col-md-2" > <span style = "font-size: 20px"class = "add_tp" > <a href = "#add_tp"class = "">✚添加选项 </a > </span > </div > </div > <ul class = "choice_list" > </ul > <span class = "fork" style = "margin-left: 800px; font-size: 30px; color: gainsboro" >× </span > </div > </li > ';
    $(".question_list").append(s)
});

//事件委派
var form_l = $(".question_list");
form_l.on("click", ".add_tp", function () {
    s = '<div id="1"> <div class = "row" style = "margin-right: 100px; margin-top: 50px;" ><label for= "id_name" class = "col-md-2 control-label" > 内容：</label > <div class = "col-md-3" > <input type = "text"name = "name"value = ""class = "form-control"maxlength = "32"required = ""id = "id_name" > </div > <label for= "id_score" class = "col-md-2 control-label" > 分值：</label > <div class = "col-md-3" > <input type = "text"name = "score"value = ""class = "form-control"required = ""id = "id_score" > </div > <label class = "col_fork" >×</label > </div > </div > ';
    $(this).parent().parent().next().append(s)
}); //事件委派，绑定添加单选的事件
form_l.on("change","[name=tp]",function () {
    if ($(this).val() == 2 ){
        $(this).parent().next().children().children().removeClass("hide")    //如果等于单选，就展示“添加选项”
    }
    else{
        $(this).parent().next().children().children().addClass("hide");    //否则，就先添加hide属性，
        $(this).parent().parent().next().children().remove()        //  删除
    }
});  // 事件委派，绑定问题类型的事件
form_l.on("click",".col_fork",function () {
    $(this).parent().parent().remove()
})   //事件委派， 绑定问题选项的删除事件操作

//保存
$(".save").click(function () {
    var ajax_post_list = [];   //设一个空列表
    $(".pk").each(function () {     //
        var ajax_dict = {
            "id":$(this).attr("pk"),    //获取值
            "caption":$(this).find("textarea[name=caption]").val(), //找到值
            "tp":Number($(this).find("select[name=tp]").val()),     //找到值   number是把字符串转换成数字
            "options":[]    //预留一个空，好让我们提交。
        };
        if (ajax_dict["tp"]==2){
            $(this).find("ul[class=choice_list]").children().each(function () {
                ajax_dict["options"].push({     //push 相当于append
                    "id": $(this).attr("id"),
                    "name":$(this).find("input[name=name]").val(),
                    "score":$(this).find("input[name=score]").val()
                })
            })
        }
        console.log(ajax_dict['options'])
        ajax_post_list.push(ajax_dict);     //把找到值添加到新设的空列表
    });
    $.post({
        url: location.pathname,
        data: JSON.stringify(ajax_post_list),
        headers: {"X-CSRFToken": $.cookie("csrftoken")},
        contentType:"application/json",
        success: function (data) {
            console.log(data)
        }

    })
})
