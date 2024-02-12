# Regression Interval Inference System
# main.py
#
#
# Set class
# This is the main class containing :
# Dual value reading adjustment, Special 15min Set adjustments, Advanced Set System Revision: Set Rules Implementation,
#
# Data imported :
# 2-min timeframe: 3 stock market days (half a week)
# 15-min timeframe: 20 stock market days (full month)
# Both are used for the whole day, then reset

# Data should be formatted as :
# { <time>: ( <open>, <close> ), <time>: ( <open>, <close> ) }


# *** Imports
import modules.set as db

# *** Functions


# ***    Main Code    ***
setClass = db.Set({"1": (1, 2), "2": (3, 4)})
recievedPreviousData = setClass.cleanUp()

# Main Code

# Set variables
data = setClass.dataOrganized
outliers = [[], [], []]
intervals = [[], [], []]
specialClassChecker = 0

# Start for loop to find all the sets
for interval in range(len(data[0])):
    # If it's the first interval of a set
    if len(intervals[0]) == 0:
        # Find the direction of the first interval
        direction = setClass.intervalDirection(data[1][0], data[2][0])
        # Add the intervals to the intervals list
        intervals[0].append(data[0][0])
        intervals[1].append(data[1][0])
        intervals[2].append(data[2][0])

        setClass.addNewRegressionLine(
            setClass.regressionLine(intervals[1] + intervals[2], intervals[0])[0]
        )

        continue

    # Check Breakout

    # IF a set’s first open value is reversed by 50% or more, breakout
    breakout1 = setClass.checkBreakoutRule1(
        direction, data[1][interval], intervals[1][0]
    )
    if breakout1:
        # Add new set
        setClass.newSet(intervals)
        outliers = [[], [], []]
        intervals = [[], [], []]
        specialClassChecker = 0
        continue

    # IF regression line changes by 400%+ (after 3 initial intervals), breakout.
    if len(intervals) > 3:
        tempRegressionLine = setClass.regressionLine(
            intervals[1] + intervals[2], intervals[0]
        )[0]
        breakout2 = setClass.checkBreakoutRule2(tempRegressionLine)

        if breakout2:
            # Add new set
            setClass.newSet(intervals)
            outliers = [[], [], []]
            intervals = [[], [], []]
            specialClassChecker = 0
            continue

    newIntervalDirection = setClass.intervalDirection(
        data[1][interval], data[2][interval]
    )

    if newIntervalDirection != direction:
        outliers[0].append(data[0][interval])
        outliers[1].append(data[1][interval])
        outliers[2].append(data[2][interval])
        specialClassChecker += 1

    # Add the new intervals to the intervals list
    else:
        intervals[0].append(data[0][interval])
        intervals[1].append(data[1][interval])
        intervals[2].append(data[2][interval])
        specialClassChecker = 0

        # Add the new regression line to the file
        newRegressionLine = setClass.regressionLine(
            intervals[1] + intervals[2], intervals[0]
        )[0]
        setClass.addNewRegressionLine(newRegressionLine)

    # Rule 4: Inverse special Classification checker
    if specialClassChecker == 2:
        newSetTime = intervals[0].pop(0)
        newSetOpen = intervals[1].pop(0)
        newSetClose = intervals[2].pop(0)

        specialClass = setClass.intervalDirection([newSetOpen], [newSetClose])

        # Create a new set with these 1 interval values and classify as specialClass
        setClass.newSet([[newSetTime], [newSetOpen], [newSetClose]])

        # Reevaluate the leftover set and find the direction
        # Since the next three need to be the opposite of specialClass
        # Set it to the direction
        direction = setClass.oppositeDirection(specialClass)

        specialClassChecker = 0

        # Add the new regression line to the file
        newRegressionLine = setClass.regressionLine(
            intervals[1] + intervals[2], intervals[0]
        )[0]
        setClass.addNewRegressionLine(newRegressionLine)
