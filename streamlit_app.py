import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="� Smart Property Finder",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .property-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .price-highlight {
        font-size: 1.2rem;
        font-weight: bold;
        color: #27ae60;
    }
    .location-info {
        color: #7f8c8d;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

class RightmovePropertyAPI:
    def __init__(self):
        self.base_url = "https://api.rightmove.co.uk/v1/properties"
        self.api_key = os.getenv("RIGHTMOVE_API_KEY")
        
    def search_properties(self, location, min_bedrooms=1, max_price=None, radius=5, property_type="rent"):
        """
        Search for properties using Rightmove API
        """
        try:
            headers = {
                "X-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            
            params = {
                "locationIdentifier": location,
                "minBedrooms": min_bedrooms,
                "radius": radius,
                "propertyTypes": property_type,
                "includeSSTC": False,
                "dontShow": ["sharedOwnership", "retirement"],
                "furnishType": "any",
                "keywords": "",
                "maxPrice": max_price if max_price else "",
                "minPrice": "",
                "numberOfPropertiesPerPage": 24,
                "radius": radius,
                "sortType": 1,  # Sort by price (lowest first)
                "index": 0
            }
            
            response = requests.get(self.base_url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Error connecting to Rightmove API: {str(e)}")
            return None

def load_sample_data():
    """Load sample property data for demonstration when API is not available"""
    sample_data = {
        "properties": [
            {
                "id": 1,
                "price": 650,
                "bedrooms": 1,
                "propertyType": "Flat",
                "location": "Manchester City Centre",
                "description": "Modern 1-bedroom flat in city centre",
                "imageUrl": "https://via.placeholder.com/300x200",
                "latitude": 53.4808,
                "longitude": -2.2426
            },
            {
                "id": 2,
                "price": 750,
                "bedrooms": 2,
                "propertyType": "Apartment",
                "location": "Salford Quays",
                "description": "Spacious 2-bedroom apartment with river views",
                "imageUrl": "https://via.placeholder.com/300x200",
                "latitude": 53.4716,
                "longitude": -2.2955
            },
            {
                "id": 3,
                "price": 550,
                "bedrooms": 1,
                "propertyType": "Studio",
                "location": "Northern Quarter",
                "description": "Cozy studio apartment in trendy area",
                "imageUrl": "https://via.placeholder.com/300x200",
                "latitude": 53.4831,
                "longitude": -2.2441
            },
            {
                "id": 4,
                "price": 850,
                "bedrooms": 2,
                "propertyType": "House",
                "location": "Didsbury",
                "description": "Family-friendly 2-bedroom house",
                "imageUrl": "https://via.placeholder.com/300x200",
                "latitude": 53.4167,
                "longitude": -2.2333
            },
            {
                "id": 5,
                "price": 600,
                "bedrooms": 1,
                "propertyType": "Flat",
                "location": "Ancoats",
                "description": "Modern 1-bedroom flat in up-and-coming area",
                "imageUrl": "https://via.placeholder.com/300x200",
                "latitude": 53.4831,
                "longitude": -2.2189
            }
        ]
    }
    return sample_data

def analyze_property_market(properties):
    """Analyze property market data and provide insights"""
    if not properties:
        return None
    
    df = pd.DataFrame(properties)
    
    analysis = {
        "total_properties": len(df),
        "avg_price": df['price'].mean(),
        "min_price": df['price'].min(),
        "max_price": df['price'].max(),
        "price_range": df['price'].max() - df['price'].min(),
        "bedroom_distribution": df['bedrooms'].value_counts().to_dict(),
        "property_types": df['propertyType'].value_counts().to_dict(),
        "price_per_bedroom": df.groupby('bedrooms')['price'].mean().to_dict()
    }
    
    return analysis

def create_price_analysis_chart(properties):
    """Create price analysis charts"""
    if not properties:
        return None
    
    df = pd.DataFrame(properties)
    
    # Price distribution chart
    fig_price_dist = px.histogram(
        df, 
        x='price', 
        nbins=20,
        title="Price Distribution",
        labels={'price': 'Monthly Rent (£)', 'count': 'Number of Properties'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_price_dist.update_layout(showlegend=False)
    
    # Price vs Bedrooms scatter plot
    fig_price_bedrooms = px.scatter(
        df,
        x='bedrooms',
        y='price',
        title="Price vs Number of Bedrooms",
        labels={'bedrooms': 'Number of Bedrooms', 'price': 'Monthly Rent (£)'},
        color='propertyType',
        hover_data=['location', 'description']
    )
    
    return fig_price_dist, fig_price_bedrooms

def display_property_cards(properties, max_display=6):
    """Display property cards in a grid layout"""
    if not properties:
        st.warning("No properties found matching your criteria.")
        return
    
    # Sort by price (lowest first)
    sorted_properties = sorted(properties, key=lambda x: x['price'])
    
    # Display properties in columns
    cols = st.columns(3)
    for i, property_data in enumerate(sorted_properties[:max_display]):
        col_idx = i % 3
        with cols[col_idx]:
            with st.container():
                st.markdown(f"""
                <div class="property-card">
                    <h4>{property_data['propertyType']} - {property_data['bedrooms']} Bed</h4>
                    <p class="price-highlight">£{property_data['price']}/month</p>
                    <p class="location-info">{property_data['location']}</p>
                    <p>{property_data['description'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add to favorites button
                if st.button(f"💖 Add to Favorites", key=f"fav_{property_data['id']}"):
                    st.success(f"Added {property_data['propertyType']} to favorites!")

def main():
    # Header
    st.markdown('<h1 class="main-header">🏠 Smart Property Finder</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Find the best deals on rental properties with AI-powered insights</p>', unsafe_allow_html=True)
    
    # Sidebar for search filters
    with st.sidebar:
        st.markdown('<h3 class="sub-header">🔍 Search Filters</h3>', unsafe_allow_html=True)
        
        # Location input
        location = st.text_input("📍 Location", placeholder="e.g., Manchester, London, Birmingham")
        
        # Price range
        max_price = st.slider("💰 Maximum Monthly Rent (£)", 400, 2000, 1000, 50)
        
        # Bedrooms
        min_bedrooms = st.selectbox("🛏️ Minimum Bedrooms", [1, 2, 3, 4], index=0)
        
        # Property type
        property_type = st.selectbox("🏘️ Property Type", ["Any", "Flat", "House", "Apartment", "Studio"])
        
        # Search radius
        radius = st.slider("📏 Search Radius (miles)", 1, 20, 5)
        
        # Search button
        search_button = st.button("🔍 Search Properties", type="primary", use_container_width=True)
        
        # Smart recommendations
        st.markdown("---")
        st.markdown('<h4>💡 Smart Tips</h4>', unsafe_allow_html=True)
        st.markdown("""
        - **Best time to rent**: January-March (lower demand)
        - **Negotiation tip**: Ask about longer-term discounts
        - **Hidden costs**: Check for service charges and bills
        - **Location hack**: Look 0.5-1 mile outside popular areas
        """)
    
    # Main content area
    if search_button and location:
        with st.spinner("🔍 Searching for properties..."):
            # Initialize API
            api = RightmovePropertyAPI()
            
            # Search properties
            if api.api_key:
                results = api.search_properties(
                    location=location,
                    min_bedrooms=min_bedrooms,
                    max_price=max_price,
                    radius=radius
                )
            else:
                # Use sample data for demonstration
                st.info("⚠️ Using sample data (API key not configured). Add your Rightmove API key to .env file for real data.")
                results = load_sample_data()
            
            if results and results.get('properties'):
                properties = results['properties']
                
                # Market analysis
                analysis = analyze_property_market(properties)
                
                # Display key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🏠 Total Properties", analysis['total_properties'])
                with col2:
                    st.metric("💰 Average Price", f"£{analysis['avg_price']:.0f}")
                with col3:
                    st.metric("💸 Lowest Price", f"£{analysis['min_price']}")
                with col4:
                    st.metric("📊 Price Range", f"£{analysis['price_range']}")
                
                # Price analysis charts
                st.markdown('<h3 class="sub-header">📊 Market Analysis</h3>', unsafe_allow_html=True)
                fig_price_dist, fig_price_bedrooms = create_price_analysis_chart(properties)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig_price_dist, use_container_width=True)
                with col2:
                    st.plotly_chart(fig_price_bedrooms, use_container_width=True)
                
                # Property recommendations
                st.markdown('<h3 class="sub-header">🏠 Best Value Properties</h3>', unsafe_allow_html=True)
                display_property_cards(properties)
                
                # Smart insights
                st.markdown('<h3 class="sub-header">🧠 Smart Insights</h3>', unsafe_allow_html=True)
                
                # Calculate insights
                df = pd.DataFrame(properties)
                cheapest_per_bedroom = df.loc[df.groupby('bedrooms')['price'].idxmin()]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>💡 Best Deals by Bedroom Count</h4>
                    """, unsafe_allow_html=True)
                    
                    for _, prop in cheapest_per_bedroom.iterrows():
                        st.markdown(f"""
                        <p><strong>{prop['bedrooms']} Bed:</strong> £{prop['price']}/month in {prop['location']}</p>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>🎯 Money-Saving Tips</h4>
                        <ul>
                            <li>Consider studios for 1-person households</li>
                            <li>Look for properties with bills included</li>
                            <li>Negotiate longer-term contracts</li>
                            <li>Check for student discounts</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                
            else:
                st.error("No properties found matching your criteria. Try adjusting your search filters.")
    
    elif not search_button:
        # Welcome screen with features
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>🎯 Find Your Perfect Rental Property</h2>
            <p style="font-size: 1.1rem; color: #666; margin-bottom: 2rem;">
                Our AI-powered assistant helps you find the best value rental properties with smart insights and market analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3>🔍 Smart Search</h3>
                <p>Advanced filters to find exactly what you need</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3>📊 Market Analysis</h3>
                <p>Real-time price trends and market insights</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h3>💡 Smart Tips</h3>
                <p>AI-powered recommendations to save money</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick start guide
        st.markdown("---")
        st.markdown('<h3>🚀 Quick Start Guide</h3>', unsafe_allow_html=True)
        st.markdown("""
        1. **Enter your desired location** in the sidebar
        2. **Set your budget** using the price slider
        3. **Choose minimum bedrooms** required
        4. **Click 'Search Properties'** to find deals
        5. **Review market analysis** and smart insights
        6. **Save your favorites** for later comparison
        """)

if __name__ == "__main__":
    main()
