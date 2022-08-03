import numpy as np
import pandas as pd
import glob
import modules.read_mist_models as md

def eep_to_df(track_path):
    eep = md.EEP(track_path)
    initial_mass = eep.minit
    ees = eep.eeps
    #usable_data
    df = pd.DataFrame(ees['star_age'],columns=['age'])
    df['age'] = df.age/1.e9
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
    return df
    exit()

    df = df.sort_values(by='age')
    sample1 = df.sample(np.shape(df)[0]) 
    source1 = ColumnDataSource(sample1)

    TOOLS = "pan,wheel_zoom,box_zoom,reset,tap"
    cpal = ['#000000','#6B6969','#00ffff','#aaff00','#FFFF00'] #bluegrass

    #AGE-PHASE
    s1 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
    s1.xgrid.grid_line_alpha = 0.2
    s1.ygrid.grid_line_alpha = 0.2
    t1 = Title()
    t1.text = 'Evolutionary track, Initial mass : '+str(initial_mass)+' Msun'
    s1.title = t1
    hrd = s1.circle('teff','logg', source=source1, size=5, color=cpal[2], alpha=1.0,name='hrd',legend_label='hrd')
    hrd = s1.line(df.teff,df.logg)

    s1.y_range.flipped = True
    s1.x_range.flipped = True
    s1.xaxis.axis_label = 'Teff'
    s1.yaxis.axis_label = 'logg'
    hrd.visible = True
    s1.legend.location = "top_left"
    s1.legend.click_policy="hide"
    s1.legend.background_fill_alpha=0
    s1.legend.border_line_alpha=0
    s1.legend.label_text_color = "white"
    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    s1.add_tools(HoverTool(names=['hrd'],tooltips=tooltips1))

    #AGE-ABUNDANCE
    s2 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
    s2.xgrid.grid_line_alpha = 0.2
    s2.ygrid.grid_line_alpha = 0.2
    t2 = Title()
    t2.text = 'Age - Central abundance'
    s2.title = t2
    age_center_h1 = s2.circle('age','center_h1', source=source1, size=5, color=cpal[2], alpha=1.0,name='age_center_h1',legend_label='age_center_h1')
    age_center_h1 = s2.line(df.age,df.center_h1)

    age_center_he4 = s2.circle('age','center_he4', source=source1, size=5, color=cpal[3], alpha=1.0,name='age_center_he4',legend_label='age_center_he4')
    age_center_he4 = s2.line(df.age,df.center_he4)

    age_center_c12 = s2.circle('age','center_c12', source=source1, size=5, color=cpal[4], alpha=1.0,name='age_center_c12',legend_label='age_center_c12')
    age_center_c12 = s2.line(df.age,df.center_c12)

    s2.xaxis.axis_label = 'Age'
    s2.yaxis.axis_label = 'Abundance'
    age_center_h1.visible = True
    s2.legend.location = "top_left"
    s2.legend.click_policy="hide"
    s2.legend.background_fill_alpha=0
    s2.legend.border_line_alpha=0
    s2.legend.label_text_color = "white"
    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    s2.add_tools(HoverTool(names=['age_center_h1','age_center_he4','age_center_c12'],tooltips=tooltips1))

    #AGE-STRUCTURE
    s3 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
    s3.xgrid.grid_line_alpha = 0.2
    s3.ygrid.grid_line_alpha = 0.2
    t3 = Title()
    t3.text = 'Age - STRUCTURE'
    s3.title = t3
    age_structure = s3.circle('age','radius', source=source1, size=5, color=cpal[2], alpha=1.0,name='age_structure',legend_label='age_structure')
    age_structure = s3.line(df.age,df.radius)
    s3.xaxis.axis_label = 'Age'
    s3.yaxis.axis_label = 'Radius'
    age_structure.visible = True
    s3.legend.location = "top_left"
    s3.legend.click_policy="hide"
    s3.legend.background_fill_alpha=0
    s3.legend.border_line_alpha=0
    s3.legend.label_text_color = "white"
    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    s3.add_tools(HoverTool(names=['age_structure'],tooltips=tooltips1))

    #central T Rho
    s4 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
    s4.xgrid.grid_line_alpha = 0.2
    s4.ygrid.grid_line_alpha = 0.2
    t4 = Title()
    t4.text = 'Central T - density'
    s4.title = t4
    s4_1 = s4.circle('center_T','center_Rho', source=source1, size=5, color=cpal[2], alpha=1.0,name='T_Rho',legend_label='center_T_Rho')
    s4_1 = s4.line(df.center_T,df.center_Rho)
    s4.xaxis.axis_label = 'center_T'
    s4.yaxis.axis_label = 'center_Rho'

    s4_1.visible = True
    s4.legend.location = "top_left"
    s4.legend.click_policy="hide"
    s4.legend.background_fill_alpha=0
    s4.legend.border_line_alpha=0
    s4.legend.label_text_color = "white"
    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    s4.add_tools(HoverTool(names=['T_Rho'],tooltips=tooltips1))

    #degeneracy - age
    s5 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
    s5.xgrid.grid_line_alpha = 0.2
    s5.ygrid.grid_line_alpha = 0.2
    t5 = Title()
    t5.text = 'Degneracy - Rho'
    s5.title = t5
    s5_1 = s5.circle('center_degeneracy','center_Rho', source=source1, size=5, color=cpal[2], alpha=1.0,name='deg_Rho',legend_label='degeneracy_Rho')
    s5_1 = s5.line(df.center_degeneracy,df.center_Rho)
    s5.xaxis.axis_label = 'center_degeneracy'
    s5.yaxis.axis_label = 'center_Rho'

    s5_1.visible = True
    s5.legend.location = "top_left"
    s5.legend.click_policy="hide"
    s5.legend.background_fill_alpha=0
    s5.legend.border_line_alpha=0
    s5.legend.label_text_color = "white"
    tooltips1 = [('Age ','@age'),('Phase ','@evphase')]
    s5.add_tools(HoverTool(names=['deg_Rho'],tooltips=tooltips1))


    #sourceTableSummary1 = ColumnDataSource(dv0)
    formatter =  HTMLTemplateFormatter()
    Columns1 = [TableColumn(field=colIndex, title=colIndex, formatter=formatter) for colIndex in df.columns] 
    data_table1 = DataTable(columns=Columns1, source=source1, index_position = 0, width=700, height=700,selectable=True,editable=True,fit_columns=False) 

    l = layout([[s1,s2,s3],[s4,s5,data_table1]], sizing_mode='stretch_both')

    show(l)


