import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Would you like to see data for Chicago, New York City, or Washington?\n')).lower()
            if city == 'chicago' or city == 'new york city' or city == 'washington':
                break
        except:
            print('\nThat is not a valid input for this data. Please enter Chicago, New York City, or Washington\n')

        else:
            print('That is not a valid city for this data. Please enter Chicago, New York City, or Washington\n')
    print('Looks like you want to hear about {}! If this is not true, restart the program now!'.format(city))

    while True:
        try:
            time_filter = str(input('\nWould you like to filter the data by month, day, or not at all? Type "none" for no time filter.\n')).lower()
            if time_filter == 'month' or time_filter == 'day' or time_filter == 'none':
                break
        except:
            print('\nThat is not a valid input for this data. Please enter "month", "day", or "none".')

        else:
            print('\nThat is not a valid input for this data. Please enter "month", "day", or "none".')

    if time_filter == 'month':
        day = 'all'
        while True:
            month = str(input('\nWhich month? January, February, March, April, May or June?\n')).lower()
            if month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june':
                break
            else:
                print('That is not a valid input or there is no data for this month.')

    elif time_filter == 'day':
        month = 'all'
        while True:
            day = str(input('\nWhich day? Please type M, Tu, W, Th, F, Sa, Su.\n')).lower()
            if day == 'm' or day == 'tu' or day == 'w' or day == 'th' or day == 'f' or day == 'sa' or day == 'su':
                break
            else:
                print('\nThat is not a valid input.')

    elif time_filter == 'none':
        month = 'all'
        day = 'all'

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['start_end_station'] = 'FROM ' + df['Start Station'] + ' TO ' + df['End Station']

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        days = {'m': 'Monday', 'tu': 'Tuesday', 'w': 'Wednesday', 'th': 'Thursday', 'f': 'Friday', 'sa': 'Saturday', 'su': 'Sunday'}
        df = df[df['day_of_week'] == days[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}
    popular_month = months[df['month'].mode()[0]]
    print('Most Popular Month:', popular_month)

    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start = df['Start Station'].mode()[0]
    print('Most Common Start Station:', most_common_start)


    most_common_end = df['End Station'].mode()[0]
    print('Most Common End Station:', most_common_end)


    most_common_trip = df['start_end_station'].mode()[0]
    print('Most Common Trip:', most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration Statistics...\n')
    start_time = time.time()

    total_travel_time = (df['Trip Duration'].sum() / 60) / 60
    print('Total Time Travelled (Hours):', total_travel_time)

    avg_travel_time = df['Trip Duration'].mean() / 60
    print('Average Trip Duration (Minutes):', avg_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('User Breakdown:\n{}'.format(user_types))

    try:
        print('\nGender Breakdown:')
        genders = df['Gender'].value_counts()
        print(genders)
    except KeyError:
        print('There is no gender data available for this city.')


    try:
        print('\nBirth Year Breakdown:')
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        user_most_common_age = int(df['Birth Year'].mode()[0])
        print('Oldest: {} \nYoungest: {} \nMost Common Birth Year: {}'.format(oldest, youngest, most_common_age))
    except KeyError:
        print('There is no birth year data available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        row_count = 5
        while True:
            view_raw = str(input('\nWould you like to view the raw data? Type "Y" to view the first/next 5 rows of data or "N" to begin calculating statistics.\n')).upper()
            if view_raw == 'N':
                break
            elif view_raw == 'Y':
                print(df.head(row_count))
                row_count += 5

        time_stats(df)
        time.sleep(3)
        station_stats(df)
        time.sleep(3)
        trip_duration_stats(df)
        time.sleep(3)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
