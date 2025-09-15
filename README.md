# SAT Results Manager

A comprehensive command-line application for managing SAT (Scholastic Assessment Test) results with persistent data storage, ranking system, and statistical analysis capabilities.

## 🎯 Overview

The SAT Results Manager is a Python-based application that allows educational institutions, tutoring centers, or individual users to efficiently manage student SAT scores. The application provides a complete suite of features for data entry, analysis, and reporting with automatic pass/fail determination based on configurable thresholds.

## ✨ Features

### Core Functionality
- **📝 Data Entry**: Insert new candidate records with comprehensive validation
- **📊 Data Visualization**: View all records in structured JSON format
- **🏆 Ranking System**: Calculate and display candidate rankings with percentile analysis
- **✏️ Score Updates**: Modify existing SAT scores with automatic status recalculation
- **🗑️ Record Management**: Safely delete candidate records with confirmation
- **📈 Statistical Analysis**: Calculate averages, pass rates, and performance metrics
- **🔍 Filtering**: Filter records by pass/fail status
- **💾 Data Persistence**: Automatic and manual data saving to JSON format

### Advanced Features
- **⚙️ Configurable Settings**: Adjustable maximum SAT scores and pass thresholds
- **🛡️ Data Validation**: Comprehensive input validation with helpful error messages
- **🔄 Data Integrity**: Rollback mechanisms to prevent data corruption
- **📚 Smart Suggestions**: Name suggestions when candidates are not found
- **📊 Enhanced Statistics**: Separate averages for passed and failed candidates

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Standard Python libraries (no external dependencies required)

### Setup
1. **Clone or Download** the repository:
   ```bash
   git clone <repository-url>
   # or download the sat_manager.py file directly
   ```

2. **Navigate** to the project directory:
   ```bash
   cd sat-results-manager
   ```

3. **Run** the application:
   ```bash
   python sat_manager.py
   ```

## 📖 Usage Guide

### Starting the Application
```bash
python sat_manager.py
```

Upon first launch, the application will create a default configuration with a maximum SAT score of 1600 (realistic SAT range).

### Main Menu Options

#### 1. Insert Data
Add a new candidate to the system with the following information:
- **Name**: Unique identifier for the candidate
- **Address**: Residential address
- **City**: City of residence
- **Country**: Country of residence  
- **Pincode**: Postal code (numeric, minimum 3 digits)
- **SAT Score**: Numeric score (0 to maximum configured score)

**Pass/Fail Calculation**: Automatically determined based on 30% of the maximum score threshold.

#### 2. View All Data
Displays all stored records in JSON format with:
- Current maximum score setting
- Total number of candidates
- Complete candidate records

#### 3. Get Rank
Enter a candidate's name to view:
- Current SAT score
- Rank among all candidates
- Percentile ranking
- Pass/Fail status
- Tie information (if applicable)

#### 4. Update Score
Modify an existing candidate's SAT score:
- Search by candidate name
- Enter new score with validation
- Automatic pass/fail status recalculation
- Before/after comparison display

#### 5. Delete One Record
Remove a candidate from the system:
- Search by candidate name
- Display record details before deletion
- Require exact confirmation for safety
- Rollback protection on save failure

#### 6. Calculate Average SAT Score
Comprehensive statistical analysis including:
- Overall average score and percentage
- Pass rate statistics
- Separate averages for passed and failed candidates
- Current passing threshold display

#### 7. Filter Records by Pass/Fail Status
View filtered results:
- Choose 'pass' to show only passed candidates
- Choose 'fail' to show only failed candidates
- JSON formatted output with count information

#### 8. Save Data to JSON File
Manually trigger data persistence:
- Explicit save operation
- Confirmation of successful save
- Current statistics display

#### 9. Exit
Safely close the application

#### 10. Set Maximum SAT Score
Configure the maximum possible SAT score:
- Change the scoring scale
- Automatic recalculation of all pass/fail statuses
- Rollback protection on save failure

## 📁 Data Structure

### Storage Format
Data is stored in `sat_data.json` with the following structure:

```json
{
  "max_score": 1600,
  "records": {
    "John Doe": {
      "name": "John Doe",
      "address": "123 Main St",
      "city": "New York",
      "country": "USA",
      "pincode": "10001",
      "sat_score": 1200,
      "passed": true
    }
  }
}
```

### Data Fields
- **max_score**: Maximum possible SAT score (configurable)
- **records**: Dictionary of candidate records keyed by name
- **name**: Candidate's full name (unique identifier)
- **address**: Full address
- **city**: City of residence
- **country**: Country of residence
- **pincode**: Postal/ZIP code
- **sat_score**: SAT score (numeric)
- **passed**: Pass/fail status (boolean, auto-calculated)

## ⚙️ Configuration

### Default Settings
- **Maximum SAT Score**: 1600 (realistic SAT range: 400-1600)
- **Pass Threshold**: 30% of maximum score
- **Data File**: `sat_data.json`
- **Minimum Pincode Length**: 3 digits
- **Maximum Name Length**: 100 characters

### Customization
All settings can be modified through the application menu or by editing the constants in the source code:

```python
DEFAULT_MAX_SCORE = 1600  # Change default maximum score
PASS_THRESHOLD = 0.3      # Change pass threshold (30%)
DATA_FILE = "sat_data.json"  # Change data file name
```

