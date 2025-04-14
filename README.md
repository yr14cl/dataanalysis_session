# dataanalysis_session
# background
Wooclap is a tool that allows teachers and trainers to easily ask different types of questions (open questions, multiple choice questions, find on image questions, etc.) to an audience of students, and to allow these students to answer via their smartphones. 
we need build "session_id" this parameter to help realted shakeholder know more information about user's reaction and to evaluate quality of each session. 

# objective

# strcuture 
```bash
wooclap-session-analysis/
├── data/                     
│   └── sample.csv
│
├── notebook/
│   ├── 01_eda.ipynb            
│   ├── 02_session_id_without_created_at.ipynb     
│   └── 03_session_id_with_created_at.ipynb  
│
├── src/                      
│   ├── data_loader.py         
│   ├── leiden_session.py      
│   ├── temporal_session.py    
│   └── session_analysis.py    
│
├── session_pipeline.py       
│── streamlit.py 
├── README.md                
├── requirements.txt          
```
