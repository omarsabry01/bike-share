import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june']


class InvalidInput(Exception):
    pass


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = 'all'
    day = 'all'

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:

        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        try:
            if city not in CITY_DATA:
                raise Exception('Invalid Input')
        except Exception:
            print('Sorry, the state you entered has no available data.\nPlease try again.\n')
        else: break

    # get user input for month (all, january, february, ... , june)
    choices = ['month', 'day', 'none', 'both']
    while True:
        filter_choice = input('\nWould you like to filter the data by month, day, both, or not at all? Type "none", for no time filter.\n').lower()
        try:
            if filter_choice not in choices:
                raise Exception('Invalid Input')
        except Exception:
            print('This is not a valid filtering option. Please try again.')
        else: break

    if filter_choice in ['month', 'both']:
        while True:
            month = input('\nWhich month? January, February, March, April, May, or June?\n').lower()
            try:
                if month not in months:
                    raise Exception('Invalid Input')
            except Exception:
                print('Please enter a month from the shown options.')
            else: break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if filter_choice in ['day', 'both']:
        while True:
            day = input('\nWhich day? Type the name of the day. (e.g. \'Sunday\')\n').lower()
            try:
                if day not in days:
                    raise Exception('Invalid Input')
            except Exception:
                print('Please enter a valid day for filtering.')
            else: break

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("Most popular month for traveling: ", months[df['month'].mode()[0] - 1].title())
    # display the most common day of week
    print("\nMost popular day for traveling: ", df['day_of_week'].mode()[0])
    # display the most common start hour
    print("\nMost popular starting hour for traviling: ", df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most popular starting station: ", df['Start Station'].mode()[0])
    # display most commonly used end station
    print("\nMost popular ending station: ", df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    print("\nMost popular combination of start and end station: ",
          df[['Start Station', 'End Station']].mode().loc[0][0], ',',
          df[['Start Station', 'End Station']].mode().loc[0][1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time: ", round(df['Trip Duration'].sum() / 360, 3), "hours")
    # display mean travel time
    print("\nAverage travel time: ", round(df['Trip Duration'].mean() / 60, 2), "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User type count:")
    types = df['User Type'].value_counts()
    print(types.index[0], types[0])
    print(types.index[1], types[1])
    # Display counts of gender
    print("\nUser gender count:")
    if 'Gender' in df.columns:
        types = df['Gender'].value_counts()
        print(types.index[0], types[0])
        print(types.index[1], types[1])
    else:
        print("No gender data to share.")
    # Display earliest, most recent, and most common year of birth
    print("\nBirth year statistics:")
    if 'Birth Year' in df.columns:
        print("Youngest user birth year: ", int(df['Birth Year'].max()))
        print("Oldest user birth year: ", int(df['Birth Year'].min()))
        print("Most common year of birth: ", int(df['Birth Year'].mode()[0]))
    else:
        print("No birth year data to share.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays raw data for the user."""

    start = 0
    end = 5
    while True:
        show = input('\nDo you want to see 5 lines of raw data? Enter yes or no.\n')
        if show.lower() != 'yes':
            break

        print(df[start:end])
        start += 5
        end += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
