''' A crossfilter plot map that uses the `Auto MPG dataset`_. This example
demonstrates the relationship of datasets together. A hover tooltip displays
information on each dot.

.. note::
    This example needs the Pandas package to run.

.. _Auto MPG dataset: https://archive.ics.uci.edu/ml/datasets/auto+mpg

'''
#from mimetypes import init
import pandas as pd
import numpy as np
from bokeh.layouts import column, row
from bokeh.models import Select, HoverTool, ColumnDataSource, Slider, Range1d
from bokeh.palettes import Spectral5
from bokeh.plotting import curdoc, figure
import modules.read_mist_models as md
import glob


def eep_to_df(i):
    '''
    Reading the eep data from the grid
    Changing data from eep to pandas dataframe
    '''
    track_list = glob.glob('./app/data/*.track.eep')
    track_path = track_list[0]
    print('p1',track_path)
    print('p2',i)
    eep = md.EEP(i)
    initial_mass = eep.minit
    ees = eep.eeps
    #usable_data
    df = pd.DataFrame(ees['star_age'],columns=['age'])
    df['age'] = df.age/1.e9
    df['logg'] = ees['log_g']
    df['teff'] = 10.**ees['log_Teff']
    #df['phase'] = ees['phase']
    #df['center_h1'] = ees['center_h1']
    #df['center_he4'] = ees['center_he4']
    #df['center_c12'] = ees['center_c12']
    #df['radius'] = 10.**ees['log_R']
    #df['center_T'] = 10.**ees['log_center_T']
    #df['center_Rho'] = 10.**ees['log_center_Rho']
    #df['center_degeneracy'] = ees['center_degeneracy']  
    #chainging phase to evolution
    evphase0=np.zeros(1)
    for i in ees['phase']:
        if i==-1: evphase = 'Pre_MS'
        elif i==0: evphase ='MS'
        elif i==2: evphase ='SGB+RGB'
        elif i==3: evphase = 'CHeB'
        elif i==4: evphase = 'EAGB'
        elif i==5: evphase = 'TPAGB'
        elif i==6: evphase = 'post_AGB'
        elif i==9: evphase ='WR'
        evphase0 = np.vstack((evphase0,evphase))
    df['evphase'] = evphase0[1:]
    print(df)
    #return df


    #track_list = glob.glob('./myapp/data/evtrack_grid/*.track.eep')
    #print(track_list[0])
    #df = eep_to_df(track_list[0])
    df = df.copy()

    SIZES = list(range(6, 22, 3))
    COLORS = Spectral5
    N_SIZES = len(SIZES)
    N_COLORS = len(COLORS)

    # data cleanup
    #df.age = df.age.astype(str)
    #df.teff = df.teff.astype(str)
    #df.logg = df.logg.astype(str)
    #del df['evphase']

    columns = sorted(df.columns)
    print(columns)
    discrete = [x for x in columns if df[x].dtype == object]
    continuous = [x for x in columns if x not in discrete]
    return columns, continuous, discrete, df

def create_new_figure():
    columns, continuous, discrete, df = eep_to_df(track.value)
    df = df.sort_values(by='age')
    sample1 = df.sample(np.shape(df)[0]) 
    source1 = ColumnDataSource(sample1)
    #xs = df[x.value].values
    #ys = df[y.value].values
    x_title = x.value.title()
    y_title = y.value.title()

    #kw = dict()
    #if x.value in discrete:
    #    kw['x_range'] = sorted(set(xs))
    #if y.value in discrete:
    #    kw['y_range'] = sorted(set(ys))
    #kw['title'] = "%s vs %s" % (x_title, y_title)
    TOOLS = "pan,wheel_zoom,box_zoom,reset,tap"

    p = figure(height=600, width=800, tools=TOOLS)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    '''
    if x.value in discrete:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        if len(set(df[size.value])) > N_SIZES:
            groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
        else:
            groups = pd.Categorical(df[size.value])
        sz = [SIZES[xx] for xx in groups.codes]

    c = "#31AADE"
    if color.value != 'None':
        if len(set(df[color.value])) > N_COLORS:
            groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
        else:
            groups = pd.Categorical(df[color.value])
        c = [COLORS[xx] for xx in groups.codes]
    '''
    age_slider.value

    p.circle(x.value, y.value, source=source1, color='blue', size=5, line_color="white", alpha=0.6,name='trackplt')
    #p.circle(x=xs, y=ys, color='blue', size=5, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
    p.x_range = Range1d(age_slider.value-0.1,float(age_slider.value)+0.1)

    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    p.add_tools(HoverTool(names=['trackplt'],tooltips=tooltips1))

    return p


def update_data(attr, old, new):
    print(attr,old,new)
    layout.children[1] = create_new_figure()

# start
track_list = glob.glob('./app/data/*.track.eep')
columns, continuous, discrete, df = eep_to_df(track_list[0])


#track side menu
track = Select(title='Track', value=track_list[0], options=track_list)
track.on_change('value', update_data)

# side menu
x = Select(title='X-Axis', value='teff', options=columns)
x.on_change('value', update_data)

y = Select(title='Y-Axis', value='logg', options=columns)
y.on_change('value', update_data)

age_slider = Slider(title="Age slider", start=0, end=3, value=0.5, step=0.05)
age_slider.on_change('value', update_data)


#size = Select(title='Size', value='None', options=['None'] + continuous)
#size.on_change('value', update_data)

#color = Select(title='Color', value='None', options=['None'] + continuous)
#color.on_change('value', update_data)

controls = column(track,x, y,age_slider, width=200)
layout = row(controls, create_new_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"
