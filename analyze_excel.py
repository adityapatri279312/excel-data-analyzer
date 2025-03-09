import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

# Set style for plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)

def load_data(file_path):
    """Load data from Excel file"""
    print(f"Loading data from {file_path}...")
    return pd.read_excel(file_path)

def basic_summary(df):
    """Generate basic summary of dataframe"""
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "numeric_columns": list(df.select_dtypes(include=np.number).columns),
        "categorical_columns": list(df.select_dtypes(include=['object', 'category']).columns),
        "datetime_columns": list(df.select_dtypes(include=['datetime']).columns)
    }
    return summary

def generate_descriptive_stats(df):
    """Generate descriptive statistics for numeric columns"""
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    if len(numeric_cols) == 0:
        return None
    
    # Calculate statistics
    stats = df[numeric_cols].describe().transpose()
    stats['range'] = stats['max'] - stats['min']
    stats['median'] = df[numeric_cols].median()
    stats['skew'] = df[numeric_cols].skew()
    stats['kurtosis'] = df[numeric_cols].kurtosis()
    
    return stats

def create_visualizations(df, output_dir):
    """Create various visualizations based on data types"""
    os.makedirs(output_dir, exist_ok=True)
    visualization_paths = []
    
    # Get column types
    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    
    # 1. Distribution plots for numeric columns (limit to first 10)
    if len(numeric_cols) > 0:
        for i, col in enumerate(numeric_cols[:10]):
            plt.figure(figsize=(10, 6))
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f'Distribution of {col}')
            plt.tight_layout()
            
            file_path = os.path.join(output_dir, f'distribution_{col}.png')
            plt.savefig(file_path)
            plt.close()
            visualization_paths.append((f'Distribution of {col}', file_path))
    
    # 2. Count plots for categorical columns (limit to first 10)
    if len(categorical_cols) > 0:
        for i, col in enumerate(categorical_cols[:10]):
            # Only plot if there are fewer than 30 unique values
            if df[col].nunique() < 30:
                plt.figure(figsize=(12, 8))
                value_counts = df[col].value_counts().sort_values(ascending=False)
                
                # If there are more than 15 categories, take only top 15
                if len(value_counts) > 15:
                    value_counts = value_counts.head(15)
                    plt.title(f'Top 15 Categories in {col}')
                else:
                    plt.title(f'Categories in {col}')
                
                sns.barplot(x=value_counts.index, y=value_counts.values)
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                file_path = os.path.join(output_dir, f'categorical_{col}.png')
                plt.savefig(file_path)
                plt.close()
                visualization_paths.append((f'Categories in {col}', file_path))
    
    # 3. Correlation heatmap (if at least 2 numeric columns)
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(12, 10))
        correlation = df[numeric_cols].corr()
        mask = np.triu(correlation)
        sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', 
                    mask=mask, vmin=-1, vmax=1)
        plt.title('Correlation Between Numeric Variables')
        plt.tight_layout()
        
        file_path = os.path.join(output_dir, 'correlation_heatmap.png')
        plt.savefig(file_path)
        plt.close()
        visualization_paths.append(('Correlation Heatmap', file_path))
    
    # 4. If there are at least 2 numeric columns, create scatter plots for highly correlated pairs
    if len(numeric_cols) >= 2:
        correlation = df[numeric_cols].corr().abs()
        # Get upper triangle of correlation matrix
        upper = correlation.where(np.triu(np.ones(correlation.shape), k=1).astype(bool))
        # Find index of feature columns with correlation greater than 0.5
        strong_pairs = [(correlation.columns[i], correlation.columns[j]) 
                        for i, j in zip(*np.where(upper > 0.5))]
        
        # Plot top 5 highly correlated pairs
        for i, (col1, col2) in enumerate(strong_pairs[:5]):
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=col1, y=col2, data=df)
            plt.title(f'Relationship between {col1} and {col2}')
            plt.tight_layout()
            
            file_path = os.path.join(output_dir, f'scatter_{col1}_{col2}.png')
            plt.savefig(file_path)
            plt.close()
            visualization_paths.append((f'Scatter plot: {col1} vs {col2}', file_path))
    
    # 5. Time series plot if datetime column exists
    datetime_cols = df.select_dtypes(include=['datetime']).columns
    if len(datetime_cols) > 0 and len(numeric_cols) > 0:
        date_col = datetime_cols[0]
        for num_col in numeric_cols[:3]:  # Plot up to 3 numeric columns
            plt.figure(figsize=(12, 6))
            df.set_index(date_col)[num_col].plot()
            plt.title(f'{num_col} over Time')
            plt.tight_layout()
            
            file_path = os.path.join(output_dir, f'timeseries_{num_col}.png')
            plt.savefig(file_path)
            plt.close()
            visualization_paths.append((f'Time series: {num_col}', file_path))
    
    return visualization_paths

