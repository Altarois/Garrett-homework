import argparse
import pandas as pd


# function that calculate minutes for call duration that intersect with both tarification
def duration_intersection(time, flag_time, minutes):
    tarification_start_time_minutes = (time - flag_time).total_seconds() // 60
    tarification_end_time_minutes = minutes - tarification_start_time_minutes
    return tarification_end_time_minutes, tarification_start_time_minutes, 0


# function that calculate minutes including bonus for call duration that intersect with both tarification
def bonus_duration_intersection(time, flag_time, minutes):
    tarification_start_time_minutes = (
        time + pd.Timedelta(minutes=5) - flag_time
    ).total_seconds() // 60
    tarification_end_time_minutes = 5 - tarification_start_time_minutes
    bonus_minutes = minutes - 5
    return tarification_end_time_minutes, tarification_start_time_minutes, bonus_minutes


# function that return minute types based on their tarification
def compute_minute_types(start, end):
    minutes = ((end - start).total_seconds() - 1) // 60
    tarification_start_time = start.replace(hour=8, minute=0, second=0)
    tarification_end_time = start.replace(hour=16, minute=0, second=0)

    tarification_end_time_minutes, tarification_start_time_minutes, bonus_minutes = (
        0,
        0,
        0,
    )

    # minutes calculation for long calls
    if minutes > 5:
        if start < tarification_start_time or start >= tarification_end_time:
            # from second tarification to first tarification
            if end > tarification_start_time and end < tarification_end_time:
                if start + pd.Timedelta(minutes=5) > tarification_start_time:
                    return bonus_duration_intersection(
                        start, tarification_start_time, minutes
                    )
            tarification_end_time_minutes = 5
            bonus_minutes = minutes - 5

        elif start > tarification_start_time and start < tarification_end_time:
            # from first tarification to second tarification
            if end > tarification_end_time:
                if start + pd.Timedelta(minutes=5) > tarification_end_time:
                    return bonus_duration_intersection(
                        start, tarification_end_time, minutes
                    )
            tarification_start_time_minutes = 5
            bonus_minutes = minutes - 5

    # minutes calculation for short calls
    else:
        if start < tarification_start_time or start >= tarification_end_time:
            # from second tarification to first tarification
            if end > tarification_start_time and end < tarification_end_time:
                return duration_intersection(end, tarification_start_time, minutes)
            tarification_end_time_minutes = minutes
        elif start > tarification_start_time and start < tarification_end_time:
            # from first tarification to second tarification
            if end > tarification_end_time:
                return duration_intersection(tarification_end_time, start, minutes)
            tarification_start_time_minutes = minutes

    return tarification_end_time_minutes, tarification_start_time_minutes, bonus_minutes


def main():
    column_names = ["number", "start", "end"]

    # adding a parser to choose the file as argument in the command ( default is set on generated_sample_2.csv)
    parser = argparse.ArgumentParser(description="Call Cost Calculator")
    parser.add_argument(
        "filename",
        nargs="?",
        default="generated_sample_2.csv",
        help="Path to the input file",
    )

    args = parser.parse_args()

    # Read the CSV file into a DataFrame with custom column names
    df = pd.read_csv(args.filename, header=None, names=column_names)

    # Convert "start" and "end" columns to datetime
    df["start"] = pd.to_datetime(df["start"])
    df["end"] = pd.to_datetime(df["end"])

    # Find the most frequent number to apply the discount
    most_frequent_number = df["number"].value_counts().idxmax()

    # Initialize the total cost of the calls in the csv file
    total_cost = 0

    for index, row in df.iterrows():
        if row["number"] == most_frequent_number:
            continue
        day, night, bonus = compute_minute_types(
            row["start"], pd.to_datetime(row["end"])
        )
        total_cost += 0.5 * night + 1 * day + 0.2 * bonus

    print("Total cost:", total_cost, "CZK")


if __name__ == "__main__":
    main()
