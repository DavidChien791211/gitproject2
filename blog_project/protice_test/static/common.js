function upload(){
        var url = '/picture/upload_picture/'
        formdata = new FormData();
        formdata.append("avatar",$("#avatar")[0].files[0]);
        $.ajax({
            processData: false,
            contentType: false,
            url: url,
            type: 'post',
            data: formdata,
            success: function(arg) {
                console.log(arg.code)
	            if (arg.code == 200) {
		            alert('成功！')
                    window.location.reload()
	            } else {
	                console.log(arg)
		            alert('失败！')
                    }
                }
            })

        }
function upload_img() {
        let formData = new FormData($("#img-form")[0]);
        $.ajax({
            url: "http://127.0.0.1:8000/picture/upload_img/", //请求路径
            type: 'POST', // 请求类型
            data: formData, // 请求数据
            dataType: "JSON", // 返回数据格式
            contentType: false, //表示不处理数据
            processData: false,
            cache: false,
            success: function (data) {
                if (data === 1) {
                    alert("上传成功");
                    url="picture"
                    $('#main').load(url)
                }else if (data === 0) {
                    alert("上传失败");
                }
            },
            error: function (data) {
                console.log(data);
            }
        });
}