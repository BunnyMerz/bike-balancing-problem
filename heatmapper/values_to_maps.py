from src.bikes import to_map
from examples.graphs.graph_loader import GraphLoader
from src.program import Main

i = 0
def save_to_file_maps(long_lats: list[tuple[float, float, float]]):
    lines = []
    for x,y,w in long_lats:
        a,b = to_map(x,y)
        line = f"{{location: new google.maps.LatLng({a}, {b}), weight: {w}}}," 
        lines.append('\t\t\t\t' + line + '\n')

    args = "".join(lines)

    _file = f'''
    <html>
    <head>
        <title>Heatmaps</title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>

        <link rel="stylesheet" type="text/css" href="../style.css" />
        <!-- <script type="module" src="index.js"></script> -->
    </head>
    <body>
        <div id="floating-panel">
        <button id="toggle-heatmap">Toggle Heatmap</button>
        <button id="change-gradient">Change gradient</button>
        <button id="change-radius">Change radius</button>
        <button id="change-opacity">Change opacity</button>
        </div>
        <div id="map"></div>

        <!-- 
        The `defer` attribute causes the callback to execute after the full HTML
        document has been parsed. For non-blocking uses, avoiding race conditions,
        and consistent behavior across browsers, consider loading using Promises.
        See https://developers.google.com/maps/documentation/javascript/load-maps-js-api
        for more information.
        -->
        <script
        src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB41DRUbKWJHPxaFjMAwdrzWzbVKartNGg&callback=initMap&libraries=visualization&v=weekly"
        defer
        ></script>
    </body>
    <script>
        // This example requires the Visualization library. Include the libraries=visualization
        // parameter when you first load the API. For example:
        // <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=visualization">
        let map, heatmap;

        function initMap() {{
        map = new google.maps.Map(document.getElementById("map"), {{
            zoom: 14,
            center: {{lat: -22.903892, lng: -43.105053}},
        }});
        heatmap = new google.maps.visualization.HeatmapLayer({{
            data: getPoints(),
            map: map,
        }});
        heatmap.set("radius", 40)
        document
            .getElementById("toggle-heatmap")
            .addEventListener("click", toggleHeatmap);
        document
            .getElementById("change-gradient")
            .addEventListener("click", changeGradient);
        document
            .getElementById("change-opacity")
            .addEventListener("click", changeOpacity);
        document
            .getElementById("change-radius")
            .addEventListener("click", changeRadius);
        }}

        function toggleHeatmap() {{
        heatmap.setMap(heatmap.getMap() ? null : map);
        }}

        function changeGradient() {{
        const gradient = [
            "rgba(0, 255, 255, 0)",
            "rgba(0, 255, 255, 1)",
            "rgba(0, 191, 255, 1)",
            "rgba(0, 127, 255, 1)",
            "rgba(0, 63, 255, 1)",
            "rgba(0, 0, 255, 1)",
            "rgba(0, 0, 223, 1)",
            "rgba(0, 0, 191, 1)",
            "rgba(0, 0, 159, 1)",
            "rgba(0, 0, 127, 1)",
            "rgba(63, 0, 91, 1)",
            "rgba(127, 0, 63, 1)",
            "rgba(191, 0, 31, 1)",
            "rgba(255, 0, 0, 1)",
        ];

        heatmap.set("gradient", heatmap.get("gradient") ? null : gradient);
        }}

        function changeRadius() {{
        heatmap.set("radius", heatmap.get("radius") ? null : 40);
        }}

        function changeOpacity() {{
        heatmap.set("opacity", heatmap.get("opacity") ? null : 0.2);
        }}

        // Heatmap data: 500 Points
        function getPoints() {{
        return [
            {args}
        ]
        }}

        window.initMap = initMap;
    </script>
    </html>
    '''
    global i
    i += 1
    with open(f'heatmapper/saved/start{i}.html', 'w') as _f:
        _f.write(_file)