This is the python backend of the carCharts project

# CarCharts.lk – Sri Lankan Automobile Market Analyzer and Classified Aggregator


Project Overview
-----------------
The CarCharts.lk project consists of two main components:

Backend (Python): Manages data scraping, processing, and business logic.
Frontend (Angular): Provides the user interface and communicates with the backend to display data and visualizations.

------------------------------------------------------------------------------------------


Backend Repository
--------------------
Repository: https://github.com/gehanjanith/CarChartsApp-backend.git

Technology: Python (Flask)
Description: The backend handles data scraping, processing, and API development. It scrapes vehicle listings from multiple sources, processes the data, and exposes it through RESTful APIs.

Frontend Repository
---------------------
Repository: https://github.com/gehanjanith/car-charts-frontend.git

Technology: Angular
Description: The frontend is responsible for displaying the user interface, allowing users to search for vehicles, view price trends, and interact with the backend APIs.


------------------------------------------------------------------------------------------+


Pre Requisites
--------------
Python (version 3.11+)

Node.js (version 20+)

Angular CLI (version 16+)

MySQL Backend Installation

------------------------------------------------------------------------------------------

HOW TO SETUP
-------------

**Backend Installation**

1. Clone the backend repository:
```
git clone https://github.com/gehanjanith/CarChartsApp-backend.git
cd CarChartsApp-backend
```
2. Create a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Run the backend server:
```
flask run
```
The backend should now be running on http://127.0.0.1:5000/.

***Frontend Installation***

1. Clone the frontend repository:
```
git clone https://github.com/gehanjanith/car-charts-frontend.git
cd car-charts-frontend
```
2. Install the required dependencies:
```
npm install
```
3. Run the frontend development server:
```
ng serve
```

The frontend should now be running on http://localhost:4200/.

Configure Environment Variables:
--------------------------------
backend API URL - http://127.0.0.1:5000

frontend development server:http://localhost:4200/

------------------------------------------------------------------------------------------


Contact
--------

For questions or support, feel free to reach out to:

+ Hetti Arachchige Don Gehan Janith

+ Index No: 20550421 

+ Reg. No: 2020/MIT/042

+ GitHub: gehanjanith
