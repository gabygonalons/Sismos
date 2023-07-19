import streamlit as st
from PIL import Image

imgsbase = Image.open("src/logo analytics world.png")
st.sidebar.image(imgsbase, use_column_width=True)

#Título1
st.markdown("# Sistema de Alertas Sísmicas")
#SubTítulo
st.markdown("### Sobre el Proyecto")
#Párrafo 1
st.markdown("La humanidad ha venido documentando cada uno de los movimientos telúricos con el fin de crear mecanismos aptos para la educación, prevención y predicción de sismos. En la actualidad, **GSN** es una red en tiempo real cuyos datos son generados diariamente por grupos operativos de monitoreo, tanto en los Estados Unidos como a nivel internacional. En los **Estados Unidos**, el *Centro Nacional de Información Sísmica* recibe datos de todas las estaciones de GSN a nivel mundial en tiempo real para ubicar terremotos. Los datos de esta red son una entrada esencial para el sistema de alarma automatizado USGS PAGER (localizador) utilizado para evaluar de manera rápida y exacta la gravedad de los daños causados por un terremoto y para proporcionar información a organizaciones de socorro en emergencias, agencias gubernamentales y los medios de comunicación con una estimación del impacto social de la catástrofe potencial.")
#Título h2
st.markdown("## ¿Por qué ejecutar este Proyecto?")
#Párrafo 2
st.markdown("Los avances tecnológicos han permitido el accceso a los datos prácticamente en tiempo real desde cualquier lugar del planeta, no obstante la captación de datos se realiza desde diversas instituciones en distintos puntos del platena con equipamientos variados. Consecuentemente los datos resultantes de los monitoreos realizados presetan variados formatos y calidades por lo que resulta imperioso el pre-procesamiento de los mismos y su adecuación a los estandares de la Red.")
#Título h2
st.markdown("## Misión")
#Párrafo 3
st.markdown("Proveer a la alianza tri-alianza los datos requeridos en formatos acordes a los estándares de la red en plazos que permitan el cuplimiento cabal de los objetivos.")
#Título h2
st.markdown("## Visión")
#Párrafo 4
st.markdown("Colaborar con la alianza tri-nacional con el máximo nivel de eficacia, eficiencia y profesionalimo.")
#Título h2
st.markdown("## Objetivos")
#Párrafo 5
st.markdown(" - Identificar las zonas de mayor riesgo a través de la individualización de patrones y tendencias dentro de los datos.")
st.markdown(" - Clasificar los eventos sísmicos a partir de sus características.")
st.markdown(" - Informar sobre los posibles efectos secundarios de los eventos sísmicos conforme a su clasificación.")
#Título h2
st.markdown("## Líneas de Acción")
#Párrafo 6
st.markdown(" - Crear una base de datos con información de la actividad sísmica histórica de los países miembros de la alianza para obtención de información relevante para la educación, prevención y predicción.")
st.markdown(" - Crear una base de datos con información de la actividad sísmica en tiempo real de los países miembros de la alianza para la emisión de alertas sísmicas.")
st.markdown(" - Elaborar un sitio web que permita la difusión de la información recopilada y de las actividades realizadas en el marco del presente proyecto.")

##################################KPIs#########################################
#Título h2
st.markdown("## Indices Claves de Rendimiento del Proyecto")
##################Transformaciones Tiempo de ejecución
st.markdown("- Tasa de Click de la notificación a la app.")
st.markdown("- Disminución de tasa de fallos.")
st.markdown("- Tiempo de ejecución de código.")
st.markdown("- Tasa de satisfacción de la app.")
