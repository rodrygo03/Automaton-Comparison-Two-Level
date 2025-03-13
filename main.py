import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def determineBranchPredAccuracy(path):
    f = h5py.File(path, 'r')

    dset = f["stats"]["root"]
    stats = dset[-1]
    coreStats = stats['westmere']

    condBranches = coreStats['condBranches']
    mispredBranches = coreStats['mispredBranches']

    # from 8 cores determine the average prediction accuracy
    return np.mean((1 - mispredBranches/condBranches))

def computePeformance(path):
    f = h5py.File(path, 'r')

    dset = f["stats"]["root"]
    stats = dset[-1]
    coreStats = stats['westmere']

    # from 8 cores determine average performance cycles
    return np.mean(coreStats['cycles'] + coreStats['cCycles'])

def plotCharts(tests, results, diff):
    plt.figure(figsize=(12, 7))
    plt.bar(tests, results[0], color='lightblue')
    plt.xlabel('Benchmark')
    plt.ylabel('Average Accuracy')
    plt.title('Two Level Adaptive Scheme Using A2')
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))
    plt.savefig("analysis-results/A2_Results.png")

    plt.clf()
    plt.bar(tests, results[1], color='skyblue')
    plt.xlabel('Benchmark')
    plt.ylabel('Average Accuracy')
    plt.title('Two Level Adaptive Scheme Using A3')
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05))
    plt.savefig("analysis-results/A3_Results.png")

    plt.clf()
    plt.bar(tests, diff, color='green')
    plt.xlabel('Benchmark')
    plt.ylabel('Average A2 - Average A3')
    plt.title('Two Level Adaptive Scheme Accuracy Difference Between A2 and A3')
    plt.gca().yaxis.set_major_locator(MultipleLocator(0.0025))
    plt.savefig("analysis-results/Diff_Results.png")

def notableMetrics(tests, resultsA2, resultsA3, diff):
    A2max = np.max(resultsA2)
    A2maxbenchmark = tests[np.where(resultsA2 == A2max)[0][0]] #dereference tuple
    A2min = np.min(resultsA2)
    A2minbenchmark = tests[np.where(resultsA2 == A2min)[0][0]] 
    A2avg = np.mean(resultsA2)

    A3max = np.max(resultsA3)
    A3maxbenchmark = tests[np.where(resultsA3 == A3max)[0][0]] 
    A3min = np.min(resultsA3)
    A3minbenchmark = tests[np.where(resultsA3 == A3min)[0][0]] 
    A3avg = np.mean(resultsA3)

    diffmax = np.max(diff)
    diffmaxbenchmark = tests[np.where(diff == diffmax)[0][0]] 
    diffmin = np.min(diff)
    diffminbenchmark = tests[np.where(diff == diffmin)[0][0]] 
    diffavg = np.mean(diff)

    with open('analysis-results/PredictionResults.txt', 'w') as file:
        file.write("For A2: \n")
        file.write(f"\tMax Accuracy: {A2max}\n")
        file.write(f"\tOn Benchmark: {A2maxbenchmark}\n")
        file.write(f"\tMin Accuracy: {A2min}\n")
        file.write(f"\tOn Benchmark: {A2minbenchmark}\n")
        file.write(f"\tAverage Accuracy: {A2avg}\n\n")
        
        file.write("For A3: \n")
        file.write(f"\tMax Accuracy: {A3max}\n")
        file.write(f"\tOn Benchmark: {A3maxbenchmark}\n")
        file.write(f"\tMin Accuracy: {A3min}\n")
        file.write(f"\tOn Benchmark: {A3minbenchmark}\n")
        file.write(f"\tAverage Accuracy: {A3avg}\n\n")
        
        file.write("A3 - A2: \n")
        file.write(f"\tMax Difference: {diffmax}\n")
        file.write(f"\tOn Benchmark: {diffmaxbenchmark}\n")
        file.write(f"\tMin Difference: {diffmin}\n")
        file.write(f"\tOn Benchmark: {diffminbenchmark}\n")
        file.write(f"\tAverage Difference: {diffavg}\n\n")

def reportPerformance(automantons, tests, performance):
    performanceDiff = np.array(performance[1]) - np.array(performance[0]) #A3 - A2
    maxDiff = np.max(performanceDiff)
    maxBench = tests[np.where(performanceDiff == maxDiff)[0][0]]
    minDiff = np.min(performanceDiff)
    minBench = tests[np.where(performanceDiff == minDiff)[0][0]]

    with open('analysis-results/PerformanceResults.txt', 'w') as file:
        for i, automaton in enumerate(automantons):
            for j, test in enumerate(tests):
                file.write(f"{automaton} | Average Number of cycles in {test}: {performance[i][j]}\n")
                
        file.write(f"Maximum difference: {maxDiff} on {maxBench}\n")
        file.write(f"Minimum difference: {minDiff} on {minBench}\n")


def main():
    tests = ['blackscholes', 'bodytrack', 'canneal', 'fluidanimate', 'freqmine', 'streamcluster', 'swaptions', 'x264']
    automatons = ['A2', 'A3']
    results = [[], []]
    performance = [[], []]

    for i, automaton in enumerate(automatons):
        for test in tests:
            path = 'simulation/zsim/outputs/hw2/' + automaton + '/' + test + '_8c_simsmall/zsim-ev.h5'
            results[i].append(determineBranchPredAccuracy(path))
            performance[i].append(computePeformance(path))
    
    resultsA2 = np.array(results[0])
    resultsA3 = np.array(results[1])
    automatonResultDiff = resultsA2 - resultsA3

    plotCharts(tests, results, automatonResultDiff)
    notableMetrics(tests, resultsA2, resultsA3, automatonResultDiff)
    reportPerformance(automatons, tests, performance)

    print("Analysis Complete")

if __name__ == "__main__": main()