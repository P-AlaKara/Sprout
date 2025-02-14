# Sprout

Sprout is a simple Business Intelligence (BI) system designed for retail stores. It consists of six separate but linked Dash applications running on different ports. The system provides key insights into inventory, sales/performance, customer behaviour, business goals, advanced analytics, and reports with customizable queries.

## Features

Sprout consists of six dashboards:

1. **Inventory Dashboard** - Displays statistics on current inventory levels assiting in inventory management.
2. **Sales Dashboard** - Shows sales performance and key metrics to track business growth.
3. **Customer Dashboard** - Analyzes customer behavior and statistics.
4. **Goals Dashboard** - Tracks existing business goals and allows users to set new ones.
5. **Analysis Dashboard** - Provides advanced analytical insights, including:
   - **Time Series Sales Prediction** using Facebook's Prophet model.
   - **Customer Lifetime Value (CLV) Analysis**.
   - **Product Affinity Analysis**.
6. **Queries Section** - A collection of reports with advanced filtering mechanisms (not a dashboard but an interactive reporting tool).

## Installation and Running the Project

### Prerequisites

- Python installed on your system
- Required dependencies (see `requirements.txt`)

### Steps to Run the Application

1. Clone the repository:
   ```sh
   git clone <repository_url>
   ```
2. Navigate into the project directory:
   ```sh
   cd Sprout
   ```
3. Navigate to the dashboards folder:
   ```sh
   cd dashboards
   ```
4. Run all the applications using the provided PowerShell script:
   ```sh
   ./run_all_apps.ps1
   ```
5. Open a web browser and visit one of the running dashboards, e.g., `http://localhost:8050`.

## Notes

- This project originally included a separate home page for access control, but it is not included in this version.
- Each dashboard runs on a separate port and contains navigation links to the other dashboards.
- Use the side menu to explore different dashboards.

## Technologies Used

- **Dash** (for building web-based dashboards)
- **Plotly** (for interactive visualizations)
- **Prophet** (for time series forecasting)
- **Pandas & NumPy** (for data manipulation)
- **Statsmodels** (for statistical analysis)
- **Dash Mantine Components, Dash Bootstrap Components** (for UI enhancements)

## Future Improvements

- User management and Access Control.
- Enhancing visualizations and with more interactivity.
- Expanding analytics with additional/better predictive models.
- Use of machine learning models for clv and products affinity analysis instead of mathematical/statistical methods.

## License

This project is open-source. Feel free to modify and extend it as needed.

---

For questions or contributions, feel free to reach out!


