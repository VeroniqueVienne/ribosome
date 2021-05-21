import numpy as np
import pandas as pd


'''fonction qui renvoie les particules qui sont toujours vivantes et celles qui présentent qu une rupture : our function!'''
def trace_selection(followed_ruptures,video,size,seuil):
    N = video.shape[0]
    moy=np.mean(video)
    ecarttype=np.std(video)

    df0 = pd.DataFrame(columns = ['particle', 'x','y','frame_break', 'mean_value_before_break', 'mean_value_after_break'])
    
    
    
    Nb_particles = max(followed_ruptures.particle) + 1
    i=0
    u=0
    j=0
    k=1
    epsilon1=0
    epsilon2=0
    
    for p in range(0,Nb_particles):
        t = followed_ruptures[followed_ruptures.particle==p]
        
        x = t['x'].mean()
        y = t['y'].mean()


        if len(t)==1:
            if (t[t.frame_break==N].mean_value_before_break >= seuil).bool():
                df1 = t.copy()
    
                u=df1.index.values.astype(int)[0]
    
                df0.loc[i,'particle'] = p
                df0.loc[i,'x']=df1.loc[u,'x']
                df0.loc[i,'y']=df1.loc[u,'y']
                df0.loc[i,'frame_break']=df1.loc[u,'frame_break']
                df0.loc[i,'mean_value_before_break']=df1.loc[u,'mean_value_before_break']
                df0.loc[i,'mean_value_after_break']=df1.loc[u,'mean_value_before_break']
                
                i=i+1
                j=j+1

                
                

        if len(t)==2: # 1 rupture
            t.mean_value_before_break = t.mean_value_before_break
            df1 = t[t.frame_break != N]
            #print((u))
            u=df1.index.values.astype(int)[0]
            df2=t[t.frame_break == N]
            
            if df2.loc[u+1,'mean_value_before_break'] < seuil:


    
                df0.loc[i,'particle'] = df1.loc[u,'particle']
                df0.loc[i,'x']=df1.loc[u,'x']
                df0.loc[i,'y']=df1.loc[u,'y']
                df0.loc[i,'frame_break']=df1.loc[u,'frame_break']
                df0.loc[i,'mean_value_before_break']=df1.loc[u,'mean_value_before_break']
                df0.loc[i,'mean_value_after_break']=df2.loc[u+1,'mean_value_before_break']
                epsilon1= abs(df0.loc[i,'mean_value_before_break']-seuil)
                epsilon2= abs(df0.loc[i,'mean_value_after_break']-moy)
                
                
                
                if (df0.loc[i,'mean_value_before_break'] >df0.loc[i,'mean_value_after_break'] )and (df0.loc[i,'mean_value_before_break'] > seuil) and (epsilon2<0.5*ecarttype) and(epsilon1>0.5*ecarttype):
                    i = i+1
                    k=k+1
                        

    return df0 ,j,k
