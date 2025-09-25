# CORD-19 Data Explorer

A comprehensive Python-based analysis of the CORD-19 research dataset with an interactive Streamlit web application.

## 📋 Project Overview

This project analyzes COVID-19 research papers from the CORD-19 dataset, providing insights into publication trends, journal distribution, and research focus areas. The analysis includes data cleaning, visualization, and an interactive web application for exploring the findings.

## 🎯 Learning Objectives

- Practice loading and exploring real-world datasets
- Learn basic data cleaning techniques
- Create meaningful visualizations
- Build interactive web applications with Streamlit
- Present data insights effectively

## 📊 Dataset Information

The project works with a sample of the CORD-19 metadata, which contains:
- Paper titles and abstracts
- Publication dates
- Authors and journals
- Source information

**Original Dataset**: [CORD-19 Research Challenge](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge)

## 🛠️ Required Tools

- Python 3.7+
- pandas (data manipulation)
- matplotlib/seaborn (visualization)
- Streamlit (web application)
- wordcloud (text visualization)
- plotly (interactive charts)

## 📁 Project Structure

```
data_analyst/
├── data/
│   └── sample_metadata.csv          # Sample CORD-19 dataset
├── notebooks/
│   └── cord19_analysis.ipynb        # Jupyter notebook for exploration
├── src/
│   └── data_analysis.py             # Main analysis script
├── app.py                           # Streamlit web application
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
└── venv/                           # Virtual environment
```

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd data_analyst
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📈 Usage

### 1. Run Data Analysis

Execute the main analysis script to generate visualizations and insights:

```bash
python src/data_analysis.py
```

This will:
- Load and explore the dataset
- Clean and prepare the data
- Generate visualizations
- Create summary statistics
- Save cleaned data as CSV

### 2. Launch Streamlit Application

Start the interactive web application:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### 3. Explore with Jupyter Notebook

Open the Jupyter notebook for interactive exploration:

```bash
jupyter notebook notebooks/cord19_analysis.ipynb
```

## 🔍 Features

### Data Analysis Script (`src/data_analysis.py`)
- **Data Loading**: Load and explore dataset structure
- **Data Cleaning**: Handle missing values and data type conversions
- **Publication Analysis**: Analyze trends by year and journal
- **Text Analysis**: Word frequency and word cloud generation
- **Visualization**: Multiple chart types for different insights

### Streamlit Application (`app.py`)
- **Interactive Dashboard**: Multi-tab interface for different analyses
- **Filtering**: Filter data by year, journal, and source
- **Visualizations**: Interactive charts using Plotly
- **Search**: Search functionality for titles and abstracts
- **Export**: Download filtered data as CSV

### Key Visualizations
- Publications by year (bar chart)
- Top publishing journals (horizontal bar chart)
- Word cloud of research titles
- Abstract length distribution (histogram)
- Monthly publication trends (line chart)

## 📊 Key Findings

Based on the analysis of the sample dataset:

1. **Temporal Distribution**: Research spans 2020-2022, with 2021 being the most active year
2. **Research Focus**: Strong emphasis on COVID-19, health, vaccines, and pandemic-related topics
3. **Journal Diversity**: Publications across multiple journals, with Nature Digital Medicine being most active
4. **Content Characteristics**: Abstracts average 8.3 words, indicating concise summaries

## 🎨 Visualizations Generated

- `publications_by_year.png` - Bar chart of publications by year
- `top_journals.png` - Horizontal bar chart of top journals
- `wordcloud_titles.png` - Word cloud of research titles
- `abstract_length_distribution.png` - Histogram of abstract lengths
- `source_distribution.png` - Pie chart of paper sources

## 🔧 Technical Details

### Data Processing
- Handles missing values appropriately
- Converts date columns to datetime format
- Creates derived features (word counts, year extraction)
- Implements text preprocessing for word analysis

### Visualization
- Uses matplotlib and seaborn for static plots
- Implements Plotly for interactive charts in Streamlit
- Generates word clouds for text analysis
- Creates publication timeline visualizations

### Web Application
- Responsive design with sidebar filters
- Multi-tab interface for organized content
- Real-time data filtering and search
- Export functionality for processed data

## 📚 Dependencies

See `requirements.txt` for complete list:
- pandas>=2.3.2
- matplotlib>=3.10.6
- seaborn>=0.13.2
- streamlit>=1.50.0
- wordcloud>=1.9.4
- plotly>=6.3.0

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes as part of the Python Frameworks Assignment.

## 📞 Contact

For questions or issues, please open an issue in the repository.

---

**Note**: This project uses a sample dataset for demonstration purposes. For production use, download the full CORD-19 dataset from the official source.
# data
