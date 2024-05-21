import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Establecer el modo wide como predeterminado
st.set_page_config(layout="wide")

# Definir las provincias de Argentina con sus coordenadas aproximadas
provincias = {
    "Buenos Aires": (-34.6037, -58.3816),
    "Catamarca": (-28.4696, -65.7852),
    "Chaco": (-27.4516, -58.9868),
    "Chubut": (-43.3007, -65.1023),
    "Córdoba": (-31.4201, -64.1888),
    "Corrientes": (-27.4712, -58.8396),
    "Entre Ríos": (-32.0000, -60.0000),
    "Formosa": (-26.1775, -58.1781),
    "Jujuy": (-24.1858, -65.2995),
    "La Pampa": (-36.6206, -64.2901),
    "La Rioja": (-29.4111, -66.8507),
    "Mendoza": (-32.8895, -68.8458),
    "Misiones": (-27.3624, -55.9000),
    "Neuquén": (-38.9516, -68.0591),
    "Río Negro": (-41.1343, -71.3082),
    "Salta": (-24.7821, -65.4232),
    "San Juan": (-31.5375, -68.5364),
    "San Luis": (-33.2950, -66.3356),
    "Santa Cruz": (-51.6230, -69.2168),
    "Santa Fe": (-31.6333, -60.7000),
    "Santiago del Estero": (-27.7824, -64.2669),
    "Tierra del Fuego": (-54.8019, -68.3029),
    "Tucumán": (-26.8083, -65.2176)
}

# Crear un grafo
G = nx.Graph()

# Añadir nodos (provincias)
G.add_nodes_from(provincias.keys())

# Añadir aristas (conexiones entre provincias)
conexiones = [
    ("Buenos Aires", "Córdoba"), ("Buenos Aires", "Santa Fe"), ("Buenos Aires", "Entre Ríos"),
    ("Córdoba", "Santa Fe"), ("Córdoba", "Santiago del Estero"), ("Córdoba", "Catamarca"),
    ("Catamarca", "La Rioja"), ("Catamarca", "Tucumán"), ("La Rioja", "San Juan"),
    ("San Juan", "Mendoza"), ("Mendoza", "San Luis"), ("San Luis", "Córdoba"),
    ("Santa Fe", "Entre Ríos"), ("Entre Ríos", "Corrientes"), ("Corrientes", "Misiones"),
    ("Misiones", "Formosa"), ("Formosa", "Chaco"), ("Chaco", "Santiago del Estero"),
    ("Santiago del Estero", "Tucumán"), ("Tucumán", "Salta"), ("Salta", "Jujuy"),
    ("Jujuy", "Formosa"), ("La Pampa", "Buenos Aires"), ("La Pampa", "Neuquén"),
    ("Neuquén", "Río Negro"), ("Río Negro", "Chubut"), ("Chubut", "Santa Cruz"),
    ("Santa Cruz", "Tierra del Fuego")
]

G.add_edges_from(conexiones)

def draw_map(route=None):
    plt.figure(figsize=(10, 10))
    m = Basemap(projection='merc', llcrnrlat=-55, urcrnrlat=-20, llcrnrlon=-75, urcrnrlon=-50, resolution='i')
    m.drawmapboundary(fill_color='lightblue')
    m.fillcontinents(color='lightgray', lake_color='lightblue')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    # Obtener posiciones de los nodos basados en sus coordenadas geográficas
    pos = {provincia: m(lon, lat) for provincia, (lat, lon) in provincias.items()}

    # Dibujar el grafo sobre el mapa
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='yellow')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='blue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif', font_color='black')

    if route:
        nx.draw_networkx_edges(G, pos, edgelist=route, edge_color='red', width=2.0)

    plt.title("Mapa de Conexiones Aéreas entre Provincias de Argentina")
    st.pyplot(plt)

st.title('Rutas de Vuelo en Argentina')
st.markdown('Selecciona el origen y el destino para ver la ruta de vuelo.')

# Crear formularios de entrada
origen = st.selectbox('Selecciona la provincia de origen:', provincias.keys())
destino = st.selectbox('Selecciona la provincia de destino:', provincias.keys())

# Botón para calcular la ruta
mostrar_ruta = st.button('Mostrar Ruta')

if mostrar_ruta:
    if origen and destino:
        try:
            ruta = nx.shortest_path(G, source=origen, target=destino)
            st.success(f'Ruta encontrada: {" -> ".join(ruta)}')
            # Generar las aristas de la ruta
            edges = [(ruta[n], ruta[n+1]) for n in range(len(ruta)-1)]
            draw_map(route=edges)
        except nx.NetworkXNoPath:
            st.error('No existe una ruta entre las provincias seleccionadas.')
    else:
        st.error('Por favor, selecciona tanto el origen como el destino.')
else:
    draw_map()
