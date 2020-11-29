from main import *


def plot_temp_cost(instance, iters, temp, cost, startTemp, coolFactor):
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('iterations')
    ax1.set_ylabel('temperature', color=color)
    ax1.plot(range(iters), temp, color=color, label='temp', linestyle='dashed')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('cost', color=color)
    ax2.plot(range(iters), cost, color=color, label='cost')
    ax2.tick_params(axis='y', labelcolor=color)

    test_case = getTestCaseName(instance)
    plt.title('Cooling Curve and Cost Optimization with t_start = ' + str(startTemp) + ' , alpha = ' + str(coolFactor), fontsize=11)
    fig.tight_layout()

    plt.savefig('../plots/'+test_case+'-'+'Temp and Cost'+'-'+str(startTemp)+'-'+str(coolFactor)+'-'+datetime.datetime.now().strftime("%d %B %Y %X")+".PNG", format="PNG")


# parse args from the paramILS command line call
parser = argparse.ArgumentParser()
parser.add_argument("instance_name",action='store')
parser.add_argument("instance-specific-information", action = 'store')
parser.add_argument("cutoff_time",action='store')
parser.add_argument("cutoff_length",action='store')
parser.add_argument("seed",action='store')
parser.add_argument("-coolFactor", action='store')
parser.add_argument("-startTemp",action='store')

args = parser.parse_args()
# pass the args into the actual python program containing the algorithm and run

results_dict = run_evaluation(args.instance_name, float(args.cutoff_time), args.seed, float(args.coolFactor), float(args.startTemp))

# plot
iters, temp, cost, startTemp, coolFactor = results_dict['Values']
plot_temp_cost(args.instance_name, iters, temp, cost, startTemp, coolFactor)

# collect results for paramILS
status, runtime, cost, seed = results_dict['Results']



# collect results and pass back to ruby/ paramILS with this format:
# Result:  <status>, <runtime>, <quality>, <seed>
# where status is either: “SUCCESS”, “TIMEOUT”, “ABORT” or “CRASHED”
# and quality is scalar value or comma separated values between brackets (a list).

print("Result for ParamILS:", status, ", ", runtime, ", ", iters, ", ", cost, ", ", args.seed)
#print("Result for ParamILS:"+status, runtime, iterations, cost, args.seed, sep=", ")
