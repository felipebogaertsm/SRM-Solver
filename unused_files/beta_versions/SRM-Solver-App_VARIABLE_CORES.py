import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
from functions.ib_functions import *
from functions.propellant import *
from functions.structural_functions import *

from functions.functions import *

# _____________________________________________________________________________________________________________________
# INITIAL DEFINITIONS

web_res = 1000

# Input label column width:
label_col_width = 1
# Input object column width:
input_col_width = 2

prop_dict = {
    'KNSB (Nakka)': 'knsb-nakka',
    'KNSB (Gudnason)': 'knsb',
    'KNER (Gudnason)': 'kner',
    'KNDX (Nakka)': 'kndx'
}

material_list = [
    {'label': '6061-T6', 'value': '6061_t6'},
    {'label': '1045 steel', 'value': '1045_steel'},
    {'label': '304 stainless', 'value': '304_stainless'}
]

# _____________________________________________________________________________________________________________________
# INPUT TAB

input_row_1 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Name'),
                    dbc.Input(
                        type='text',
                        id='motor_name',
                        placeholder='Enter motor name...'
                    )
                ]
            ),
            width=6
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Manufacturer'),
                    dbc.Input(
                        type='text',
                        id='motor_manufacturer',
                        placeholder='Enter motor manufacturer...'
                    )
                ]
            ),
            width=6
        )
    ]
)

input_row_2 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Propellant composition'),
                    dbc.Select(
                        id='propellant_select',
                        options=[
                            {'label': i, 'value': j} for i in list(prop_dict.keys()) for j in list(prop_dict.values())
                        ],
                        value='knsb-nakka'
                    )
                ]
            ),
            width=6
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Grain segment count'),
                    dbc.Input(
                        placeholder='Set integer...',
                        id='N',
                        value='4',
                        type='number'
                    )
                ]
            ),
            width=6
        )
    ]
)

input_row_3 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Grain diameter (mm)'),
                    dbc.Input(
                        placeholder='Insert grain diameter',
                        id='D_grain',
                        value='41',
                        type='number'
                    )
                ]
            ),
            width=6
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Grain spacing (mm)'),
                    dbc.Input(
                        placeholder='Insert grain spacing...',
                        id='grain_spacing',
                        value='2',
                        type='number'
                    )
                ]
            )
        )
    ]
)

input_row_4 = html.Div([
    dbc.Row(
        [
            dbc.Col(
                dbc.FormGroup(
                    [
                        daq.BooleanSwitch(
                            id='neutral_burn_profile',
                            label='Neutral burn profile',
                            on=True
                        )
                    ]
                ), width=6
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        daq.BooleanSwitch(
                            id='single_core_diameter',
                            label='Single core diameter',
                            on=True
                        )
                    ]
                ), width=6
            )
        ]
    )
])

input_row_5 = dbc.Row(
    [
        dbc.Col(
            id='core_diameter_inputs',
            children=[]
        ),
        dbc.Col(
            id='segment_length_inputs',
            children=[]
        )
    ]
)

input_row_6 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Throat diameter (mm)'),
                    dbc.Input(
                        placeholder='Insert throat diameter...',
                        id='D_throat',
                        value='9.5',
                        type='number'
                    )
                ]
            ), width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Divergent angle (°)'),
                    dbc.Input(
                        placeholder='Enter divergent angle...',
                        id='Div_angle',
                        value='12',
                        type='number'
                    )
                ]
            ), width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Convergent angle (°)'),
                    dbc.Input(
                        placeholder='Enter convergent angle...',
                        id='Conv_angle',
                        value='30',
                        type='number'
                    )
                ]
            ), width=4
        )
    ]
)

input_row_7 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Inside diameter (mm)'),
                    dbc.Input(
                        placeholder='Insert inside diameter...',
                        id='D_in',
                        value='44.45',
                        type='number'
                    ),
                    dbc.FormText('Including the thermal liner!'),
                ]
            ), width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Outside diameter (mm)'),
                    dbc.Input(
                        placeholder='Insert outside diameter...',
                        id='D_out',
                        value='50.8',
                        type='number'
                    )
                ]
            ), width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Liner thickness (mm)'),
                    dbc.Input(
                        placeholder='Insert liner thickness...',
                        id='liner_thickness',
                        value='1',
                        type='number'
                    )
                ]
            ), width=4
        )
    ]
)

