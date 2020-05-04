import sys
import heapq
import corona

def main(do_plot=False,input_filename='input_data/input.csv',log_filename='log_parameter_tidsserie.csv',exp_weight=1,bugfix=False):
    a_inp,d_inp = corona.read_input(input_filename)

    alpha,beta,gamma,K,L,_ = corona.get_best_parameters(a_inp,d_inp,days=len(a_inp),log_file=log_filename,exp_weight=exp_weight,bugfix=bugfix)
    s,i,d,r,a = corona.run_simul(alpha,beta,gamma,int(L),K,bugfix=bugfix)

    print("\nExponential mean squared error of a is: {:.2f}\n\
Exponential mean squared error of d is: {:.2f}\n\
Penalty function is given by {:.2f}*exp_mse(a)+{:.2f}*exp_mse(d) with exponential decay {:.2f}\n\
The penalty function is {:.2f}\n".format(corona.exp_mse(a_inp,a[:len(a_inp)],exp_weight),\
                                        corona.exp_mse(d_inp,d[:len(d_inp)],exp_weight),\
                                        corona.a_weight,1-corona.a_weight,exp_weight,\
                                        corona.score(a_inp,a[:len(a_inp)],d_inp,d[:len(d_inp)],a_weight=0.8,exp_weight=exp_weight)))
    print("Parameters are:\n\
alpha: {}\n\
beta:  {}\n\
gamma: {}\n\
K:     {}\n\
L:     {}".format(alpha,beta,gamma,K,L))

    if do_plot: corona.plot(i,d,s,r,a,a_inp,d_inp)

if __name__ == '__main__':
    do_plot = len(sys.argv) > 1
    input_filename = sys.argv[1] if len(sys.argv) > 1 else 'input_data/input.csv'
    log_filename = sys.argv[2] if len(sys.argv) > 2 else 'log_parameter_tidsserie.csv'
    exp_weight = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    bug_fix = len(sys.argv) > 4
    if len(sys.argv) > 3:
        assert str(exp_weight) in log_filename, 'Exp weight needs to be in filenames'
    if len(sys.argv) > 4 and sys.argv[4] == 'bugfix':
        assert 'bugfix' in log_filename, 'Bugfix needs to be included in log name'
    elif len(sys.argv) <= 4 or sys.argv[4] != 'bugfix':
        assert 'bugfix' not in log_filename, 'Not bugfix -> bugfix not in log name'
    main(do_plot,input_filename,log_filename,exp_weight,bug_fix)
