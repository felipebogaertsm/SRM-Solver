import matplotlib.gridspec as gs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.subplots


def performance_interactive_plot(ib_parameters):

    index = np.where(ib_parameters.t == ib_parameters.t_thrust)[0][0]
    pressure_color = '#008141'
    thrust_color = '#581845'

    figure = plotly.subplots.make_subplots(specs=[[{"secondary_y": True}]])

    figure.add_trace(
        go.Scatter(
            x=ib_parameters.t[: index],
            y=ib_parameters.T[: index],
            name='Thrust',
            line=go.scatter.Line(color=thrust_color)
        ),
        secondary_y=False
    )
    figure.add_trace(
        go.Scatter(
            x=ib_parameters.t[: index],
            y=ib_parameters.P0[: index] * 1e-6,
            name='Pressure',
            line=go.scatter.Line(color=pressure_color),
            yaxis='y2'
        ),
        secondary_y=True
    )

    figure.update_layout(
        title_text='<b>Performance plots</b>'
    )

    # Set x-axis title:
    figure.update_xaxes(title_text='Time (s)')

    # Set y-axes titles:
    figure.update_yaxes(title_text="<b>Thrust</b> (N)", secondary_y=False, color='#6a006a')
    figure.update_yaxes(title_text="<b>Pressure</b> (MPa)", secondary_y=True, color='#008141')

    return figure


def motor_to_eng(t, F, dt, V_prop_CP, D_out, L_chamber, eng_res, pp, m_motor, manufacturer, name):
    """Exports an eng file to the directory 'outputs' inside the program folder. """

    # Making the received volume array the same length as the time vector.
    V_prop = np.zeros(np.size(t))
    for i, volume in enumerate(V_prop_CP):
        V_prop[i] += volume

    # Forming a new time vector that has exactly 'eng_res' points (independent on time step input):
    t_out = np.linspace(0, t[- 1] + dt, eng_res)
    # Interpolating old thrust-time data into new time vector:
    F_out = np.interp(t_out, t, F, left=0, right=0)
    # Interpolating the Propellant volume with the new time vector (to find propellant. mass with t):
    m_prop_out = pp * np.interp(t_out, t, V_prop, right=0)

    # Writing to the ENG file:
    eng_header = f'{name} {D_out * 1e3:.4f} {L_chamber * 1e3:.4f} P ' \
                 f'{m_prop_out[0]:.4f} {m_prop_out[0] + m_motor:.4f} {manufacturer}\n'
    saveFile = open(f'output/{name}.eng', 'w')
    saveFile.write(
        '; Generated by SRM Solver program written by Felipe Bogaerts de Mattos\n; Juiz de Fora, Brasil\n')
    saveFile.write(eng_header)
    for i in range(eng_res):
        saveFile.write('   %.2f %.0f\n' % ((t_out[i]), (F_out[i])))
    saveFile.write(';')
    saveFile.close()


def ballistics_plots(t, a, v, y, g):
    fig1 = plt.figure()

    plt.subplot(3, 1, 1)
    plt.ylabel('Height (m)')
    plt.grid(linestyle='-.')
    plt.plot(t, y, color='b')
    plt.subplot(3, 1, 2)
    plt.ylabel('Velocity (m/s)')
    plt.grid(linestyle='-.')
    plt.plot(t, v, color='g')
    plt.subplot(3, 1, 3)
    plt.ylabel('Acc (m/s2)')
    plt.xlabel('Time (s)')
    plt.grid(linestyle='-.')
    plt.plot(t, a, color='r')

    fig1.savefig('output/TrajectoryPlots.png', dpi=300)

    fig2 = plt.figure()

    plt.plot(t, y, color='b')
    plt.ylabel('Height (m)')
    plt.xlabel('Time (s)')
    plt.ylim(0, np.max(y) * 1.1)
    plt.xlim(0, t[-1])
    plt.grid()

    fig2.savefig('output/HeightPlot.png', dpi=300)

    fig3, ax3 = plt.subplots()

    ax3.set_xlim(0, t[-1])
    ax3.set_ylim(np.min(v * 3.6), np.max(v * 3.6) * 1.05)
    ax3.plot(t, v * 3.6, color='#009933')
    ax3.set_ylabel('Velocity (km/h)')
    ax3.set_xlabel('Time (s)')
    ax3.grid()

    ax4 = ax3.twinx()
    ax4.set_xlim(0, t[-1])
    ax4.set_ylim(np.min(a / g), np.max(a / g) * 1.3)
    ax4.plot(t, a / g, color='#ff6600')
    ax4.set_ylabel('Acceleration (g)')

    fig3.savefig('output/VelocityAcc.png', dpi=300)


