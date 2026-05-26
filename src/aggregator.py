import os
import re
import pandas as pd

def aggregate_memos(output_dir="output/", save_path="output/final_thesis_data.csv"):
    """
    Parses all evaluation memos using regular expressions and compiles 
    the metrics into a master dataset for portfolio analysis.
    """
    print("Starting data extraction pipeline...")
    data = []
    
    # Define the regex patterns to isolate the exact values
    ticker_pattern = re.compile(r"TICKER:\s*([A-Z]+)")
    car_pattern = re.compile(r"NET MARKET IMPACT \(CAR\):\s*([-\d\.]+)%")
    beta_pattern = re.compile(r"MARKET BETA \(Correlation to NASDAQ\):\s*([-\d\.]+)")

    # Sweep the directory for memo files
    for filename in os.listdir(output_dir):
        if filename.endswith("_evaluation_memo.txt"):
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, "r") as file:
                content = file.read()
                
                # Extract the data
                ticker_match = ticker_pattern.search(content)
                car_match = car_pattern.search(content)
                beta_match = beta_pattern.search(content)

                if ticker_match and car_match and beta_match:
                    data.append({
                        "Ticker": ticker_match.group(1),
                        "CAR_Percentage": float(car_match.group(1)),
                        "Beta": float(beta_match.group(1))
                    })
    
    # Convert to DataFrame and sort by the highest market impact
    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values(by="CAR_Percentage", ascending=False).reset_index(drop=True)
        df.to_csv(save_path, index=False)
        
        print(f"Successfully aggregated {len(df)} companies into {save_path}\n")
        print("--- TOP 3 AI VALUE DRIVERS ---")
        print(df.head(3))
        print("------------------------------")
    else:
        print("No memo files found to process.")

if __name__ == "__main__":
    aggregate_memos()