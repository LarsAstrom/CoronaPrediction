#Parameters that do not change
days = 300
pop = 1.377e6
a_weight = 0.8
#K*gamma = 3

#Parameters that do change (possible values in list)
beta_list  = [i*1e-8 for i in range(10,30)]
gamma_list = [i*1e-4 for i in range(6,21)]
L_list = [i for i in range(3,13)]
alpha_list = [i*1e-4 for i in range(1,11)]
K_gamma_list = [i*0.1 for i in range(10,105,5)]

'''
Help functions
'''
def read_input(input_file='input_data/input.csv'):
    f = open(input_file,'r')
    content = f.read().strip().split('\n')
    a_inp = list(map(float,content[0].split(';')))
    d_inp = list(map(float,content[1].split(';')))
    days_inp = len(a_inp)
    assert len(a_inp) == len(d_inp), 'Unequal length of deaths and sick people in input.'
    f.close()
    return a_inp,d_inp

def plot(i,d,s,r,a,a_inp,d_inp):
    import matplotlib.pyplot as plt
    plt.figure()
    plt.semilogy(i,label='Immuna')
    plt.semilogy(d,label='Döda')
    plt.semilogy(s,label='Sjuka')
    plt.semilogy(r,label='Risk')
    plt.semilogy(a,label='Inlagda')
    plt.semilogy(a_inp,label='Inladga, verklig data')
    plt.semilogy(d_inp,label='Döda, verklig data')
    plt.legend()
    plt.title("Antal personer i olika kategorier över tid")
    plt.xlabel("Dagar efter 10/3")
    plt.ylabel("Antal individer i respektive grupp (logaritmisk skala)")
    plt.show()

def mse(a,b):
    assert len(a) == len(b), "MSE needs vectors of equal length."
    return sum([(a[i]-b[i])**2 for i in range(len(a))])/len(a)

def exp_mse(a,b,w):
    weights = [(1/w)**i for i in range(len(a))]
    s = sum(weights)
    weights = [w/s for w in weights]
    return sum([weights[i]*(a[i]-b[i])**2 for i in range(len(a))])

def score(a_inp,a,d_inp,d,a_weight=a_weight,exp_weight=1):
    return a_weight*exp_mse(a,a_inp,exp_weight) + (1-a_weight)*exp_mse(d,d_inp,exp_weight)
    # return a_weight*mse(a_inp,a) + (1-a_weight)*mse(d_inp,d)

def run_simul(alpha,beta,gamma,L,K,stop=None,bugfix=False):
    num_days = stop if stop != None else days
    s = [K]
    if bugfix: to_rem = [K/L for _ in range(L)]
    else: to_rem = [0]*L
    i,d,r = [0],[0],[pop-s[0]]
    a = [gamma*s[0]]
    for day in range(1,num_days+1):
        i.append(i[-1] + (1-alpha) * (to_rem[day-1] if day-L < 0 else (beta * r[day-L] * s[day-L])))
        d.append(d[-1] + alpha * (to_rem[day-1] if day-L < 0 else (beta * r[day-L] * s[day-L])))
        s.append(s[-1] + beta * r[-1] * s[-1] - (to_rem[day-1] if day-L < 0 else (beta * r[day-L] * s[day-L])))
        r.append(r[-1] - beta * r[-1] * s[-1])
        a.append(gamma * s[day])
    return s,i,d,r,a

def get_best_parameters(a_inp,d_inp,days=None,log_file='log_parameter_tidsserie.csv',exp_weight=1,bugfix=False):
    if days == None: days = len(a_inp)
    try:
        f = open(log_file,'r')
        content = f.read().strip().split('\n')
        f.close()
    except:
        content = []
    results = []
    for x in content:
        if len(x) < 10: continue
        results.append(tuple(map(float,x.split(';'))))
        if results[-1][0] == days:
            return results[-1][1],results[-1][2],results[-1][3],results[-1][4],results[-1][5],results[-1][6]
    no_best_models = 1

    BEST = (10**20,None)
    for beta in beta_list:
        for gamma in gamma_list:
            for kgamma in K_gamma_list:
                K = kgamma/gamma
                for L in L_list:
                    for alpha in alpha_list:
                        s,i,d,r,a = run_simul(alpha,beta,gamma,L,K,stop=days+4,bugfix=bugfix)
                        sc = score(a_inp[:days],a[:days],d_inp[:days],d[:days],a_weight=a_weight,exp_weight=exp_weight)
                        BEST = min(BEST,(sc,[alpha,beta,gamma,K,L,kgamma]))

    sc,vals = BEST
    alpha,beta,gamma,K,L,kgamma = vals[0],vals[1],vals[2],vals[3],vals[4],vals[5]
    results.append((days,alpha,beta,gamma,K,L,kgamma,sc))
    results.sort()
    f = open(log_file,'w')
    for x in results:
        f.write('{}'.format(int(x[0])))
        for y in x[1:]:
            f.write(';{}'.format(y))
        f.write('\n')
    f.close()
    return alpha,beta,gamma,K,L,kgamma
