import streamlit as st
import pandas as pd
import plotly.express as px
import base64 

# Se emplea streamlit y plotly para generar las visualizaciones para el informe.

# Cargar el dataset para el informe e imagen
df_informe = pd.read_csv("df_limpio.csv")

with open("dvd.jpeg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Ordenar días de la semana y meses
dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
meses_orden = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

df_informe['Día Semana'] = pd.Categorical(df_informe['Día Semana'], categories=dias_orden, ordered=True)
df_informe['Mes'] = pd.Categorical(df_informe['Mes'], categories=meses_orden, ordered=True)

# Crear barra lateral para filtros
st.sidebar.header("Filtros")

# Filtro por Local
locales = df_informe['Local'].unique()
local_seleccionado = st.sidebar.multiselect(
    "Selecciona los locales:", options=locales, default=locales
)

# Filtro por Año
anios = sorted(df_informe['Año'].unique())
ano_seleccionado = st.sidebar.multiselect(
    "Selecciona los años:", options=anios, default=anios
)
if not ano_seleccionado:
    st.warning("⚠️  Por favor, debes seleccionar, al menos, uno de los años en los filtros (2019 y/o 2020). ¡Gracias!")
    st.stop()

# Filtro por Semana (slider)
semanas = sorted(df_informe[df_informe['Año'].isin(ano_seleccionado)]['Semana'].unique())
min_semana, max_semana = min(semanas), max(semanas)

# Slider para seleccionar rango de semanas
rango_semanas = st.sidebar.slider(
    "Selecciona el rango de semanas:",
    min_value=min_semana,
    max_value=max_semana,
    value=(min_semana, max_semana)  # Por defecto, todas las semanas
)

# Filtrar el DataFrame según los filtros seleccionados
df_filtrado = df_informe[
    (df_informe['Local'].isin(local_seleccionado)) &
    (df_informe['Año'].isin(ano_seleccionado)) &
    (df_informe['Semana'] >= rango_semanas[0]) & (df_informe['Semana'] <= rango_semanas[1])
]

# KPIs
st.title("💶 Facturación y Ventas")

# Total sumado
total_suma = df_filtrado['Total'].sum()
st.metric(label="Facturación (€):", value=f"{total_suma:,.2f}")

# Número de servicios
numero_servicios = df_filtrado['Servicio'].nunique()
st.metric(label="Número de Servicios:", value=numero_servicios)

# Ticket medio
ticket_medio = total_suma / numero_servicios if numero_servicios > 0 else 0
st.metric(label="Servicio Medio (€):", value=f"{ticket_medio:,.2f}")

# Gráfico 1: Suma de la columna "Total"
st.subheader("Facturación por Semana y Local")
grafico_total = px.bar(
    df_filtrado.groupby(['Semana', 'Local'])['Total'].sum().reset_index(),
    x='Semana', y='Total', color='Local',
    labels={"Total": "Facturación (€)", "Semana": "Semana"},
    title="Facturación (€)"
)
st.plotly_chart(grafico_total)
st.text("Insights del analista:")

st.markdown(
    f"""
    <div style="display: flex; align-items: flex_start; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="David">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            <b>Año 2019:</b> se obtiene una facturación total de unos <b>869K €</b> con un servicio medio de <b>29.96 €</b>. <b>Valencia</b> y <b>Pozuelo</b> suponen más del <b>50%</b>
              de la facturación total. <b>Malasaña</b> destaca con el servicio medio más alto (<b>34.65 €</b>) a pesar de su baja facturación con respecto a los anteriores locales.
              Una facturación de unos <b>115K €</b>, mucho más en la línea de las sucursales de <b>Barcelona</b> o <b>Mallorca</b>.
              <br><br>
            <b>Año 2020:</b> se obtiene una facturación total de unos <b>394K €</b> con un servicio medio de <b>29.48 €</b>. <b>Barcelona</b> y <b>Pozuelo</b> suponen la práctica totalidad
            de la facturación. Es importante destacar que solo contamos con registros de las primeras 32 semanas de 2020.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Gráfico 2: Número de Servicios
grafico_servicios = px.bar(
    df_filtrado.groupby(['Semana', 'Local'])['Servicio'].nunique().reset_index(),
    x='Semana', y='Servicio', color='Local',
    labels={"Servicio": "Número de Servicios", "Semana": "Semana"},
    title="Número de Servicios"
)
st.plotly_chart(grafico_servicios)
st.text("Insights del analista:")

st.markdown(
    f"""
    <div style="display: flex; flex_start: center; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="Tu cara">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            Según los registros, el número de servicios nos permite observar que la franquicia comienza con los locales de <b>Barcelona</b> y <b>Valencia</b> para, en la <b>primavera de 2019</b>, abrir las sucursales de
            <b>Mallorca</b>, <b>Pozuelo</b> y <b>Malasaña</b>. Es en <b>2020</b> cuando se cierra el local de <b>Malasaña</b> a principios de año. Coincidiendo con la crisis de COVID-19, parece que se cierran todos las sucursales exceptuando la de <b>Barcelona</b>.
            <br><br>
            Desde la segunda semana de <b>abril de 2020</b>, la franquicia se mantiene hasta la <b>semana 32 de 2020</b> (última semana de registros) con las sucursales de <b>Barcelona</b> y <b>Pozuelo</b>.
            <br><br>
            El número de servicios también nos permite detectar patrones de ventas. Es tanto en lo meses de inicio de verano (<b>semana 22-24</b>) como en las semanas que cuentan con puentes y festivos
            (<b>semana 44</b>) cuando se registran los mayores picos de afluencia de clientes. <b>Agosto</b> supone de forma consistentemente el mes de menos afluencia de forma global.
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

# Detalle Temporal
st.title("🕒 Detalle Temporal")

# Número de Servicios por Hora
df_servicios_hora = df_filtrado.groupby(['Hora', 'Local'])['Servicio'].nunique().reset_index()
grafico_servicios_hora = px.bar(
    df_servicios_hora,
    x='Hora',
    y='Servicio',
    color='Local',
    labels={"Servicio": "Número de Servicios", "Hora": "Hora"},
    title="Número de Servicios por Hora"
)
st.plotly_chart(grafico_servicios_hora)
st.text("Insights del analista:")

st.markdown(
    f"""
    <div style="display: flex; flex_start: center; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="Tu cara">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            Este apartado nos permite observar el detalle de la afluencia por hora. Se puede observar como el turno de <b>Noche</b> tiene más afluencia que el turno de <b>Mediodía</b> de forma global.
            Además, podemos observar que respectivamente para cada uno de estos turnos, las <b>21h.</b> y las <b>15h.</b> son las horas pico de forma generalizada en todas las sucursales.
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

# Facturación por Día Semana
df_dia_semana = df_filtrado.groupby(['Día Semana', 'Local'])['Total'].sum().reset_index()
grafico_facturacion_dia = px.bar(
    df_dia_semana,
    x='Día Semana',
    y='Total',
    color='Local',
    labels={"Total": "Facturación (€)", "Día Semana": "Día de la Semana"},
    title="Facturación por Día de la Semana"
)
st.plotly_chart(grafico_facturacion_dia)
st.text("Insights del analista:")

st.markdown(
    f"""
    <div style="display: flex; flex_start: center; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="Tu cara">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            Este gráfico nos permite observar los días de la semana que representan los mayores picos de facturación. Son los <b>fines de semana</b> los momentos de mayor facturación.
            Destaca el <b>sábado</b> como día de mayor facturacion de forma global. Entre los días de diario, es el <b>martes</b> el día que mayor facturación se recibe de forma consistente.
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

# Número de Servicios por Día Semana
df_servicios_dia = df_filtrado.groupby(['Día Semana', 'Local'])['Servicio'].nunique().reset_index()
grafico_servicios_dia = px.bar(
    df_servicios_dia,
    x='Día Semana',
    y='Servicio',
    color='Local',
    labels={"Servicio": "Número de Servicios", "Día Semana": "Día de la Semana"},
    title="Número de Servicios por Día de la Semana"
)
st.plotly_chart(grafico_servicios_dia)
st.text("Insights del analista:")

st.markdown(
    f"""
    <div style="display: flex; flex_start: center; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="Tu cara">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            Aunque muy correlacionada con el gráfico anterior, esta visualización nos permite observar que <b>viernes</b> y <b>sábado</b> reciben una afluencia similar a pesar de la diferencia en 
            facturación total que se producen los <b>sábados</b> respecto al quinto día de la semana.
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

# Facturación por Mes
df_facturacion_mes = df_filtrado.groupby(['Mes', 'Local'])['Total'].sum().reset_index()
grafico_facturacion_mes = px.bar(
    df_facturacion_mes,
    x='Mes',
    y='Total',
    color='Local',
    labels={"Total": "Facturación (€)", "Mes": "Mes"},
    title="Facturación por Mes"
)
st.plotly_chart(grafico_facturacion_mes)
st.text("Insights del analista:")

st.markdown(
    f"""
    <div style="display: flex; flex_start: center; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="Tu cara">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            Aunque sesgado por la tipología de los registros (no contamos con registros para todas las sucursales en todas las semanas y años), se puede observar como los meses de 
            <b>mayo</b>, <b>junio</b> y <b>julio</b> representan los mayores pico de facturación de la franquicia. <b>Agosto</b> es un mes valle en todas las sucursales.
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

# Detalle de Productos
st.title("🍜 Detalle de Productos")

# Filtro por Familia (local al gráfico)
familias = df_informe['Familia'].unique()
familia_seleccionada = st.multiselect(
    "Selecciona la Familia:", options=familias, default=["RICE BOWL", "NOODLES"]
)

# Filtrar el DataFrame por Familia seleccionada
df_productos = df_filtrado[df_filtrado['Familia'].isin(familia_seleccionada)]

# Agrupar por Producto y sumar Cantidad
df_productos_agrupado = df_productos.groupby(['Producto', 'Local']).agg(
    Cantidad=('Cantidad', 'sum')
).reset_index()

# Limitar a los 20 productos más vendidos
df_top_productos = df_productos_agrupado.groupby('Producto')['Cantidad'].sum().nlargest(20).index
df_productos_agrupado = df_productos_agrupado[df_productos_agrupado['Producto'].isin(df_top_productos)]

# Gráfico de Productos
grafico_productos = px.bar(
    df_productos_agrupado,
    x='Producto',
    y='Cantidad',
    color='Local',
    labels={"Cantidad": "Cantidad Vendida", "Producto": "Producto"},
    title="Cantidad Vendida por Producto"
)
grafico_productos.update_layout(xaxis={'categoryorder': 'total descending'}, xaxis_tickangle=-45)

st.plotly_chart(grafico_productos)

st.text("Insights del analista:")

st.markdown(
    f"""
    <div style="display: flex; align-items: flex_start; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="Tu cara">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            Los productos estrella de esta franquicia en todas sus ubicaciones son el <b>Pad Thai</b> y el <b>Nasi Goreng</b>. Pudiéndote comer los más baratos
            en <b>Malasaña</b> y <b>Valencia</b> y los más caros en <b>Mallorca</b>.<br><br>
            En cuanto a la bebida, los clientes prefieren acompañar su comida con <b>agua</b> o <b>cerveza</b>.<br><br>
            Aunque no es una opción muy frecuente, cuando los clientes piden postre, <b>Pasabog CheeseCake</b> o una sencilla <b>Bolsa de Helado</b> son las elegidas.
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

st.subheader("¿Cuánto cuesta un...?")

# Filtro por Producto (máximo 2 seleccionados)
productos = df_informe['Producto'].unique()
producto_seleccionado = st.multiselect(
    "Selecciona hasta 2 productos:", 
    options=productos, 
    default=["Pad Thai", "Nasi Goreng"],
    max_selections=2  # Solo permite seleccionar un máximo de 2
)

# Verificar que hay selección y evitar errores si está vacío
if len(producto_seleccionado) == 0:
    st.warning("Por favor, selecciona al menos un producto.")
    st.stop()

# Generar dinámicamente métricas para los productos seleccionados
for producto in producto_seleccionado:
    precio_medio = df_filtrado[df_filtrado['Producto'] == producto]['Precio Unitario'].mean()
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-top: 20px; margin-bottom: 20px;">
            <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); width: 100%;">
                <b>{producto}</b><br>
                Precio Medio: <b>{precio_medio:.2f} €</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.text("Nota del analista:")
st.markdown(
    f"""
    <div style="display: flex; align-items: flex_start; margin-top: 20px; margin-bottom: 20px;">
        <img src="data:image/jpeg;base64,{encoded_image}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" alt="Tu cara">
        <div style="background-color: #f1f1f1; padding: 10px 15px; border-radius: 15px; max-width: 1000px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
            Debido al bajo número de registros de <b>clientes</b> y <b>descuentos</b> <span style="background-color: yellow;">se ha decidido no oportuno profundizar en el análisis de estas variables.</span>
            Los resultados no resultaban suficientemente significativos.<br><br>
            ¡Te animo a filtrar por locales, semanas o años para <b>obtener tus propios insights</b>!
        </div>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)


# Mostrar primeras filas del dataset filtrado
st.subheader("Resumen de los datos empleados")
st.dataframe(df_filtrado.head())
