$(document).ready(function() { // вся мaгия пoсле зaгрузки стрaниц
    document.getElementById("pct").addEventListener("change", function () {
        if (this.files[0]) {
            var fr = new FileReader();

            fr.addEventListener("load", function () {
                try {
                    document.getElementById("LabelImage").style.backgroundImage = "url(" + fr.result + ")";
                }catch (e) {

                }
                 try {
                    document.getElementById("LabelImage2").style.backgroundImage = "url(" + fr.result + ")";
                }catch (e) {

                }

            }, false);

            fr.readAsDataURL(this.files[0]);
            }
        });



});

var files;

// Вешаем функцию на событие
// Получим данные файлов и добавим их в переменную

$('#pct').change(function(){
    files = this.files;
});

function productAddSubmit(){

    // file = $("#pct")[0].files[0];
    // alert(file);
    // file = $("#pct").prop('files')[0];
    // alert(file);
    // var fd = new FormData();
    // fd.append('image', file);

    let data = new FormData();
    $.each( files, function( key, value ){
        data.append( key, value );
    });

    let title = document.getElementById("title").value;
    let code = document.getElementById("code").value;
    let balance = document.getElementById("balance").value;
    let description = document.getElementById("description").value;

    data.append("title",title);
    data.append("code",code);
    data.append("balance",balance);
    data.append("description",description);
    alert("sendAjax...");

    $.ajax({
        url: '/product/add/',
        type: 'POST',
        data: data,
        cache: false,
        dataType: 'json',
        contentType: false,
        processData: false,
        success: function (data) {
            alert(data);
        }

    });
}
// $('input[type=file]').each(function(x){
//     var form = $('<form action="async-upload.php" method="post" enctype="multipart/form-data" target="iframe-name' + x + '"></form>');
//     //динамически создается айфрейм перед инпут файлом, что бы не сабмитить родительскую форму целиком обрамляю инпут формой и сабмичу во фрейм
//     $(this).before('<iframe name="iframe-name' + x + '" src="#"></iframe>').wrap(form).delay(1500).change(function(){
//         $(this).parent().submit().prev().one('load',
//         function(){
//             $(this).next()[0].reset(); //очищает инпут для того что бы не сабмитить файл в родительской форме
//             alert($(this).contents().find('body').html());
//         });
//     });
// });


// document.getElementById("asdfasdf").click( function () {
//   if (this.files[0]) {
//     var fr = new FileReader();
//
//     fr.addEventListener("load", function () {
//       document.getElementById("LabelImage").style.backgroundImage = "url(" + fr.result + ")";
//     }, false);
//
//     fr.readAsDataURL(this.files[0]);
//   }
// });