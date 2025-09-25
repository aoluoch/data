"""
CORD-19 Data Analysis Script
This script performs comprehensive analysis of the CORD-19 research dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from collections import Counter
import re

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class CORD19Analyzer:
    """Class to handle CORD-19 dataset analysis."""
    
    def __init__(self, data_path):
        """Initialize the analyzer with data path."""
        self.data_path = data_path
        self.df = None
        self.cleaned_df = None
        
    def load_data(self):
        """Load the dataset from CSV file."""
        print("Loading CORD-19 dataset...")
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset loaded successfully! Shape: {self.df.shape}")
        return self.df
    
    def basic_exploration(self):
        """Perform basic data exploration."""
        print("\n" + "="*50)
        print("BASIC DATA EXPLORATION")
        print("="*50)
        
        # Dataset dimensions
        print(f"Dataset shape: {self.df.shape}")
        print(f"Number of rows: {self.df.shape[0]}")
        print(f"Number of columns: {self.df.shape[1]}")
        
        # Column information
        print("\nColumn Information:")
        print(self.df.info())
        
        # First few rows
        print("\nFirst 5 rows:")
        print(self.df.head())
        
        # Data types
        print("\nData Types:")
        print(self.df.dtypes)
        
        # Missing values
        print("\nMissing Values:")
        missing_data = self.df.isnull().sum()
        missing_percent = (missing_data / len(self.df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing_data,
            'Missing Percentage': missing_percent
        })
        print(missing_df[missing_df['Missing Count'] > 0])
        
        # Basic statistics for numerical columns
        print("\nBasic Statistics:")
        print(self.df.describe())
        
        return self.df
    
    def clean_data(self):
        """Clean and prepare the data for analysis."""
        print("\n" + "="*50)
        print("DATA CLEANING")
        print("="*50)
        
        # Create a copy for cleaning
        self.cleaned_df = self.df.copy()
        
        # Handle missing values in abstracts
        print("Handling missing values in abstracts...")
        self.cleaned_df['abstract'] = self.cleaned_df['abstract'].fillna('')
        
        # Convert publish_time to datetime
        print("Converting publish_time to datetime...")
        self.cleaned_df['publish_time'] = pd.to_datetime(self.cleaned_df['publish_time'], errors='coerce')
        
        # Extract year from publish_time
        print("Extracting year from publish_time...")
        self.cleaned_df['year'] = self.cleaned_df['publish_time'].dt.year
        
        # Create abstract word count
        print("Creating abstract word count...")
        self.cleaned_df['abstract_word_count'] = self.cleaned_df['abstract'].apply(
            lambda x: len(str(x).split()) if pd.notna(x) and x != '' else 0
        )
        
        # Create title word count
        print("Creating title word count...")
        self.cleaned_df['title_word_count'] = self.cleaned_df['title'].apply(
            lambda x: len(str(x).split()) if pd.notna(x) and x != '' else 0
        )
        
        # Remove rows with missing critical data
        print("Removing rows with missing critical data...")
        initial_count = len(self.cleaned_df)
        self.cleaned_df = self.cleaned_df.dropna(subset=['title', 'publish_time'])
        final_count = len(self.cleaned_df)
        print(f"Removed {initial_count - final_count} rows with missing critical data")
        
        print(f"Cleaned dataset shape: {self.cleaned_df.shape}")
        return self.cleaned_df
    
    def analyze_publications_by_year(self):
        """Analyze publications by year."""
        print("\n" + "="*50)
        print("PUBLICATIONS BY YEAR ANALYSIS")
        print("="*50)
        
        # Count publications by year
        year_counts = self.cleaned_df['year'].value_counts().sort_index()
        print("Publications by year:")
        print(year_counts)
        
        # Create visualization
        plt.figure(figsize=(12, 6))
        year_counts.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title('Number of COVID-19 Publications by Year', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Number of Publications', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('publications_by_year.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return year_counts
    
    def analyze_top_journals(self):
        """Analyze top publishing journals."""
        print("\n" + "="*50)
        print("TOP PUBLISHING JOURNALS ANALYSIS")
        print("="*50)
        
        # Count publications by journal
        journal_counts = self.cleaned_df['journal'].value_counts().head(10)
        print("Top 10 journals by publication count:")
        print(journal_counts)
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        journal_counts.plot(kind='barh', color='lightcoral', edgecolor='black')
        plt.title('Top 10 Journals Publishing COVID-19 Research', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Publications', fontsize=12)
        plt.ylabel('Journal', fontsize=12)
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.savefig('top_journals.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return journal_counts
    
    def analyze_word_frequency(self):
        """Analyze word frequency in titles."""
        print("\n" + "="*50)
        print("WORD FREQUENCY ANALYSIS")
        print("="*50)
        
        # Combine all titles
        all_titles = ' '.join(self.cleaned_df['title'].dropna().astype(str))
        
        # Clean and tokenize
        words = re.findall(r'\b\w+\b', all_titles.lower())
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequency
        word_counts = Counter(words)
        top_words = word_counts.most_common(20)
        
        print("Top 20 most frequent words in titles:")
        for word, count in top_words:
            print(f"{word}: {count}")
        
        # Create word cloud
        plt.figure(figsize=(15, 8))
        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                            max_words=100, colormap='viridis').generate(all_titles)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Word Cloud of COVID-19 Research Paper Titles', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('wordcloud_titles.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return top_words
    
    def analyze_abstract_length(self):
        """Analyze abstract length distribution."""
        print("\n" + "="*50)
        print("ABSTRACT LENGTH ANALYSIS")
        print("="*50)
        
        # Calculate statistics
        abstract_stats = self.cleaned_df['abstract_word_count'].describe()
        print("Abstract word count statistics:")
        print(abstract_stats)
        
        # Create visualization
        plt.figure(figsize=(12, 6))
        plt.hist(self.cleaned_df['abstract_word_count'], bins=20, color='lightgreen', 
                edgecolor='black', alpha=0.7)
        plt.title('Distribution of Abstract Word Count', fontsize=16, fontweight='bold')
        plt.xlabel('Word Count', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('abstract_length_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return abstract_stats
    
    def analyze_sources(self):
        """Analyze paper sources."""
        print("\n" + "="*50)
        print("SOURCE ANALYSIS")
        print("="*50)
        
        # Count papers by source
        source_counts = self.cleaned_df['source'].value_counts()
        print("Papers by source:")
        print(source_counts)
        
        # Create visualization
        plt.figure(figsize=(10, 6))
        source_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribution of Papers by Source', fontsize=16, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig('source_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return source_counts
    
    def generate_summary_report(self):
        """Generate a summary report of findings."""
        print("\n" + "="*50)
        print("SUMMARY REPORT")
        print("="*50)
        
        print(f"Total number of papers analyzed: {len(self.cleaned_df)}")
        print(f"Date range: {self.cleaned_df['publish_time'].min().year} - {self.cleaned_df['publish_time'].max().year}")
        print(f"Most active year: {self.cleaned_df['year'].mode().iloc[0]}")
        print(f"Average abstract length: {self.cleaned_df['abstract_word_count'].mean():.1f} words")
        print(f"Most common journal: {self.cleaned_df['journal'].mode().iloc[0]}")
        print(f"Primary source: {self.cleaned_df['source'].mode().iloc[0]}")
        
        # Save cleaned dataset
        self.cleaned_df.to_csv('cleaned_cord19_data.csv', index=False)
        print("\nCleaned dataset saved as 'cleaned_cord19_data.csv'")

def main():
    """Main function to run the analysis."""
    # Initialize analyzer
    analyzer = CORD19Analyzer('data/sample_metadata.csv')
    
    # Load data
    analyzer.load_data()
    
    # Basic exploration
    analyzer.basic_exploration()
    
    # Clean data
    analyzer.clean_data()
    
    # Perform analyses
    analyzer.analyze_publications_by_year()
    analyzer.analyze_top_journals()
    analyzer.analyze_word_frequency()
    analyzer.analyze_abstract_length()
    analyzer.analyze_sources()
    
    # Generate summary
    analyzer.generate_summary_report()
    
    print("\nAnalysis completed successfully!")

if __name__ == "__main__":
    main()