track_list = glob.glob('data\evtrack_grid\*.track.eep')
for i in track_list:
    evtrack_gen(i)


exit()
#######################################################
## MODEL
#######################################################
df = pd.read_csv('all_errgbr_datamsrgbrc_run1/all_errgbr_datamsrgbrc_run1.csv') #gmagw parallel
#age,feh,mM,ex,s,chisq
df_chimin = df[df.chisq==df.chisq.min()]
df_smin = df[df.s==df.s.min()]
#print('S',df_smin)
#print('chsq',df_chimin)

df_best = df.sort_values('s')
df_best['s'] = df_best.s - np.min(df_best.s) 
print('Relative goodness : ',np.min(df_best.s)-np.max(df_best.s))
df_best = df_best.reset_index()


df_best = df_best[:3]
print('MS + RGB + RC - G magnitude error * BP-RP error')
print('================================================')
print(df_best)

##############
# HR
##############


#data
dv = pd.read_csv('data/NGC6819.csv') 
dv0 = dv[dv['Teff'].notna()]
dv0 = dv0[dv0['logg'].notna()]
ta = np.zeros(1)
ta_er = np.zeros(1) 
la = np.zeros(1)
la_er = np.zeros(1)
for i in dv0.ID:
    dv1 = dv0[dv0.ID==i]

    ta = np.vstack((ta,float(dv1.Teff.values[0][:dv1.Teff.values[0].find('(')])))
    ta_er = np.vstack((ta_er,float(dv1.Teff.values[0][dv1.Teff.values[0].find('(')+1:dv1.Teff.values[0].find(')')])))

    la = np.vstack((la,float(dv1.logg.values[0][:dv1.logg.values[0].find('(')])))
    la_er = np.vstack((la_er,float(dv1.logg.values[0][dv1.logg.values[0].find('(')+1:dv1.logg.values[0].find(')')])))
    
dv0['tf']=ta[1:]
dv0['tf_er']=ta_er[1:]
dv0['lg']=la[1:]
dv0['lg_er']=la_er[1:]


dngc0 = dv0[dv0.MEMBER=='cluster']
dngc1 = dv0[dv0.MEMBER=='field']

