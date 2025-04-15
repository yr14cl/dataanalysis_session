# dataanalysis_session
## Overview
This project focuses on reconstructing and analyzing user sessions in Wooclap, a digital classroom interaction platform. Since Wooclap logs do not provide session identifiers, our goal is to infer them from user interaction data, enabling more realistic, session-oriented analytics.

I implement two distinct strategies depends on whether have timestamp data:

  1. Temporal-Based Splitting: Using timestamp gaps and session span limits.

  2. Graph-Based Clustering (Leiden Algorithm): Constructing bipartite graphs between participants and questions to detect implicit groupings.

A fully interactive Streamlit dashboard is provided to explore session distribution, user participation trends, and identify top-performing students across months. 

<iframe width="560" height="315" src="https://www.youtube.com/watch?v=-Zs4XUPZ8bg" frameborder="0" allowfullscreen></iframe>

## Getting Started

To explore the dashboard and insights:

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
├── src/                      
│   ├── data_loader.py         
│   ├── leiden_session.py         
│   └── temporal_session.py  
│── run_all_sessions.py
├── streamlit.py        
├── README.md                
└── requirements.txt          
```
# Data Pipeline 

```
          +----------------+                 
          |  sample.csv    |                  
          +----------------+                 
                  |                                
          [Step 1: Data Cleaning]                   
                  |                                
          +---------------------+         
          | Filter & Split Data |  <---- Pandas                    
          +---------------------+         
           /                          \       
    [with timestamp]         [without timestamp]     
           |                          |        
     [Session Split]           [Leiden Clustering]    
      (Gap + Span Rule)         (Bipartite Graph)    
           |                          |
    +-----------------+     +-----------------+     
    | temporal_sessions |   | leiden_sessions  |    
    +-----------------+     +-----------------+     
           \______________________/                
                 [Merge Results]                    
                      |                             
              [All Sessions CSV]                    
                      |                             
         [Streamlit Dashboard Visualization]         
                      |                             
          Insights for Product Manager
``` 
# Technologies
- **Data Processing**: pandas, numpy
- **Graph Clustering**: networkx, python-igraph, leidenalg
- **Visualization**: matplotlib, seaborn
- **Web Dashboard**: streamlit
