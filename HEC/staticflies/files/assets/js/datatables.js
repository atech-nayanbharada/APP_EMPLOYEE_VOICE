$(document).ready(function () {
    var eventFired = function (type) {
        var n = $('#demo_info')[0];
        n.innerHTML += '<div>' + type + ' event - ' + new Date().getTime() + '</div>';
        n.scrollTop = n.scrollHeight;
    };
 
    $('#example')
        .on('order.dt', function () {
            eventFired('Order');
        })
        .on('search.dt', function () {
            eventFired('Search');
        })
        .on('page.dt', function () {
            eventFired('Page');
        })
        .DataTable();
});