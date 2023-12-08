import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go
import pandas as pd
import time
import plotly.express as px
from dash import dash_table
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import statsmodels.api as sm




# Función para obtener los datos del sensor seleccionado
# Función para crear el gráfico comparativo
def escogerSensor(sensor_id):
    sensor = ""
    if sensor_id == "emjeor":
        sensor = "Sensor 1,1"
    elif sensor_id == "emjeos":
        sensor = "Sensor 1,2"
    elif sensor_id == "emjfex":
        sensor = "Sensor 2,4"
    elif sensor_id == "emjfey":
        sensor = "Sensor 2,5"
    elif sensor_id == "emjfez":
        sensor = "Sensor 2,6"
    elif sensor_id == "emjfkn":
        sensor = "Sensor 4,1"
    elif sensor_id == "emjfko":
        sensor = "Sensor 4,2"
    else:
        sensor = ""
    return sensor


def crearLista(json):
    datos=[]
    for i in range(len(json)):
        epoch_time = json[i][0]
        dia = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(epoch_time))
        datos.append([dia, json[i][1]])
    return datos

def obtener_datos(api_url, api_token, sensor_name):
    headers = {
        'Authorization': f'Bearer {api_token}'
        # Otros encabezados si son necesarios
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses

        json = response.json()
        datos = crearLista(json)  # nos creamos una lista [fecha, valor]
        fechas = [datos[i][0] for i in range(len(datos))]
        valores = [datos[i][1] for i in range(len(datos))]
        sensor = [sensor_name for i in range(len(datos))]
        df = pd.DataFrame({'fechas': fechas, 'valores': valores, 'sensores': sensor})
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos desde la API. Error: {e}")
        return None






    return fechas
def crear_graficoAlterna(sensor11, sensor12, sensor24,sensor25,sensor26):
    # Definir las URL de la API para cada sensor
    api_url_sensor1 = "https://api.energomonitor.com/v1/feeds/emjeic/streams/emjeor/data?limit=80000"
    api_url_sensor2 = "https://api.energomonitor.com/v1/feeds/emjeic/streams/emjeos/data?limit=80000"
    api_url_sensor3 = "https://api.energomonitor.com/v1/feeds/emjeic/streams/emjfex/data?limit=80000"
    api_url_sensor4 = "https://api.energomonitor.com/v1/feeds/emjeic/streams/emjfey/data?limit=80000"
    api_url_sensor5 = "https://api.energomonitor.com/v1/feeds/emjeic/streams/emjfez/data?limit=80000"


    # Definir los tokens de API para cada sensor
    token = "3QUluAp7EODWp4xFaMBAeb2ZkEOnhm"

    # Obtener datos para cada sensor
    df1 = obtener_datos(api_url_sensor1, token, 'Sensor 1,1')
    df2 = obtener_datos(api_url_sensor2, token, 'Sensor 1,2')
    df3 = obtener_datos(api_url_sensor3, token, 'Sensor 2,4')
    df4 = obtener_datos(api_url_sensor4, token, 'Sensor 2,5')
    df5 = obtener_datos(api_url_sensor5, token, 'Sensor 2,6')


    
    
    
    fig = go.Figure()
    if sensor11:
        fig.add_trace(go.Scatter(x=df1["fechas"], y=df1["valores"], mode='lines', name="sensor1,1"))
    if sensor12:
        fig.add_trace(go.Scatter(x=df2["fechas"], y=df2["valores"], mode='lines', name="sensor1,2"))
    if sensor24:
        fig.add_trace(go.Scatter(x=df3["fechas"], y=df3["valores"], mode='lines', name="sensor2,4"))
    if sensor25:
        fig.add_trace(go.Scatter(x=df4["fechas"], y=df4["valores"], mode='lines', name="sensor2,5"))
    if sensor26:
        fig.add_trace(go.Scatter(x=df5["fechas"], y=df5["valores"], mode='lines', name="sensor2,6"))
    
    
    
    
    return fig
def crear_graficoContinua(sensor41, sensor42):
    # Definir las URL de la API para cada sensor
    api_url_sensor1 = "https://api.energomonitor.com/v1/feeds/emjeic/streams/emjfkn/data?limit=80000"
    api_url_sensor2 = "https://api.energomonitor.com/v1/feeds/emjeic/streams/emjfko/data?limit=80000"


    # Definir los tokens de API para cada sensor
    token = "3QUluAp7EODWp4xFaMBAeb2ZkEOnhm"

    # Obtener datos para cada sensor
    df1 = obtener_datos(api_url_sensor1, token, "Sensor 4,1")
    df2 = obtener_datos(api_url_sensor2, token, "Sensor 4,2")


    
    fig = go.Figure()
    if sensor41:
        fig.add_trace(go.Scatter(x=df1["fechas"], y=df1["valores"], mode='lines', name="sensor4,1"))
    if sensor42:
        fig.add_trace(go.Scatter(x=df2["fechas"], y=df2["valores"], mode='lines', name="sensor4,2"))
    
    return fig

def crearMapa():
    # Coordenadas de Kitui, Kenia
    latitud_kitui = 1.3833
    longitud_kitui = 38.0136

    # Crear figura con Plotly Graph Objects
    fig = go.Figure(go.Scattermapbox(
        fill="toself",
        lon=[longitud_kitui - 0.05, longitud_kitui + 0.05, longitud_kitui + 0.05, longitud_kitui - 0.05],
        lat=[latitud_kitui - 0.05, latitud_kitui - 0.05, latitud_kitui + 0.05, latitud_kitui + 0.05],
        marker={'size': 10, 'color': "orange"}
    ))

    # Configurar diseño del mapa
    fig.update_layout(
        mapbox={
            'style': "carto-positron",  # Cambiado a un estilo con fondo claro
            'center': {'lon': longitud_kitui, 'lat': latitud_kitui},
            'zoom': 10
        },
        showlegend=False
    )

    return fig


def calcular_estadisticas_sensor(df):
    max_valor = df['valores'].max()
    min_valor = df['valores'].min()
    dia_max = df.loc[df['valores'].idxmax()]['fechas']
    dia_min = df.loc[df['valores'].idxmin()]['fechas']
    media = df['valores'].mean()
        
    return max_valor, dia_max, min_valor, dia_min, media



def calcular_estadisticas_globales(datos_sensores):
    estadisticas_globales = []

    for sensor_id, df_sensor in datos_sensores.items():
        max_valor, dia_max, min_valor, dia_min, media = calcular_estadisticas_sensor(df_sensor)
        sensor = escogerSensor(sensor_id)
        estadisticas_globales.append({
            'Sensor': sensor,
            'Máximo': max_valor,
            'Día Máximo': dia_max,
            'Mínimo': min_valor,
            'Día Mínimo': dia_min,
            'Media': media
        })

    estadisticas_df = pd.DataFrame(estadisticas_globales)
    return estadisticas_df

def actualizar_tabla_estadisticas(sensores_seleccionados):
    datos_sensores = {}

    for sensor_id in sensores_seleccionados:
        api_url_sensor = f"https://api.energomonitor.com/v1/feeds/emjeic/streams/{sensor_id}/data?limit=80000"
        token = "3QUluAp7EODWp4xFaMBAeb2ZkEOnhm"
        sensor=escogerSensor(sensor_id)
        df_sensor = obtener_datos(api_url_sensor, token, sensor) #lista con fechas, valor, sensor
        if df_sensor is not None:
            datos_sensores[sensor_id] = df_sensor

    estadisticas_globales = calcular_estadisticas_globales(datos_sensores)
    estadisticas_data = estadisticas_globales.to_dict('records')
    return estadisticas_data

    
def predecir_arima(datos, sensor_id):
    # Ajustar el modelo ARIMA
    modelo = sm.tsa.ARIMA(datos['valores'], order=(1, 1, 1))
    resultados = modelo.fit()

    # Hacer predicciones para el próximo día
    predicciones = resultados.get_forecast(steps=1)

    # Crear un DataFrame con la fecha y la predicción
    fecha_prediccion = pd.date_range(start=datos['fechas'].max(), periods=2, freq='D')[1:]
    df_predicciones = pd.DataFrame({'fechas': fecha_prediccion, f'predicciones_{sensor_id}': predicciones.predicted_mean})

    return df_predicciones






# Crear la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': 'white'},
    children=[
        html.H1("ANÁLISIS ENERGÍA EN NYUMBANI, KENIA", style={
            'textAlign': 'center', 
            'color': 'white',
            'background-color': 'black',
            'font-family': 'Times New Roman',
            'border-radius': '10px',  # Puntas acirculadas
            'padding': '10px',
            'box-shadow': '5px 5px 15px grey',
            }),

      html.Div([ #Primera fila
        # Primera Columna (Caja de texto)
        html.Div([
            html.H3("Información esencial sobre Nyumbani", style={'textAlign': 'center', 'font-family': 'Times New Roman'}),
            html.P("Nyumbani es una organización internacional no lucrativa que tiene sus orígenes en 1992 ya que no paraba de crecer el número de niños que se veían afectados por la pandemia del SIDA.", style={'textAlign': 'justify', 'font-family': 'Times New Roman'}),
            html.P("La vocación de este poblado es la lucha contra esta enfermedad, el hambre, el abandono y el sufrimiento físico al que se enfrentan los hombres, mujeres y niños indefensos.", style={'textAlign': 'justify', 'font-family': 'Times New Roman'}),
            html.P("Energía Sin Fronteras inauguró en 2014 un huerto solar de 44.280 vatios. Este huerto lo formaban 216 paneles solares de 205 vatios cada uno. Gracias a esta instalación se abastece con energía a la aldea, beneficiando a 1000 personas. El huerto entró en funcionamiento desde marzo de 2014 y provee unos 45 kilovatios-hora de energía eléctrica", style={'textAlign': 'justify', 'font-family': 'Times New Roman'}),
        ], style={'display': 'inline-block', 'width': '28%', 'background-color': '#f2f2f2', 'padding': '30px', 'box-shadow': '5px 5px 15px grey'}),

        # Segunda Columna (Imagen)
        html.Div([
            html.Img(src='assets/Foto.jpg', style={'width': '100%', 'height': 'auto', 'display': 'block'}),
        ], style={'display': 'inline-block', 'width': '57%', 'padding': '30px', 'height': '60%', 'vertical-align': 'top'}),
            
    ]),
     html.Div([
            html.H2("¿Dónde esta Nyumbani?", style={'textAlign': 'left', 'font-family': 'Times New Roman', 'color': 'black'}),
        ], style={ 'padding': '10px', 'border-radius': '10px'}),
    

    html.Div([#SEGUNDA FILA
        html.Div([ #Primera columna (Mapa)
                    dcc.Graph(id='mapa', figure=crearMapa(), style={'width': '100%', 'height': '450px'})
                ], style={'width': '50%', 'display': 'inline-block', 'padding': '20px', 'vertical-align': 'top'}),

        html.Div([
            html.H3("Información sobre los sensores", style={'textAlign': 'center', 'font-family': 'Times New Roman'}),
            html.P(" Sensor 1 → ALTERNA con conexiones 1 y 2", style={'textAlign': 'justify', 'font-family': 'Times New Roman', 'font-weight': 'bold'}),
            html.P(" Sensor 2 → ALTERNA con conexiones 4, 5 y 6", style={'textAlign': 'justify', 'font-family': 'Times New Roman', 'font-weight': 'bold'}),
            html.P(" Sensor 4 → CONTINUA con conexiones 1 y 2", style={'textAlign': 'justify', 'font-family': 'Times New Roman', 'font-weight': 'bold'}),
            html.P("El sensor 1,1 está conectado a administración, por lo tanto, mide la energía que generan las placas solares destinadas a esta parte del High School. El sensor 1, 2 mide la energía de las cocinas. El sensor 2,4 mide la energía de la sala de ordenadores. El sensor 2,5 mide la energía de la sala de reuniones y por último el sensor 2,6 mide la energía de la zona de profesores. ", style={'textAlign': 'justify', 'font-family': 'Times New Roman'}),
            html.P("Lo sensores de alterna miden la energía generada por las baterías para 	que funcionen las placas solares ", style={'textAlign': 'justify', 'font-family': 'Times New Roman'}),
        ], style={'display': 'inline-block', 'width': '28%', 'background-color': '#F9C5B1', 'padding': '30px', 'box-shadow': '5px 5px 15px grey'}),


    ]),
    html.Div([
            html.H2("Sensores de alterna", style={'textAlign': 'center', 'font-family': 'Times New Roman', 'color': 'white'}),
        ], style={'background-color': '#804000', 'padding': '10px', 'border-radius': '10px'}),

    html.Div([ #TERCERA FILA 
                # Primera Columna (Gráfico 1)
                html.Div([
                    html.Label("Comparemos los sensores de energía:"),
                    dcc.Dropdown(
                        id='sensores-checkboxes1',
                        options=[
                            {'label': 'Sensor 1,1', 'value': 'emjeor'},
                            {'label': 'Sensor 1,2', 'value': 'emjeos'},
                            {'label': 'Sensor 2,4', 'value': 'emjfex'},
                            {'label': 'Sensor 2,5', 'value': 'emjfey'},
                            {'label': 'Sensor 2,6', 'value': 'emjfez'},
                        ],
                        multi=True,
                        value=[]
                    ),
                    dcc.Graph(id='comparacion-grafico-1', style={'width': '100%', 'height': '400px'}),
                ], style={'width': '50%', 'display': 'inline-block', 'background-color': 'white', 'padding': '10px'}),

                # Segunda Columna (Tabla)
                html.Div([
                    dash_table.DataTable(
                        id='tabla-estadisticas',
                        columns=[
                             {"name": "Sensor","id" : "Sensor" },
                            {'name': 'Máximo', 'id': 'Máximo'},
                            {'name': 'Día Máximo', 'id': 'Día Máximo'},
                            {'name': 'Mínimo', 'id': 'Mínimo'},
                            {'name': 'Día Mínimo', 'id': 'Día Mínimo'},
                            {'name': 'Media', 'id': 'Media'}
                        ],
                        style_table={'height': '400px', 'overflowY': 'auto'},
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'background-color': 'white', 'padding': '20px'}),
            ], style={'width': '100%', 'display': 'flex'}),
        
        
        html.Div([
            html.H2("Sensores de Continua", style={'textAlign': 'center', 'font-family': 'Times New Roman', 'color': 'white'}),
        ], style={'background-color': '#804000', 'padding': '10px', 'border-radius': '10px'}),

        # Segunda Fila
        html.Div([
            # Tercera Columna (Gráfico 3)
            html.Div([
                html.Label("Comparemos los sensores de energía continua:"),
                 dcc.Dropdown(
                    id='sensores-checkboxes3',
                    options=[
                        {'label': 'Sensor 4,1', 'value': 'emjfkn'},
                        {'label': 'Sensor 4,2', 'value': 'emjfko'},
                    ],
                    multi=True,
                    value=[]
                ),
                dcc.Graph(id='comparacion-grafico-3', style={'width': '100%', 'height': '400px'}),
            ], style={'width': '45%', 'display': 'inline-block'}),

            # Cuarta Columna (Gráfico 4)
            
            # Segunda Columna (Tabla)
                html.Div([
                    dash_table.DataTable(
                        id='tabla-estadisticas2',
                        columns=[
                            {"name": "Sensor","id" : "Sensor" },
                            {'name': 'Máximo', 'id': 'Máximo'},
                            {'name': 'Día Máximo', 'id': 'Día Máximo'},
                            {'name': 'Mínimo', 'id': 'Mínimo'},
                            {'name': 'Día Mínimo', 'id': 'Día Mínimo'},
                            {'name': 'Media', 'id': 'Media'}
                        ],
                        style_table={'height': '400px', 'overflowY': 'auto'},
                    )
                ], style={'width': '50%', 'display': 'inline-block', 'background-color': 'white', 'padding': '20px'}),

        ]),
        html.Div([
            html.H2("Predicciones a esta hora de cada sensor mañana", style={'textAlign': 'center', 'font-family': 'Times New Roman', 'color': 'white'}),
        ], style={'background-color': '#804000', 'padding': '10px', 'border-radius': '10px'}),

        #PREDICCIONES
       html.Div([
        html.H2("Predicciones ARIMA", style={'textAlign': 'center', 'font-family': 'Times New Roman', 'color': 'white'}),
        html.Div(id='prediccion-arima-texto-container', style={'display': 'flex', 'flexWrap': 'wrap'}),]),




    ]
)

# Callback para actualizar el gráfico cuando cambian las selecciones de los desplegables
# Callback para actualizar el gráfico cuando cambian las selecciones de los desplegables
@app.callback(
    Output('comparacion-grafico-1', 'figure'),
    [Input('sensores-checkboxes1', 'value')],
    
    
    
)
def actualizar_grafico(sensores_seleccionados):
    sensor11 = 'emjeor' if 'emjeor' in sensores_seleccionados else None
    sensor12 = 'emjeos' if 'emjeos' in sensores_seleccionados else None
    sensor24 = 'emjfex' if 'emjfex' in sensores_seleccionados else None
    sensor25 = 'emjfey' if 'emjfey' in sensores_seleccionados else None
    sensor26 = 'emjfez' if 'emjfez' in sensores_seleccionados else None
    # Predicciones de las horas del día en las que más se genera energía
   

    fig = crear_graficoAlterna(sensor11, sensor12, sensor24, sensor25, sensor26)
    
    return fig


@app.callback(
    Output('tabla-estadisticas', 'data'),
    [Input('sensores-checkboxes1', 'value')],
)

def actualizar_tabla(sensores_seleccionados):
    sensor11 = 'emjeor' if 'emjeor' in sensores_seleccionados else None
    sensor12 = 'emjeos' if 'emjeos' in sensores_seleccionados else None
    sensor24 = 'emjfex' if 'emjfex' in sensores_seleccionados else None
    sensor25 = 'emjfey' if 'emjfey' in sensores_seleccionados else None
    sensor26 = 'emjfez' if 'emjfez' in sensores_seleccionados else None

    id_sensores = [sensor for sensor in [sensor11, sensor12, sensor24, sensor25, sensor26] if sensor is not None]


    return actualizar_tabla_estadisticas(id_sensores)




@app.callback(
    Output('comparacion-grafico-3', 'figure'),
    [Input('sensores-checkboxes3', 'value')],
)

def actualizar_grafico(sensores_seleccionados):
    sensor41 = 'emjfkn' if 'emjfkn' in sensores_seleccionados else None
    sensor42 = 'emjfko' if 'emjfko' in sensores_seleccionados else None
    return crear_graficoContinua(sensor41, sensor42)

@app.callback(
    Output('tabla-estadisticas2', 'data'),
    [Input('sensores-checkboxes3', 'value')],
)

def actualizar_tabla(sensores_seleccionados):
    sensor41 = 'emjfkn' if 'emjfkn' in sensores_seleccionados else None
    sensor42 = 'emjfko' if 'emjfko' in sensores_seleccionados else None

    id_sensores = [sensor for sensor in [sensor41, sensor42] if sensor is not None]


    return actualizar_tabla_estadisticas(id_sensores)
# Después de las funciones actuales, añade dos nuevas funciones para actualizar los gráficos ARIMA
@app.callback(
    [Output('prediccion-arima-texto-container', 'children')],
    [Input('sensores-checkboxes1', 'value'),
     Input('sensores-checkboxes3', 'value')],
)
def actualizar_prediccion_texto(sensores_alterna, sensores_continua):
    texto_predicciones = []

    if sensores_alterna:
        for sensor_id in sensores_alterna:
            sensor=escogerSensor(sensor_id)
            api_url_sensor = f"https://api.energomonitor.com/v1/feeds/emjeic/streams/{sensor_id}/data?limit=80000"
            df_sensor = obtener_datos(api_url_sensor, "p9pbDtQLtXui9OVz8KBoXIdp0916qE", sensor)
            
            if df_sensor is not None:
                df_predicciones = predecir_arima(df_sensor, sensor_id)
                max_prediccion = df_predicciones[f'predicciones_{sensor_id}'].max()
                fecha_max_prediccion = df_predicciones.loc[df_predicciones[f'predicciones_{sensor_id}'].idxmax()]['fechas']

                # Formatear el texto para mostrar la predicción
                texto_sensor = html.Div([
                    html.H4(f"{sensor}", style={'textAlign': 'center'}),
                    html.P(fecha_max_prediccion.strftime("%H:%M:%S"), style={'textAlign': 'center'}),
                    html.P(f"{max_prediccion:.2f} kWh", style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'}),
                ], style={'backgroundColor': '#f2f2f2', 'borderRadius': '10px', 'margin': '10px', 'padding': '10px'})

                texto_predicciones.append(texto_sensor)

    if sensores_continua:
        for sensor_id in sensores_continua:
            sensor=escogerSensor(sensor_id)
            api_url_sensor = f"https://api.energomonitor.com/v1/feeds/emjeic/streams/{sensor_id}/data?limit=80000"
            df_sensor = obtener_datos(api_url_sensor, "p9pbDtQLtXui9OVz8KBoXIdp0916qE", sensor)
            
            if df_sensor is not None:
                df_predicciones = predecir_arima(df_sensor, sensor_id)
                max_prediccion = df_predicciones[f'predicciones_{sensor_id}'].max()
                fecha_max_prediccion = df_predicciones.loc[df_predicciones[f'predicciones_{sensor_id}'].idxmax()]['fechas']

                # Formatear el texto para mostrar la predicción
                texto_sensor = html.Div([
                    html.H4(f"{sensor}", style={'textAlign': 'center'}),
                    html.P(fecha_max_prediccion.strftime("%H:%M:%S"), style={'textAlign': 'center'}),
                    html.P(f"{max_prediccion:.2f} kWh", style={'fontSize': 20, 'fontWeight': 'bold', 'textAlign': 'center'}),
                ], style={'backgroundColor': '#f2f2f2', 'borderRadius': '10px', 'margin': '10px', 'padding': '10px'})

                texto_predicciones.append(texto_sensor)

    return [texto_predicciones]




# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

