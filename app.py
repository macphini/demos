import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

server = app.server

app.title = 'SALARY PROJECTIONS'

provinces = {'AB':70000, 'ON':72000, 'MB': 58000, 'BC':73000, 'NL':53000, 'SK':56000, 'QB':53000, 'NB':57000}

modal = html.Div(
    [
        dbc.Button("About", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("About Dashboard"),
                dbc.ModalBody("""This dashboard shows a projection of a Data Scientist salary for several 
                                provinces in Canada. Please note!!! these are just ficitious values!"""),
                dbc.ModalFooter(
                    [dbc.Button("Close", id="close", className="ml-auto")]
                ),
            ],
            id="modal",
        ),
    ]
)



header = dbc.Card([
    dbc.Row([
        dbc.Col([html.H5('DATA SCIENTIST SALARY PROJECTION FOR CANADIAN PROVINCES')], width=9, style={'text-align':'center'}),
        dbc.Col([dbc.Button("Github", href='https://github.com/macphini/demos', target="_blank", color="link")], width=1),
        dbc.Col(modal, width=1),
        dbc.Col([html.Img(src='./assets/logo.jpg', style={'width':'60px', 'height':'60px'})], width=1, style={'align-items':'right'})
    ], style={'align-items':'center', 'margin':'20px'})
], style={'margin':'20px'})

form = dbc.FormGroup(
    [
        dbc.Label('Enter years of Experience', html_for='ex-yrs', width=5),
        dbc.Col([dcc.Input(id='ex-yrs', type='number', min=0, value=10)], width=5),
    ],
    row=True, style={'align-items':'center'}
)

form1 = dbc.FormGroup(
    [
        dbc.Label('Select Province(s)', html_for='province-drops', width=5),
        dbc.Col([dcc.Dropdown(id='province-drops',
        options=[
            {'label': k, 'value': k} for k, v in provinces.items()
        ],
        value=[*provinces.keys()],
        multi=True
    )], width=5),
    ],
    row=True, style={'align-items':'center'}
)


body1 = dbc.Row([
    dbc.Col([form, form1], width=4),
    dbc.Col([dbc.Spinner(dcc.Graph(id='plot'))], width=8)
], style={'margin':'4px'})

# def make_layout():
#     return ()


def get_pay(yr):
    val = lambda k, x: int(provinces[k] * (1.02)**x)
    return {k:[val(k, x) for x in range(yr, yr+15)] for k, v in provinces.items()}
    

app.layout = html.Div([header, body1])

@app.callback(
    Output("plot", "figure"),
    [Input("province-drops", "value"), Input("ex-yrs", "value")],
)
def generate_figure(province_list, yr_exp):
    fig = go.Figure(data=[
    go.Bar(name=k, x=[*range(yr_exp, yr_exp+15)], y=get_pay(yr_exp)[k]) for k in province_list
    ])
    # Change the bar mode
    fig.update_layout(barmode='group', xaxis={'title':'Years of Experience'}, yaxis={'title':'Salary in CAD'})
    return fig

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

