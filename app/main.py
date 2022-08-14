
import pandas as pd
import numpy as np
from bokeh.layouts import column, row, layout
from bokeh.models import Select, HoverTool, ColumnDataSource, Div, TextInput
#from bokeh.palettes import Spectral5
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
    j = './app/data/'+i+'M.track.eep'
    print(j)
    eep = md.EEP(j)
    initial_mass = eep.minit
    ees = eep.eeps
    #usable_data
    df = pd.DataFrame(ees['star_age'],columns=['age'])
    df['age'] = df.age/1e9
    df['logg'] = ees['log_g']
    df['teff'] = 10.**ees['log_Teff']
    df['phase'] = ees['phase']
    df['center_h1'] = ees['center_h1']
    df['center_he4'] = ees['center_he4']
    df['center_c12'] = ees['center_c12']
    df['radius'] = 10.**ees['log_R']
    df['center_T'] = 10.**ees['log_center_T']
    df['center_Rho'] = 10.**ees['log_center_Rho']
    df['center_degeneracy'] = ees['center_degeneracy']  
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

    #SIZES = list(range(6, 22, 3))
    #COLORS = Spectral5
    #N_SIZES = len(SIZES)
    #_COLORS = len(COLORS)

    # data cleanup
    #df.age = df.age.astype(str)
    #df.teff = df.teff.astype(str)
    #df.logg = df.logg.astype(str)
    #del df['evphase']

    columns = sorted(df.columns)
    print(columns)
    discrete = [x for x in columns if df[x].dtype == object]
    continuous = [x for x in columns if x not in discrete]
    return columns, continuous, discrete, initial_mass, df

def create_new_figure():
    columns, continuous, discrete, initial_mass, df = eep_to_df(track.value)
    #df = df.sort_values(by='age')
    sample1 = df.sample(np.shape(df)[0]) 
    source1 = ColumnDataSource(sample1)
    x1_title = x1.value.title()
    y1_title = y1.value.title()
    x2_title = x2.value.title()
    y2_title = y2.value.title()

    #age_indicator
    agedif = abs(df.age-float(age_input.value))
    aid = np.where(agedif==np.min(agedif))
    print(aid,min(df.age.values),max(df.age.values),age_input.value)
    xs1 = df[x1.value].values[aid]
    ys1 = df[y1.value].values[aid]
    xs2 = df[x2.value].values[aid]
    ys2 = df[y2.value].values[aid]

    TOOLS = "pan,box_select,wheel_zoom,box_zoom,reset,tap"
    #plot1
    p1 = figure(height=600, width=800, background_fill_color='black', tools=TOOLS)
    p1.xaxis.axis_label = x1_title
    p1.yaxis.axis_label = y1_title
    p1.circle(x1.value, y1.value, source=source1, color='cyan',selection_color="red", size=5, alpha=0.6,name='trackplt1')
    p1.circle(xs1, ys1, color='red', size=10)
    if((x1.value=='teff')&(y1.value=='logg')):
        p1.y_range.flipped = True
        p1.x_range.flipped = True
    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    p1.add_tools(HoverTool(names=['trackplt1'],tooltips=tooltips1))
    p1.title = x1.value +" vs "+ y1.value
    
    #plot2
    p2 = figure(height=600, width=800, background_fill_color='black', tools=TOOLS)
    p2.xaxis.axis_label = x2_title
    p2.yaxis.axis_label = y2_title
    p2.circle(x2.value, y2.value, source=source1, color='cyan',selection_color="red", size=5, alpha=0.6,name='trackplt2')
    p2.circle(xs2, ys2, color='red', size=10)
    if((x2.value=='teff')&(y2.value=='logg')):
        p2.y_range.flipped = True
        p2.x_range.flipped = True
    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    p2.add_tools(HoverTool(names=['trackplt2'],tooltips=tooltips1))
    p2.title = x2.value +" vs "+ y2.value
    
    return row(p1, p2)


def update_data(attr, old, new):
    print(attr,old,new)
    ui.children[1] = create_new_figure()



# Program start
track_list = glob.glob('./app/data/*.track.eep')

#making initial mass list from track list
ls0=[]
for ls in track_list:
    lsi, lsf = ls.find('data/'), ls.find('M')
    ls0.append(str(ls[lsi+5:lsf]))  

columns, continuous, discrete, initial_mass, df = eep_to_df(ls0[0])

track = Select(title='Initial Mass (* 0.0001 Msun)', value=ls0[0], options=ls0)
track.on_change('value', update_data)

#track side menu
#track = Select(title='Track', value=track_list[0], options=track_list)
#track.on_change('value', update_data)

# side menu
x1 = Select(title='X1-Axis', value='teff', options=columns)
x1.on_change('value', update_data)

y1 = Select(title='Y1-Axis', value='logg', options=columns)
y1.on_change('value', update_data)

x2 = Select(title='X2-Axis', value='age', options=columns)
x2.on_change('value', update_data)

y2 = Select(title='Y2-Axis', value='center_h1', options=columns)
y2.on_change('value', update_data)

age_input = TextInput(title="Input age(Gyr)",value="2.5") 
age_input.on_change('value', update_data)
    
div = Div(text=""" 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {
             background:black;
             color:white;
     }
    </style>
</head>
<body>
 <div class="p-5 text-dark-center text"> 
 <h1>Modules and Experiments in Stellar Astrophysics (MESA)</h1>
 <h3> MESA Isochrones and Stellar Tracks (MIST)</h3>
 </div>
""",sizing_mode="stretch_width")

controls = column(track,x1, y1,x2,y2,age_input, width=300)
ui = row(controls, create_new_figure())
#curdoc().add_root(layout)
plot = create_new_figure()
l = layout([div],[ui])
curdoc().add_root(l)
#curdoc().title = "Evolutionary tracks"
