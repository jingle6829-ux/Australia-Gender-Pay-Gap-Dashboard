# Australia Gender Pay Gap Dashboard
An interactive dashboard analysing the gender pay gap and workforce composition data across Australian employers, based on a multi-source dataset.

## Description
Existing government data portals (such as ABS and WGEA) often suffer from fragmentation, forcing users to navigate across multiple isolated web pages and non-interactive tables. 

This project delivers a **unified, interactive analytical platform** designed for policymakers, researchers, and business units. It bridges the data gap by integrating official Australian Bureau of Statistics (ABS) datasets—including the *Employee Earnings and Hours (EEH)* and *Average Weekly Earnings (AWE)* surveys—into a seamless, user-friendly interface.

## Preview
<img style="width: 80%;" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/e8c95afb-fd19-4bdb-87ab-771c8e1e4371" />
<img style="width: 80%;" alt="Industry Analysis" src="https://github.com/user-attachments/assets/f82df9b2-f98c-4d0c-ab15-cfd34d925ab3" />
<img style="width: 80%;" alt="State Map View" src="https://github.com/user-attachments/assets/3ac6f95d-1789-4554-a2db-a1bbb50f85b2" />

## Data source
- Australian Bureau of Statistics (ABS): Employee Earnings and Hours (EEH) survey
- Australian Bureau of Statistics (ABS): Average Weekly Earnings (AWE) survey

## Key Features
* **Multi-Dimensional Filtering:** Filter data dynamically by state, year, industry, and occupation to perform targeted analysis.
* **Interactive Choropleth Map:** Visualize state-level metrics spatially using integrated geographic boundary data.
* **Core Metric Cards:** Instantly track high-level indicators including the Gender Pay Gap Ratio, Participation Rate Gap, and Employee Gap.
* **Time-Series Analysis:** Explore historical gender pay gap trends spanning from 2010 to 2025.
* **Paginated & Optimized Layout:** Designed following UX best practices (Miller's Law, Shneiderman's mantra) to minimize cognitive load and maintain a clean, responsive workflow.

## Tech Stack
- **Backend/Framework**: Python, Dash, Flask
- **Data processing**: Pandas, NumPy
- **Visualization**: Plotly (choropleth maps, interactive charts)
- **Frontend**: Dash Bootstrap Components

<!-- <details id=2 open>
<summary><h2>Data Source</h2></summary>


</details> -->