input_row_8 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Structural safety factor'),
                    dbc.Input(
                        placeholder='Enter safety factor...',
                        id='sf',
                        type='number',
                        value='4'
                    )
                ]
            ), width=6
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    daq.BooleanSwitch(
                        id='steel_nozzle',
                        label='Steel nozzle',
                        on=True
                    )
                ]
            )
        )
    ]
)

input_row_9 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Casing Material'),
                    dbc.Select(
                        options=material_list,
                        id='casing_material',
                        value='6061_t6',
                    )
                ]
            ), width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Nozzle material'),
                    dbc.Select(
                        options=material_list,
                        id='nozzle_material',
                        value='304_stainless',
                    )
                ]
            ), width=4
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Bulkhead material'),
                    dbc.Select(
                        options=material_list,
                        id='bulkhead_material',
                        value='6061_t6',
                    )
                ]
            )
        )
    ]
)

input_row_10 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Rocket mass w/o the motor (kg)'),
                    dbc.Input(
                        placeholder='Enter the rocket mass without the motor...',
                        id='m_rocket',
                        type='number',
                        value='2.8'
                    )
                ]
            ), width=6
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Motor structural mass (kg)'),
                    dbc.Input(
                        placeholder='Enter the motor structural mass...',
                        id='m_motor',
                        type='number',
                        value='0.85'
                    )
                ]
            ), width=6
        )
    ]
)

input_row_11 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Rocket drag coefficient'),
                    dbc.Input(
                        placeholder='Enter the drag coefficient of the rocket...',
                        id='Cd',
                        type='number',
                        value='0.4'
                    )
                ]
            ), width=6
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label('Frontal diameter (mm)'),
                    dbc.Input(
                        placeholder='Enter the rocket frontal diameter...',
                        id='D_rocket',
                        type='number',
                        value='67.5'
                    )
                ]
            ), width=6
        )
    ]
)

# _____________________________________________________________________________________________________________________
# GRAPHS

# _____________________________________________________________________________________________________________________
# INTERNAL BALLISTICS TAB

ib_row_1 = dbc.Row(
    [
        dbc.Col(
            html.Div(
                [
                    dbc.Label(
                        children=[
                            '.'
                        ]
                    )
                ]
            )
        )
    ]
)

# _____________________________________________________________________________________________________________________
# TABS

input_tab = dbc.Tab(label='Inputs', children=[
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2([dbc.Badge('Motor data')]),
                            input_row_1,
                            html.H2([dbc.Badge('Propellant grain')]),
                            input_row_2,
                            input_row_3,
                            html.H3([dbc.Badge('Grain segments')]),
                            input_row_4,
                            input_row_5,
                            html.H2([dbc.Badge('Thrust chamber')]),
                            input_row_6,
                            html.H3([dbc.Badge('Combustion chamber')]),
                            input_row_7,
                            input_row_8,
                            input_row_9,
                            html.H2([dbc.Badge('Vehicle data')]),
                            input_row_10,
                            input_row_11,
                        ]
                    )
                ),
                width=6
            ),
            dbc.Col(
                dbc.Card(
                    dcc.Graph(
                        id='grain_radial',
                        figure={}
                    )
                ),
                width=6
            )
        ]
    )
])

ib_tab = dbc.Tab(
    label='Internal Ballistics',
    id='ib_tab',
    disabled=[],
    children=[
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2([dbc.Badge('IB parameters')]),
                                html.H3([dbc.Badge('Burn Regression')]),
                                ib_row_1,
                            ]
                        )
                    ), width=6
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                    id='burn_regression_graph',
                                )
                            ]
                        )
                    ), width=6
                )
            ]
        )
    ]
)

nozzle_tab = dbc.Tab(
    label='Nozzle Design',
    children=[
        html.P('.')
    ]
)

structure_tab = dbc.Tab(
    label='Structure',
    children=[
        html.P('.')
    ]
)

ta_tab = dbc.Tab(
    label='Thermal Analysis',
    children=[
        html.P('.')
    ]
)

ballistic_tab = dbc.Tab(
    label='Rocket Trajectory',
    children=[
        html.P('.')
    ]
)

# _____________________________________________________________________________________________________________________
# DASH APP EXECUTION

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H1("SRM Solver", style={'textAlign': 'center'}),
            html.H5('Build a BATES grain Solid Rocket Motor inside your own browser', style={'textAlign': 'center'}),
        ],
            width={'size': 12}
        )
    ],
    ),
    dbc.Tabs([
        input_tab,
        ib_tab,
        structure_tab,
        ta_tab,
        ballistic_tab
    ]),

    html.Div([
        dcc.Markdown('Written by Felipe Bogaerts de Mattos, October 2020.', style={'textAlign': 'right'})
    ])

])


