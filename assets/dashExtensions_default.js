window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng) {
            const flag = L.icon({
                iconUrl: `/static/assets/target.png`,
                iconSize: [30, 30]
            });
            return L.marker(latlng, {
                icon: flag
            });
        }
    }
});