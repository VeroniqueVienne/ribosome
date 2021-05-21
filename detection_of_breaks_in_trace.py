import numpy as np
import pandas as pd
import ruptures as rp
import matplotlib.pyplot as plt



def breaks_in_trace(FILENAME,followed_particles,video,THRESHOLD = 0.5):
    
    
    n_frames = video.shape[0]
    Nb_particles = max(followed_particles.particle)+1

    df0= pd.DataFrame(columns = ['particle', 'x','y','frame_break', 'mean_value_before_break'])
    
    #followed_particles['mean_value']=0
 
    for p in range(Nb_particles):
        
        t = followed_particles[followed_particles.particle==p]
        x = t['x'].mean()
        y = t['y'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        signal = t.signal.to_numpy()
        mean_signal = np.zeros(n_frames, dtype=signal.dtype)
        
       
        model="l2"
       
        algo = rp.Binseg(model=model,min_size=3,jump=1).fit(signal)
        ax.plot(signal, "*-", alpha=0.5)
        
        ax.set_xlim(0, signal.size)

        n_bkps_max = 7
        
        algo.predict(n_bkps=n_bkps_max)
        cost_list = [1]
        c_0 = algo.cost.sum_of_costs([signal.size])
        for n_bkps in range(1, n_bkps_max + 1):
            my_bkps = algo.predict(n_bkps=n_bkps)
            cost_list.append(algo.cost.sum_of_costs(my_bkps) / c_0)
    
        cost_gain_list = -np.diff(cost_list)
        if cost_gain_list.max() < THRESHOLD:
            n_bkps_estimated = 0
        else:
            n_bkps_estimated = [
                k
                for (k, cost_value) in enumerate(-np.diff(cost_list), start=1)
                if cost_value > THRESHOLD
            ][-1]
    
        my_bkps = algo.predict(n_bkps=n_bkps_estimated)
        for (start, end) in rp.utils.pairwise([0] + my_bkps):
            mean_signal[start:end] = signal[start:end].mean()
        ax.plot(mean_signal, "--")
        
        


        i = 0
        for xrupt in my_bkps:
            mean = np.average(signal[i:xrupt])


            df1 = pd.DataFrame({'particle':[p], 'x':[x],'y':[y],'frame_break':[xrupt],'mean_value_before_break':[mean]})
            mean_signal[i:xrupt]=mean
            i=xrupt
            df0 = pd.concat([df0,df1],ignore_index = True)
            
        if len(my_bkps) == 1:

        
            title_msg = (
                f"Particle {p}: {n_bkps_estimated} changes (frames {my_bkps[:-1]})"
            )
            ax.set_title(title_msg)
    
            plt.savefig(
                f"{FILENAME.split('.')[0]}/keep0/particle-{p}-{model.upper()}.png"
            )
            plt.close()
    
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(range(1, n_bkps_max + 1), -np.diff(cost_list), "-*")
            ax.set_ylim(0, 1.2)
            ax.axhline(THRESHOLD, color="k", ls="--")
            ax.set_title(title_msg)
    
            plt.savefig(
                f"{FILENAME.split('.')[0]}/keep0/particle-{p}-{model.upper()}-cost.png"
            )
            plt.close()
                
        if len(my_bkps) == 2:
        

            title_msg = (
                f"Particle {p}: {n_bkps_estimated} changes (frames {my_bkps[:-1]})"
            )
            ax.set_title(title_msg)
    
            plt.savefig(
                f"{FILENAME.split('.')[0]}/keep1/particle-{p}-{model.upper()}.png"
            )
            plt.close()
    
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(range(1, n_bkps_max + 1), -np.diff(cost_list), "-*")
            ax.set_ylim(0, 1.2)
            ax.axhline(THRESHOLD, color="k", ls="--")
            ax.set_title(title_msg)
    
            plt.savefig(
                f"{FILENAME.split('.')[0]}/keep1/particle-{p}-{model.upper()}-cost.png"
            )
            plt.close()
    
            
            

    return df0


