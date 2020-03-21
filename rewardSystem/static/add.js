
// 添加复选框
$('.addCheckboxAll').click(function () {
    $("[name=student-list]:checkbox").prop("checked", this.checked)
});
// 添加
$(".add-student").click(function () {
    // alert("hello")
    var checkedarr = [];
    var count = $("[name=student-list]:checkbox:checked").length
    var meeting_id = $(".meeting_id").val()
    if(count>0){
        $("[name=student-list]:checkbox:checked").each(function () {
            if($(this).val() != "on"){
                checkedarr.push($(this).val());
            }
        })
        var randint = "";
        for(var i = 0; i < 4; i++){
            randint += Math.floor(Math.random()*10);
        }
        var con=prompt("请输入随机验证码:" + randint );
        if(con == randint){
            $.ajax(
                {
                    url: changehousts,
                    type: "post",
                    cache: false,
                    data: {"student_id": JSON.stringify(checkedarr),"meeting_id": meeting_id, csrfmiddlewaretoken:csrf_token},
                    // data: {"student_id": JSON.stringify(checkedarr), "meeting_id":meeting_id, },
                    success: function(data) {
                        if(data.status == "成功"){
                            alert("添加成功"+count+"人")
                            // window.location.reload();
                        }else {
                            alert("添加失败")
                        }
                    },
                    error: function (xhr) {
                        console.log("出现问题")

                    }
                }
            )
        }else {
            alert("验证码错误")
        }
    }else {
        alert("请至少选择一个")
    }
})

// 修改保存
