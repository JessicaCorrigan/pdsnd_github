#Import necessary libraries
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' ]


def user_input(message, user_list):
    """
    Function to obtain user input
    Args:
        (str) message - request information
    Returns:
        (str) user_data - data input by user
    """

    while True:
        user_data = input(message).lower()
        if user_data in user_list:
            break
        elif user_data == 'all':
            break
        else:
            print('Program cannot move on without valid input, please re-enter selection.')

    return user_data

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = user_input("Please select a city from the following that you would like to explore: Chicago, New York, Washington: ", CITIES)
    month = user_input("Please enter the month you would like to filter by (Ex: january, february, ..june) or enter \'all\' to view unfilterd data:  ", MONTHS)
    day = user_input("Please input the day of the week you would like to filter by or enter \'all\' to view unfiltered data.  ", DAYS)

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

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to Datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create new columns by extracting month/dow/hr from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month if users does not input 'all'
    if month != 'all':
        month =  MONTHS.index(month) + 1
        df = df[ df['month'] == month ]

    # Filter by day if users does not input 'all'
    if day != 'all':
        # Filter by dow to create the new df
        df = df[ df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month for travel is:", most_common_month)

    # Display the most common day of week
    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of the week that people travel is:", most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour for people to begin their travels is:", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmin()
    print("The most commonly used start station is:", most_common_start_station)

    # Display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is:", most_common_end_station)

    # Display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station is: {}, {}"            .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    # Display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Average travel time :", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Displaying counts of user types:\n")
    user_counts = df['User Type'].value_counts()
    # Print out the total numbers of user types
    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    print()

    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_birth_stats(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats_gender(df):
    """Displays bikeshare users gender stats."""

    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    # Print out the total numbers of each genders
    for index,gender_count   in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))


def user_birth_stats(df):
    """Displays bikeshare users birth stats."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # the most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)
    # the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    # the most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)

def display_data_filtered(filtered_data):
    '''Displays the selected city data and filtered data, diplays in increments of five
    Args:
        filtered_data, data filtered by user input
    Returns:
        dataset
    '''
    x=0
    y=5
    user_ind_data = input('\nView individual trip data? '
                            ' Enter: \'yes\' / \'no\'. ')
    if user_ind_data == 'yes':
        print(filtered_data.iloc[x:y])
        while x < len(filtered_data.index):
            next_rows = input('\nView the next five rows?'
                                    ' Enter: \'yes\' / \'no\'. ')
            if next_rows == 'yes':
                x = x + 5
                y = y + 5
                print(filtered_data.iloc[x:y])
            else:
                break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data_filtered(df)


        restart = input('\nWould you like to restart the program?'
                                        ' Enter: \'yes\' / \'no\'. ')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
