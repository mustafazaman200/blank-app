"""
Utility functions for data processing and analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def clean_property_data(properties: List[Dict]) -> List[Dict]:
    """
    Clean and standardize property data
    """
    cleaned_properties = []
    
    for prop in properties:
        cleaned_prop = prop.copy()
        
        # Ensure required fields exist
        cleaned_prop['id'] = prop.get('id', 0)
        cleaned_prop['price'] = float(prop.get('price', 0))
        cleaned_prop['bedrooms'] = int(prop.get('bedrooms', 1))
        cleaned_prop['propertyType'] = prop.get('propertyType', 'Unknown')
        cleaned_prop['location'] = prop.get('location', 'Unknown')
        cleaned_prop['description'] = prop.get('description', 'No description available')
        
        # Add calculated fields
        cleaned_prop['price_per_bedroom'] = calculate_price_per_bedroom(
            cleaned_prop['price'], cleaned_prop['bedrooms']
        )
        
        # Add timestamp if not present
        if 'timestamp' not in cleaned_prop:
            cleaned_prop['timestamp'] = datetime.now().isoformat()
            
        cleaned_properties.append(cleaned_prop)
    
    return cleaned_properties

def calculate_price_per_bedroom(price: float, bedrooms: int) -> float:
    """Calculate price per bedroom"""
    if bedrooms <= 0:
        return price
    return price / bedrooms

def analyze_property_market(properties: List[Dict]) -> Dict:
    """
    Comprehensive market analysis of properties
    """
    if not properties:
        return {}
    
    df = pd.DataFrame(properties)
    
    # Basic statistics
    analysis = {
        "total_properties": len(df),
        "avg_price": df['price'].mean(),
        "median_price": df['price'].median(),
        "min_price": df['price'].min(),
        "max_price": df['price'].max(),
        "price_range": df['price'].max() - df['price'].min(),
        "price_std": df['price'].std(),
        "price_variance": df['price'].var()
    }
    
    # Bedroom analysis
    analysis.update({
        "bedroom_distribution": df['bedrooms'].value_counts().to_dict(),
        "avg_price_per_bedroom": df['price_per_bedroom'].mean(),
        "price_per_bedroom_stats": df.groupby('bedrooms')['price'].agg(['mean', 'min', 'max']).to_dict()
    })
    
    # Property type analysis
    analysis.update({
        "property_types": df['propertyType'].value_counts().to_dict(),
        "avg_price_by_type": df.groupby('propertyType')['price'].mean().to_dict()
    })
    
    # Value analysis
    analysis.update({
        "best_value_properties": find_best_value_properties(df),
        "price_quartiles": df['price'].quantile([0.25, 0.5, 0.75]).to_dict(),
        "price_percentiles": df['price'].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).to_dict()
    })
    
    # Market insights
    analysis.update({
        "market_insights": generate_market_insights(df),
        "recommendations": generate_recommendations(df)
    })
    
    return analysis

def find_best_value_properties(df: pd.DataFrame, top_n: int = 3) -> List[Dict]:
    """
    Find properties with the best value (lowest price per bedroom)
    """
    if df.empty:
        return []
    
    # Calculate value score (lower is better)
    df_copy = df.copy()
    df_copy['value_score'] = df_copy['price_per_bedroom']
    
    # Sort by value score and get top properties
    best_value = df_copy.nsmallest(top_n, 'value_score')
    
    return best_value.to_dict('records')

def generate_market_insights(df: pd.DataFrame) -> List[str]:
    """
    Generate market insights based on data analysis
    """
    insights = []
    
    if df.empty:
        return ["No data available for analysis"]
    
    # Price insights
    avg_price = df['price'].mean()
    median_price = df['price'].median()
    
    if avg_price > median_price * 1.1:
        insights.append("Market shows some high-value properties skewing average prices")
    
    # Bedroom insights
    bedroom_counts = df['bedrooms'].value_counts()
    most_common_bedrooms = bedroom_counts.index[0]
    insights.append(f"Most common property type: {most_common_bedrooms} bedroom")
    
    # Price per bedroom insights
    price_per_bedroom = df.groupby('bedrooms')['price'].mean()
    if len(price_per_bedroom) > 1:
        best_value_bedrooms = price_per_bedroom.idxmin()
        insights.append(f"Best value per bedroom: {best_value_bedrooms} bedroom properties")
    
    # Property type insights
    type_counts = df['propertyType'].value_counts()
    most_common_type = type_counts.index[0]
    insights.append(f"Most common property type: {most_common_type}")
    
    # Price range insights
    price_range = df['price'].max() - df['price'].min()
    if price_range > avg_price * 0.5:
        insights.append("High price variation suggests diverse property options")
    
    return insights

def generate_recommendations(df: pd.DataFrame) -> List[str]:
    """
    Generate personalized recommendations based on data
    """
    recommendations = []
    
    if df.empty:
        return ["Consider expanding your search criteria"]
    
    # Find cheapest properties
    cheapest = df.nsmallest(3, 'price')
    if not cheapest.empty:
        cheapest_price = cheapest.iloc[0]['price']
        recommendations.append(f"Lowest available price: £{cheapest_price}/month")
    
    # Find best value properties
    best_value = df.nsmallest(3, 'price_per_bedroom')
    if not best_value.empty:
        best_value_prop = best_value.iloc[0]
        recommendations.append(
            f"Best value: {best_value_prop['bedrooms']} bed {best_value_prop['propertyType']} "
            f"at £{best_value_prop['price']}/month"
        )
    
    # Price distribution recommendations
    price_25th = df['price'].quantile(0.25)
    price_75th = df['price'].quantile(0.75)
    
    recommendations.append(f"25% of properties cost less than £{price_25th:.0f}/month")
    recommendations.append(f"75% of properties cost less than £{price_75th:.0f}/month")
    
    # Bedroom recommendations
    bedroom_analysis = df.groupby('bedrooms')['price'].agg(['count', 'mean'])
    if len(bedroom_analysis) > 1:
        most_affordable_bedrooms = bedroom_analysis['mean'].idxmin()
        recommendations.append(
            f"Most affordable bedroom count: {most_affordable_bedrooms} bedroom"
        )
    
    return recommendations

def create_price_analysis_charts(properties: List[Dict]) -> Tuple[go.Figure, go.Figure, go.Figure]:
    """
    Create comprehensive price analysis charts
    """
    if not properties:
        return None, None, None
    
    df = pd.DataFrame(properties)
    
    # 1. Price distribution histogram
    fig_price_dist = px.histogram(
        df, 
        x='price', 
        nbins=20,
        title="Price Distribution",
        labels={'price': 'Monthly Rent (£)', 'count': 'Number of Properties'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_price_dist.update_layout(
        showlegend=False,
        xaxis_title="Monthly Rent (£)",
        yaxis_title="Number of Properties"
    )
    
    # 2. Price vs Bedrooms scatter plot
    fig_price_bedrooms = px.scatter(
        df,
        x='bedrooms',
        y='price',
        title="Price vs Number of Bedrooms",
        labels={'bedrooms': 'Number of Bedrooms', 'price': 'Monthly Rent (£)'},
        color='propertyType',
        hover_data=['location', 'description'],
        size='price_per_bedroom',
        size_max=20
    )
    fig_price_bedrooms.update_layout(
        xaxis_title="Number of Bedrooms",
        yaxis_title="Monthly Rent (£)"
    )
    
    # 3. Property type price comparison
    fig_type_comparison = px.box(
        df,
        x='propertyType',
        y='price',
        title="Price Comparison by Property Type",
        labels={'propertyType': 'Property Type', 'price': 'Monthly Rent (£)'}
    )
    fig_type_comparison.update_layout(
        xaxis_title="Property Type",
        yaxis_title="Monthly Rent (£)"
    )
    
    return fig_price_dist, fig_price_bedrooms, fig_type_comparison

def create_market_summary_chart(analysis: Dict) -> go.Figure:
    """
    Create a summary chart showing key market metrics
    """
    if not analysis:
        return None
    
    # Create subplot with multiple metrics
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Price Statistics', 'Bedroom Distribution', 'Property Types', 'Price Range'),
        specs=[[{"type": "bar"}, {"type": "pie"}],
               [{"type": "bar"}, {"type": "indicator"}]]
    )
    
    # Price statistics
    price_stats = [analysis.get('min_price', 0), analysis.get('avg_price', 0), analysis.get('max_price', 0)]
    price_labels = ['Min', 'Average', 'Max']
    
    fig.add_trace(
        go.Bar(x=price_labels, y=price_stats, name="Price Statistics", marker_color=['#2ecc71', '#3498db', '#e74c3c']),
        row=1, col=1
    )
    
    # Bedroom distribution
    bedroom_dist = analysis.get('bedroom_distribution', {})
    if bedroom_dist:
        fig.add_trace(
            go.Pie(labels=list(bedroom_dist.keys()), values=list(bedroom_dist.values()), name="Bedrooms"),
            row=1, col=2
        )
    
    # Property types
    property_types = analysis.get('property_types', {})
    if property_types:
        fig.add_trace(
            go.Bar(x=list(property_types.keys()), y=list(property_types.values()), name="Property Types"),
            row=2, col=1
        )
    
    # Price range indicator
    price_range = analysis.get('price_range', 0)
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=price_range,
            title={'text': "Price Range (£)"},
            gauge={'axis': {'range': [None, price_range * 1.2]}},
        ),
        row=2, col=2
    )
    
    fig.update_layout(height=600, title_text="Market Summary")
    
    return fig

def filter_properties(properties: List[Dict], filters: Dict) -> List[Dict]:
    """
    Filter properties based on criteria
    """
    if not properties:
        return []
    
    df = pd.DataFrame(properties)
    
    # Apply filters
    if 'min_price' in filters and filters['min_price']:
        df = df[df['price'] >= filters['min_price']]
    
    if 'max_price' in filters and filters['max_price']:
        df = df[df['price'] <= filters['max_price']]
    
    if 'min_bedrooms' in filters and filters['min_bedrooms']:
        df = df[df['bedrooms'] >= filters['min_bedrooms']]
    
    if 'max_bedrooms' in filters and filters['max_bedrooms']:
        df = df[df['bedrooms'] <= filters['max_bedrooms']]
    
    if 'property_type' in filters and filters['property_type'] and filters['property_type'] != 'Any':
        df = df[df['propertyType'].str.contains(filters['property_type'], case=False, na=False)]
    
    if 'location' in filters and filters['location']:
        df = df[df['location'].str.contains(filters['location'], case=False, na=False)]
    
    return df.to_dict('records')

def sort_properties(properties: List[Dict], sort_by: str = 'price', ascending: bool = True) -> List[Dict]:
    """
    Sort properties by specified criteria
    """
    if not properties:
        return []
    
    df = pd.DataFrame(properties)
    
    if sort_by == 'price':
        df = df.sort_values('price', ascending=ascending)
    elif sort_by == 'price_per_bedroom':
        df = df.sort_values('price_per_bedroom', ascending=ascending)
    elif sort_by == 'bedrooms':
        df = df.sort_values('bedrooms', ascending=ascending)
    elif sort_by == 'property_type':
        df = df.sort_values('propertyType', ascending=ascending)
    elif sort_by == 'location':
        df = df.sort_values('location', ascending=ascending)
    
    return df.to_dict('records')

def calculate_savings_potential(properties: List[Dict]) -> Dict:
    """
    Calculate potential savings and value opportunities
    """
    if not properties:
        return {}
    
    df = pd.DataFrame(properties)
    
    # Calculate savings potential
    avg_price = df['price'].mean()
    median_price = df['price'].median()
    
    # Properties below average price
    below_avg = df[df['price'] < avg_price]
    
    # Properties below median price
    below_median = df[df['price'] < median_price]
    
    # Best value properties (lowest price per bedroom)
    best_value = df.nsmallest(3, 'price_per_bedroom')
    
    savings_analysis = {
        "average_price": avg_price,
        "median_price": median_price,
        "properties_below_average": len(below_avg),
        "properties_below_median": len(below_median),
        "potential_savings_vs_avg": avg_price - df['price'].min(),
        "potential_savings_vs_median": median_price - df['price'].min(),
        "best_value_properties": best_value.to_dict('records'),
        "price_efficiency_score": (df['price'].min() / avg_price) * 100
    }
    
    return savings_analysis