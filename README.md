# TimeSeriesPrediction
This repository is the code base for the Bachelor's thesis 'Financial Time Series Prediction using the Sparse Grids Library SG++'.

Implemented:
A basic pipeline that can evaluate functions based on the SG++ tutorial. Needs to be modified to accept arbitrary datasets.

# ToDo's:
1. Rebuild the reference paper grid and cross-check results
    1.1 Figure out how to change the current function implementation to a timeseries implementation (possibly just use a dataset
        directly by pre-calculating the values, instead of worrying about functions)
    1.2 Test it with the Henon map
2. Create .csv file reader for time series {low, high, open, close, adjusted close, volume}
3. Create Pipeline for Financial Time Series (input, grid, output)
    3.1 Pre-processing of data into correct format
    3.2 Pre-conditioning the iteratior
    3.3 Setup grid with the correct function, SG++ tutorial only uses a simplified version
    3.4 Calculate alphas
    3.5 Evaluate
4. Check Pipeline for Financial Time Series
5. Test for possible correlations between the different input streams from 2.
6. Improve the prediction

Optional:
- Build automatic result visualization