from main import *


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

(status, runtime, cost, seed) = run_evaluation(args.instance_name, float(args.cutoff_time), args.seed, float(args.coolFactor), float(args.startTemp))

# collect results and pass back to ruby/ paramILS with this format:
# Result:  <status>, <runtime>, <quality>, <seed>
# where status is either: “SUCCESS”, “TIMEOUT”, “ABORT” or “CRASHED”
# and quality is scalar value or comma separated values between brackets (a list).

print("Result: " + status, runtime, cost, seed)
