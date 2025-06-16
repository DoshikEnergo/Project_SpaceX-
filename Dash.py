import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

label_side = spacex_df["Launch Site"].unique()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                  dcc.Dropdown(
                                     id='site-dropdown',
                                        options=[
                                        {'label': 'All Sites', 'value': 'ALL'}] + 
                                        [{'label': site, 'value': site}
                                         for site in spacex_df['Launch Site'].unique()],
                                        value='ALL',
                                        placeholder="Select a launch site",
                                        searchable=True
                                        ),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                html.Div(dcc.RangeSlider(id = "payload-slider" ,min = min_payload, max = max_payload)),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Фільтруємо тільки успішні запуски
        df_success = spacex_df[spacex_df['class'] == 1]
        fig = go.Figure(
            data=[go.Pie(
                labels=df_success['Launch Site'].value_counts().index,
                values=df_success['Launch Site'].value_counts().values,
                hole=0.3
            )]
        )
        fig.update_layout(title='Total Successful Launches by Site')
    else:
        # Фільтруємо по вибраному Launch Site
        df_site = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Підрахунок кількостей для class=1 і class=0
        counts = df_site['class'].value_counts().sort_index()
        labels = ['Failure', 'Success'] if 0 in counts else ['Success']
        values = [counts.get(0, 0), counts.get(1, 0)]
        fig = go.Figure(
            data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.3
            )]
        )
        fig.update_layout(title=f'Success vs. Failure Launches for {selected_site}')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback([Input(component_id='site-dropdown', component_property='value'), 
Input(component_id="payload-slider", component_property="value")],
Output(component_id='success-payload-scatter-chart', component_property='figure'))

def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    # Фільтруємо по payload діапазону
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites'
        )
    else:
        # Додаткове фільтрування по Launch Site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for {selected_site}'
        )
    

# Run the app
if __name__ == '__main__':
    app.run()
print(spacex_df)