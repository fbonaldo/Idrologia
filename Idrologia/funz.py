import numpy as np

# Interpolazione

def valInt(X,Y,Xval):
    Yval=np.empty(len(Xval))
    dX=np.diff(X)
    dY=np.diff(Y)
    M=dY/dX
    M=np.append(M,M[-1])
    idx=np.digitize(Xval,X,right=True)
    for n,i in enumerate(idx):
        if i==0:
            i=1
        x=Xval[n]
        x0=X[i-1]
        y0=Y[i-1]
        m=M[i-1]
        y=y0+m*(x-x0)
        Yval[n]=y
    return Yval

# Tasso di ruscellamento a partire dalle precipitazioni cumulate

def R_calc(Tp,Pcum,deltaT,Z,Atot,Arel,Apioggia,Aneve=0,Zneve=None,Ztrans=None):
    #Uso la stessa campionatura di tempo dell'idrogramma di piena
    Tprec=np.arange(0,Tp[-1],deltaT/3600)
    Tprec=np.append(Tprec,Tp[-1])
    #Interpolazione
    P=valInt(Tp,Pcum,Tprec) #[mm]
    intP=np.diff(P)/deltaT #intensità di precipitazione[mm/s]
    
    #In base alla quota neve associo a ogni quota un suo coefficiente
    
    if Zneve is None: #solo pioggia
        Amedio=Apioggia
    else:
        ALFA=valInt([Z[0],Zneve,Zneve+Ztrans,Z[-1]],[Apioggia,Apioggia,Aneve,Aneve],Z)
        print("Alfa: ",ALFA)
        Adiff=np.diff(Arel) # area relativa per ogni intervallo di quota (la somma è 100)
        Amedio=np.dot(ALFA[1:],Adiff)/100 #media ponderata    
    R=Amedio*intP*Atot/1000 #[m^3/s]
    V_in=R.sum()*deltaT
    return Tprec,intP,R,Amedio,V_in

# Vettore portate turbinate come ieri

def TB_vett(inizio,fine,deltaT,lun):
    n=int(3600/deltaT)
    TB1=np.zeros(inizio*n)
    TB2=np.ones((fine-inizio)*n)
    TB3=np.zeros((24-fine)*n)
    TBg=np.concatenate((TB1,TB2,TB3))
    leng=len(TBg)
    while leng<lun:
        TBg=np.concatenate((TBg,TBg))
        leng=len(TBg)
    TB=TBg[:lun]
    return TB

# Caratteristiche grafici
    
def plotting(ax,val,xmin,xmax,xlab,ylab,txt):
    ax.axhline(val,linestyle='--',color='red',linewidth=2.5)
    ax.grid()
    ax.set_xticks(np.arange(xmin,xmax+1,6))
    ax.set_xlim([xmin,xmax])
    ax.set_xlabel(xlab,fontsize=15)
    ax.set_ylabel(ylab,fontsize=15)
    ax.legend(fontsize=15,loc='right')
    ax.annotate(txt,(0,val),xytext=(10,5),textcoords='offset points',color='red',fontsize=15)