# _____________________________________________________________________________________________________________________
# CALLBACKS


@app.callback(
    Output(component_id='grain_radial', component_property='figure'),
    [
        Input(component_id='D_grain', component_property='value'),
        Input(component_id='D_core', component_property='value')
    ]
)
def update_grain_radial_graph(D_grain, D_core):
    D_grain = float(D_grain)
    D_core = float(D_core)
    R_grain = D_grain / 2
    R_core = D_core / 2
    x = np.linspace(0.5 * - 1 * D_grain, 0.5 * D_grain)
    figure_grain_radial = go.Figure(
        data=go.Scatter(
            x=[0, R_grain],
            y=[R_core, 0]
        ),
        layout=go.Layout(
            title='Grain radial perspective',
            yaxis={'scaleanchor': 'x', 'scaleratio': 1},
        )
    )
    figure_grain_radial.add_shape(
        type='circle',
        xref='x', yref='y',
        fillcolor='#dac36d',
        x0=- R_grain, x1=R_grain, y0=- R_grain, y1=R_grain
    )
    figure_grain_radial.add_shape(
        type='circle',
        xref='x', yref='y',
        fillcolor='#e3e3e3',
        x0=- R_core, x1=R_core, y0=- R_core, y1=R_core
    )
    return figure_grain_radial


# Update the core diameter input boxes:
@app.callback(
    Output(component_id='core_diameter_inputs', component_property='children'),
    [
        Input(component_id='single_core_diameter', component_property='on'),
        Input(component_id='neutral_burn_profile', component_property='on'),
        Input(component_id='N', component_property='value')
    ]
)
def update_core_input_box(single_core_diameter, neutral_burn_profile, N):
    N = int(N)
    if single_core_diameter:
        core_col = dbc.FormGroup(
            children=[
                dbc.Label('Core diameter (mm)'),
                dbc.Input(
                    placeholder='Insert core diameter...',
                    id='D_core',
                    value='15',
                    type='number'
                )
            ]
        )
    else:
        core_col = [dbc.FormGroup(
            children=[
                dbc.Label(f'Core #{i + 1} diameter (mm)'),
                dbc.Input(
                    placeholder=f'Insert #{i + 1} core diameter...',
                    id=f'D_core_{i + 1}',
                    value='15',
                    type='number'
                )
            ]
        ) for i in range(N)]
    return core_col


# Update the length input boxes:
@app.callback(
    Output(component_id='segment_length_inputs', component_property='children'),
    [
        Input(component_id='single_core_diameter', component_property='on'),
        Input(component_id='neutral_burn_profile', component_property='on'),
        Input(component_id='N', component_property='value'),
        Input(component_id='D_core', component_property='value'),
        Input(component_id='D_grain', component_property='value')
    ]
)
def update_length_input_box(single_core_diameter, neutral_burn_profile, N, D_core, D_grain):
    D_core = float(D_core)
    D_grain = float(D_grain)
    N = int(N)
    if single_core_diameter and neutral_burn_profile:
        length_col = dbc.FormGroup(
            children=[
                dbc.Label('Segment length (mm)'),
                dbc.Input(
                    placeholder='Insert segment length...',
                    id='L_grain',
                    value=f'{0.5 * (3 * D_grain + D_core)}',
                    type='number',
                    disabled=True,
                ),
                dbc.FormText('To edit this value, disable \"Neutral burn profile\"')
            ]
        )
    elif single_core_diameter is True and neutral_burn_profile is False:
        length_col = dbc.FormGroup(
            children=[
                dbc.Label('Segment length (mm)'),
                dbc.Input(
                    placeholder='Insert segment length...',
                    id='L_grain',
                    value=f'{0.5 * (3 * D_grain + D_core)}',
                    type='number',
                    disabled=False
                )
            ]
        )
    elif single_core_diameter is False and neutral_burn_profile is False:
        length_col = [dbc.FormGroup(
            children=[
                dbc.Label(f'Segment #{i + 1} length (mm)'),
                dbc.Input(
                    placeholder=f'Insert #{i + 1} segment length...',
                    id=f'L_grain_{i + 1}',
                    value='68',
                    type='number'
                )
            ]
        ) for i in range(N)]
    return length_col


if __name__ == '__main__':
    app.run_server()
