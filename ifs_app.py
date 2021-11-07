import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

IFS_df = pd.read_pickle("IFS_df.pkl")

if_por_uf = IFS_df.groupby(['UF']).size().reset_index(name='Quantidade')

if_por_uf = if_por_uf.sort_values('Quantidade', ascending=False)

# st.map(IFS_df)

# st.pydeck_chart(pdk.Deck(
#     map_style='mapbox://styles/mapbox/light-v9',
#     initial_view_state=pdk.ViewState(
#         latitude=-15,
#         longitude=-46.525,
#         zoom=3,
#         pitch=5
#     ),
#     layers=[
#         pdk.Layer(
#             'ColumnLayer',
#             data=IFS_df,
#             get_position='[longitude, latitude]',
#             radius=20000,
#             auto_highlight=True,
#             elevation_scale=100,
#             elevation_range=[0, 5000],
#             pickable=True,
#             extruded=True
#         )
#     ]
# ))

with st.sidebar:
    ufs = st.multiselect(
        'Escolha uma UF para visualizar dados:',
        IFS_df['UF'].unique(),
        default=IFS_df['UF'].unique()
    )


# st.write('You selected:', ', '.join(ufs))

st.title("Instituições da Rede Federal")

st.markdown('''
## Visualizando dados das seguintes UF's:
''')
st.write(', '.join(ufs))

fig1 = px.scatter_mapbox(
    IFS_df[IFS_df['UF'].isin(ufs)],
    color_discrete_sequence =['orangered']*len(IFS_df[IFS_df['UF'].isin(ufs)]),
    lat="latitude",
    lon="longitude",
    zoom=3.2,
    center = {
        'lat':-15,
        'lon':-55,
    },
    mapbox_style="open-street-map",
    hover_name='IF',
    hover_data={
        'latitude': False,
        'longitude': False,
        'Município': True,
        'UF': True,
        'Instituicao': True
    },
    width=650,
    height=700)

fig2 = px.bar(if_por_uf, x='UF', y='Quantidade',
              color_discrete_sequence =['darkgreen']*len(if_por_uf),
              labels={'Quantidade':'Instituições da Rede Federal'}, height=400)


st.plotly_chart(fig1, use_container_width=True)

st.plotly_chart(fig2, use_container_width=True)