def pressure_plot(t, P0, t_burnout):
    """ Returns plotly figure with pressure data. """
    data = [go.Scatter(x=t[t <= t_burnout],
                       y=P0 * 1e-6,
                       mode='lines',
                       name='lines',
                       marker={'color': '#009933'}
                       )]
    layout = go.Layout(title='Pressure-time curve',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Pressure [MPa]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    figure_plotly.add_shape(
        type='line',
        x0=0,
        y0=np.mean(P0) * 1e-6,
        x1=t[- 1],
        y1=np.mean(P0) * 1e-6,
        line={'color': '#ff0000', }
    )
    return figure_plotly


def thrust_plot(t, F):
    """ Returns plotly figure with pressure data. """
    data = [go.Scatter(x=t,
                       y=F,
                       mode='lines',
                       name='lines',
                       marker={'color': '#6a006a'}
                       )]
    layout = go.Layout(title='Thrust-time curve',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Pressure [MPa]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    figure_plotly.add_shape(
        type='line',
        x0=0,
        y0=np.mean(F),
        x1=t[-1],
        y1=np.mean(F),
        line={'color': '#ff0000', }
    )
    return figure_plotly


def height_plot(t, y):
    """ Returns plotly figure with altitude data. """
    data = [go.Scatter(x=t,
                       y=y,
                       mode='lines',
                       name='lines',
                       marker={'color': '#6a006a'}
                       )]
    layout = go.Layout(title='Altitude (AGL)',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Altitude [m]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    return figure_plotly


def velocity_plot(t, v):
    """ Returns plotly figure with velocity data. """
    data = [go.Scatter(x=t,
                       y=v,
                       mode='lines',
                       name='lines',
                       marker={'color': '#6a006a'}
                       )]
    layout = go.Layout(title='Velocity plot',
                       xaxis=dict(title='Time [s]'),
                       yaxis=dict(title='Velocity [m/s]'),
                       hovermode='closest')
    figure_plotly = go.Figure(data=data, layout=layout)
    return figure_plotly


def performance_plot(F, P0, t, t_thrust):
    """ Plots the chamber pressure and thrust in the same figure, saves to 'output' folder. """

    t = t[t <= t_thrust]
    F = F[: np.size(t)]
    P0 = P0[: np.size(t)]
    fig1, ax1 = plt.subplots()

    ax1.set_xlim(0, t[-1])
    ax1.set_ylim(0, 1.05 * np.max(F))
    ax1.set_ylabel('Thrust [N]', color='#6a006a')
    ax1.set_xlabel('Time [s]')
    ax1.grid(linestyle='-', linewidth='.4')
    ax1.plot(t, F, color='#6a006a', linewidth='1.5')
    ax1.tick_params(axis='y', labelcolor='k')

    ax2 = ax1.twinx()
    ax2.set_ylim(0, 1.15 * np.max(P0) * 1e-6)
    ax2.set_ylabel('Chamber Pressure [MPa]', color='#008141')
    ax2.plot(t, P0 * 1e-6, color='#008141', linewidth='1.5')
    ax2.tick_params(axis='y', labelcolor='k')

    fig1.tight_layout()
    fig1.savefig('output/PressureThrust.png', dpi=300)


def main_plot(t, F, P0, Kn, m_prop, t_burnout):
    """ Returns pyplot figure and saves motor plots to 'output' folder. """

    t = t[t <= t_burnout]
    F = F[: np.size(t)]
    P0 = P0[: np.size(t)]
    Kn = Kn[: np.size(t)]
    m_prop = m_prop[: np.size(t)]
    main_figure = plt.figure(3)
    main_figure.suptitle('Motor Data', size='xx-large')
    gs1 = gs.GridSpec(nrows=2, ncols=2)

    ax1 = plt.subplot(gs1[0, 0])
    ax1.set_ylabel('Thrust [N]')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylim(0, np.max(F) * 1.05)
    ax1.set_xlim(0, t[-1])
    ax1.grid(linestyle='-', linewidth='.4')
    ax1.plot(t, F, color='#6a006a', linewidth='1.5')

    ax2 = plt.subplot(gs1[0, 1])
    ax2.set_ylabel('Pressure [MPa]')
    ax2.yaxis.set_label_position('right')
    ax2.set_xlabel('Time [s]')
    ax2.set_ylim(0, np.max(P0) * 1e-6 * 1.05)
    ax2.set_xlim(0, t[-1])
    ax2.grid(linestyle='-', linewidth='.4')
    ax2.plot(t, P0 * 1e-6, color='#008141', linewidth='1.5')

    ax3 = plt.subplot(gs1[1, 0])
    ax3.set_ylabel('Klemmung')
    ax3.set_xlabel('Time [s]')
    ax3.set_ylim(0, np.max(Kn) * 1.05)
    ax3.set_xlim(0, t[-1])
    ax3.grid(linestyle='-', linewidth='.4')
    ax3.plot(t, Kn, color='b', linewidth='1.5')

    ax4 = plt.subplot(gs1[1, 1])
    ax4.set_ylabel('Propellant Mass [kg]')
    ax4.yaxis.set_label_position('right')
    ax4.set_xlabel('Time [s]')
    ax4.set_ylim(0, np.max(m_prop) * 1.05)
    ax4.set_xlim(0, t[-1])
    ax4.grid(linestyle='-', linewidth='.4')
    ax4.plot(t, m_prop, color='r', linewidth='1.5')

    main_figure.set_size_inches(12, 8, forward=True)
    main_figure.savefig('output/MotorPlots.png', dpi=300)
    return main_figure


def mass_flux_plot(t, grain_mass_flux, t_burnout):
    """ Plots and saves figure of the mass flux for all the grain segments """
    t = t[t <= t_burnout]
    t = np.append(t, t[- 1])
    grain_mass_flux = grain_mass_flux
    N, index = grain_mass_flux.shape
    mass_flux_figure = plt.figure()
    for i in range(N):
        plt.plot(t, grain_mass_flux[i] * 1.42233e-3)
    plt.ylabel('Mass Flux [lb/s-in-in]')
    plt.xlabel('Time [s]')
    plt.ylim(0, np.max(grain_mass_flux) * 1.42233e-3 * 1.05)
    plt.xlim(0, t[-1])
    plt.grid(linestyle='-', linewidth='.4')
    mass_flux_figure.savefig('output/GrainMassFlux.png', dpi=300)
    return mass_flux_figure


def print_results(grain, structure, propellant, ib_parameters, structural_parameters, ballistics):
    print('\nResults generated by SRM Solver program, by Felipe Bogaerts de Mattos')

    print('\nBURN REGRESSION')
    if ib_parameters.m_prop[0] > 1:
        print(f' Propellant initial mass {ib_parameters.m_prop[0]:.3f} kg')
    else:
        print(f' Propellant initial mass {ib_parameters.m_prop[0] * 1e3:.3f} g')
    print(' Mean Kn: %.2f' % np.mean(ib_parameters.Kn))
    print(f' Initial to final Kn ratio: {ib_parameters.initial_to_final_kn:.3f}')
    print(f' Volumetric efficiency: {(ib_parameters.V_prop[0] * 100 / ib_parameters.V_empty):.3f} %')
    print(f' Grain length for neutral profile vector: {ib_parameters.optimal_grain_length}')

    print(' Burn profile: ' + ib_parameters.burn_profile)
    print(f' Initial port-to-throat (grain #{grain.N:d}): {ib_parameters.initial_port_to_throat:.3f}')
    print(' Motor L/D ratio: %.3f' % (np.sum(grain.L_grain) / grain.D_grain))
    print(f' Max initial mass flux: {np.max(ib_parameters.grain_mass_flux):.3f} kg/s-m-m or '
          f'{np.max(ib_parameters.grain_mass_flux) * 1.42233e-3:.3f} lb/s-in-in')

    print('\nCHAMBER PRESSURE')
    print(f' Maximum, average chamber pressure: {(np.max(ib_parameters.P0) * 1e-6):.3f}, '
          f'{(np.mean(ib_parameters.P0) * 1e-6):.3f} MPa')

    print('\nTHRUST AND IMPULSE')
    print(f' Maximum, average thrust: {np.max(ib_parameters.T):.3f}, {ib_parameters.T_mean:.3f} N')
    print(f' Total, specific impulses: {ib_parameters.I_total:.3f} N-s, {ib_parameters.I_sp:.3f} s')
    print(f' Burnout time, thrust time: {ib_parameters.t_burnout:.3f}, {ib_parameters.t_thrust:.3f} s')

    print('\nNOZZLE DESIGN')
    print(f' Average opt. exp. ratio: {np.mean(ib_parameters.E_opt):.3f}')
    print(f' Nozzle exit diameter: {structure.D_throat * np.sqrt(np.mean(ib_parameters.E_opt)) * 1e3:.3f} mm')
    print(f' Average nozzle efficiency: {np.mean(ib_parameters.nozzle_eff) * 100:.3f} %')

    print('\nROCKET BALLISTICS')
    print(f' Apogee: {np.max(ballistics.y):.2f} m')
    print(f' Max. velocity: {np.max(ballistics.v):.2f} m/s')
    print(f' Max. Mach number: {np.max(ballistics.Mach):.3f}')
    print(f' Max. acceleration: {np.max(ballistics.acc) / 9.81:.2f} gs')
    print(f' Time to apogee: {ballistics.apogee_time:.2f} s')
    print(f' Velocity out of the rail: {ballistics.v_rail:.2f} m/s')
    print(f' Height at motor burnout: {ballistics.y_burnout:.2f} m')
    print(f' Flight time: {ballistics.flight_time:.2f} s')

    print('\nPRELIMINARY STRUCTURAL PROJECT')
    print(f' Casing safety factor: {structural_parameters.casing_sf:.2f}')
    print(f' Minimal nozzle convergent, divergent thickness: {structural_parameters.nozzle_conv_t * 1e3:.3f}, '
          f'{structural_parameters.nozzle_div_t * 1e3:.3f} mm')
    print(f' Minimal bulkhead thickness: {structural_parameters.bulkhead_t * 1e3:.3f} mm')
    print(f' Optimal number of screws: {structural_parameters.optimal_fasteners + 1:d}')
    print(f' Shear, tear, compression screw safety factors: '
          f'{structural_parameters.shear_sf[structural_parameters.optimal_fasteners]:.3f}, '
          f'{structural_parameters.tear_sf[structural_parameters.optimal_fasteners]:.3f}, '
          f'{structural_parameters.compression_sf[structural_parameters.optimal_fasteners]:.3f}')
    print('\nDISCLAIMER: values above shall not be the final dimensions.')
    print('Critical dimensions shall be investigated in depth in order to guarantee safety.')

    print('\n')


def output_eng_csv(ib_parameters, structure, propellant, eng_res, dt, manufacturer, name):
    """
    This program exports the motor data into three separate files.
    The .eng file is compatible with most rocket ballistic simulators such as openRocket and RASAero.
    The output .csv file contains thrust, time, propellant mass, Kn, chamber pressure, web thickness and burn rate data.
    The input .csv file contains all info used in the input section.
    """
    # Writing the ENG file:
    index = np.where(ib_parameters.t == ib_parameters.t_burnout)
    time = ib_parameters.t[: index[0][0]]
    thrust = ib_parameters.T[: index[0][0]]
    prop_vol = ib_parameters.V_prop[: index[0][0]]
    motor_to_eng(time, thrust, dt, prop_vol, structure.D_out, structure.L_chamber, eng_res, propellant.pp,
                 structure.m_motor, manufacturer, name)
    # Writing to output CSV file:
    motor_data = {'Time': time, 'Thrust': thrust, 'Prop_Mass': prop_vol * propellant.pp}
    motor_data_df = pd.DataFrame(motor_data)
    motor_data_df.to_csv(f'output/{name}.csv', decimal='.')
