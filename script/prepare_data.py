import pandas as pd


def clean_data(input):
    """ Change object to datetime dtypes. """
    for col in input.columns:
        if input[col].dtypes == object:
            input[col] = pd.to_datetime(input[col]) 
    return input

def split_per_day(order_data):
    """ Split the data per day. """
    data_per_day = [date[1] for date in order_data.groupby(order_data['order_placed'].dt.date)] 
    return data_per_day