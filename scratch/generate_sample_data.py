import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data():
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(365 * 2)]
    
    # Generate some synthetic sales data with seasonality and trend
    n = len(dates)
    trend = np.linspace(100, 500, n)
    seasonality = 50 * np.sin(2 * np.pi * np.array(range(n)) / 365)
    noise = np.random.normal(0, 20, n)
    sales = trend + seasonality + noise
    
    df = pd.DataFrame({
        'date': dates,
        'sales': sales
    })
    
    output_path = 'files/uploads/sample_sales_data.xlsx'
    df.to_excel(output_path, index=False)
    print(f"Sample data generated at: {output_path}")

if __name__ == "__main__":
    import os
    os.makedirs('files/uploads/', exist_ok=True)
    generate_sales_data()
