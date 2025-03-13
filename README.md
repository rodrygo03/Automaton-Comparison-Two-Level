# Two-Level Adaptive Branch Predictor Automaton Comparison

This project compares the performance of two-level adaptive branch predictor automaton, specifically implementations A2 and A3, based on the research presented in:

> Tse-Yu Yeh and Yale N. Patt, “Alternative Implementations of Two-Level Adaptive Branch Prediction,” ISCA 1992

## Simulation Details

The simulation was conducted using **zsim**, with custom logic implementing A3. To analyze the results, a Python virtual environment should be used with dependencies listed in `deps.sh`.

## Results

The following table presents the performance observed for A2 and A3 across various benchmarks:

| Benchmark       | A2 Cycles          | A3 Cycles          |
|---------------|------------------|------------------|
| blackscholes  | 397,305,868.75   | 398,383,860.75   |
| bodytrack     | 57,414,568.375   | 57,580,830.875   |
| canneal       | 106,983,608.375  | 107,030,265.0    |
| fluidanimate  | 460,300,610.5    | 494,649,771.875  |
| freqmine      | 484,794,172.5    | 501,378,768.875  |
| streamcluster | 125,476,911.5    | 129,977,263.5    |
| swaptions     | 70,845,551.0     | 71,818,187.625   |
| x264          | 362,736,348.125  | 371,054,124.875  |

## Visual Analysis

The results of the prediction are illustrated in the following graphs:

- **A2 Results: analysis-results/A2_Results.png**
- **A3 Results: analysis-results/A3_Results.png**
- **Difference between A3 and A2: analysis-results/Diff_Results.png**

## Usage

To run the analysis on the simulation data:
1. Set up the Python virtual environment and install dependencies:
   ```sh
   source deps.sh
   ```
2. Execute the analysis script:
   ```sh
   python main.py
   ```