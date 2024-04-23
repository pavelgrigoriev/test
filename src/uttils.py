import csv
from io import StringIO

import numpy as np


def prepare_to_csv(data):
    aggregated_stats = {}
    for stat in data:
        for field, value in stat.items():
            if field != "DataTime":
                # Replace NaN values with 0
                value = 0 if value is None or np.isnan(value) else value
                if field in aggregated_stats:
                    aggregated_stats[field] += value
                else:
                    aggregated_stats[field] = value
    # Prepare CSV data
    csv_data = StringIO()
    fieldnames = ["Field", "Sum"]
    writer = csv.DictWriter(csv_data, fieldnames=fieldnames)
    writer.writeheader()
    for field, sum_value in aggregated_stats.items():
        writer.writerow({"Field": field, "Sum": sum_value})   
    return csv_data