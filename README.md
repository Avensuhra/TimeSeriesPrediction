# TimeSeriesPrediction
This repository is the code base for the Bachelor's thesis 'Analysis of financial timeseries prediction using sparse grids'

Sparse Grid Library: SG++ http://sgpp.sparsegrids.org/

The implementation is based on the reference paper "An adaptive sparse grid approach for time series prediction" by B. Bohn and M. Griebel.

Done so far:
1. Compared results of the SG++ pipeline with the results in the reference paper for regular and space-adaptive sparse grids for the test cases Henon Map and Jump Map.
2. Built a basic pipeline for financial data, using data provided by Quandl (https://www.quandl.com/) to evaluate the prediction accuracy on the U.S. stock market.
3. Stored stock values and calculated embedded dimension for over 2000 stocks (the biggest U.S. companies, available on the Quandl EOD Wiki) in a file so it doesn't have to be recalculated every time.

Planned:
1. Modify the prediction to only predict n steps into the future and then retrain.
2. Implement a statistical evaluation of the prediction results
3. (Optional) Implement a stock-trading algorithm that buys/sells according to the prediction on an ideal platform (no buy/sell delay, no fees)
4. (Optional) Combine different charts instead of only using adjusted close
5. Improve the prediction
