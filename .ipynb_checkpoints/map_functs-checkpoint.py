import folium as f

def generatemap(lookat):
    # Render Map
    return f.Map(location=lookat, zoom_start=15)

def plot_features(features,MAP):
    for feature in features:

        if feature.Type == 'Point':
            f.Marker(feature.midpoint, popup=feature.name, color=feature.color).add_to(MAP)
        elif feature.Type == 'Linesting':
            f.PolyLine(feature.coords, color = feature.color).add_to(MAP)
        else:
            f.Polygon(feature.coords, color = feature.color).add_to(m)
            f.Marker(feature.midpoint, color = feature.color, popup = feature.name).add_to(MAP)