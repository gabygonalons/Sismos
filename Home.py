import streamlit as st 
import pandas as pd
import folium 
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


######################################### Cabecera #########################################
#HEADER, "Título" o banner, aún se decide.
st.title("Sistema de Notificación Sísmica")
st.markdown('“Working towards global standardization of seismological networks and effective communication to the civilian community. ” ')
st.markdown("---")

######################################### RESULTADO ML #####################################
#CUERPO 1, "Machine learning", mapas y últimas alertas.
st.markdown("### Actividad últimos minutos")
st.markdown("Observación y clasificación sísmica en tiempo real")

#Crear columnas
col1, col2, col3 = st.columns(3)

with col1:
    #Transformación de la data
    mldf = pd.read_csv(r"combined_earthquake_data.csv")
    ultimosism = mldf["Coordinates"].iloc[-1]
    val = ultimosism.replace('[', '')
    val = val.replace(']','')
    val = val.replace(' ','')
    val = val.split(',')

    #EstructurarMapa
    lon = float(val[0])
    lat = float(val[1])
    nota = mldf['Place'].iloc[-1]
    mag = mldf['Magnitude'].iloc[-1]
    mapusa1 = folium.Map(location=[lat,lon], zoom_start=6)
    folium.Marker([lat, lon], popup= nota, tooltip= nota).add_to(mapusa1)
    #Título del Mapa
    st.markdown("### ***EEUU***")
    #Mostrar Mapa USA
    st_data = st_folium(mapusa1, height=250 ,width=220)
    #El texto de la alerta enviada   
    st.write("***Alertas enviada:***", nota, "/ *Magnitud:*", str(mag))

with col2:
    #Transformación de la data
    mexico = pd.read_csv(r'earthquakes_mexico.csv')
        
    #EstructurarMapa
    lon = mexico['Longitud'].iloc[-1]
    lat = mexico['Latitud'].iloc[-1]
    nota = mexico['Lugar'].iloc[-1]
    mag = mexico['Magnitud'].iloc[-1]
    mapmx = folium.Map(location=[lat,lon], zoom_start=6)
    folium.Marker([lat, lon], popup= nota, tooltip= nota).add_to(mapmx)
    #Título del Mapa 
    st.markdown("### ***MÉXICO***")
    #Mostrar Mapa México 
    st_data = st_folium(mapmx, height=250 ,width=220)
    #El texto de la alerta enviada    
    st.write("***Alertas enviada:***", nota, "/ *Magnitud:*", str(mag))

with col3:
    #Transformación de la data
    ultimosism = mldf["Coordinates"].iloc[-2]
    val = ultimosism.replace('[', '')
    val = val.replace(']','')
    val = val.replace(' ','')
    val = val.split(',')

    #EstructurarMapa
    lon = float(val[0])
    lat = float(val[1])
    nota = mldf['Place'].iloc[-2]
    mag = mldf['Magnitude'].iloc[-2]
    mapusa3 = folium.Map(location=[lat,lon], zoom_start=6)
    folium.Marker([lat, lon], popup= nota, tooltip= nota).add_to(mapusa3)

    #Título del Mapa
    st.markdown("### ***JAPÓN***")
    #Mostrar Mapa Japón
    st_data = st_folium(mapusa3, height=250 ,width=220)
    #El texto de la alerta enviada
    st.write("***Alertas enviada:***", nota, "/ *Magnitud:*", str(mag))

st.markdown("---")

######################################### DASSHBOARD ###################################################
#CUERPO 2, "Dashboard análisis histórico", filtros, y gráficos
st.markdown("<h1 style= 'text-align: center;'>Sísmos Mas Importantes</h1>", unsafe_allow_html=True)
mex = pd.read_csv(r"data mexico for analysis.csv")
jp = pd.read_csv(r"data japan for analysis.csv")
usa = pd.read_csv(r"data usa for analysis.csv")
usa['Year'] = pd.to_datetime(usa['Datetime']).dt.year
jp['Year'] = pd.to_datetime(jp['Datetime']).dt.year
mex['Year'] = pd.to_datetime(mex['Datetime']).dt.year
aniousa = usa['Year'].astype(int)
mmusa = usa['MMI Int']
aniomex = mex['Year'].astype(int)
mmmex = mex['MMI Int']
aniojp = jp['Year'].astype(int)
mmjp = jp['MMI Int']
sismos_por_aniousa = usa['Year'].value_counts().sort_index()
sismos_por_aniomex = mex['Year'].value_counts().sort_index()
sismos_por_aniojp = jp['Year'].value_counts().sort_index()
top_loc_usa = usa['Location Name'].value_counts().head(10)
top_loc_mex= mex['Location Name'].value_counts().head(10)
top_loc_jp = jp['Location Name'].value_counts().head(10)
data_usa = usa.filter(['Location Name', 'Latitude', 'Longitude'], axis=1)
data_mex = mex.filter(['Location Name', 'Latitude', 'Longitude'], axis=1)
data_jp = jp.filter(['Location Name', 'Latitude', 'Longitude'], axis=1)

