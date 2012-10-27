(function () {
    if (!window.InstaBus) {
        window.InstaBus = {};
    }

    var onInit = function () {
        // Initialize the map
        window.InstaBus.initMap()
    };


    // on DOM Ready
    $(onInit);
})();
