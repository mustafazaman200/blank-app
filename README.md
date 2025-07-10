# � Smart Property Finder

An AI-powered property search assistant that helps you find the best deals on rental properties using the Rightmove Property Feed API. The application provides smart insights, market analysis, and personalized recommendations to help you make informed decisions.

## ✨ Features

- **🔍 Smart Search**: Advanced filters for location, price, bedrooms, and property type
- **📊 Market Analysis**: Real-time price trends and market insights with interactive charts
- **💡 AI Insights**: Smart recommendations and money-saving tips
- **🎯 Best Value Finder**: Automatically identifies the cheapest properties by bedroom count
- **📱 Responsive Design**: Beautiful, modern UI that works on all devices
- **💾 Favorites System**: Save and compare your favorite properties

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Rightmove Property Feed API key (optional - app works with sample data)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-property-finder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API (Optional)**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Rightmove API key:
   ```
   RIGHTMOVE_API_KEY=your_api_key_here
   ```
   
   **Note**: The app works perfectly with sample data if you don't have an API key!

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🎯 How to Use

### Basic Search
1. Enter your desired location (e.g., "Manchester", "London", "Birmingham")
2. Set your maximum monthly rent budget
3. Choose minimum number of bedrooms required
4. Select property type (Any, Flat, House, Apartment, Studio)
5. Adjust search radius as needed
6. Click "Search Properties"

### Understanding Results
- **Market Metrics**: View total properties, average price, lowest price, and price range
- **Price Analysis**: Interactive charts showing price distribution and price vs bedrooms
- **Best Value Properties**: Properties sorted by price (lowest first)
- **Smart Insights**: AI-powered recommendations and money-saving tips

### Smart Tips
- **Best time to rent**: January-March (lower demand)
- **Negotiation tip**: Ask about longer-term discounts
- **Hidden costs**: Check for service charges and bills
- **Location hack**: Look 0.5-1 mile outside popular areas

## 🔧 API Configuration

### Getting a Rightmove API Key
1. Visit [Rightmove Property Feed API](https://api-docs.rightmove.co.uk/docs/property-feed-api-product/1/overview)
2. Sign up for an account
3. Request API access
4. Add your API key to the `.env` file

### API Features
- Real-time property data
- Advanced search filters
- Location-based search
- Price range filtering
- Property type filtering

## 📊 Sample Data

When no API key is configured, the app uses realistic sample data including:
- 5 sample properties in Manchester area
- Various property types (Flats, Houses, Apartments, Studios)
- Price range from £550-£850/month
- 1-2 bedroom properties
- Realistic locations and descriptions

## 🛠️ Technical Details

### Built With
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive charts and visualizations
- **Requests**: HTTP library for API calls
- **Python-dotenv**: Environment variable management

### Architecture
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with modular design
- **Data Processing**: Pandas for analysis and insights
- **Visualization**: Plotly for interactive charts
- **API Integration**: Rightmove Property Feed API

### Key Components
- `RightmovePropertyAPI`: API client for property searches
- `analyze_property_market()`: Market analysis and insights
- `create_price_analysis_chart()`: Interactive visualizations
- `display_property_cards()`: Property display with favorites
- `load_sample_data()`: Fallback data when API unavailable

## 🎨 Customization

### Styling
The app uses custom CSS for a modern, professional look. You can modify the styles in the `st.markdown()` section at the top of the file.

### Adding Features
- **New Filters**: Add to the sidebar section
- **Additional Charts**: Extend the `create_price_analysis_chart()` function
- **More Insights**: Enhance the `analyze_property_market()` function
- **Property Details**: Add more property information fields

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:
1. Check that all dependencies are installed
2. Verify your API key is correct (if using real data)
3. Ensure you have internet connection for API calls
4. Check the browser console for any JavaScript errors

## 🔮 Future Enhancements

- [ ] Map integration with property locations
- [ ] Email alerts for new properties
- [ ] Property comparison tool
- [ ] Historical price tracking
- [ ] Neighborhood insights and ratings
- [ ] Virtual tour integration
- [ ] Mortgage calculator integration
- [ ] Property investment analysis

---

**Happy house hunting! 🏠✨**
