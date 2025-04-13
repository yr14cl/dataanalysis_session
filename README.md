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
├── notebooks/             
│   ├── 01_object_id_frequency.ipynb     
│   ├── 02_participant_session_split.ipynb
│   └── 03_leiden_graph_clustering.ipynb  
│
├── src/                      
│   ├── data_loader.py         
│   ├── leiden_session.py      
│   ├── temporal_session.py    
│   └── session_analysis.py    
│
├── session_pipeline.py       
│
├── README.md                
├── requirements.txt          
```
