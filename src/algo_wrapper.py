from main import *


def plot_temp(instance, iters, temp, startTemp, coolFactor):
    fig = plt.figure(figsize=(20,10))
    plt.plot(range(iters), temp, label='temp')
    plt.title('Cooling Curve with StartTemp = ' + str(startTemp) + ' , alpha = ' + str(coolFactor))
    plt.legend()
    test_case = getTestCaseName(instance)
    plt.savefig('../plots/'+test_case+'-'+'Cooling Curve'+'-'+str(startTemp)+'-'+str(coolFactor)+'-'+datetime.datetime.now().strftime("%d %B %Y %X"))

def plot_cost(instance, iters, cost, startTemp, coolFactor):
    fig = plt.figure(figsize=(20,10))
    plt.plot(range(iters), cost, label='temp')
    plt.title('Optimization of Cost with StartTemp = ' + str(startTemp) + ' , alpha = ' + str(coolFactor))
    plt.legend()
    test_case = getTestCaseName(instance)
    plt.savefig('../plots/'+test_case+'-'+'Cost Curve'+'-'+str(startTemp)+'-'+str(coolFactor)+'-'+datetime.datetime.now().strftime("%d %B %Y %X"))

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
iterations, temperature_progress, cost_progress, startTemp, coolFactor = results_dict['Values']
#plot_temp(args.instance_name, iterations, temperature_progress, startTemp, coolFactor)
#plot_cost(args.instance_name, iterations, cost_progress, startTemp, coolFactor)


# collect results for paramILS
status, runtime, cost, seed = results_dict['Results']



# collect results and pass back to ruby/ paramILS with this format:
# Result:  <status>, <runtime>, <quality>, <seed>
# where status is either: “SUCCESS”, “TIMEOUT”, “ABORT” or “CRASHED”
# and quality is scalar value or comma separated values between brackets (a list).

print("Result for ParamILS:", status, ", ", runtime, ", ", iterations, ", ", cost, ", ", args.seed)
#print("Result for ParamILS:"+status, runtime, iterations, cost, args.seed, sep=", ")
