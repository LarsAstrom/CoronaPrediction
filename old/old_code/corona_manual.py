import matplotlib.pyplot as plt
input_file = 'input_data/input.txt'
f = open(input_file,'r')
content = f.read().strip().split('\n')
a_inp = list(map(int,content[0].split(';')))
d_inp = list(map(int,content[1].split(';')))
days_inp = len(a_inp)
assert len(a_inp) == len(d_inp), 'Unequal length of input.'
f.close()

#Parameters
days = 300
pop = 1.377e6
alpha = 1e-2
beta  = 1.1e-7
gamma = 1e-2
L = 14
K = 300

s = [K]
i,d,r = [0],[0],[pop-s[0]]
a = [gamma*s[0]]
day_list = list(range(days+1))
for day in range(1,days+1):
    i.append(i[-1] + (1-alpha) * (0 if day-L < 0 else (beta * r[day-L] * s[day-L])))
    d.append(d[-1] + alpha * (0 if day-L < 0 else (beta * r[day-L] * s[day-L])))
    s.append(s[-1] + beta * r[-1] * s[-1] - (0 if day-L < 0 else (beta * r[day-L] * s[day-L])))
    r.append(r[-1] - beta * r[-1] * s[-1])
    a.append(gamma * s[day])
    for x in [i,d,s,r,a]:
        x[-1] = int(x[-1]+0.5)

for x in [i,d,r,s,a]: print(x[:30])

day_list_inp = list(range(len(a_inp)))

plt.figure()
plt.semilogy(day_list,i,label='Immuna')
plt.semilogy(day_list,d,label='Döda')
plt.semilogy(day_list,s,label='Sjuka')
plt.semilogy(day_list,r,label='Risk')
plt.semilogy(day_list,a,label='Allvarligt Sjuka')
plt.semilogy(day_list_inp,a_inp,label='Allvarligt Sjuka, verklig data')
plt.semilogy(day_list_inp,d_inp,label='Döda, verklig data')
plt.legend()
#plt.title("Days,pop,alpha,beta,gamma,L,K: {},{},{},{},{},{},{}".format(days,pop,alpha,beta,gamma,L,K))
plt.title("Antal personer i olika kategorier över tid")
plt.xlabel("Dagar efter 10/3")
plt.ylabel("Antal individer i respektive grupp (logaritmisk skala)")
plt.show()
