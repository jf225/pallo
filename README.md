# pallo v0.1.1

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
    #Load a custom dataset as a 2d list with each asset's previous price moves as a one list 
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
