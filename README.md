# dataanalysis_session
## Overview
Wooclap is a tool that allows teachers and trainers to easily ask different types of questions (open questions, multiple choice questions, find on image questions, etc.) to an audience of students, and to allow these students to answer via their smartphones. 
we need build "session_id" this parameter to help realted shakeholder know more information about user's reaction and to evaluate quality of each session. 


## Project Structure

### A. Data Preparation
### B. Exploratory Data Analysis (EDA）
### C. Modelling
### D. Forecasting
### E. Streamlit Dashboard

## Getting Started

To explore our dashboard and insights:

1. Clone this repository:
    ```git clone https://github.com/yr14cl/dataanalysis_session.git```
2. Install required dependencies:
    ```pip install -r requirements.txt```
3. Run the application:
    ```python run_all_sessions.py```
4. Open the provided web app URL in your browser.
   
# strcuture 
```bash
wooclap-session-analysis/
├── data/                     
│   └── sample.csv
├── outputs/
│   ├── temporal_sessions.csv
│   ├── leiden_sessions.csv
│   └── all_sessions.csv
├── notebook/
│   ├── 01_eda.ipynb            
│   ├── 02_session_id_without_created_at.ipynb
│   ├── 03_session_id_with_created_at.ipynb  
│   └── 04_test.ipynb  
│
├── src/                      
│   ├── data_loader.py         
│   ├── leiden_session.py         
│   └── temporal_session.py  
│── run_all_sessions.py
├── streamlir.py        
├── README.md                
├── requirements.txt          
```