def identify_trends_and_patterns(df):
    """Identify key trends and patterns in the data"""
    insights = []
    
    # Get numeric columns
    numeric_cols = df.select_dtypes(include=np.number).columns
    
    # 1. Check for outliers in numeric columns
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            
            if len(outliers) > 0:
                pct_outliers = (len(outliers) / len(df)) * 100
                insights.append(f"Column '{col}' has {len(outliers)} outliers ({pct_outliers:.2f}% of data)")
    
    # 2. Check for strong correlations
    if len(numeric_cols) >= 2:
        correlation = df[numeric_cols].corr().abs()
        # Get upper triangle
        upper = correlation.where(np.triu(np.ones(correlation.shape), k=1).astype(bool))
        # Find strong correlations
        strong_pairs = [(correlation.columns[i], correlation.columns[j], correlation.iloc[i, j]) 
                        for i, j in zip(*np.where(upper > 0.7))]
        
        for col1, col2, corr in strong_pairs:
            insights.append(f"Strong correlation detected between '{col1}' and '{col2}' (r = {corr:.2f})")
    
    # 3. Check for skewed distributions
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            skew_val = df[col].skew()
            if abs(skew_val) > 1:
                direction = "right" if skew_val > 0 else "left"
                insights.append(f"Column '{col}' is highly skewed to the {direction} (skew = {skew_val:.2f})")
    
    # 4. Identify imbalanced categories
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        for col in categorical_cols:
            if df[col].nunique() < 10:  # Only check if fewer than 10 unique values
                value_counts = df[col].value_counts(normalize=True)
                # If one category represents more than 80% of the data
                if value_counts.iloc[0] > 0.8:
                    insights.append(f"Imbalanced category in '{col}': '{value_counts.index[0]}' represents {value_counts.iloc[0]*100:.1f}% of the data")
    
    return insights

def generate_markdown_report(file_path, summary, stats, visualizations, insights):
    """Generate a markdown report with the analysis results"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(file_path, 'w') as f:
        # Title
        f.write(f"# Data Analysis Report\n\n")
        f.write(f"*Generated on: {now}*\n\n")
        
        # Dataset overview
        f.write("## Dataset Overview\n\n")
        f.write(f"- **Rows**: {summary['rows']}\n")
        f.write(f"- **Columns**: {summary['columns']}\n\n")
        
        # Column information
        f.write("### Column Information\n\n")
        f.write("| Column | Type | Missing Values |\n")
        f.write("|--------|------|---------------|\n")
        
        for col in summary['column_names']:
            dtype = summary['data_types'][col]
            missing = summary['missing_values'][col]
            missing_pct = (missing / summary['rows']) * 100 if summary['rows'] > 0 else 0
            f.write(f"| {col} | {dtype} | {missing} ({missing_pct:.2f}%) |\n")
        
        f.write("\n")
        
        # Descriptive statistics
        if stats is not None:
            f.write("## Descriptive Statistics\n\n")
            f.write("| Metric | " + " | ".join(stats.index) + " |\n")
            f.write("|--------|" + "|".join(["-" * len(col) for col in stats.index]) + "|\n")
            
            for col in stats.columns:
                if col in ['count', 'median', 'mean', 'std', 'min', 'max', 'range']:
                    row_values = [f"{stats.loc[idx, col]:.2f}" if isinstance(stats.loc[idx, col], (int, float)) 
                                  else str(stats.loc[idx, col]) for idx in stats.index]
                    f.write(f"| **{col}** | " + " | ".join(row_values) + " |\n")
            
            f.write("\n")
        
        # Key Insights and Trends
        if insights:
            f.write("## Key Insights and Trends\n\n")
            
            for insight in insights:
                f.write(f"- {insight}\n")
            
            f.write("\n")
        
        # Visualizations
        if visualizations:
            f.write("## Visualizations\n\n")
            
            for title, path in visualizations:
                # Get relative path for markdown
                rel_path = os.path.relpath(path, os.path.dirname(file_path))
                f.write(f"### {title}\n\n")
                f.write(f"![{title}]({rel_path})\n\n")

def main():
    # Input and output paths
    input_file = "User.xls"
    output_dir = "report_output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Load data
        df = load_data(input_file)
        
        # Generate summary
        print("Generating data summary...")
        summary = basic_summary(df)
        
        # Generate descriptive statistics
        print("Calculating statistics...")
        stats = generate_descriptive_stats(df)
        
        # Create visualizations
        print("Creating visualizations...")
        vis_dir = os.path.join(output_dir, "visualizations")
        visualizations = create_visualizations(df, vis_dir)
        
        # Identify trends and patterns
        print("Identifying trends and patterns...")
        insights = identify_trends_and_patterns(df)
        
        # Generate markdown report
        print("Generating markdown report...")
        report_path = os.path.join(output_dir, "data_analysis_report.md")
        generate_markdown_report(report_path, summary, stats, visualizations, insights)
        
        print(f"Analysis complete! Report saved to {report_path}")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()