# pallo v0.2.1

This is a Python package available on PyPi that simplifies the creation and usage of probabilistic asset allocation models.

**Pallo currently supports:**
 - Geometric Mean Maximization
 - Custom Drawdown constraints
 - Margin Trading Calculation Options
 - Maximizing Sharpe Ratios

# Installation
    pip install pallo

# Usage
In v0.2.1 there are two asset allocation models currently available, a geometric mean maximization model and an efficient frontier model. There are plans for additional options in the future.
```
#Load a custom dataset as a 2d list with each asset's percentage price moves as a one list
#Use the createDataset() method to create a 2d list to use with the gphrModel
stocks = ["SGRY", "AA", "MTX"]
dataset = createDataset(stocks, 30)

#Create a gphrModel object and load the dataset
model = gphrModel(dataset)

#defineBins(), calcGPHRs(), and findBestUnderDrawdown() (need to be executed in that order)
#will compute the best asset allocation based on the inputted specifications. View method parameters below. 
model.defineBins()
model.calcGPHRs()
model.findBestUnderDrawdown(.90, 12, .2)

#Print the best possible asset allocation under the inputted drawdown constraint.
model.showStats()




#Find the best possible Sharpe ratio out of a collection of stocks
allStocks = ["BK", "MTZ", "SGRY", "AA", "ARCB", "RDNT", "MMYT", "DECK", "TEO", "WK"]

#Make a efModel object and input the list of stocks
mod = efModel(allStocks)

#Returns the best possible Sharpe ratio, stocks, and asset allocation
print(mod.findMaxSharpe(30))

```

# Object and Method Details
**gphrModel(dataset):**\
This is the object that will hold all calculations and information related to the inputted dataset.
>Dataset Specifications For Proper Function:
 - Must be a 2d list that holds the percentage price movements of each asset.
 - Each sub-list in the dataset must be of equal length to one another
 - The period (timeframe) referenced in each object of each sublist must be equal in all sublists
 - The dataset has a minimum asset count of 2 and an uncapped maximum

**gphrModel.defineBins(numBins=5):**\
This method will take the dataset you have inputted and create the probabilistic range as well as setup the most of the attributes for computation.
>Parameters:
 - numBins
    - This parameter determines how many probability bins are to be created for the model. This will have a low-moderate impact on the speed of computation and granularity of results.
    - Default: 5
    - Minimum to function: 3
    - No Maximum, however, the more you add the longer the computations will take later.

**gphrModel.calcGPHRs(portfolioLimit=.33):**\
This method will calculate all of the possible combinations of asset allocations within the portfolio limit.
>Parameters:
 - portfolioLimit
   - This is the percentage of the overall portfolio available funds that you will allow to compute. This will have a very high impact on the speed of computation, lower = faster, higher = slower. Consider lowering the input from default if your assets are highly volatile or you are seeking a low risk of hitting your drawdown constraint. Consider raising the input from default if your assets aren't volatile.
   - Default: .33
   - Minimum: .01
   - No Maximum for the method to function properly but to calculate for cash accounts 1.0 would equate to your entire account value. The input should exceed 1.0 for margin accounts.

**gphrModel.findBestUnderDrawdown(drawdownConstraint, periods, percentChance, extraBranches=False):**\
This method will do a pseudo tree traversal to calculate the best asset allocation that has a percent change below percentChance of hitting your drawdown constraint.
>Parameters:
 - drawdownConstraint
   - This will determine your drawdown constraint over the trading period. .90 equates to a 10% decrease on initial capitalization.
   - Minimum: .01
   - Maximum: .99
 - periods
   - This is the number of trading periods you want to calculate for. The timeframe for the period is the same as the timeframe between each percent change in your dataset.
   - Minimum: 1
   - No Maximum but it should be noted that as the periods grow larger the chance of hitting your drawdown will increase so you will find that the percentage of your overall portfolio you can trade will decrease.
   - This has a moderate impact on computation speed.
 - percentChance
   - This determines what percent chance you are willing to have of hitting your drawdown constraint over the trading period.
   - Minimum: .01
   - Maximum: 1.0
   - This has a moderate impact on computation speed.
 - **extraBranches**
   - This should only be set to true after extensive testing as this will **significantly** increase computation time. However, if this is set to true the results will be significantly more accurate and viable for use. With this set to false the results will not be consistent however the computation time is low and testing is more viable.
   - Default: False
     
**createDataset(stockList, timeIncluded):**\
This is a method that will turn a list of stocks into a usable 2d dataset for the gphrModel object.
>Parameters:
 - stockList
   - Input that determines the stocks the dataset is based off
   - Current functionality requires that the stock list length must be 3 exactly
 - Time Included
   - Integer that determines how many days prior to today will be included in the creation of the datset
   - Minimum: 1 (More if previous days were weekend or holiday)
   - Maximum: Uncapped
   
**efModel(stockList):**\
This object will intake a list of stocks and then calculate the best combination of three stocks and weights to produce the highest possible Sharpe ratio out of the inputted stocks.
>Stock List Specifications for Proper Function:
 - Must be List of stock tags as strings
 - Minimum: 2
 - Uncapped Maximum

**efModel.findMaxSharpe(timeIncluded)**
This method will calculate all of the best Sharpe ratios in the list of possible stock combinations and output the best possible Sharpe ratio and the asset allocation that achieves it.
>Parameters:
 - timeIncluded
   - Integer that determines how many days prior to today will be included in the calculation of Sharpe ratios
   - Minimum: 1 (More if previous days were weekend or holiday)
   - Maximum: Uncapped

# Roadmap
>Efficient Frontier Model Additional Customization
 - Add the ability to import custom datasets rather than downloading from yfinance.
 - Return a list of all Sharpe ratios and asset allocations.
 - Allow different numbers of final stock combinations aside from the default 3.
>Expanding Options/Interperiod Methods For gprhModel
 - Will be adding additional methods that adjust asset allocations depending upon ROI between periods.
 - Planning to add saving and recovering methods.
 - Also working towards a multiprocessing solution to reduce computation times.

# Recent Changes
v0.2.1
  - Added the createDataset() method to make it easier to test the gphrModel
    
v0.2.0
  - New efModel is finished with the ability to input any length stock list and find the best possible asset allocation of a combination of three stocks.
  - Cleaned up and updated README.
