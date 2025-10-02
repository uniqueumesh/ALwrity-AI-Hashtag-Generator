# 🔖 ALwrity AI Hashtag Generator

An intelligent hashtag generator powered by Google Gemini AI that creates trending, brand-safe hashtags for your social media content.

## ✨ Features

- **🤖 AI-Powered Generation**: Uses Google Gemini 2.5 Flash for smart hashtag creation
- **🎯 Customizable Output**: Generate 5-20 hashtags per request
- **✏️ Editable Results**: Modify generated hashtags before copying
- **📋 One-Click Copy**: Instant clipboard integration
- **🎨 Modern UI**: Clean dark theme with intuitive design
- **📱 Responsive**: Works seamlessly on desktop and mobile

## 🚀 Live Demo

**[Try ALwrity AI Hashtag Generator](https://your-app-url.streamlit.app)**

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash
- **Language**: Python 3.12+
- **Deployment**: Streamlit Community Cloud

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- Google Gemini API key

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/uniqueumesh/ALwrity-AI-Hashtag-Generator.git
cd ALwrity-AI-Hashtag-Generator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up API key**
   - Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Set environment variable:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
   - Or create `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```

4. **Run the application**
```bash
streamlit run app.py
```

## 🎯 Usage

1. **Enter Keywords**: Type your content topic or existing caption
2. **Select Count**: Choose how many hashtags you want (5-20)
3. **Generate**: Click "Generate Hashtags" to create AI-powered hashtags
4. **Edit & Copy**: Modify the results if needed, then copy to clipboard

### Example Input/Output

**Input**: `sustainable travel`

**Output**: 
```
#SustainableTravel #EcoAdventures #ConsciousJourneys #GreenGetaways #TravelWithImpact #EcoTourism #ResponsibleTravel #SustainableExploration #GreenTravel #EcoFriendlyTrips
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Customization
- Modify `BASE_PROMPT` in `app.py` to adjust hashtag generation style
- Update CSS in `inject_styles()` to customize the UI theme

## 📁 Project Structure

```
ALwrity-AI-Hashtag-Generator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── LICENSE               # MIT License
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful language model capabilities
- **Streamlit** for the amazing web app framework
- **Contributors** who helped improve this tool

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/uniqueumesh/ALwrity-AI-Hashtag-Generator/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/uniqueumesh/ALwrity-AI-Hashtag-Generator/discussions)

---

**Made with ❤️ for content creators and social media marketers**