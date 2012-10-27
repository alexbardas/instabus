(function () {
    if (!window.InstaBus) {
        window.InstaBus = {};
    }
    var map = InstaBus.map;
    var $map = $('#map')


    var onInit = function () {
        InstaBus.initMap()
    };


    $(onInit);
})();