## 🛡️ Data Safety Features

### Input Validation
- **Score Validation**: Range checking, numeric validation
- **Name Validation**: Length limits, empty name prevention
- **Pincode Validation**: Numeric format, minimum length requirements

### Error Handling
- **File Corruption Recovery**: Automatic fallback to fresh data
- **Save Failure Protection**: Rollback mechanisms prevent data loss
- **Graceful Error Messages**: User-friendly error reporting

### Data Integrity
- **Atomic Operations**: All-or-nothing save operations
- **Backup on Modification**: Temporary backups during updates
- **Validation on Load**: Data structure verification

## 🔧 Troubleshooting

### Common Issues

**Issue**: "File not found" error
**Solution**: The application will automatically create `sat_data.json` on first use.

**Issue**: "Invalid JSON format" error  
**Solution**: The application will backup corrupted files and start fresh.

**Issue**: "Permission denied" when saving
**Solution**: Ensure write permissions in the application directory.

**Issue**: Score validation errors
**Solution**: Ensure scores are numeric and within the 0 to maximum score range.

### Data Recovery
If the data file becomes corrupted:
1. The application automatically creates a backup
2. A fresh data file is initialized
3. Previous data can be recovered from `sat_data.json.backup` if needed

## 🧪 Testing

### Manual Testing Checklist
- [ ] Insert candidate with valid data
- [ ] Insert candidate with invalid data (test validation)
- [ ] View all data with empty and populated datasets
- [ ] Calculate rank for existing and non-existing candidates
- [ ] Update scores with valid and invalid inputs
- [ ] Delete records with proper confirmation
- [ ] Calculate averages with various dataset sizes
- [ ] Filter by pass/fail status
- [ ] Test explicit save functionality
- [ ] Change maximum score and verify recalculation

### Edge Cases Tested
- Empty datasets
- Single candidate scenarios
- All passed or all failed scenarios
- Tied scores
- Maximum and minimum score values
- File permission issues
- Corrupted data files

## 📊 Performance Considerations

### Scalability
- **Memory Usage**: All data stored in memory for fast access
- **File I/O**: JSON format provides good balance of readability and performance
- **Search Operations**: Linear search suitable for typical educational datasets (< 1000 candidates)

### Optimization Recommendations
For large datasets (> 1000 candidates):
- Consider implementing database storage (SQLite recommended)
- Add indexing for faster name searches
- Implement pagination for data viewing

## 🔮 Future Enhancements

### Planned Features
- **Database Integration**: SQLite support for larger datasets
- **Data Export**: CSV and Excel export functionality
- **Backup System**: Automated backup with timestamp
- **User Authentication**: Multi-user support with access controls
- **Reporting**: PDF report generation
- **Data Import**: Bulk import from CSV/Excel files
- **Grade Distribution**: Histogram and distribution analysis
- **Search Functionality**: Advanced search and filtering options

### Technical Improvements
- **Unit Testing**: Comprehensive test suite
- **Logging**: Detailed operation logging
- **Configuration File**: External configuration management
- **Web Interface**: Browser-based GUI option
- **API Endpoints**: REST API for integration

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 Python style guidelines
2. **Documentation**: Update README for new features
3. **Testing**: Test all changes thoroughly
4. **Error Handling**: Implement proper exception handling
5. **Validation**: Add input validation for new features

### Reporting Issues
When reporting bugs, please include:
- Python version
- Operating system
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages (if any)

## 📄 License

This project is released under the MIT License. See LICENSE file for details.

## 👥 Support

### Getting Help
- **Documentation**: Refer to this README for comprehensive guidance
- **Issues**: Report bugs and feature requests through the issue tracker
- **Community**: Join discussions in the project forum

### Contact Information
For technical support or questions:
- Email: [your-email@example.com]
- GitHub: [your-github-username]
- Documentation: [project-wiki-url]

## 🔄 Version History

### v2.0.0 (Current)
- **Added**: Object-oriented design
- **Added**: Comprehensive input validation
- **Added**: Enhanced error handling with rollback protection
- **Added**: Smart name suggestions
- **Added**: Detailed statistical analysis
- **Added**: Improved user interface with visual formatting
- **Changed**: Default maximum score to 1600 (realistic SAT range)
- **Fixed**: Data corruption issues
- **Fixed**: Edge cases in ranking calculations

### v1.0.0 (Original)
- **Added**: Basic CRUD operations
- **Added**: JSON data persistence
- **Added**: Menu-driven interface
- **Added**: Pass/fail calculation
- **Added**: Ranking system
- **Added**: Statistical analysis

---

## 🚀 Quick Start Example

```bash
# Start the application
python sat_manager.py

# Follow these steps for a quick test:
# 1. Choose option 1 (Insert data)
# 2. Enter sample candidate data
# 3. Choose option 2 (View all data) to verify
# 4. Choose option 3 (Get rank) to test ranking
# 5. Choose option 6 (Calculate average) to see statistics
```

**Sample Data for Testing:**
```
Name: Alice Johnson
Address: 123 Oak Street
City: Boston
Country: USA
Pincode: 02101
SAT Score: 1350
```

This will create a passed candidate (1350 > 30% of 1600 = 480) and allow you to explore all features of the application.

---

*Last Updated: September 2025*
*Version: 2.0.0*
