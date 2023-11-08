# pallo v0.1.3

This is a Python package available on PyPi that simplifies the creation and usage of probabilistic asset allocation models.

**Pallo currently supports:**
 - Geometric Mean Maximization
 - Custom Drawdown constraints
 - Margin Trading Calculation Options

# Installation
    pip install pallo

# Usage
In v0.1.1 there is only one currently available asset allocation model available, however, there are plans for additional options in the future.
```
#Load a custom dataset as a 2d list with each asset's percentage price moves as a one list 
dataset = [[-.42, 1.3, .18, -1.2, -.74], [2.1, -3.4, 1.1, .98, -4.3], [1.1, .72, .31, -.11, -1.4]]

#Create a gphrModel object and load the dataset
model = gphrModel(dataset)

#defineBins(), calcGPHRs(), and findBestUnderDrawdown() (need to be executed in that order)
#will compute the best asset allocation based on the inputted specifications. View method parameters below. 
model.defineBins()
model.calcGPHRs()
model.findBestUnderDrawdown(.90, 12, .2)

#Print the best possible asset allocation under the inputted drawdown constraint.
model.showStats()

```

# Object and Method Details
**gphrModel(dataset):**\
This is the object that will hold all calculations and information related to the inputted dataset.
>Dataset Specifications For Proper Function:
 - Must be a 2d list that holds the percentage price movements of each asset.
 - Each sub-list in the dataset must be of equal length to one another
 - The period (timeframe) referenced in each object of each sublist must be equal in all sublists
 - The dataset has a minimum asset count of 2 and an uncapped maximum

**defineBins(numBins=5):**\
This method will take the dataset you have inputted and create the probabilistic range as well as setup the most of the attributes for computation.
>Parameters:
 - numBins
    - This parameter determines how many probability bins are to be created for the model. This will have a low-moderate impact on the speed of computation and granularity of results.
    - Default: 5
    - Minimum to function: 3
    - No Maximum, however, the more you add the longer the computations will take later.

**calcGPHRs(portfolioLimit=.33):**\
This method will calculate all of the possible combinations of asset allocations within the portfolio limit.
>Parameters:
 - portfolioLimit
   - This is the percentage of the overall portfolio available funds that you will allow to compute. This will have a very high impact on the speed of computation, lower = faster, higher = slower. Consider lowering the input from default if your assets are highly volatile or you are seeking a low risk of hitting your drawdown constraint. Consider raising the input from default if your assets aren't volatile.
   - Default: .33
   - Minimum: .01
   - No Maximum for the method to function properly but to calculate for cash accounts 1.0 would equate to your entire account value. The input should exceed 1.0 for margin accounts.

**findBestUnderDrawdown(drawdownConstraint, periods, percentChance, extraBranches=False):**\
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
   - This should only be set to true after extensive testing as this will **significantly** increase computation speed. However, if this is set to true the results will be significantly more accurate and viable for use. With this set to false the results will not be consistent however the computation speed is low and testing is more viable.
   - Default: False
