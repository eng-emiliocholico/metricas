import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import webbrowser
import threading
from dash import Dash

# ====================================================================
# 1. SETUP DE DATOS INICIALES Y LÓGICA
# ====================================================================

# -----------------
# 1.1: Data Inicial (COMPLETA)
# -----------------
data = [
    # Comercial
    {'Área': 'Comercial', 'Indicador': 'Cumplimiento de meta de ventas (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.04, 'Meta': 100, 'Actual': 0, 'Responsable': 'Gerente Sucursal', 'Fuente de Datos': 'Alpha ERP / Reporte ventas', 'Comentarios': '', 'Definicion': '(Venta real ÷ Meta) x 100'},
    {'Área': 'Comercial', 'Indicador': 'Nuevos clientes registrados', 'Frecuencia': 'Mensual', 'Ponderacion': 0.04, 'Meta': 10, 'Actual': 0, 'Responsable': 'Gerente Sucursal', 'Fuente de Datos': 'CRM / Alpha ERP', 'Comentarios': '', 'Definicion': 'Total clientes nuevos en el periodo'},
    {'Área': 'Comercial', 'Indicador': 'Tasa de conversión de cotizaciones (%)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.04, 'Meta': 40, 'Actual': 0, 'Responsable': 'Líder Comercial', 'Fuente de Datos': 'CRM / Alpha ERP', 'Comentarios': '', 'Definicion': '(Cerradas ÷ Emitidas) x 100'},
    {'Área': 'Comercial', 'Indicador': 'Tiempo promedio de atención de cotizaciones (horas)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.04, 'Meta': 24, 'Actual': 0, 'Responsable': 'Ventas Internas', 'Fuente de Datos': 'CRM / Alpha ERP', 'Comentarios': '', 'Definicion': 'Horas promedio desde solicitud a envío'},
    {'Área': 'Comercial', 'Indicador': 'Seguimiento postventa (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.04, 'Meta': 80, 'Actual': 0, 'Responsable': 'Gerente Sucursal', 'Fuente de Datos': 'CRM / Alpha ERP', 'Comentarios': '', 'Definicion': '% clientes contactados después de venta'},
    
    # ADMINISTRACIÓN
    {'Área': 'Administración', 'Indicador': 'Reportes administrativos a tiempo (%)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.066, 'Meta': 100, 'Actual': 0, 'Responsable': 'Admin Sucursal', 'Fuente de Datos': 'Checklists / Drive', 'Comentarios': '', 'Definicion': '% cierres, inventarios, compras entregados en fecha'},
    {'Área': 'Administración', 'Indicador': 'Cumplimiento de políticas internas (%)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.066, 'Meta': 90, 'Actual': 0, 'Responsable': 'Gerente Sucursal', 'Fuente de Datos': 'Checklist físico/digital', 'Comentarios': '', 'Definicion': 'Checklist semanal (uniforme, orden, limpieza, horarios)'},
    {'Área': 'Administración', 'Indicador': 'Control documental correcto (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.066, 'Meta': 100, 'Actual': 0, 'Responsable': 'Admin Sucursal', 'Fuente de Datos': 'Carpeta fiscal / ERP', 'Comentarios': '', 'Definicion': '% documentos correctos (facturas, CFDI, bitácoras)'},

    # Finanzas
    {'Área': 'Finanzas', 'Indicador': 'Margen bruto promedio (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.05, 'Meta': 20, 'Actual': 0, 'Responsable': 'Finanzas Sucursal', 'Fuente de Datos': 'Alpha ERP', 'Comentarios': '', 'Definicion': '(Utilidad bruta ÷ Ventas netas) x 100'},
    {'Área': 'Finanzas', 'Indicador': 'Cuentas por cobrar vencidas (%)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.05, 'Meta': 10, 'Actual': 0, 'Responsable': 'Finanzas Sucursal', 'Fuente de Datos': 'Alpha ERP', 'Comentarios': '', 'Definicion': '% cartera vencida sobre total'},
    {'Área': 'Finanzas', 'Indicador': 'Gasto vs presupuesto (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.05, 'Meta': 100, 'Actual': 0, 'Responsable': 'Gerente + Finanzas', 'Fuente de Datos': 'Alpha ERP', 'Comentarios': '', 'Definicion': '(Gasto real ÷ Presupuesto) x 100'},
    {'Área': 'Finanzas', 'Indicador': 'Depósitos diarios en tiempo (%)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.05, 'Meta': 100, 'Actual': 0, 'Responsable': 'Admin Sucursal', 'Fuente de Datos': 'Bancario / ERP', 'Comentarios': '', 'Definicion': '% días con depósito correcto/mismo día'},

    # Operaciones
    {'Área': 'Operaciones', 'Indicador': 'Exactitud de inventario (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.05, 'Meta': 98, 'Actual': 0, 'Responsable': 'Almacén', 'Fuente de Datos': 'Alpha ERP / Conteo cíclico', 'Comentarios': '', 'Definicion': 'Precisión en conteos de inventario'},
    {'Área': 'Operaciones', 'Indicador': 'Órdenes entregadas a tiempo (%)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.05, 'Meta': 95, 'Actual': 0, 'Responsable': 'Operaciones', 'Fuente de Datos': 'Alpha ERP / Despacho', 'Comentarios': '', 'Definicion': 'Órdenes entregadas según plazo establecido'},
    {'Área': 'Operaciones', 'Indicador': 'Mermas (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.05, 'Meta': 2, 'Actual': 0, 'Responsable': 'Operaciones', 'Fuente de Datos': 'Alpha ERP', 'Comentarios': '', 'Definicion': 'Pérdidas de inventario sobre ventas totales'},
    {'Área': 'Operaciones', 'Indicador': 'Disponibilidad de stock A', 'Frecuencia': 'Semanal', 'Ponderacion': 0.05, 'Meta': 2, 'Actual': 0, 'Responsable': 'Almacén', 'Fuente de Datos': 'Alpha ERP', 'Comentarios': '', 'Definicion': '% SKUs A con stock disponible'},
    
    # CAPITAL HUMANO
    {'Área': 'Capital Humano', 'Indicador': 'Asistencia y puntualidad (%)', 'Frecuencia': 'Semanal', 'Ponderacion': 0.05, 'Meta': 95, 'Actual': 0, 'Responsable': 'Gerente Sucursal', 'Fuente de Datos': 'Nómina', 'Comentarios': '', 'Definicion': '% cumplimiento asistencia y puntualidad'},
    {'Área': 'Capital Humano', 'Indicador': 'Rotación de personal (%)', 'Frecuencia': 'Trimestral', 'Ponderacion': 0.05, 'Meta': 5, 'Actual': 0, 'Responsable': 'Capital Humano', 'Fuente de Datos': 'Nómina', 'Comentarios': '', 'Definicion': 'Salidas ÷ Promedio personal'},
    {'Área': 'Capital Humano', 'Indicador': 'Cumplimiento de capacitaciones (%)', 'Frecuencia': 'Mensual', 'Ponderacion': 0.05, 'Meta': 80, 'Actual': 0, 'Responsable': 'Capital Humano', 'Fuente de Datos': 'Bitácoras', 'Comentarios': '', 'Definicion': '% colaboradores capacitados'},
    {'Área': 'Capital Humano', 'Indicador': 'Clima laboral / satisfacción (%)', 'Frecuencia': 'Trimestral', 'Ponderacion': 0.05, 'Meta': 80, 'Actual': 0, 'Responsable': 'Capital Humano', 'Fuente de Datos': 'Encuesta', 'Comentarios': '', 'Definicion': 'Encuesta de 1-10 convertido a %'},
]

df_initial = pd.DataFrame(data)

AREAS = df_initial['Área'].unique()
KPI_MENOR_MEJOR = [
    'Cuentas por cobrar vencidas (%)', 
    'Mermas (%)', 
    'Rotación de personal (%)',
    'Tiempo promedio de atención de cotizaciones (horas)'
] 

# Crear lista de responsables únicos
RESPONSABLES = sorted(df_initial['Responsable'].unique())

def calcular_kpis(df):
    def calcular_resultado(row):
        meta = row['Meta']
        actual = row['Actual']
        if meta == 0 or actual == 0: 
            return 0.0
            
        if row['Indicador'] in KPI_MENOR_MEJOR or row['Comentarios'] == 'Menor es Mejor':
            # Para KPIs "Menor es Mejor", invertimos la lógica
            if actual == 0:
                return 0.0
            return (meta / actual) * 100
        else:
            # Para KPIs "Mayor es Mejor", cálculo normal
            return (actual / meta) * 100

    df['Resultado %'] = df.apply(calcular_resultado, axis=1)
    df['Semáforo Color'] = df['Resultado %'].apply(lambda r: '#28a745' if r >= 100 else '#ffc107' if r >= 80 else '#dc3545')
    df['Contribucion'] = (df['Ponderacion'] * df['Resultado %']) / 100
    puntaje_general = df['Contribucion'].sum()

    return df, puntaje_general

df_kpis, puntaje_inicial = calcular_kpis(df_initial.copy())


# ====================================================================
# 2. DEFINICIÓN DE COMPONENTES VISUALES Y LAYOUT
# ====================================================================

app = dash.Dash(__name__, external_stylesheets=['https://bootswatch.com/4/slate/bootstrap.min.css'])
app.title = "Tablero Ejecutivo KPI Ponderado"


def crear_gauge_general(puntaje):
    puntaje_porcentaje = puntaje * 100
    
    # Definir zonas de color
    if puntaje_porcentaje >= 100:
        color_gauge = '#28a745'  # Verde
        nivel_texto = 'EXCELENTE'
    elif puntaje_porcentaje >= 80:
        color_gauge = '#ffc107'  # Amarillo
        nivel_texto = 'BUENO'
    else:
        color_gauge = '#dc3545'  # Rojo
        nivel_texto = 'REQUIERE ATENCIÓN'

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=puntaje_porcentaje,
        domain={'x': [0, 1], 'y': [0, 1]},  # Dominio completo
        title={
            'text': f"<b>PUNTUACIÓN GENERAL</b><br><span style='font-size:16px;color:{color_gauge};font-weight:bold'>{nivel_texto}</span>", 
            'font': {'size': 20, 'color': 'white', 'family': 'Arial'}
        },
        number={
            'suffix': "%", 
            'valueformat': ".1f", 
            'font': {'size': 40, 'color': 'white', 'family': 'Arial Black'},
        },
        gauge={
            'axis': {
                'range': [0, 120], 
                'tickwidth': 1, 
                'tickcolor': "white",
                'tickfont': {'color': 'white', 'size': 10},
                'tickformat': '.0f',
                'ticks': 'outside',
                'ticklen': 8,
                'dtick': 20
            },
            'bar': {'color': 'white', 'thickness': 0.02},
            'bgcolor': "rgba(0,0,0,0)",  # Fondo transparente
            'borderwidth': 0,  # Sin borde
            'bordercolor': "rgba(0,0,0,0)",  # Borde transparente
            'steps': [
                {'range': [0, 79], 'color': '#dc3545'},
                {'range': [80, 99], 'color': '#ffc107'}, 
                {'range': [100, 120], 'color': '#28a745'}
            ],
            'threshold': {
                'line': {'color': "rgba(0,0,0,0)", 'width': 0},  # Línea transparente
                'thickness': 0.8, 
                'value': puntaje_porcentaje
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",  # Fondo completamente transparente
        plot_bgcolor="rgba(0,0,0,0)",   # Fondo del plot transparente
        font={'color': "white", 'family': "Arial"},
        height=300,
        margin=dict(l=40, r=40, t=80, b=40),
        # Eliminar cualquier línea o borde adicional
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

def crear_grafico_area(df_area):
    if df_area.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Sin datos para el filtro seleccionado", 
            plot_bgcolor="white",
            paper_bgcolor="white",  
            font_color="black",
            height=300
        )
        return fig
    
    df_area_calculado, _ = calcular_kpis(df_area.copy())
    df_plot = df_area_calculado[['Indicador', 'Meta', 'Actual', 'Resultado %', 'Semáforo Color']].copy()

    fig = go.Figure()
    
    # BARRA DE RESULTADO ACTUAL
    fig.add_trace(go.Bar(
        name='Resultado Actual',
        x=df_plot['Indicador'],
        y=df_plot['Resultado %'],
        marker_color=df_plot['Semáforo Color'],
        marker_line=dict(width=2, color='white'),
        opacity=0.9,
        text=df_plot['Resultado %'].round(1).astype(str) + '%',
        textposition='auto',
        textfont=dict(color='white', size=11, weight='bold'),
        width=0.4,
        offset=-0.2,
        hovertemplate='<b>%{x}</b><br>Resultado: %{y:.1f}%<extra></extra>'
    ))
    
    # BARRA DE META
    fig.add_trace(go.Bar(
        name='Meta (100%)',
        x=df_plot['Indicador'],
        y=[100] * len(df_plot),
        marker_color='#2d3748',
        marker_line=dict(width=2, color='white'),
        opacity=0.7,
        text=['100%'] * len(df_plot),
        textposition='auto',
        textfont=dict(color='white', size=11, weight='bold'),
        width=0.4,
        offset=0.2,
        hovertemplate='<b>%{x}</b><br>Meta: 100%<extra></extra>'
    ))

    # Función para hacer wrap por palabras completas
    def wrap_text_by_words(text, max_chars_per_line=25):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Si agregar la palabra excede el límite, empezar nueva línea
            if len(current_line) + len(word) + 1 > max_chars_per_line and current_line:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return '<br>'.join(lines)

    # Aplicar wrap por palabras completas a los indicadores
    ticktext_wrapped = df_plot['Indicador'].apply(wrap_text_by_words)

    fig.update_layout(
        title=dict(
            text=f"Cumplimiento por Indicador ({df_area['Área'].iloc[0]})",
            x=0.5,
            font=dict(size=16, color='black')
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="black",
        barmode='group',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='rgba(0,0,0,0.2)',
            font=dict(color='black', size=12)
        ),
        height=500,
        margin=dict(t=80, b=150, l=80, r=80),  # Margen inferior aumentado para los textos
        xaxis=dict(
            tickangle=0,
            tickmode='array',
            tickvals=df_plot['Indicador'],
            ticktext=ticktext_wrapped,
            tickfont=dict(size=10),
            # Centrar el texto sobre las dos columnas
            tickson="boundaries",
            # Asegurar que el texto se centre correctamente
            automargin=True,
            showgrid=False
        )
    )
    
    fig.update_yaxes(
        gridcolor='#e1e5e9',
        range=[0, 120],
        color='black',
        title_text='Porcentaje (%)',
        title_font=dict(color='black')
    )
    
    return fig

def crear_tabla_area(df_area, area_name):
    columnas_tabla = ['Indicador', 'Frecuencia', 'Ponderacion', 'Meta', 'Actual', 'Responsable', 'Fuente de Datos', 'Comentarios']
    
    columns = []
    for i in columnas_tabla:
        col_config = {"name": i, "id": i, "editable": False}
        if i in ['Actual']: 
            col_config.update({"editable": True, "type": 'numeric'})
        elif i in ['Comentarios']: 
            col_config.update({"editable": True, "type": 'text'})
        columns.append(col_config)

    tooltip_data = [{'Indicador': {'value': row['Definicion'], 'type': 'text'}} for row in df_area.to_dict('records')]
    
    return html.Div([
        dash_table.DataTable(
            id={'type': 'tabla-editable', 'index': area_name}, 
            columns=columns, 
            data=df_area.to_dict('records'),
            tooltip_data=tooltip_data, 
            tooltip_header={i: i for i in columnas_tabla},
            style_table={'overflowX': 'auto', 'border': '1px solid #343a40'},
            style_header={
                'backgroundColor': '#DDDAD9', 
                'color': 'black', 
                'fontWeight': 'bold', 
                'textAlign': 'center',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_data={
                'backgroundColor': '#ffffff', 
                'color': 'black', 
                'borderBottom': '1px solid #343a40',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_data_conditional=[
                {'if': {'column_id': 'Actual'}, 'backgroundColor': '#fff', 'color': '#000', 'fontWeight': 'bold'},
                {'if': {'column_id': 'Comentarios'}, 'backgroundColor': '#fff', 'color': '#000', 'minWidth': '150px', 'fontWeight': 'light'},
                {'if': {'state': 'active'}, 'backgroundColor': '#fff', 'border': '3px solid #007bff'},
                {'if': {'state': 'selected'}, 'backgroundColor': '#fff', 'border': '3px solid #007bff'},
            ],
            export_format='none',
            css=[{
                'selector': '.dash-table-tooltip',
                'rule': 'background-color: #2a2d33; color: white; border: 1px solid #495057;'
            }]
        )
    ], className="mb-4")


# -----------------
# 2.4: Layout Principal
# -----------------

app.layout = html.Div(style={'background': 'linear-gradient(to bottom, #1D187A 45%, #DBDBDB 45%)',
    'minHeight': '100vh', 
    'padding': '20px'
    }, children=[
    
    html.Div(className="container", children=[
        
        dcc.Store(id='store-inicial', data=df_kpis.to_dict('records')),
        
        html.H1("Tablero de Desempeño Gerencial Ponderado", className="text-center mb-4 text-white"),
        
        # --- FILTRO DE RESPONSABLE ---
        html.Div(className="card p-3 mb-4",
        
    style={"backgroundColor": "#130F4A","border":"1px solid #130F4A"},  children=[
            html.H5("Filtro por Responsable", className="text-white"),
            html.Div(className="row", children=[
                html.Div(className="col-md-8", children=[
                    dcc.Dropdown(
                        id='responsable-filter', 
                        options=[{'label': 'Todos los responsables', 'value': 'ALL'}] + 
                               [{'label': i, 'value': i} for i in RESPONSABLES],
                        placeholder="Selecciona un responsable para filtrar la vista", 
                        multi=False,
                        value='ALL',  # Por defecto muestra todos
                        style={'backgroundColor': '#212529', 'color': '#000'}
                    )
                ]),
                html.Div(className="col-md-4", children=[
                    html.Button('🔄 Limpiar Filtro', 
                               id='clear-filter-button', 
                               n_clicks=0,
                               className='btn btn-outline-warning btn-block',
                               style={'marginTop': '0px'})
                ])
            ])
        ]),

        # --- ACELERÓMETRO ---
        html.Div(
    id='gauge-container', 
    className="card p-3 mb-4", 
    style={"backgroundColor": "#130F4A","border":"1px solid #130F4A"},  # Cambiado a diccionario
    children=[
        dcc.Graph(
            id='gauge-general', 
            figure=crear_gauge_general(puntaje_inicial), 
            config={'displayModeBar': False}
        )
    ]
),
        
        # --- TABS (ÁREAS) ---
        dcc.Tabs(id="tabs-area", value=AREAS[0], children=[
            dcc.Tab(label=area, value=area, children=html.Div(id=f'tab-content-{area}'))
            for area in AREAS
        ], colors={"border": "darkgray", "primary": "#007bff", "background": "#212529"}),
        
        # --- BOTÓN GUARDAR ---
        html.Div(className="mb-4 mt-4", children=[
            html.Button('💾 Guardar Cambios a Excel', id='save-button', n_clicks=0, className='btn btn-success btn-lg btn-block'),
            html.Div(id='save-output', className="text-center text-warning mt-3")
        ])
    ])
])


# ====================================================================
# 3. CALLBACKS (FUNCIONALIDAD)
# ====================================================================

# -----------------
# 3.1: CALLBACK PARA INICIALIZAR LAS TABLAS
# -----------------
@app.callback(
    [Output(f'tab-content-{area}', 'children') for area in AREAS],
    [Input('store-inicial', 'data'),
     Input('responsable-filter', 'value')]
)
def inicializar_tabs(datos_iniciales, filtro_responsable):
    if not datos_iniciales:
        raise dash.exceptions.PreventUpdate
        
    df_completo = pd.DataFrame(datos_iniciales)
    
    # Manejar el filtro especial para "Gerente + Finanzas"
    if filtro_responsable == 'Gerente + Finanzas':
        df_filtrado = df_completo[df_completo['Responsable'].isin(['Gerente Sucursal', 'Finanzas Sucursal'])]
    elif filtro_responsable == 'ALL' or filtro_responsable is None:
        df_filtrado = df_completo
    else:
        df_filtrado = df_completo[df_completo['Responsable'] == filtro_responsable]

    tab_contents = []
    for area in AREAS:
        df_area_filtrada = df_filtrado[df_filtrado['Área'] == area]
        
        if df_area_filtrada.empty:
            if filtro_responsable == 'Gerente + Finanzas':
                mensaje = f"No hay KPIs de {area} asignados a Gerente Sucursal o Finanzas Sucursal."
            elif filtro_responsable == 'ALL' or filtro_responsable is None:
                mensaje = f"No hay KPIs de {area}."
            else:
                mensaje = f"No hay KPIs de {area} asignados al responsable '{filtro_responsable}'."
            
            tab_contents.append(html.Div(
                html.P(mensaje, className="text-light mt-4 p-3 bg-secondary rounded")
            ))
        else:
            # Asegurarnos de que tenemos los datos calculados para la tabla
            df_area_calculado, _ = calcular_kpis(df_area_filtrada.copy())
            tabla = crear_tabla_area(df_area_calculado, area)
            figura = crear_grafico_area(df_area_filtrada)
            
            content = html.Div(className="container", children=[
                html.Div(className="rounded-top rounded-5 bg-light p-3 mt-4 ", children=[
                    dcc.Graph(figure=figura, config={'displayModeBar': False})
                ]),
                
                # TABLA SIEMPRE VISIBLE
                html.Div(className="rounded-bottom rounded-5 bg-white p-3", children=[
                    html.H5("Tabla de Ingreso y Comentarios", className="text-primary mb-3"),
                    tabla
                ])
            ])
            tab_contents.append(content)

    return tab_contents

# -----------------
# 3.2: CALLBACK PARA LIMPIAR FILTRO
# -----------------
@app.callback(
    Output('responsable-filter', 'value'),
    [Input('clear-filter-button', 'n_clicks')]
)
def limpiar_filtro(n_clicks):
    if n_clicks and n_clicks > 0:
        return 'ALL'

# -----------------
# 3.3: CALLBACK PARA ACTUALIZAR EL GAUGE Y DATOS
# -----------------
@app.callback(
    [Output('gauge-general', 'figure'),
     Output('store-inicial', 'data')],
    [Input({'type': 'tabla-editable', 'index': dash.dependencies.ALL}, 'data')],
    [State('store-inicial', 'data')]
)
def actualizar_dashboard_y_store(tablas_data, datos_actuales_store):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    
    df_actualizado = pd.DataFrame()
    for data in tablas_data:
        if data:
            df_actualizado = pd.concat([df_actualizado, pd.DataFrame(data)], ignore_index=True)
    
    if df_actualizado.empty:
        raise dash.exceptions.PreventUpdate
    
    df_actualizado, nuevo_puntaje = calcular_kpis(df_actualizado.copy())
    fig_gauge = crear_gauge_general(nuevo_puntaje)
    
    return fig_gauge, df_actualizado.to_dict('records')

# -----------------
# 3.4: Callback de Guardado
# -----------------
@app.callback(
    Output('save-output', 'children'),
    [Input('save-button', 'n_clicks')],
    [State('store-inicial', 'data')]
)
def guardar_datos_a_excel(n_clicks, datos_guardados):
    if n_clicks is None or n_clicks == 0: 
        return ""

    try:
        if not datos_guardados:
            return "❌ No hay datos para guardar."

        df_final = pd.DataFrame(datos_guardados)
        df_final, _ = calcular_kpis(df_final.copy())
        
        columnas_a_exportar = ['Área', 'Indicador', 'Frecuencia', 'Ponderacion', 'Meta', 'Actual', 
                              'Responsable', 'Fuente de Datos', 'Comentarios', 'Definicion']
        df_export = df_final[columnas_a_exportar]

        archivo_salida = 'kpi_data_guardada.xlsx'
        df_export.to_excel(archivo_salida, index=False)
        
        return f"✅ ¡Datos guardados exitosamente en '{archivo_salida}'!"
        
    except Exception as e:
        print(f"Error al guardar: {e}")
        return f"❌ Error al guardar los datos: {e}"

url = "http://127.0.0.1:8050/"
port = 8050 
def open_browser():
    threading.Timer(1.5, lambda: webbrowser.open_new(url)).start()

if __name__ == '__main__':
    if not dash.get_app().server.debug or dash.get_app().server.config.get("ENV") == "development":
        open_browser()
    app.run(debug=True, port=port)
