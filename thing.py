import praw

# Declare variables for user input
monthName = ''
ticker = ''
day = ''
month = ''
year = ''

# Get user input
ticker = input("Input Ticker: ")
dateString = input("Enter Date (mm/dd/yyyy): ")

# Get values for month date and year from the user input
month = int(dateString[0] + dateString[1])
day = dateString[3] + dateString[4]
year = dateString[6] + dateString[7] + dateString[8] + dateString[9]

# Convert month digit to abbreviated month name as well as asigning each month
# a conversion for calculating the day of the week
if month == 1:
    monthName = 'Jan'
    monthConversion = 6
elif month == 2:
    monthName = 'Feb'
    monthConversion = 2
elif month == 3:
    monthName = 'Mar'
    monthConversion = 2
elif month == 4:
    monthName = 'Apr'
    monthConversion = 5
elif month == 5:
    monthName = 'May'
    monthConversion = 0
elif month == 6:
    monthName = 'Jun'
    monthConversion = 3
elif month == 7:
    monthName = 'Jul'
    monthConversion = 5
elif month == 8:
    monthName = 'Aug'
    monthConversion = 1
elif month == 9:
    monthName = 'Sep'
    monthConversion = 4
elif month == 10:
    monthName = 'Oct'
    monthConversion = 6
elif month == 11:
    monthName = 'Nov'
    monthConversion = 2
elif month == 12:
    monthName = 'Dec'
    monthConversion = 4

# Find day of the week from date using formula found on
# https://lifehacker.com/how-to-quickly-figure-out-the-day-of-the-week-any-date-5848651
# First subtract multiple of seven from the date
day = int(day)
if day == (7 or 14 or 21 or 28):
    dayConversion = 0
    dayConversion = day
elif day < 14:
    dayConversion = (day - 7)
elif day < 21:
    dayConversion = (day - 14)
elif day < 28:
    dayConversion = (day - 21)
else:
    dayConversion = (day - 28)

# Make neccecary ajustments for leap years
year = int(year)
if year % 4 == 0:
    if month == 1:
        monthConversion = 5
    if month == 2:
        monthConversion = 1

# Create instance of the reddit class
reddit = praw.Reddit(client_id='C4UWIsiXzcFKOA',
                     client_secret='-XNDsOiH_f6x1E5JqChWTibj4o72jA',
                     user_agent='Python Script',
                     username='*****',
                     password='*****')

# Create a class for r/stocks
stocks = reddit.subreddit('stocks')

# Create an array to store search results
searchResults = []

# Turn the user input into a string that can
# be used to search for the thread for the desired day
if day < 10:
    searchTerm = ("r/Stocks Daily Discussion - " +
                  monthName + " 0" + str(day) + ", " + str(year))
else:
    searchTerm = ("r/Stocks Daily Discussion - " + monthName +
                  " " + str(day) + ", " + str(year))
# Search the subreddit with the searchTerm and add results to the array
for sub in stocks.search(searchTerm):
    searchResults.append(sub)

# Check to see if the search result array is empty
# If this is the case, prompt the user to input a valid weekday

if not searchResults:
    print("Please enter a valid non-holiday weekday")
    quit()

# The desired result will always be the first result,
# meaning the first element in the array can be used
# as the desired submission
subm = searchResults[0]

# Declare a counter to count the amount of times the ticker appears
counter = 0

# Make all comments available to be searched
subm.comments.replace_more(limit=None)

# Seach each comment for upper and lowercase mentions of the stock ticker,
# keeping track of each time it appears
for comm in subm.comments.list():
    if (" " + (ticker or ticker.lower()) +
       (' ' or ',' or '.' or '?' or ';' or ')')) in comm.body:
        counter += 1

# Print final result
print(counter)
