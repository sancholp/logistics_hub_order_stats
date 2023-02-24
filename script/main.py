import pandas as pd
import prepare_data as prep
import infer_closures as inf
import missed_orders as miss


def main():
    """
    Main script function.
    Writes closures.csv file containing time intervals at which dark store was abnormally closed,
    along with expected orders to have been received in that time.
    """
    input = pd.read_csv("data/orders.csv", usecols=['order_placed']) # Only interested in orderes placed

    order_data = prep.clean_data(input)
    data_per_day = prep.split_per_day(order_data) # Don't want gaps between days to be counted
    hub_closed_threshold = inf.define_closure(data_per_day, num_sigma=3) # Define closed as timedelta > μ + 3σ
    data_with_diff = [inf.get_times_between_orders(data) for data in data_per_day]
    # Calculate times of abnormal store closures 
    closure_start_datetime = []
    closure_end_datetime = []
    for df in data_with_diff:
        closure_starts, closure_ends = inf.get_closed_intervals(df, hub_closed_threshold)
        closure_start_datetime.extend(closure_starts)
        closure_end_datetime.extend(closure_ends)
    # Calculate orders missed during the abnormal closures
    orders_distributions = miss.get_daily_distribution(order_data) # Hourly distribution of orders placed per weekday
    number_missed_orders = []
    for closure in zip(closure_start_datetime, closure_end_datetime):
        missed_orders = miss.orders_expected(closure[0], closure[1], orders_distributions)
        number_missed_orders.append(missed_orders)

    output = pd.DataFrame({
        "closure_start_datetime": closure_start_datetime,
        "closure_end_datetime": closure_end_datetime,
        "number_missed_orders": number_missed_orders
    })
    output.to_csv("output/closures.csv")

if __name__ == "__main__":
    main()