import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chi': 'chicago.csv',
              'new': 'new_york_city.csv',
              'was': 'washington.csv' }

    #valid inputs to check against and repeating questions/statements to shorten overall length
validmonth = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "all"]
datamonth = ["jan", "feb", "mar", "apr", "may", "jun"]
validcity = ["chi", "new", "was"]
validday = ["sun", "mon", "tue", "wed", "thu", "fri", "sat", "all"]
citycity = "initial"


def get_filters():
    global validmonth
    global validcity
    global validday
    global citycity

    #makes while loops go loopy
    citychoice = "intial"
    monthchoice = "initial"
    daychoice = "initial"

    #possible errors
    oops = "\nI'm sorry, that was an invalid entry.  Please try again\n"
    question = "\n Please input the first three letters of the {} you would like to view data for: \n{}"
    #note to self: review data BEFORE assuming things
    oopsmonth = "\nFor some reason that month isn't in the data.\nPlease only select a month from January to June."

    print('\nHello! Let\'s explore some US bikeshare data!')
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) citychoice - first three letters of city to anlayze
        (str) monthchoice - first three letters of month to analyze (or all)
        (str) daychoice - first three letters of day to analyze (or all)
    """


    while citychoice not in validcity:
        citychoice = input(question.format("city", "Chicago, New York or Washington: "))
        citycity = citychoice
        if citychoice not in validcity:
            print(oops)
        else:
            break

    while monthchoice not in datamonth:
        monthchoice = input(question.format("month", "(or type 'all'): "))
        if monthchoice not in validmonth:
            print(oops)
        elif monthchoice in validmonth and monthchoice not in datamonth and monthchoice != "all":
            print(oopsmonth)
        else:
            break

    while daychoice not in validday:
        daychoice = input(question.format("day", "(or type 'all'): "))
        if daychoice not in validday:
            print(oops)
        else:
            break

    #nice words on the GUI
    if citychoice == "was":
        citydisplay = "Washington"
    elif citychoice == "new":
        citydisplay = "New Your City"
    elif citychoice == "chi":
        citydisplay = "Chicago"
    else:
        print ("You broke the program :(")

    if monthchoice == "jan":
        displaymonth = "January"
    elif monthchoice == "feb":
        displaymonth = "February"
    elif monthchoice == "mar":
        displaymonth = "March"
    elif monthchoice == "apr":
        displaymonth = "April"
    elif monthchoice == "may":
        displaymonth = "May"
    elif monthchoice == "jun":
        displaymonth = "June"
    elif monthchoice == "all":
        displaymonth = "January to June.  (no data available for July to December)"
    else:
        print("Why must you break the program :(")

    if daychoice == "mon":
        daydisplay = "Monday"
    elif daychoice == "tue":
        daydisplay = "Tuesday"
    elif daychoice == "wed":
        daydisplay = "Wednesday"
    elif daychoice == "thu":
        daydisplay = "Thursday"
    elif daychoice == "fri":
        daydisplay = "Friday"
    elif daychoice == "sat":
        daydisplay = "Saturday"
    elif daychoice == "sun":
        daydisplay = "Sunday"
    elif daychoice == "all":
        daydisplay = "Everyday!"
    else:
        print("Broken Program = Much Sad.")

    print("\n" + "^*"*23)
    print("Thanks!  You have chosen:\n     CITY: " + citydisplay + "\n    MONTH: " + displaymonth + "\n      DAY: " + daydisplay)
    print("^*"*23 + "\n")

    #print("~"*28 + "\nCODE HAS NOT BROKEN YET! 001\n" + "~"*28)
    return citychoice, monthchoice, daychoice


def load_data(citychoice, monthchoice, daychoice):
    global validmonth
    global validcity
    global validday

    #because python doesnt like words
    if daychoice == "sun":
        daychoice = 6
    elif daychoice == "mon":
        daychoice = 0
    elif daychoice == "tue":
        daychoice = 1
    elif daychoice == "wed":
        daychoice = 2
    elif daychoice == "thu":
        daychoice = 3
    elif daychoice == "fri":
        daychoice = 4
    elif daychoice == "sat":
        daychoice = 5
    elif daychoice == "all":
        daychoice = "all"
    else:
        print("Congratulations!  You broke the program(daychoice)!")

    if monthchoice == "jan":
        monthchoice = 1
    elif monthchoice == "feb":
        monthchoice = 2
    elif monthchoice == "mar":
        monthchoice = 3
    elif monthchoice == "apr":
        monthchoice = 4
    elif monthchoice == "may":
        monthchoice = 5
    elif monthchoice == "jun":
        monthchoice = 6
    elif monthchoice == "all":
        monthchoice = "all"
    else:
        print("Congratulations!  You broke the program(monthchoice)!")


    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

        #Load chosen csv and get month and day in new columns
    df = pd.read_csv(CITY_DATA[citychoice])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_of_week

        #Month Filter
    if monthchoice != "all":
        df = df[df["month"] == monthchoice]

        #Day Filter
    if daychoice != "all":
        df = df[df["day_of_week"] == daychoice]

    #print("~"*28 + "\nCODE HAS NOT BROKEN YET! 002\n" + "~"*28)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #calculate most popular month, week and hour
    xmonth = df["month"].mode()[0]
    xday = df["day_of_week"].mode()[0]
    df["hour"] = df["Start Time"].dt.hour
    xhour = df["hour"].mode()[0]

    #convert to nice things to read
    if xday == 0:
        xday = "Monday"
    elif xday == 1:
        xday = "Tuesday"
    elif xday == 2:
        xday = "Wednesday"
    elif xday == 3:
        xday = "Thursday"
    elif xday == 4:
        xday = "Friday"
    elif xday == 5:
        xday = "Saturday"
    elif xday == 6:
        xday = "Sunday"
    else:
        print("Congratulations!  You broke the program(dayniceread)!")

    if xmonth == 1:
        xmonth = "January"
    elif xmonth == 2:
        xmonth = "February"
    elif xmonth == 3:
        xmonth = "March"
    elif xmonth == 4:
        xmonth = "April"
    elif xmonth == 5:
        xmonth = "May"
    elif xmonth == 6:
        xmonth = "June"

    else:
        print("Congratulations!  You broke the program(monthniceread)!")

    #print the popular times
    print("~"*40)
    print("    Most popular month: ", xmonth)
    print("      Most popular day: ", xday)
    print("     Most popular hour: ", xhour, "(24hr)")
    print("~"*40 + "\n")
    print('-'*40)
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #print("~"*28 + "\nCODE HAS NOT BROKEN YET! 003\n" + "~"*28)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print("~"*40)
    # display most commonly used start station
    popss = df["Start Station"].mode()[0]
    print("The most popular Start Station is: ", popss)

    # display most commonly used end station
    popes = df["End Station"].mode()[0]
    print("The most popular End Station is: ", popes)

    # display most frequent combination of start station and end station trip
    popcomb = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print("The most popular Start-End combination is from {} to {}.".format(popcomb[0], popcomb[1]))
    print("~"*40 + "\n")
    print('-'*40)
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #print("~"*28 + "\nCODE HAS NOT BROKEN YET! 004\n" + "~"*28)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    mins = df["Trip Duration"].count()

    print("~"*40)
    print("Total trave time: " + str(mins) + " minutes")
    if mins == 300000:
        print("Weird how every city's total is exactly 300000.  I spent a sad amount of time trying to debug this because it seemed really sus.")
    # display mean travel time

    print("~"*40 + "\n")
    print('-'*40)
    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)

    #print("~"*28 + "\nCODE HAS NOT BROKEN YET! 005\n" + "~"*28)



def user_stats(df):
    global citycity
    """Displays statistics on bikeshare users."""
    print
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("~"*40)
    usercount = df["User Type"].value_counts()
    print(usercount)
    print("~"*40)
    # Display counts of gender

    if citycity != "was":
        gencount = df["Gender"].value_counts()
        print(gencount)
        print("~"*40)
    # Display earliest, most recent, and most common year of birth
        lst = int(df["Birth Year"].min())
        fst = int(df["Birth Year"].max())
        com = int(df["Birth Year"].mode())
        print("The youngest user was born in {}, the oldest in {}.".format(fst, lst))
        print("The most common birth year of users is {}".format(com))
        print("~"*40)
        print('-'*40)
        print("This took %s seconds." % (time.time() - start_time))
        print('-'*40)
    elif citycity == "was":
        print("\nWashington State does not collect demographic information on its users.")
    else:
        print("This should not ever print")

    #print("~"*28 + "\nCODE HAS NOT BROKEN YET! 006\n" + "~"*28)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
