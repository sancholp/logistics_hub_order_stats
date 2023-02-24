import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.integrate import quad


def get_daily_distribution(order_data):
    """
    Returns distribution of orders per hour for each day of the week.
    The distribution is obtained using spline interpolation. 
    """
    df = order_data["order_placed"].groupby(order_data["order_placed"].dt.dayofweek)
    orders_placed_per_weekday = [pd.DataFrame(df.get_group(x)) for x in df.groups]
    orders_distributions = []
    for df in orders_placed_per_weekday:
        count = df['order_placed'].groupby(df["order_placed"].dt.hour).count().to_numpy()/5
        count = np.hstack((count, count[-1]))
        dist = interp1d(range(8,23), count, bounds_error=False, fill_value=0, kind='cubic')
        orders_distributions.append(dist)
    return orders_distributions

def orders_expected(t_start, t_end, orders_distributions):
    """
    Calculate the number of orders expected between t_start and t_end.
    Does this by integrating an interpolated distribution of orders placed per time of day,
    also taking into account the day of the week.
    """
    t_start = pd.to_datetime(t_start)
    t_end = pd.to_datetime(t_end)
    weekday = t_start.weekday()
    start_h = t_start.hour + t_start.minute/60 + t_start.second/3600
    end_h = t_end.hour + t_end.minute/60 + t_end.second/3600
    dist = orders_distributions[weekday]
    return quad(dist, start_h, end_h)[0] # Not interested in integration error
