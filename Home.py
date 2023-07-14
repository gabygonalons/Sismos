import streamlit as st 
import pandas as pd
import folium 
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

######################################## Configuración #################################
st.set_page_config(
    page_title="Sismos-Notificación",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded")

######################################### Cabecera #########################################
#HEADER, "Título" o banner, aún se decide.
st.title("Sistema de Notificación Sísmica")


st.markdown('“Working towards global standardization of seismological networks and effective communication to the civilian community. ” ')

st.markdown("---")

######################################### RESULTADO ML #####################################
#CUERPO 1, "Machine learning", mapas y últimas alertas.
st.markdown("### Actividad últimos minutos")
if st.button('Earthquake Classfication APP'):
    link='[Real Time Earthquake Classfication APP](http://54.233.115.161:8501/)'
    st.markdown(link,unsafe_allow_html=True)

with st.expander("Observación y clasificación sísmica en tiempo real"):

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
st.markdown("<h3 style= 'text-align: center;'>Datos Históricos y Rendimiento del Proyecto</h3>", unsafe_allow_html=True)
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
rango_anios = st.sidebar.select_slider('Selecciona un rango de años', options=list(range(1900, 2023)), value=(1900, 2022))

################################## Gráficos ###################################

tab1, tab2 = st.tabs(["     Sísmos Importantes     ", "     KPIs     "])
with tab1:
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
        
            ##########Grafico 1 col2
            data.rename(columns={'Latitude':'lat','Longitude':'lon'}, inplace=True)
            fig = px.scatter_mapbox(data, lat="lat", lon="lon", hover_name="Location Name", hover_data=["Location Name"],
                                    color_discrete_sequence=["orange"], zoom=zoom, height=350)
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

        with col2:
            ##########Grafico 2 COL1
            fig = px.bar(y=top_loc.index, x=top_loc.values)
            fig.update_traces(marker_color='orange', width=0.5)
            fig.update_layout(xaxis_title='Localidades', yaxis_title='Cantidad de sismos', title='Sismos por localidad', bargap=0.5, height=380)
            st.plotly_chart(fig, use_container_width=True)
            
    with st.container():        
        col1, col2 = st.columns(2)        
        
        with col1:
            ###########GRAFICO 1 col 2.
            indices_filtrados = [i for i, a in enumerate(anio) if a >= rango_anios[0] and a <= rango_anios[1]]
            x_filtrados = [anio[i] for i in indices_filtrados]
            y_filtrados = [mm[i] for i in indices_filtrados]

            # Crear el primer gráfico de dispersión
            fig1 = go.Figure(data=go.Scatter(x=x_filtrados, y=y_filtrados, mode='markers', marker=dict(size=9, color='orange')))
            fig1.update_layout(xaxis_title='Años', yaxis_title='Escala de Mercalli', yaxis=dict(range=[0, 12]), title='Sismos por nivel de daño (Escala Mercalli)', height=360)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            ##################GRAFICO 2 Col 2
            st.markdown(' ')
            # Filtrar los datos para el segundo gráfico
            sismos_filtrados = sismos_por_anio[(sismos_por_anio.index >= rango_anios[0]) & (sismos_por_anio.index <= rango_anios[1])]

            # Crear el segundo gráfico de líneas
            fig2 = px.line(x=sismos_filtrados.index, y=sismos_filtrados.values, markers=True)
            fig2.update_traces(line=dict(color='orange'))
            fig2.update_layout(xaxis_title='Año', yaxis_title='Cantidad de sismos', title='Sismos por año', margin = dict(b=36), height=315)
            st.plotly_chart(fig2, use_container_width=True)
    with st.expander("***¿Qué es la La Escala de Mercalli?***"):
        st.markdown("***La Escala de Mercalli*** evalúa los efectos y daños observados en estructuras, personas y el entorno. Esta escala va desde el grado I (no se siente) hasta el grado XII (daños totales).")

with tab2:
    ################################## KPIs######################################################################
    tab1, tab2, tab3, tab4 = st.tabs(["Tasa de Click de la notificación de la app", "Tasa de fallos", "Tiempo de Ejecución", "Tasa de satisfacción" ])
    df = pd.read_csv('data_indicadores.csv')
    col1, col2 = st.columns(2)
    with tab1:
        #########################Tasa de Click de la notificación de la app
        # Convertir la columna 'date' a tipo fecha
        df['date'] = pd.to_datetime(df['date'])

        # Ordenar los datos por fecha
        df = df.sort_values('date')

        # Calcular la tasa de clic de las páginas con oferta premium
        df['click_rate_pages'] = (df['users on pages with premium offer'] / df['total users']) * 100

        # Crear la figura del gráfico de la tasa de clic
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number+gauge+delta",
            value=df['click_rate_pages'].iloc[-1],  # Último valor de la tasa de clic
            delta={'reference': 1.01, 'increasing': {'color': "green"}},
            domain={'x': [0.1, 0.9], 'y': [0.2, 0.9]},
            title={'text': "Tasa de Click de la notificación a la app"},
            gauge={
                'shape': 'angular',
                'axis': {'range': [0, 100]},  # Actualizar el rango del eje vertical
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, 100], 'color': 'white'},  # Eliminar los rangos de color
                ]
            }
        ))

        # Configurar la actualización de la tasa de clic en función del control deslizante
        steps = []
        for i, row in df.iterrows():
            step = dict(
                method='restyle',
                args=['value', [row['click_rate_pages']]],
                label=f"Week {row['month']}-{row['day']}"
            )
            steps.append(step)

        sliders = [dict(
            active=len(df)-1,
            currentvalue={ "xanchor": "center"},
            pad={"t": 50},
            steps=steps
        )]

        fig.update_layout(
            sliders=sliders,
            autosize=False,
            width=500,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:

        ###########################"Tasa de fallos"##################
        # Convertir la columna 'date' a tipo fecha
        df['date'] = pd.to_datetime(df['date'])

        # Ordenar los datos por fecha
        df = df.sort_values('date')

        # Calcular la tasa de fallos
        df['failure_rate'] = (df['failure_count'] / df['total users']) * 100

        # Obtener el último valor y el penúltimo valor de la tasa de fallos
        last_value = df['failure_rate'].iloc[-1]
        previous_value = df['failure_rate'].iloc[-2]

        # Crear la figura del gráfico de la tasa de fallos
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="number+gauge+delta",
            value=last_value,
            delta={'reference': previous_value, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
            domain={'x': [0.1, 0.9], 'y': [0.2, 0.9]},
            title={'text': "Tasa de fallos"},
            gauge={
                'shape': 'angular',
                'axis': {'range': [0, 10]},  # Modificar el rango del eje vertical
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, max(df['failure_rate'])], 'color': 'white'},
                ]
            }
        ))

        # Configurar la actualización de la tasa de fallos en función del control deslizante
        steps = []
        for i, row in df.iterrows():
            step = dict(
                method='restyle',
                args=['value', [row['failure_rate']]],
                label=f"Week {row['month']}-{row['day']}"
            )
            steps.append(step)

        sliders = [dict(
            active=len(df) - 1,
            currentvalue={"xanchor": "center"},
            pad={"t": 50},
            steps=steps
        )]

        fig.update_layout(
            sliders=sliders,
            autosize=False,
            width=500,
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)
  
    with tab3:
        ########################## "Tiempo de Ejecución"#######################
        # Crear el DataFrame con datos resumidos
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05', ...],
            'execution_avg': [2.00, 6.00, 8.00, 2.00, 2.00, ...],
            'month': [1, 1, 1, 1, 1, ...],
            'day': [1, 2, 3, 4, 5, ...]
        })

        # Convertir la columna 'date' a tipo fecha
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Filtrar los últimos 6 meses
        last_6_months = pd.date_range(end=df['date'].max(), periods=6, freq='D')
        df = df[df['date'].isin(last_6_months)]

        # Calcular la diferencia respecto al día anterior
        df['execution_diff'] = df['execution_avg'].diff()

        # Crear la figura del gráfico del indicador de tiempo promedio de ejecución
        fig = go.Figure(go.Indicator(
            mode="number+gauge+delta",
            gauge={'shape': "bullet", 'bar': {'color': 'orange'}},  # Cambiar el color de la barra a naranja
            value=df['execution_avg'].iloc[-1],  # Último valor del tiempo promedio de ejecución
            delta={'reference': df['execution_avg'].iloc[-2], 'relative': True, 'increasing': {'color': "red"}},
            domain={'x': [0.1, 1], 'y': [0.2, 0.9]},
            title={'text': "Tiempo<br>Promedio<br>de Ejecución", 'font': {'size': 18}},
            gauge_axis={
                'range': [0, 10],  # Rango de valores para la barra verde (0 ms a 10 ms)
                'tickmode': 'array',
                'tickvals': [0, 2, 4, 6, 8, 10],  # Valores de los ticks inferiores (0 ms a 10 ms)
                'ticktext': ['0 ms', '2 ms', '4 ms', '6 ms', '8 ms', '10 ms']  # Texto de los ticks inferiores
            }
        ))

        # Configurar la actualización interactiva del tiempo promedio de ejecución en función del control deslizante
        steps = []
        dates = ['14 Jul', '15 Jul', '16 Jul', '17 Jul', '18 Jul']  # Fechas personalizadas
        for i, row in df.iterrows():
            step = dict(
                method='restyle',
                args=['value', [row['execution_avg']]],
                label=f"Día {dates[i]}"  # Etiqueta personalizada para cada día
            )
            steps.append(step)

        sliders = [dict(
            active=len(df) - 1,
            currentvalue={"prefix": "Fecha: ", "visible": True, "xanchor": "center"},
            pad={"t": 50},
            steps=steps
        )]

        fig.update_layout(
            sliders=sliders,
            autosize=False,
            width=700,
            height=400,
            showlegend=False  # Eliminar leyenda de la barra interactiva
        )

        # Mostrar el gráfico interactivo
        st.plotly_chart(fig, use_container_width=True)
   
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            df = pd.read_csv('data_indicadores.csv')

            # Convertir la columna 'date' a tipo fecha
            df['date'] = pd.to_datetime(df['date'])

            # Ordenar los datos por fecha
            df = df.sort_values('date')

            # Calcular la tasa de satisfacción promedio por mes y asignarla a la columna "satisfaction_month"
            df['satisfaction_month'] = df.groupby('month')['user satisfaction'].transform('mean')

            # Crear la figura del gráfico de la tasa de satisfacción
            fig = go.Figure()

            fig.add_trace(go.Indicator(
                mode="number+delta",
                value=df['satisfaction_month'].iloc[-1],  # Último valor de la tasa de satisfacción
                delta={'reference': df['satisfaction_month'].iloc[-2], 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
                title={'text': "Tasa de satisfacción"},
                number={"suffix": "%"}
            ))

            # Configurar la actualización de la tasa de satisfacción en función del control deslizante
            steps = []
            for i, row in df.iterrows():
                step = dict(
                    method='restyle',
                    args=['value', [row['satisfaction_month']]],
                    label=f"Month {row['month']}"
                )
                steps.append(step)

            sliders = [dict(
                active=len(df)-1,
                currentvalue={"xanchor": "center"},
                pad={"t": 50},
                steps=steps
            )]

            fig.update_layout(
                sliders=sliders,
                autosize=False,
                width=500,
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Convertir la columna 'date' a tipo fecha
            df['date'] = pd.to_datetime(df['date'])

            # Ordenar los datos por fecha
            df = df.sort_values('date')

            # Calcular la tasa de satisfacción promedio por mes y asignarla a la columna "satisfaction_month"
            df['satisfaction_month'] = df.groupby('month')['user satisfaction'].transform('mean')

            # Crear el gráfico de línea de tiempo
            fig = px.line(df, x='date', y='satisfaction_month', title='Tasa de satisfacción a lo largo del tiempo')

            # Configurar la actualización del gráfico de línea de tiempo en función del control deslizante
            steps = []
            for i, row in df.iterrows():
                step = dict(
                    method='update',
                    args=[{'x': [df['date'].iloc[:i+1]], 'y': [df['satisfaction_month'].iloc[:i+1]]}],
                    label=f"Fecha: {row['date']}"
                )
                steps.append(step)

            sliders = [dict(
                active=len(df)-1,
                currentvalue={"xanchor": "center"},
                pad={"t": 50},
                steps=steps
            )]

            fig.update_layout(
                sliders=sliders
            )

            st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


     





#FOOTER, "Enlaces de interés"
