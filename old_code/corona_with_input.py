import matplotlib.pyplot as plt

f = open('input.txt','r')
content = f.read().strip().split('\n')
a_inp = list(map(int,content[0].split(';')))
d_inp = list(map(int,content[1].split(';')))
days_inp = len(a_inp)
assert len(a_inp) == len(d_inp), 'Unequal length of input.'



'''
This score returns the sum for all the days of
((ahat[i]-a[i])/a[i])**2+((dhat[i]-d[i])/d[i])**2
'''
def score(ahat,a,dhat,d):
    if ahat == None: return 1e100
    adiff2 = [(ahat[i]-a[i])**2 for i in range(len(ahat))]
    ddiff2 = [(dhat[i]-d[i])**2 for i in range(len(dhat))]
    return sum([adiff2[i]/(1 if a[i] == 0 else a[i])**2 for i in range(len(ahat))]) + \
            sum([ddiff2[i]/(1 if d[i] == 0 else d[i])**2 for i in range(len(dhat))])

def run_simul(pop,alpha,beta,gamma,L,K,days=days_inp,complete=False):
    try:
        pop,alpha,beta,gamma,L,K = map(int,[pop,alpha,beta,gamma,L,K])
        # print(pop,alpha,beta,gamma,L,K)
        s = [K]
        i,d,r = [0],[0],[pop-s[0]]
        a = [gamma*s[0]]
        for day in range(1,days+1):
            i.append(i[-1] + (1-alpha) * (0 if day-L < 0 else (beta * r[day-L] * s[day-L])))
            d.append(d[-1] + alpha * (0 if day-L < 0 else (beta * r[day-L] * s[day-L])))
            s.append(s[-1] + beta * r[-1] * s[-1] - (0 if day-L < 0 else (beta * r[day-L] * s[day-L])))
            r.append(r[-1] - beta * r[-1] * s[-1])
            a.append(gamma * s[day])
            for x in [i,d,s,r,a]:
                x[-1] = int(x[-1]+0.5)
        if complete: return s,i,d,r,a
        return a,d
    except:
        return None,None

days = 100
parameters = {'pop':[1.345e6,1.345e6],'alpha':[1e-6,3e-2],'beta':[1e-8,1e-4],'gamma':[1e-6,1e-1],'L':[10,20],'K':[1000,10000]}
#no_steps = {'pop':1,'alpha':10,'beta':100,'gamma':100,'L':10,'K':100}
no_steps = {'pop':1,'alpha':10,'beta':10,'gamma':10,'L':10,'K':10}
iterations = 5
for _ in range(iterations):
    print(parameters)
    BEST = (1e100,None)
    step_length = {}
    for x in parameters:
        if no_steps[x] == 1: step_length[x] = 0
        else:
            step_length[x] = (parameters[x][1] - parameters[x][0]) / (no_steps[x] - 1)
    for pi in range(no_steps['pop']):
        for ai in range(no_steps['alpha']):
            print('Alpha',ai)
            for bi in range(no_steps['beta']):
                for ci in range(no_steps['gamma']):
                    for li in range(no_steps['L']):
                        for ki in range(no_steps['K']):
                            # p = parameters['pop'][0] + pi * step_length['pop']
                            # a = parameters['alpha'][0] + ai * step_length['alpha']
                            # b = parameters['beta'][0] + bi * step_length['beta']
                            # c = parameters['gamma'][0] + ci * step_length['gamma']
                            # l = parameters['L'][0] + li * step_length['L']
                            # k = parameters['K'][0] + ki * step_length['K']
                            p = parameters['pop'][0] * (parameters['pop'][1]/parameters['pop'][0])**(pi/(no_steps['pop']-1) if no_steps['pop'] > 1 else 0)
                            a = parameters['alpha'][0] * (parameters['alpha'][1]/parameters['alpha'][0])**(ai/(no_steps['alpha']-1) if no_steps['alpha'] > 1 else 0)
                            b = parameters['beta'][0] * (parameters['beta'][1]/parameters['beta'][0])**(bi/(no_steps['beta']-1) if no_steps['beta'] > 1 else 0)
                            c = parameters['gamma'][0] * (parameters['gamma'][1]/parameters['gamma'][0])**(ci/(no_steps['gamma']-1) if no_steps['gamma'] > 1 else 0)
                            l = parameters['L'][0] * (parameters['L'][1]/parameters['L'][0])**(li/(no_steps['L']-1) if no_steps['L'] > 1 else 0)
                            k = parameters['K'][0] * (parameters['K'][1]/parameters['K'][0])**(ki/(no_steps['K']-1) if no_steps['K'] > 1 else 0)

                            ahat,dhat = run_simul(p,a,b,c,l,k)
                            if ahat != None:
                                sc = score(ahat[1:],a_inp,dhat[1:],d_inp)
                                if sc < BEST[0]:
                                    BEST = (sc,{'pop':p,'alpha':a,'beta':b,'gamma':c,'L':l,'K':k})

    for x in parameters:
        _,mids = BEST
        parameters[x] = [max(parameters[x][0],mids[x]-step_length[x]/2),min(parameters[x][1],mids[x]+step_length[x]/2)]

print(parameters)
p,a,b,c,l,k = (parameters['pop'][0]+parameters['pop'][1])/2,(parameters['alpha'][0]+parameters['alpha'][1])/2,\
                (parameters['beta'][0]+parameters['beta'][1])/2,(parameters['gamma'][0]+parameters['gamma'][1])/2,\
                (parameters['L'][0]+parameters['L'][1])/2,(parameters['K'][0]+parameters['K'][1])/2
s,i,d,r,a = run_simul(p,a,b,c,l,k,days=days,complete=True)
day_list = list(range(days))
day_list_inp = list(range(days_inp))

print(s)
print(i)
print(d)
print(r)
print(a)

plt.figure()
plt.semilogy(day_list,i[1:],label='Immune')
plt.semilogy(day_list,d[1:],label='Dead')
plt.semilogy(day_list,s[1:],label='Sick')
plt.semilogy(day_list,r[1:],label='Risk')
plt.semilogy(day_list,a[1:],label='Sick, serious condition')
plt.semilogy(day_list_inp,a_inp,label='Sick, serious condition, real data')
plt.semilogy(day_list_inp,d_inp,label='Dead, real data')
plt.legend()
plt.show()
