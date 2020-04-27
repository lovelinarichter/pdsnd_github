import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    #get user input for city (chicago, new york city, washington)

    while True:
      city = input("\nWhich city would you like to filter by? New York City, Chicago, or Washington?\n")
      if city.lower() not in ('new york city', 'chicago', 'washington'):
        print("Please try again.")
        continue
      else:
        break

    #get user input for month (january, february, march, april, may , june, or all)
    while True:
      month = input("\nWhich month would you like to filter by? January, February, March, April, May, June, or type 'all'?\n")
      if month.lower() not in ('january', 'jebruary', 'march', 'april', 'may', 'june', 'all'):
        print("Please try again.")
        continue
      else:
        break

    #get user input for day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday)
    while True:
      day = input("\n Enter the day: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all'.\n")
      if day.lower() not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        print("Please try again.")
        continue
      else:
        break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.lower() != 'all':
   	 	# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Common Month:', popular_month)

    #display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', Start_Station)

    #display most commonly used end station
    End_Station = df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', End_Station)

    #display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(['Start Station', 'End Station']).count()
    print('\nMost Commonly used combination of start and end station trip:', Start_Station, " & ", End_Station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    Total_Travel_Time = sum(df['Trip Duration'])
    print('Total travel time:', Total_Travel_Time/86400, " Days")

    #display mean travel time
    Mean_Travel_Time = df['Trip Duration'].mean()
    print('Mean travel time:', Mean_Travel_Time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #display counts of user types
    user_types = df['User Type'].value_counts()
    #print(user_types)
    print('User Types:\n', user_types)

    #display gender counts
    try:
      gender_types = df['Gender'].value_counts()
      print('\nGender Types:\n', gender_types)
    except KeyError:
      print("\nGender Types:\nNo data available for this month.")

    #display earliest, most recent, and most common year of birth
    try:
      Earliest_Year = df['Birth Year'].min()
      print('\nEarliest Year:', Earliest_Year)
    except KeyError:
      print("\nEarliest Year:\nNo data available for this month.")

    try:
      Most_Recent_Year = df['Birth Year'].max()
      print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
      print("\nMost Recent Year:\nNo data available for this month.")

    try:
      Most_Common_Year = df['Birth Year'].value_counts().idxmax()
      print('\nMost Common Year:', Most_Common_Year)
    except KeyError:
      print("\nMost Common Year:\nNo data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Prompt the user if they want to see 5 lines of raw data
    Display that data if the answer is 'y'
    and continue these prompts and displays until the user says 'n'
    """
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1    # use index values for rows

    print('\n    Would you like to see some raw data from the current dataset?')
    while True:
        raw_data = input('      (y or n):  ')
        if raw_data.lower()        == 'y':      # display show_rows number
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))

            print('\n', df.iloc[rows_start : rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows

            print('\n    Would you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city.lower(), month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter y or n \n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