Av = 0.382 # extintion
mM = 12.198 # 13.35 Antony Twarog 2006
#distance modulus from parallax of 2400 and extintion
#mM = 5*np.log10(2400)-5+Av
ex = 0.191 # 0.09

dfeh=0.01
fh =-0.02
for i in range(3):
    #print(i)
    fh = fh + 0.01
    df_best = df[(df.age==9.40)&(df.feh==np.round(fh,3))]
    df_best = df_best.reset_index()
    print(fh)
    print(df_best)
    isocmd = read_mist_models.ISOCMD('grid/MIST_iso_feh'+f'{df_best.feh[0]:0.2f}'+'_av0.00_vvcrit0.0.iso.cmd')
    age_ind = isocmd.age_index(df_best.age[0]) 
    isocmd0 = isocmd.isocmds[age_ind]
    logTeff = isocmd0['log_Teff'] 
    logg = isocmd0['log_g'] 

    G = isocmd0['Gaia_G_EDR3'] + mM
    BP = isocmd0['Gaia_BP_EDR3']
    RP = isocmd0['Gaia_RP_EDR3']
    BPRP = BP-RP + ex


sample1 = dngc0.sample(np.shape(dngc0)[0]) #FOV
source1 = ColumnDataSource(sample1)

sample2 = dngc1.sample(np.shape(dngc1)[0]) #FOV
source2 = ColumnDataSource(sample2)



TOOLS = "pan,wheel_zoom,box_zoom,reset,tap"
cpal = ['#000000','#6B6969','#00ffff','#aaff00'] #bluegrass


#CMD
s1 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
s1.xgrid.grid_line_alpha = 0.2
s1.ygrid.grid_line_alpha = 0.2

t1 = Title()
t1.text = 'CMD - NGC6819, Isochrone - Age : 2.51Gyr,  [Fe/H] : 0.01,  (m-M) : 12.19, E(BP-RP) : 0.22'
s1.title = t1

ngc_vstar = s1.circle('BP_RP','GMAG', source=source1, size=5, color=cpal[2], alpha=1.0,name='ngc',legend_label='cl*')
ngc_field = s1.circle('BP_RP','GMAG', source=source2, size=5, color=cpal[3], alpha=1.0,name='ngc',legend_label='field*')
iso = s1.line(BPRP,G,color='snow',legend_label='ischrone')
s1.xaxis.axis_label = 'BP-RP'
s1.yaxis.axis_label = 'G'
s1.y_range.flipped = True
s1.x_range.flipped = True
s1.x_range=Range1d(0, 2.4)
s1.y_range=Range1d(20, 10)

ngc_field.visible = False
ngc_vstar.visible = True
iso.visible = True


s1.legend.location = "top_left"
s1.legend.click_policy="hide"
s1.legend.background_fill_alpha=0
s1.legend.border_line_alpha=0
s1.legend.label_text_color = "white"


tooltips1 = [('ID ','@ID'),('Memb ','@MEMBER'),('Type ', '@VARIABILITY_TYPE'),('CMD ','@CMD'),('Spec ','@USED_SPEC')]
s1.add_tools(HoverTool(names=['ngc'],tooltips=tooltips1))


#HRD
s2 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
s2.xgrid.grid_line_alpha = 0.2
s2.ygrid.grid_line_alpha = 0.2

t2 = Title()
t2.text = 'Teff-logg - NGC6791, Isochrone - Age : 2.51Gyr,  [Fe/H] : 0.01'
s2.title = t2

#ngc_memb = s2.circle('dr2_rv_template_teff','dr2_rv_template_logg', source=source2, size=7, color=cpal[1], alpha=0.5,legend_label='gaia_teff_logg')
ngc_vstar = s2.circle('tf','lg', source=source1, size=5, color=cpal[2], alpha=1.0,name='ngc',legend_label='cl*')
ngc_field = s2.circle('tf','lg', source=source2, size=5, color=cpal[3], alpha=1.0,name='ngc',legend_label='field*')
iso = s2.line(10.**logTeff,logg,color='snow',legend_label='ischrone')
s2.xaxis.axis_label = 'Teff'
s2.yaxis.axis_label = 'logg'
s2.y_range.flipped = True
s2.x_range.flipped = True
s2.x_range=Range1d(10000,2500)
s2.y_range=Range1d(5.5, 1.4)

ngc_field.visible = False
ngc_vstar.visible = True
iso.visible = True


s2.legend.location = "top_left"
s2.legend.click_policy="hide"
s2.legend.background_fill_alpha=0
s2.legend.border_line_alpha=0
s2.legend.label_text_color = "white"