st.markdown("<h3 style= 'text-align: right;'>Dashboard</h3>", unsafe_allow_html=True)

############ FITROS ******
st.sidebar.write("# Filtros para las visualizaciones")
paises = st.sidebar.radio('Seleccione un país de la Tri-Alianza',('Japón','México','EEUU'), horizontal = True)
if paises == 'Japón':
    top_loc = top_loc_jp
    data = data_jp
    zoom = 4
    anio = aniojp
    mm = mmjp
    sismos_por_anio = sismos_por_aniojp
elif paises == 'México':
    top_loc = top_loc_mex
    data = data_mex
    zoom = 4
    anio = aniomex
    mm = mmjp
    sismos_por_anio = sismos_por_aniomex
else:
    top_loc = top_loc_usa
    data = data_usa
    zoom = 2
    anio = aniousa
    mm = mmusa
    sismos_por_anio = sismos_por_aniousa

#year: start_year, end_year = st.slider('Seleccione un rango de año', options
rango_anios = st.sidebar.select_slider('Selecciona un rango de años', options=list(range(1900, 2021)), value=(1900, 2020))

################################## Gráficos ###################################
with st.container():
    col1, col2 = st.columns(2)
    with col1:
    
        ##########Grafico 1 col2
        fig = px.bar(y=top_loc.index, x=top_loc.values)
        fig.update_traces(marker_color='orange', width=0.5)
        fig.update_layout(xaxis_title='Localidades', yaxis_title='Cantidad de sismos', title='Cantidad de sismos por localidad', bargap=0.5)
        st.plotly_chart(fig, use_container_width=True)

        ##########Grafico 2 COL1

        data.rename(columns={'Latitude':'lat','Longitude':'lon'}, inplace=True)
        fig = px.scatter_mapbox(data, lat="lat", lon="lon", hover_name="Location Name", hover_data=["Location Name"],
                                color_discrete_sequence=["orange"], zoom=zoom, height=400)
        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {
                    "below": 'traces',
                    "sourcetype": "raster",
                    "sourceattribution": "Cantidad de Sismos",
                    "source": [
                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                    ]
                }
            ])
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

    # Mapa
    with col2:
        ###########GRAFICO 1 col 2.
        # Crear el gráfico de dispersión solo para los datos de Estados Unidos
    
        # Filtrar los datos por el rango de años seleccionado
        indices_filtrados = [i for i, a in enumerate(anio) if a >= rango_anios[0] and a <= rango_anios[1]]
        x_filtrados = [anio[i] for i in indices_filtrados]
        y_filtrados = [mm[i] for i in indices_filtrados]

        # Crear el primer gráfico de dispersión
        fig1 = go.Figure(data=go.Scatter(x=x_filtrados, y=y_filtrados, mode='markers', marker=dict(size=12, color='orange')))
        fig1.update_layout(xaxis_title='Años', yaxis_title='Escala de Mercalli', title='Sismos por nivel de daño (Escala Mercalli)')
        st.plotly_chart(fig1, use_container_width=True)

        ##################GRAFICO 2 Col 2
        # Filtrar los datos para el segundo gráfico
        sismos_filtrados = sismos_por_anio[(sismos_por_anio.index >= rango_anios[0]) & (sismos_por_anio.index <= rango_anios[1])]

        # Crear el segundo gráfico de líneas
        fig2 = px.line(x=sismos_filtrados.index, y=sismos_filtrados.values, markers=True)
        fig2.update_traces(line=dict(color='orange'))
        fig2.update_layout(xaxis_title='Año', yaxis_title='Cantidad de sismos', title='Cantidad de sismos por año')
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

import streamlit as st
 # Crear una variable de estado de sesión
if 'page' not in st.session_state:
    st.session_state.page = 1
 # Crear botones para navegar entre las páginas


    





#FOOTER, "Enlaces de interés"
