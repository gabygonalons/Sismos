import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # para interactividad


#Titulo1
st.markdown("# Sobre el Sistemea de de Alertas Sísmicas")
#SupTítulo
st.markdown("### Sobre el proyecto")
#Parrafao
st.markdown("La humanidad ha venido documentando cada uno de estos movimientos telúricos con el fin de crear mecanismos de educación, prevención y predicción. En la actualidad, GSN es una red en tiempo real cuyos datos son generados diariamente por grupos operativos de monitoreo, tanto en los Estados Unidos como a nivel internacional. En los Estados Unidos, el Centro Nacional de Información Sísmica recibe datos de todas las estaciones de GSN a nivel mundial en tiempo real para ubicar terremotos. Los datos de esta red son una entrada esencial para el sistema de alarma automatizado USGS PAGER (localizador) utilizado para evaluar de manera rápida y exacta la gravedad de los daños causados por un terremoto y para proporcionar información a organizaciones de socorro en emergencias, agencias gubernamentales y los medios de comunicación con una estimación del impacto social de la catástrofe potencial.")
#Título 2
st.markdown("## ¿Por qué realizar este sistema de alertas sísmicas?")
#parrafo 2
st.markdown("Los avances tecnológicos han permitido el accceso a los datos prácticamente en tiempo real desde cualquier lugar del planeta, no obstante la captación de datos se realiza desde diversas instituciones en distintos puntos del platena con equipamientos variados. Consecuentemente los datos resultantes de los monitoreos realizados presetan variados formatos y calidades por lo que resulta imperioso el pre-procesamiento de los mismos y su adecuación a los estandares de la Red.")
#Titulo h2
st.markdown("## Misión")
#Parrafo
st.markdown("Proveer a la alianza tri-alianza los datos requeridos en formatos acordes a los estándares de la red en plazos que permitan el cuplimiento cabal de los objetivos.")
#Título h2
st.markdown("## Visión")
#Parrafo
st.markdown("Colaborar con la alianza tri-nacional con el máximo nivel de eficacia, eficiencia y profesionalimo.")
#Título h2
st.markdown("## Objetivos")
#Parrafo 
st.markdown("Crear una base de datos, con la información sobre la actividad sísmica de los países miembros de la alianza: Estados Unidos, Japón y México.")

st.markdown("Identificar las zonas de mayor riesgo a través de la individualización de patrones y tendencias dentro de los datos.")
st.markdown("Clasificar los eventos sísmicos a partir de sus características.")
st.markdown("Informar sobre los posibles efectos secundarios de los eventos sísmicos conforme a su clasificación.")
##################################KPIs#########################################
#Título h2
st.markdown("## Indices Cláves de Rendimiento del Proyecto")
##################Transformaciones Tiempo de ejecución
kpi = pd.read_csv('kpi_data.csv')
# Obtiene los meses únicos en el DataFrame "kpi"
meses_unicos = kpi['month'].unique()

# Diccionario para almacenar los promedios por mes
promedios_por_mes = {}

# Calcula el promedio del tiempo de ejecución para cada mes y guarda los resultados
for mes in meses_unicos:
    promedio_mes = kpi[kpi['month'] == mes]['execution time'].mean()
    promedios_por_mes[mes] = promedio_mes

#############Transformación Tasa de satisfacción
# Definir una función para transformar los valores a porcentajes
def transform_to_percentage(value):
    if value == 1:
        return 0  # Completamente insatisfecho
    elif value == 2:
        return 20  # Insatisfecho
    elif value == 3:
        return 50  # Neutral
    elif value == 4:
        return 80  # Satisfecho
    elif value == 5:
        return 100  # Completamente satisfecho
    else:
        return None

# Aplicar la transformación a la columna "user satisfaction"
kpi['user satisfaction'] = kpi['user satisfaction'].apply(transform_to_percentage)

# Agrupar los datos por mes y calcular la tasa de satisfacción del usuario
satisfaction_by_month = kpi.groupby('month')['user satisfaction'].mean()

st.markdown("### Tasa de Click de la notificación a la app.")
# Convertir la columna 'date' a tipo fecha
kpi['date'] = pd.to_datetime(kpi['date'])

# Ordenar los datos por fecha
kpi = kpi.sort_values('date')

# Calcular la tasa de clic de las páginas con oferta premium
kpi['click_rate_pages'] = (kpi['users on pages with premium offer'] / kpi['total users']) * 100

# Calcular el incremento semanal en la tasa de clic
kpi['weekly_increase'] = kpi['click_rate_pages'].pct_change(periods=7) + 1

# Crear la figura del gráfico de la tasa de clic
fig1 = go.Figure()

fig1.add_trace(go.Indicator(
    mode="number+gauge+delta",
    value=kpi['click_rate_pages'].iloc[-1],  # Último valor de la tasa de clic
    delta={'reference': 1.01, 'increasing': {'color': "green"}},
    domain={'x': [0.1, 0.9], 'y': [0.2, 0.9]},
    title={'text': "Tasa de Click de la notificación a la app"},
    gauge={
        'shape': 'angular',
        'axis': {'range': [0, 10]},
        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 5},
        'bar': {'color': "orange"},
        'steps': [
            {'range': [0, 5], 'color': 'lightgray'},
            {'range': [5, 10], 'color': 'gray'}
        ]
    }
))

fig1.update_layout(
    autosize=False,
    width=500,  # Aumentar el ancho del gráfico
    height=400  # Aumentar la altura del gráfico
)

st.plotly_chart(fig1)


st.markdown("Disminución de tasa de fallos.")
st.markdown("Tiempo de ejecución de código.")
fig = go.Figure(go.Indicator(
    mode="number+gauge+delta",
    gauge={'shape': "bullet"},
    delta={'reference': promedios_por_mes[1], 'increasing': {'color': 'red'}, 'decreasing': {'color': 'green'}},
    value=promedios_por_mes[2],
    domain={'x': [0.1, 1], 'y': [0.2, 0.9]},
    title={'text': "Tiempo<br>Promedio<br>de Ejecución", 'font': {'size': 13}},
))

# Personaliza el diseño del gráfico
fig.update_layout(
    height=250,  # Altura del gráfico
    margin=dict(t=70),  # Espacio superior para el título
)

# Muestra el gráfico
st.plotly_chart(fig, use_container_width=True)
st.markdown("Tasa de satisfacción de la app.")
## Satisfacción del mes 2 en relación al mes 1
fig = go.Figure(go.Indicator(
    mode = "number+delta",
    value = satisfaction_by_month[2],
    number = {'prefix': "%"},
    delta = {'position': "top", 'reference': satisfaction_by_month[1]},
    domain = {'x': [0, 1], 'y': [0, 1]}
))

fig.update_layout(
    paper_bgcolor = "lightgray",
    title = "User Satisfaction"  # Agregar la leyenda al gráfico
)
st.plotly_chart(fig, use_container_width=True)
