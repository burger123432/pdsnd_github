import time
import pandas as pd
import numpy as np
import os

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
    print('-'*40)
    print('Hello! Let\'s explore some US bikeshare data!')
    # initialize return values to empty strings
    city, month, day = '', '', '' 
    
    # loop until the entered city name is valid
    cities = ['chicago','new york city','washington']
    while city not in cities:
        city = input('Please enter one of the following cities: \'chicago\', \'new york city\', \'washington\' \n')
        city = city.lower().strip() # cast to lowercase and strip leading and trailing white space
        if city not in cities:
            print(city + ' is an invalid entry for city. \n')
    print(city + ' selected!')

    # get user input for month (all, january, february, ... , june)
    months = ['all','january','february','march','april','may','june']
    while month not in months:
        month = input('Please specify the month of the calendar year (up until June) or enter \'all\' to select all months: \n')
        month = month.lower().strip() # cast to lowercase and strip leading and trailing white space
        if month not in months:
            print(month + 'is an invalid entry for month. \n')
    print(month + ' selected!')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    while day not in days:
        day = input('Please specify the day of the week or enter \'all\' to select all days of the week: \n')
        day = day.lower().strip() # cast to lowercase and strip leading and trailing white space
        if day not in days:
            print(day + 'is an invalid entry for day of the week. \n')
    print(day + ' selected!')

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
    df = None
    while df is None:
        try:
            f = os.path.join(os.getcwd(), CITY_DATA[city]) # define file path of dataset for user-entered city
            df = pd.read_csv(f, dtype=str) # Read in every field as a string initially so we can define each of our field types otherwise
            
            # Format data type of fields
            for col in df.columns.values:
                if 'Time' in col:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                if col == 'Trip Duration':
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                if col == 'Birth Year':
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            
            # Note: the start day and end day are always the same day; no dataset contains an instance of overnight travel
            #       --as such, we only need to worry about extracting the month and day from one of the start/end time stamp fields
            df['Month'] = pd.DatetimeIndex(df['Start Time']).month_name().str.lower()
            df['Day'] = pd.DatetimeIndex(df['Start Time']).day_name().str.lower()
            df['Start Hour'] = pd.DatetimeIndex(df['Start Time']).strftime('%H')
            
            # Drop our carried in index with useless values
            df = df.drop(columns=['Unnamed: 0'])
            
            # Condition on user entered filters
            if (month == day == 'all'):
                return df.reset_index(drop=True)
            elif (month != 'all') & (day == 'all'):
                return df.loc[df['Month'] == month].reset_index(drop=True)
            elif (month == 'all') & (day != 'all'):
                return df.loc[df['Day'] == day].reset_index(drop=True)
            else:
                return df.loc[(df['Day'] == day) & (df['Month'] == month)].reset_index(drop=True)
            
        except FileNotFoundError:
            print('File ' + f + ' does not exist. Program is exiting and must be restarted after file has been saved to the referenced file path.' )
            os._exit(os.EX_OK)
            
def view_data(df):
    """
    Asks user if they would like to view the first 5 rows of data and each successive set of 5 rows in the dataset
    
    Args:
        (Pandas Dataframe) df - dataframe being viewed/analyzed by the user
    """
    s = input('\nWould you like to see the first 5 rows of data? Enter yes or anything else for no.\n')
    rowCount = 0
    while s.lower() == 'yes':
        if (rowCount <= df.shape[0]):
            print(df.iloc[rowCount:rowCount + 5])
            rowCount += 5
            s = input('\nWould you like to see the next 5 rows of data? Enter yes or anything else for no.\n')
        else:
            print('\n User has viewed all data in the dataset. \n')
            break
        if s.lower() != 'yes':
            print('\n User has exited viewing the dataset 5 records at a time. \n')
            break
    
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if df.shape[0] > 0:
        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        # display the most common month
        print('Most commonly traveled month: ' + str(df['Month'].mode()[0]))

        # display the most common day of week
        print('Most commonly traveled day of the week: ' + str(df['Day'].mode()[0]))

        # display the most common start hour
        print('Most commonly traveled starting hour: ' + str(df['Start Hour'].mode()[0]) + ':00')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
        view_data(df)
    else:
        print('There is no available data to compute time stats for the combination of city, month, and day which were entered. \n')
        print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    if df.shape[0] > 0:
        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # display most commonly used start station
        print('Most commonly used Start Station: ' + str(df['Start Station'].mode()[0]))

        # display most commonly used end station
        print('Most commonly used End Station: ' + str(df['End Station'].mode()[0]))

        # display most frequent combination of start station and end station trip
        startStation, endStation = (df['Start Station'] + '-' + df['End Station']).mode()[0].split('-')
        print('Most common trip taken: ' + startStation + ' to ' + endStation)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
        view_data(df)
    else:
        print('There is no available data to compute station stats for the combination of city, month, and day which were entered. \n')
        print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if df.shape[0] > 0:
        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # display total travel time
        print('Total trip duration: ' + str(df['Trip Duration'].sum()) + ' minutes')

        # display mean travel time
        print('Mean trip duration: ' + str(round(df['Trip Duration'].mean(),0))[:-2] + ' minutes')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
        view_data(df)
    else:
        print('There is no available data to compute trip duration stats for the combination of city, month, and day which were entered. \n')
        print('-'*40)
        
def user_stats(df):
    """Displays statistics on bikeshare users."""
    if df.shape[0] > 0:
        print('\nCalculating User Stats...\n')
        start_time = time.time()
        
        colNames = df.columns.values
        if 'User Type' in colNames:
            # Display counts of user types
            print('User Type Counts: \n')
            print(df.groupby(by=['User Type']).size())
            print('\n')
        else:
            print('Column \'User Type\' not found in dataset. \n')

        if 'Gender' in colNames:
            # Display counts of gender
            print('Gender Counts: \n')
            print(df.groupby(by=['Gender']).size())
            print('\n')
        else:
            print('Column \'Gender\' not found in dataset. \n')

        if 'Birth Year' in colNames:
            # Display earliest, most recent, and most common year of birth
            print('Oldest Passenger\'s Year of Birth: ' + str(round(df['Birth Year'].min(),0))[:-2])
            print('Youngest Passenger\'s Year of Birth: ' + str(round(df['Birth Year'].max(),0))[:-2])
            print('Most common Year of Birth: ' + str(round(df['Birth Year'].mode()[0],0))[:-2])
        else:
            print('Column \'Birth Year\' not found in dataset. \n')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
        view_data(df)
    else:
        print('There is no available data to compute trip duration stats for the combination of city, month, and day which were entered. \n')
        print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or anything else for no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
