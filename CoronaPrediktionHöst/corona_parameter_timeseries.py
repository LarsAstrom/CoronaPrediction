import sys
import heapq
import time
import corona

def main(do_plot=False,input_filename='input_data/input.csv',log_filename='log_parameter_tidsserie.csv',exp_weight=1,bugfix=False):
    t0 = time.time()
    a_inp,d_inp = corona.read_input(input_filename)
    alphas,betas,gammas,Ks,Ls,Kgammas,immune_starts = [],[],[],[],[],[],[]
    for num_days in range(14,len(a_inp)+1):
        print('Dag {} av {} startad.'.format(num_days,len(a_inp)))
        a,b,g,k,l,kg,imst = corona.get_best_parameters(a_inp,d_inp,days=num_days,log_file=log_filename,exp_weight=exp_weight,bugfix=bugfix)
        alphas.append(a)
        betas.append(b)
        gammas.append(g)
        Ks.append(k)
        Ls.append(l)
        Kgammas.append(kg)
        immune_starts.append(imst)
        time_passed = time.time()-t0
        print('Dag {} av {} slutford. Tidsatgang: {:.1f}.'.format(num_days,len(a_inp),time_passed))

    print('Alpha\t',alphas)
    print('Beta\t',betas)
    print('Gamma\t',gammas)
    print('K\t',Ks)
    print('L\t',Ls)
    print('Kgamma\t',Kgammas)
    print('Immune_start\t',immune_starts)

    print('\nSista parametrarna:')
    print('Alpha\t',alphas[-1],'\nBeta\t',betas[-1],'\nGamma\t',gammas[-1],'\nK\t',Ks[-1],'\nL\t',Ls[-1],'\nKgamma\t',Kgammas[-1],'\nImmune start\t',immune_starts[-1])

    if do_plot:
        import matplotlib.pyplot as plt
        plt.figure()
        plt.semilogy(alphas,label='alpha')
        plt.semilogy(betas,label='beta')
        plt.semilogy(gammas,label='gamma')
        plt.semilogy(Ks,label='K')
        plt.semilogy(Ls,label='L')
        plt.semilogy(Kgammas,label='Kgamma')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    do_plot = len(sys.argv) > 1
    input_filename = sys.argv[1] if len(sys.argv) > 1 else 'input_data/input.csv'
    log_filename = sys.argv[2] if len(sys.argv) > 2 else 'log_parameter_tidsserie.csv'
    exp_weight = float(sys.argv[3]) if len(sys.argv) > 3 else 0.9
    bug_fix = True
    main(do_plot,input_filename,log_filename,exp_weight,bug_fix)
