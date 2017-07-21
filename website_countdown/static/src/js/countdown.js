$(document).ready(function () {
    $(this).find('.countdown').each(function() {
        var d= new Date($(this).attr('value').split('-').join("/"));
        var formated_date = d.getMonth() + 1 + '/' + d.getDate() + '/' + d.getFullYear() + ' ' +  d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
        $(this).downCount({
            date : formated_date,
            offset : +1
        });
    });
});