tooltips1 = [('ID ','@ID'),('Memb ','@MEMBER'),('Type ', '@VARIABILITY_TYPE'),('CMD ','@CMD'),('Spec ','@USED_SPEC')]
s2.add_tools(HoverTool(names=['ngc','field'],tooltips=tooltips1))

#sourceTableSummary1 = ColumnDataSource(dv0)
formatter =  HTMLTemplateFormatter()
Columns1 = [TableColumn(field=colIndex, title=colIndex, formatter=formatter) for colIndex in dngc0.columns] 
data_table1 = DataTable(columns=Columns1, source=source1, index_position = 0, width=700, height=700,selectable=True,editable=True,fit_columns=False) 


#sourceTableSummary1 = ColumnDataSource(dv)
formatter =  HTMLTemplateFormatter()
Columns2 = [TableColumn(field=colIndex, title=colIndex, formatter=formatter) for colIndex in dngc1.columns] 
data_table2 = DataTable(columns=Columns2, source=source2, index_position = 0, width=700, height=700,selectable=True,editable=True,fit_columns=False) 

l = layout([[s1,s2],[data_table1,data_table2]], sizing_mode='stretch_both')

show(l)

exit()

#Bokeh plots
sample1 = dfov.sample(np.shape(dfov)[0]) #FOV
source1 = ColumnDataSource(sample1)

sample2 = dngc.sample(np.shape(dngc)[0]) #almost certain members
source2 = ColumnDataSource(sample2)

sample3 = dvngc.sample(np.shape(dvngc)[0]) #variable almost certain members
source3 = ColumnDataSource(sample3)

sample4 = dvfield.sample(np.shape(dvfield)[0]) #variable almost certain members
source4 = ColumnDataSource(sample4)

TOOLS = "pan,wheel_zoom,box_zoom,reset,tap"

cpal = ['#000000','#6B6969','#00ffff','#aaff00'] #bluegrass

#CMD
s2 = figure(plot_width=700, plot_height=700,background_fill_color=cpal[0],tools=TOOLS)
s2.xgrid.grid_line_alpha = 0.2
s2.ygrid.grid_line_alpha = 0.2
ngc_memb = s2.circle('bp_rp','phot_g_mean_mag', source=source2, size=7, color=cpal[1], alpha=0.5,legend_label='Cluster Members')
ngc_vstar = s2.circle('BP_RP','GMAG', source=source3, size=5, color=cpal[2], alpha=1.0,name='ngc',legend_label='Solar-like Members')
ngc_vfield = s2.circle('BP_RP','GMAG', source=source4, size=5, color=cpal[3], alpha=1.0,name='field',legend_label='Solar-like Field') 

age_gyr = 10**(age-9)
iso = s2.line(BP-RP+ex,G+mM,color='snow',legend_label='ISO '+str(np.round(age_gyr,2))+' Gyr')

labels1 = LabelSet(x='BP_RP', y='GMAG', text='ID',text_font_size="11px",text_color='#999999',x_offset=5, y_offset=5, source=source3)
labels2 = LabelSet(x='BP_RP', y='GMAG', text='ID',text_font_size="11px",text_color='#999999',x_offset=5, y_offset=5, source=source4)



l1 = s2.add_layout(labels1)
l2 = s2.add_layout(labels2)

labels1.visible = True
labels2.visible = True
ngc_memb.visible = True
ngc_vstar.visible = True
ngc_vfield.visible = True
iso.visible = True

s2.legend.location = "top_left"
s2.legend.click_policy="hide"
s2.legend.background_fill_alpha=0
s2.legend.border_line_alpha=0
s2.legend.label_text_color = "white"

s2.xaxis.axis_label = 'BP-RP'
s2.yaxis.axis_label = 'G'
t2 = Title()
t2.text = 'CMD - Solar-like stars in NGC6791           ( Use exploration tools on the right)'
s2.title = t2
s2.y_range.flipped = True
s2.x_range=Range1d(-0.5, 4.5)
s2.y_range=Range1d(20, 10)
tooltips1 = tooltips1 = [('ID','@ID'),('NAME : ', '@NAME')]
s2.add_tools(HoverTool(names=['ngc','field'],tooltips=tooltips1))

l = layout([[s2]], sizing_mode='stretch_both')

#l = layout([[s1,s2,s3]], sizing_mode='stretch_both')

show(l)

