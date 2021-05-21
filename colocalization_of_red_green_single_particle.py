import numpy as np
import pandas as pd



def colocalization(dfr,dfg,radius=3):
    df = pd.DataFrame(columns = ['particle','color', 'x','y'])
    dfr1= pd.DataFrame(columns = ['particle','color', 'x','y'])
    dfg1=pd.DataFrame(columns = ['particle','color', 'x','y'])
    i = 0
    for itemr,rowr in dfr.iterrows(): #each line is a different fluorophore
        xr = dfr.loc[itemr,'x']
        #print(xr)
        yr = dfr.loc[itemr,'y']
        #print(yr)
        dftest = dfg.copy()
        dftest.x =((dfg.x-xr)**2 + (dfg.y-yr)**2)**(0.5)
        #0print(dftest.x)
        for itemg,rowg in dftest.iterrows():
            if (dftest.loc[itemg,'x']<radius):
                df.loc[i,'particle'] = dfr.loc[itemr,'particle']-1
                df.loc[i,'color'] = 'red'
                df.loc[i,'x'] = dfr.loc[itemr,'x']
                df.loc[i,'y'] = dfr.loc[itemr,'y']
                
                
                
                df.loc[i+1,'particle'] = dfg.loc[itemg,'particle']-1
                df.loc[i+1,'color'] = 'green'
                df.loc[i+1,'x'] = dfg.loc[itemg,'x']
                df.loc[i+1,'y'] = dfg.loc[itemg,'y']
           
                
                           
            
                dfr1.loc[i]=df.loc[i]
                dfg1.loc[i]=df.loc[i+1]
                i = i+2
                
    print('percentage of colocalization for red particles=', len(dfr1)/len(dfr)*100,"%")
    print('percentage of colocalization for green particles=', len(dfg1)/len(dfg)*100 ,"%")
    #return df,dfr1, dfg1


def colocalization_codepart(dfr,dfg,radius,Nbframe):
    df = pd.DataFrame(columns = ['particle','color', 'x','y','frame_break', 'mean_value_before_break','Dt'])
    dfr1= pd.DataFrame(columns = ['particle','color', 'x','y','frame_break', 'mean_value_before_break','Dt'])
    dfg1=pd.DataFrame(columns = ['particle','color', 'x','y','frame_break', 'mean_value_before_break','Dt'])
    i = 0
    for itemr,rowr in dfr.iterrows(): #each line is a different fluorophore
        xr = dfr.loc[itemr,'x']
        #print(xr)
        yr = dfr.loc[itemr,'y']
        #print(yr)
        dftest = dfg.copy()
        dftest.x =((dfg.x-xr)**2 + (dfg.y-yr)**2)**(0.5)
        #0print(dftest.x)
        for itemg,rowg in dftest.iterrows():
            if (dftest.loc[itemg,'x']<radius):
                df.loc[i,'particle'] = dfr.loc[itemr,'particle']-1
                df.loc[i,'color'] = 'red'
                df.loc[i,'x'] = dfr.loc[itemr,'x']
                df.loc[i,'y'] = dfr.loc[itemr,'y']
                df.loc[i,'frame_break'] = dfr.loc[itemr,'frame_break']
                df.loc[i,'Dt'] = dfr.loc[itemr,'frame_break']-dfg.loc[itemg,'frame_break']
                df.loc[i,'mean_value_before_break'] = dfr.loc[itemr,'mean_value_before_break']
                
                
                df.loc[i+1,'particle'] = dfg.loc[itemg,'particle']-1
                df.loc[i+1,'color'] = 'green'
                df.loc[i+1,'x'] = dfg.loc[itemg,'x']
                df.loc[i+1,'y'] = dfg.loc[itemg,'y']
                df.loc[i+1,'frame_break'] = dfg.loc[itemg,'frame_break']
                df.loc[i+1,'Dt'] = dfg.loc[itemg,'frame_break']-dfr.loc[itemr,'frame_break']
                df.loc[i+1,'mean_value_before_break'] = dfg.loc[itemg,'mean_value_before_break']
                
                           
                if df.loc[i,'frame_break']==Nbframe or df.loc[i+1,'frame_break']==Nbframe:
                    df.loc[i,'Dt'] = Nbframe+1
                    df.loc[i+1,'Dt'] = Nbframe+1
                dfr1.loc[i]=df.loc[i]
                dfg1.loc[i]=df.loc[i+1]
                i = i+2
    return df,dfr1, dfg1