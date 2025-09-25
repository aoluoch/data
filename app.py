"""
CORD-19 Data Explorer - Streamlit Application
Interactive web application for exploring COVID-19 research data.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
import numpy as np

# Page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the dataset."""
    try:
        df = pd.read_csv('data/sample_metadata.csv')
        # Clean the data
        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        df['year'] = df['publish_time'].dt.year
        df['abstract_word_count'] = df['abstract'].apply(
            lambda x: len(str(x).split()) if pd.notna(x) and x != '' else 0
        )
        df['title_word_count'] = df['title'].apply(
            lambda x: len(str(x).split()) if pd.notna(x) and x != '' else 0
        )
        return df
    except FileNotFoundError:
        st.error("Data file not found. Please ensure 'data/sample_metadata.csv' exists.")
        return None

def create_word_cloud(text):
    """Create a word cloud from text."""
    if not text or text.strip() == '':
        return None
    
    # Clean and prepare text
    words = re.findall(r'\b\w+\b', text.lower())
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
                  'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 
                  'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
    words = [word for word in words if word not in stop_words and len(word) > 2]
    
    if not words:
        return None
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                         max_words=100, colormap='viridis').generate(' '.join(words))
    return wordcloud

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🔬 CORD-19 Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive exploration of COVID-19 research papers")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.header("🔍 Filters & Controls")
    
    # Year filter
    years = sorted(df['year'].dropna().unique())
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=years,
        default=years
    )
    
    # Journal filter
    journals = df['journal'].unique()
    selected_journals = st.sidebar.multiselect(
        "Select Journals",
        options=journals,
        default=journals
    )
    
    # Source filter
    sources = df['source'].unique()
    selected_sources = st.sidebar.multiselect(
        "Select Sources",
        options=sources,
        default=sources
    )
    
    # Filter data based on selections
    filtered_df = df[
        (df['year'].isin(selected_years)) &
        (df['journal'].isin(selected_journals)) &
        (df['source'].isin(selected_sources))
    ]
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Trends", "📚 Journals", "🔤 Text Analysis", "📋 Data Table"])
    
    with tab1:
        st.header("📊 Dataset Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Papers", len(filtered_df))
        
        with col2:
            st.metric("Unique Journals", filtered_df['journal'].nunique())
        
        with col3:
            st.metric("Date Range", f"{filtered_df['year'].min()}-{filtered_df['year'].max()}")
        
        with col4:
            avg_abstract_length = filtered_df['abstract_word_count'].mean()
            st.metric("Avg Abstract Length", f"{avg_abstract_length:.1f} words")
        
        # Publications by year chart
        st.subheader("📈 Publications by Year")
        year_counts = filtered_df['year'].value_counts().sort_index()
        
        fig = px.bar(
            x=year_counts.index, 
            y=year_counts.values,
            title="Number of Publications by Year",
            labels={'x': 'Year', 'y': 'Number of Publications'},
            color=year_counts.values,
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top journals
        st.subheader("🏆 Top Publishing Journals")
        journal_counts = filtered_df['journal'].value_counts().head(10)
        
        fig = px.bar(
            x=journal_counts.values,
            y=journal_counts.index,
            orientation='h',
            title="Top 10 Journals by Publication Count",
            labels={'x': 'Number of Publications', 'y': 'Journal'},
            color=journal_counts.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("📈 Publication Trends")
        
        # Time series analysis
        st.subheader("📅 Publication Timeline")
        monthly_data = filtered_df.groupby(filtered_df['publish_time'].dt.to_period('M')).size()
        
        fig = px.line(
            x=monthly_data.index.astype(str),
            y=monthly_data.values,
            title="Monthly Publication Trends",
            labels={'x': 'Month', 'y': 'Number of Publications'}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Abstract length over time
        st.subheader("📏 Abstract Length Trends")
        abstract_trend = filtered_df.groupby('year')['abstract_word_count'].mean()
        
        fig = px.line(
            x=abstract_trend.index,
            y=abstract_trend.values,
            title="Average Abstract Length by Year",
            labels={'x': 'Year', 'y': 'Average Word Count'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.header("📚 Journal Analysis")
        
        # Journal distribution
        st.subheader("📊 Journal Distribution")
        journal_dist = filtered_df['journal'].value_counts()
        
        fig = px.pie(
            values=journal_dist.values,
            names=journal_dist.index,
            title="Distribution of Papers by Journal"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Journal performance metrics
        st.subheader("📈 Journal Performance Metrics")
        journal_metrics = filtered_df.groupby('journal').agg({
            'title': 'count',
            'abstract_word_count': 'mean',
            'year': ['min', 'max']
        }).round(2)
        
        journal_metrics.columns = ['Paper Count', 'Avg Abstract Length', 'First Year', 'Last Year']
        st.dataframe(journal_metrics, use_container_width=True)
    
    with tab4:
        st.header("🔤 Text Analysis")
        
        # Word frequency analysis
        st.subheader("📝 Most Frequent Words in Titles")
        
        # Combine all titles
        all_titles = ' '.join(filtered_df['title'].dropna().astype(str))
        
        # Analyze word frequency
        words = re.findall(r'\b\w+\b', all_titles.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 
                      'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 
                      'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'}
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        if words:
            word_counts = Counter(words)
            top_words = word_counts.most_common(20)
            
            # Create bar chart
            words_df = pd.DataFrame(top_words, columns=['Word', 'Count'])
            fig = px.bar(
                words_df,
                x='Count',
                y='Word',
                orientation='h',
                title="Top 20 Most Frequent Words in Titles",
                labels={'Count': 'Frequency', 'Word': 'Word'}
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Word cloud
            st.subheader("☁️ Word Cloud")
            wordcloud = create_word_cloud(all_titles)
            if wordcloud:
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                ax.set_title('Word Cloud of Research Paper Titles', fontsize=16, fontweight='bold')
                st.pyplot(fig)
        
        # Abstract length distribution
        st.subheader("📏 Abstract Length Distribution")
        fig = px.histogram(
            filtered_df,
            x='abstract_word_count',
            nbins=20,
            title="Distribution of Abstract Word Count",
            labels={'abstract_word_count': 'Word Count', 'count': 'Frequency'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("📋 Data Table")
        
        # Display filtered data
        st.subheader("📊 Filtered Dataset")
        st.write(f"Showing {len(filtered_df)} papers")
        
        # Search functionality
        search_term = st.text_input("🔍 Search in titles and abstracts:")
        if search_term:
            search_mask = (
                filtered_df['title'].str.contains(search_term, case=False, na=False) |
                filtered_df['abstract'].str.contains(search_term, case=False, na=False)
            )
            filtered_df = filtered_df[search_mask]
            st.write(f"Found {len(filtered_df)} papers matching '{search_term}'")
        
        # Display data
        display_columns = ['title', 'authors', 'journal', 'publish_time', 'abstract_word_count']
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name=f"cord19_filtered_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("### 📚 About This Application")
    st.markdown("""
    This interactive dashboard explores the CORD-19 research dataset, providing insights into:
    - Publication trends over time
    - Journal distribution and performance
    - Text analysis of research papers
    - Interactive filtering and search capabilities
    
    **Data Source**: CORD-19 Research Challenge (Allen Institute for AI)
    """)

if __name__ == "__main__":
    main()
