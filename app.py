import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page layout
st.set_page_config(page_title="Venture AI Thesis", layout="wide")

st.title("Enterprise AI: Market Impact Evaluator")
st.markdown("Quantifying the statistical value-creation of autonomous agent and generative AI integrations.")

# Load the aggregated data
data_path = "output/final_thesis_data.csv"
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    
    # --- INTERACTIVE CONTROLS (THE MERGE) ---
    st.sidebar.header("Thesis Parameters")
    st.sidebar.markdown("Filter the market noise to identify true alpha drivers.")
    
    # Get dynamic bounds for the slider based on your actual data
    min_car = float(df['CAR_Percentage'].min())
    max_car = float(df['CAR_Percentage'].max())
    
    # Interactive Slider
    min_car_filter = st.sidebar.slider(
        "Minimum Market Impact (CAR %)", 
        min_value=min_car, 
        max_value=max_car, 
        value=min_car,  # Default to showing everything
        step=0.5
    )
    
    # Filter the dataframe dynamically based on the slider input
    filtered_df = df[df['CAR_Percentage'] >= min_car_filter]
    # ----------------------------------------
    
    # Top-level metrics (Now recalculate dynamically based on the filtered data)
    avg_car = filtered_df['CAR_Percentage'].mean() if not filtered_df.empty else 0
    win_rate = (len(filtered_df[filtered_df['CAR_Percentage'] > 0]) / len(filtered_df)) * 100 if not filtered_df.empty else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Events in View", len(filtered_df))
    col2.metric("Average Market Impact (CAR)", f"{avg_car:.2f}%")
    col3.metric("Positive Reaction Rate", f"{win_rate:.1f}%")
    
    st.divider()
    
    if not filtered_df.empty:
        # Interactive Bar Chart
        st.subheader("Cumulative Abnormal Returns by Ticker")
        fig_bar = px.bar(
            filtered_df, x="Ticker", y="CAR_Percentage", 
            color="CAR_Percentage", color_continuous_scale="RdYlGn",
            labels={"CAR_Percentage": "Net Market Impact (%)"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Scatter Plot: Risk vs. Reward
        st.subheader("Risk vs. Reward: Market Beta vs. Event Impact")
        fig_scatter = px.scatter(
            filtered_df, x="Beta", y="CAR_Percentage", text="Ticker",
            color="CAR_Percentage", color_continuous_scale="RdYlGn",
            labels={"Beta": "Market Beta (Volatility)", "CAR_Percentage": "Impact (CAR %)"}
        )
        fig_scatter.update_traces(textposition='top center')
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("No data matches the selected filter criteria. Lower the minimum CAR requirement in the sidebar.")

else:
    st.warning("Data not found. Please run `python src/aggregator.py` first.")