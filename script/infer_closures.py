import numpy as np
import pandas as pd


def define_closure(data_per_day, num_sigma):
    """
    Define when a dark store is closed, defined as δt > μ + nσ. 
    Concatenates all gaps between orders and returns mean + :num_sigma: standard deviations.
    """
    total_times_between_orders = []
    for day in range(len(data_per_day)):
        total_times_between_orders.append((data_per_day[day]['order_placed'].diff().iloc[1:].dt.total_seconds()/60).to_numpy())
    total_times_between_orders = np.concatenate(total_times_between_orders)
    return np.mean(total_times_between_orders) + num_sigma * np.std(total_times_between_orders)

def get_times_between_orders(data):
    """ 
    Return a dataframe containing timestamps of consecutive orders and their difference.
    For first and last orders, the difference is calculated with the dark store's opening and closing 
    times respectively (08:00 & 22:00).
    """
    opening_time = pd.to_datetime(data.iloc[0]['order_placed'].strftime('%Y-%m-%d') + " 08:00:00")
    closing_time = pd.to_datetime(data.iloc[0]['order_placed'].strftime('%Y-%m-%d') + " 22:00:00")
    data = pd.concat([data, pd.DataFrame([closing_time], columns=['order_placed'])], ignore_index=True)
    data['previous_order'] = data['order_placed'].shift(1, fill_value=opening_time)
    data['timedelta'] = (data['order_placed'] - data['previous_order']).dt.total_seconds()/60
    return data

def get_closed_intervals(data, threshold):
    """
    Get start and end timestamps of closed intervals.
    Closed is defined when the difference between consecutive orders is greater than the threshold.
    """
    closed_hours = data[data['timedelta'] > threshold]
    closure_start_datetime, closure_end_datetime = [], []
    for _, row in closed_hours.iterrows():
        start = row['previous_order'].strftime('%Y-%m-%d %H:%M:%S')
        end = row['order_placed'].strftime('%Y-%m-%d %H:%M:%S')
        closure_start_datetime.append(start)
        closure_end_datetime.append(end)
    return closure_start_datetime, closure_end_datetime