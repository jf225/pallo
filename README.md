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
    dataset = [[-.42, 1.3, .18, -1.2, -.74], [], []]
    #Load a custom dataset as a 2d list with each asset's previous price moves as a one list 
    #This example dataset is comparing three separate assets price changes
