# Chkscription
A full-stack web app to generate and verify prescriptions, revolutionizing healthcare one click at a time!

# Instructions
To run, first install the requirements.
```
pip install -r requirements.txt
```

Make sure you have all the keys setup. Follow `keys/README.md` to do the same

Then run all the servers - 

Authorization Server - 
```
python3 backend/auth_server.py
```

Ticket Generating Server - 
```
python3 backend/tgs.py
```

Backend Flask Server - 
```
python3 backend/server.py
```

Then run the client
```
streamlit run frontend/app.py
```
