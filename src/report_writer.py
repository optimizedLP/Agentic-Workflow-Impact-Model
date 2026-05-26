import os
import matplotlib.pyplot as plt
import seaborn as sns
from data_pipeline import load_events_data
from event_study_model import run_impact_model

# Set visual style for charts
sns.set_theme(style="whitegrid")

def generate_visual_report(result_dict, output_dir="output/"):
    """
    Generates a venture-style quantitative chart and memo.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ticker = result_dict['Ticker']
    car = result_dict['CAR']
    abnormal_returns = result_dict['Abnormal_Returns']
    
    # 1. Generate the Chart
    plt.figure(figsize=(10, 6))
    
    # Plot the cumulative sum of abnormal returns over the event window
    cumulative_ar = abnormal_returns.cumsum()
    plt.plot(cumulative_ar.index, cumulative_ar.values, marker='o', color='#2ca02c', linewidth=2)
    
    # Formatting the chart
    plt.axhline(0, color='black', linewidth=1, linestyle='--') # Baseline
    plt.title(f"Market Impact Analysis: {ticker}", fontsize=14, fontweight='bold')
    plt.ylabel("Cumulative Abnormal Return (CAR)", fontsize=12)
    plt.xlabel("Date", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save chart
    chart_filename = f"{output_dir}{ticker}_impact_chart.png"
    plt.savefig(chart_filename)
    plt.close()
    
    # 2. Generate the Text Memo
    memo = f"""
    MARKET IMPACT EVALUATION MEMO
    --------------------------------------------------
    TICKER: {ticker}
    NET MARKET IMPACT (CAR): {car:.2%}
    MARKET BETA (Correlation to NASDAQ): {result_dict['Beta']:.2f}
    
    THESIS SUMMARY:
    Based on a 252-day OLS regression against the NASDAQ benchmark, 
    the asset exhibited a Cumulative Abnormal Return (CAR) of {car:.2%} 
    over the event window. 
    
    {'Positive market validation detected.' if car > 0 else 'Market reaction was muted or negative, indicating the event was priced in or poorly received.'}
    --------------------------------------------------
    """
    
    # Save Memo
    memo_filename = f"{output_dir}{ticker}_evaluation_memo.txt"
    with open(memo_filename, "w") as f:
        f.write(memo)
        
    print(f"Generated report for {ticker}. Saved to {output_dir}")

if __name__ == "__main__":
    # Orchestrate the entire pipeline
    print("Starting Quantitative Pipeline...")
    
    # Load the events
    events_df = load_events_data()
    
    # Process each event
    for index, row in events_df.iterrows():
        try:
            print(f"\nProcessing event for {row['Ticker']} on {row['Event_Date'].date()}...")
            
            # Run the math model (from event_study_model.py)
            result = run_impact_model(
                ticker=row['Ticker'], 
                event_date=row['Event_Date']
            )
            
            # Generate the final reports
            generate_visual_report(result)
            
        except Exception as e:
            print(f"Failed to process {row['Ticker']}: {e}")
            
    print("\nPipeline execution complete. Check the /output directory.")