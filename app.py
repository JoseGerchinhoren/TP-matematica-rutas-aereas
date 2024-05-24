import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd

# Cargar el archivo CSV
data = pd.read_csv('aeropuertos.csv')

# Definir los aeropuertos de Argentina con sus coordenadas aproximadas
aeropuertos = {
    "Ezeiza": (-34.8222, -58.5358),
    "Córdoba": (-31.3156, -64.2088),
    "Mendoza": (-32.8317, -68.7928),
    "Tucumán": (-26.8400, -65.1042),
    "Salta": (-24.8560, -65.4862),
    "Rosario": (-32.9036, -60.7854),
    "Neuquén": (-38.9499, -68.1557),
    "Bariloche": (-41.1512, -71.1579),
    "Ushuaia": (-54.8433, -68.2950),
    "Comodoro Rivadavia": (-45.7859, -67.4655)
}

# Crear un grafo
G = nx.Graph()

# Añadir nodos (aeropuertos)
G.add_nodes_from(aeropuertos.keys())

# Añadir aristas (conexiones entre aeropuertos) desde el archivo CSV
for index, row in data.iterrows():
    G.add_edge(row['origen'], row['destino'], distancia=row['distancia'], tiempo=row['tiempo'], costo=row['costo'])

# Función para calcular el peso basado en costo y distancia
def peso(u, v, d):
    costo = d['costo']
    distancia = d['distancia']
    # Se da más peso al costo, normalizando y combinando con la distancia
    return costo * 1000 + distancia

def draw_map(route=None):
    plt.figure(figsize=(10, 10))
    m = Basemap(projection='merc', llcrnrlat=-55, urcrnrlat=-20, llcrnrlon=-75, urcrnrlon=-50, resolution='i')
    m.drawmapboundary(fill_color='lightblue')
    m.fillcontinents(color='lightgray', lake_color='lightblue')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    # Obtener posiciones de los nodos basados en sus coordenadas geográficas
    pos = {provincia: m(lon, lat) for provincia, (lat, lon) in aeropuertos.items()}

    # Dibujar el grafo sobre el mapa
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='yellow')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='blue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', font_color='black')

    if route:
        nx.draw_networkx_edges(G, pos, edgelist=route, edge_color='red', width=2.0)

    plt.title("Mapa de Conexiones Aéreas entre Provincias de Argentina")
    st.pyplot(plt)

st.title('Rutas de Vuelo en Argentina')
st.markdown('Selecciona el origen y el destino, en el sidebar, para ver la ruta de vuelo.')

# Crear formularios de entrada en el sidebar
origen = st.sidebar.selectbox('Selecciona la provincia de origen:', aeropuertos.keys())
destino = st.sidebar.selectbox('Selecciona la provincia de destino:', aeropuertos.keys())

# Botón para calcular la ruta en el sidebar
mostrar_ruta = st.sidebar.button('Mostrar Ruta')

if mostrar_ruta:
    if origen and destino:
        try:
            ruta = nx.shortest_path(G, source=origen, target=destino, weight=peso)
            st.success(f'Ruta encontrada: {" -> ".join(ruta)}')
            # Generar las aristas de la ruta
            edges = [(ruta[n], ruta[n+1]) for n in range(len(ruta)-1)]
            # Calcular costo y distancia total
            costo_total = 0
            distancia_total = 0
            
            st.markdown("### Detalles del viaje:")
            for u, v in edges:
                costo = G[u][v]['costo'] * 1000
                distancia = G[u][v]['distancia']
                st.info(f'**De {u} a {v}:** Costo ${costo}, Distancia {distancia} km')
                costo_total += costo
                distancia_total += distancia

            # Mostrar costo y distancia total solo si hay escalas
            if len(ruta) > 2:
                st.markdown("### Totales del viaje:")
                st.info(f'**Costo Total:** ${costo_total}')
                st.info(f'**Distancia Total:** {distancia_total} km')
            draw_map(route=edges)
            
        except nx.NetworkXNoPath:
            st.error('No existe una ruta entre las aeropuertos seleccionadas.')
    else:
        st.error('Por favor, selecciona tanto el origen como el destino.')
else:
    draw_map()
