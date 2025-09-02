# **Daily Time Record Manager**

## **Overview**

This Daily Time Record Manager is a desktop application built with Python and Tkinter that helps you track and manage your working hours. The application allows you to:

- Log daily work time entries with start and end times
- View and edit your time records
- Generate monthly reports
- View total hours across all months

## **Installation**

### Prerequisites

- Python 3.6 or higher

### Setup Instructions

1. Clone or download this repository to your local machine
2. Navigate to the project directory
3. Run the application:
   
   ```
     python GUI_dtr.py
   ```

## **Features**

### Data Entry

- Add time entries with start and end times for specific days
- Format time using 12-hour format (e.g., "8:00 am", "5:00 pm")
- Edit or delete existing entries
- Entries are automatically saved to JSON files

### Monthly Report

- View a detailed report for the selected month
- See a breakdown of hours worked each day
- Calculate total hours worked for the month

### Total Hours Summary

- View total hours worked across all months
- See a breakdown of hours by month
- Percentage distribution of your work hours

## **How to Use**

### Adding Time Entries

1. Select the desired month and year from the dropdown menus
2. Enter the day number (1-31) in the "Day" field
3. Enter start and end times in 12-hour format (e.g., "8:00 am", "5:00 pm")
4. Click "Add Entry"

### Managing Entries

- To delete an entry: Select it in the list and click "Delete Selected"
- To view entries for a different month/year: Use the dropdown menus at the top

### Generating Reports

- Click the "Generate Report" button to view the monthly report
- Click the "Total Hours" button to view your accumulated hours

## **Data Storage**

The application stores your time records in JSON files named `dtr_data_YEAR.json` (e.g., dtr_data_2025.json). These files are saved in the same directory as the application.

## **Troubleshooting**

- **Invalid time format errors**: Ensure times are entered in the correct format (e.g., "8:00 am", "5:00 pm")
- **End time before start time**: The application validates that end times are after start times
- **Missing data**: If you don't see your data, verify you've selected the correct month and year

## **Contributing**

Feel free to fork this project and submit pull requests for any enhancements or bug fixes.

## **License**

This project is open source and available for personal or educational use.
