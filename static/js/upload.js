function showLoading() {
    document.getElementById("loading").style = "visibility: visible";
}

function hideLoading() {
    document.getElementById("loading").style = "visibility: hidden";
}


$("#upload").click(function () {
    //call show loading function here
    showLoading();
    $.ajax({
        type: "POST",
        url: "/uploader",
        enctype: 'multipart/form-data',
        data: {
            file: file
        },
        success: function () {
            //call hide function here
            hideLoading();
        },
        error: function (a) {//if an error occurs
            hideLoading();
        }
    });
});