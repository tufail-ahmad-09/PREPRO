# 🚀 Prepro - Advanced Data Preprocessing Platform

<div align="center">

![Prepro Logo](https://img.shields.io/badge/Prepro-Data%20Preprocessing-blueviolet?style=for-the-badge&logo=python)

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat)]()

**A beautiful, modern web application for data preprocessing that makes data cleaning effortless for data scientists.**

[🚀 Demo](#demo) • [📖 Documentation](#installation) • [🛠️ Features](#features) • [🤝 Contributing](#contributing)

</div>

---

## ✨ Features

### 🎯 **Core Data Preprocessing**
- **📤 Smart File Upload** - Drag & drop CSV/Excel files with instant validation
- **🔍 Missing Data Analysis** - Comprehensive detection and intelligent handling options
- **🗂️ Duplicate Detection** - Identify and remove duplicate rows efficiently
- **📊 Outlier Detection** - IQR-based anomaly detection with visual summaries
- **🎲 Train-Test Split** - Intelligent data splitting with stratification support

### 🎨 **Modern User Interface**
- **✨ Glassmorphism Design** - Beautiful translucent interface with blur effects
- **🌈 Gradient Aesthetics** - Professional color schemes and smooth animations
- **📱 Fully Responsive** - Perfect experience on desktop, tablet, and mobile
- **🚫 No Page Reloads** - Seamless AJAX-powered operations
- **💫 Smooth Animations** - Engaging transitions and loading states

### 📈 **Advanced Analytics**
- **📊 Data Overview Dashboard** - Instant statistics and data health metrics
- **📋 Comprehensive Reports** - Detailed profiling with pandas-profiling
- **💾 Multiple Export Formats** - Download cleaned data and split datasets
- **🔧 Preprocessing Pipeline** - Track all applied transformations

---

## 🚀 Demo

### Upload & Preview
![Upload Demo](https://via.placeholder.com/800x400/667eea/ffffff?text=Upload+%26+Preview+Demo)

### Data Cleaning Pipeline
![Cleaning Demo](https://via.placeholder.com/800x400/764ba2/ffffff?text=Data+Cleaning+Pipeline)

### Modern Dashboard
![Dashboard Demo](https://via.placeholder.com/800x400/f093fb/ffffff?text=Modern+Dashboard)

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/prepro.git
   cd prepro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5001`

---

## 📚 Usage Guide

### 1. **Upload Your Dataset**
- Drag and drop your CSV or Excel file
- Supported formats: `.csv`, `.xlsx`, `.xls`
- Maximum file size: 100MB

### 2. **Analyze Data Quality**
- View comprehensive statistics
- Identify missing values and duplicates
- Examine data distribution

### 3. **Clean Your Data**
- **Missing Data**: Choose from multiple imputation methods
- **Duplicates**: Remove duplicate rows with one click
- **Outliers**: Detect and handle anomalous values
- **Export**: Download cleaned dataset

### 4. **Prepare for ML**
- Split data into training and testing sets
- Configure stratification options
- Download separate train/test files

---

## 🏗️ Architecture

### Backend (Python/Flask)
```
app.py              # Main Flask application
functions.py        # Data processing functions
requirements.txt    # Python dependencies
```

### Frontend (HTML/CSS/JS)
```
templates/
├── index.html      # Main application interface
static/
├── style.css       # Modern UI styles
```

### API Endpoints
- `POST /api/upload` - File upload and initial analysis
- `POST /api/handle_missing` - Missing data treatment
- `POST /api/remove_duplicates` - Duplicate removal
- `POST /api/detect_outliers` - Outlier detection
- `POST /api/remove_outliers` - Outlier removal
- `POST /api/train_test_split` - Dataset splitting

---

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Configure upload settings
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=100MB
```

### Customization
- Modify `static/style.css` for UI theming
- Update `functions.py` for custom preprocessing logic
- Extend `app.py` for additional API endpoints

---

## 📊 Supported Operations

| Operation | Description | Options |
|-----------|-------------|---------|
| **Missing Data** | Handle null values | Drop rows/columns, Fill mean/median/mode, Custom values |
| **Duplicates** | Remove duplicate entries | Complete row matching |
| **Outliers** | Detect anomalies | IQR method with configurable thresholds |
| **Data Types** | Automatic detection | Numeric, categorical, datetime |
| **Export** | Multiple formats | CSV, cleaned datasets, train/test splits |

---

## 🚀 Advanced Features

### Data Profiling
Generate comprehensive reports with:
- Column statistics and distributions
- Correlation matrices
- Missing value patterns
- Data quality scores

### Batch Processing
- Process multiple files
- Save preprocessing pipelines
- Reproduce transformations

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Add docstrings to functions
- Update README for new features
- Test your changes thoroughly

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Pandas** - For powerful data manipulation
- **Flask** - For the lightweight web framework
- **Bootstrap** - For responsive UI components
- **Font Awesome** - For beautiful icons
- **Animate.css** - For smooth animations

---

## 📞 Support

- 🐛 **Bug Reports**: [Create an issue](https://github.com/yourusername/prepro/issues)
- 💡 **Feature Requests**: [Suggest a feature](https://github.com/yourusername/prepro/issues)
- 📧 **Questions**: [Discussions](https://github.com/yourusername/prepro/discussions)

---

## 🎯 Roadmap

### Upcoming Features
- [ ] **Advanced Visualizations** - Interactive charts and plots
- [ ] **ML Model Integration** - Auto-suggest preprocessing steps
- [ ] **Data Validation Rules** - Custom validation logic
- [ ] **API Authentication** - Secure API access
- [ ] **Cloud Storage** - S3/GCS integration
- [ ] **Scheduled Processing** - Automated data pipelines

---

<div align="center">

**Made with ❤️ for Data Scientists**

⭐ **Star this repo if you find it useful!** ⭐

</div>
