import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="GTIS - Global Trend Intelligence",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://backend:8000"

st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stMetric { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; color: white; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🌐 GTIS")
    st.markdown("### Global Trend Intelligence System")
    
    page = st.selectbox(
        "Navigation",
        ["📊 Trend Analysis", "🔮 Predictions", "🗺️ Regional Interest", 
         "🔗 Correlations", "🎯 Emerging Topics"]
    )
    
    st.markdown("---")
    st.markdown("### Settings")
    timeframe = st.selectbox(
        "Timeframe",
        ["today 1-m", "today 3-m", "today 12-m", "today 5-y"],
        index=2
    )
    
    st.markdown("---")
    st.info("💡 Powered by AI & ML")

def call_api(endpoint, method="GET", data=None):
    url = f"{API_BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

st.title(f"{page}")

if page == "📊 Trend Analysis":
    st.markdown("### Compare Search Trends")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        keywords_input = st.text_input(
            "Enter keywords (comma-separated)",
            "artificial intelligence, machine learning, data science"
        )
        keywords = [k.strip() for k in keywords_input.split(",")]
    
    with col2:
        geo = st.text_input("Country Code (optional)", "")
    
    if st.button("🔍 Fetch Trends", type="primary"):
        with st.spinner("Fetching data from Google Trends..."):
            result = call_api("/api/fetch-trends", "POST", {
                "keywords": keywords,
                "timeframe": timeframe,
                "geo": geo
            })
            
            if result and result.get('status') == 'success':
                df = pd.DataFrame(result['data'])
                
                cols = st.columns(len(keywords))
                for idx, keyword in enumerate(keywords):
                    if keyword in df.columns:
                        avg_interest = df[keyword].mean()
                        cols[idx].metric(keyword, f"{avg_interest:.1f}", "Average Interest")
                
                fig = go.Figure()
                for keyword in keywords:
                    if keyword in df.columns:
                        fig.add_trace(go.Scatter(
                            x=df['date'],
                            y=df[keyword],
                            mode='lines',
                            name=keyword,
                            line=dict(width=2)
                        ))
                
                fig.update_layout(
                    title="Interest Over Time",
                    xaxis_title="Date",
                    yaxis_title="Interest Score",
                    height=500,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander("📋 View Raw Data"):
                    st.dataframe(df, use_container_width=True)

elif page == "🔮 Predictions":
    st.markdown("### Forecast Future Trends")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        keyword = st.text_input("Enter keyword to predict", "artificial intelligence")
    
    with col2:
        periods = st.slider("Prediction Days", 7, 90, 30)
    
    if st.button("🎯 Generate Predictions", type="primary"):
        with st.spinner("Running ML models..."):
            result = call_api("/api/predict-trends", "POST", {
                "keyword": keyword,
                "periods": periods
            })
            
            if result and result.get('status') == 'success':
                predictions = result['predictions']
                
                st.markdown("### Model Performance")
                metrics = result.get('model_performance', {})
                cols = st.columns(3)
                
                for idx, (model_name, metric) in enumerate(metrics.items()):
                    with cols[idx % 3]:
                        st.metric(
                            f"{model_name.upper()}",
                            f"MAPE: {metric.get('mape', 0):.2%}",
                            f"RMSE: {metric.get('rmse', 0):.2f}"
                        )
                
                fig = go.Figure()
                
                for model_name, pred in predictions.items():
                    if 'values' in pred:
                        fig.add_trace(go.Scatter(
                            x=pred['dates'],
                            y=pred['values'],
                            mode='lines+markers',
                            name=model_name.capitalize(),
                            line=dict(width=2)
                        ))
                
                fig.update_layout(
                    title=f"Predictions for '{keyword}'",
                    xaxis_title="Date",
                    yaxis_title="Predicted Interest",
                    height=500,
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)

elif page == "🗺️ Regional Interest":
    st.markdown("### Geographic Distribution")
    
    keyword = st.text_input("Enter keyword", "technology")
    
    if st.button("🌍 Analyze Regions", type="primary"):
        with st.spinner("Fetching regional data..."):
            result = call_api(f"/api/regional-interest/{keyword}")
            
            if result and result.get('status') == 'success':
                df = pd.DataFrame(result['regional_data'])
                
                if not df.empty:
                    fig = px.bar(
                        df.head(20),
                        x=keyword,
                        y=df.index[:20],
                        orientation='h',
                        title=f"Top 20 Regions for '{keyword}'",
                        labels={keyword: "Interest Score", "index": "Country"}
                    )
                    
                    fig.update_layout(height=600)
                    st.plotly_chart(fig, use_container_width=True)

elif page == "🔗 Correlations":
    st.markdown("### Cross-Domain Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        keyword = st.text_input("Keyword", "stock market")
    
    with col2:
        external_source = st.selectbox(
            "External Data Source",
            ["financial_markets", "job_postings", "social_media"]
        )
    
    if st.button("📊 Compute Correlations", type="primary"):
        with st.spinner("Analyzing correlations..."):
            result = call_api("/api/correlations", "POST", {
                "keyword": keyword,
                "external_data_source": external_source
            })
            
            if result and result.get('status') == 'success':
                st.success(f"✅ {result.get('best_correlation', {}).get('interpretation', '')}")
                
                corr_data = result.get('correlations', [])
                df = pd.DataFrame(corr_data)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df['lag'],
                    y=df['pearson_correlation'],
                    mode='lines+markers',
                    name='Pearson',
                    line=dict(color='blue', width=2)
                ))
                
                fig.update_layout(
                    title="Correlation by Lag",
                    xaxis_title="Lag (days)",
                    yaxis_title="Correlation Coefficient",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)

elif page == "🎯 Emerging Topics":
    st.markdown("### Detect Rising Trends")
    
    if st.button("🔍 Find Emerging Topics", type="primary"):
        with st.spinner("Scanning for emerging trends..."):
            result = call_api("/api/emerging-topics")
            
            if result and result.get('status') == 'success':
                topics = result.get('emerging_topics', [])
                
                if topics:
                    st.markdown("### 🔥 Trending Now")
                    
                    for idx, topic in enumerate(topics[:10], 1):
                        st.markdown(f"**{idx}.** {topic}")
                else:
                    st.info("No emerging topics detected at this time.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Built with ❤️ using FastAPI, Streamlit & ML</div>",
    unsafe_allow_html=True
)
