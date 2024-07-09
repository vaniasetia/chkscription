# Chkscription
A full-stack web app to generate and verify prescriptions, revolutionizing healthcare one click at a time!

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- MongoDB
- Streamlit

### Installation

1. Clone the repository:
```sh
git clone https://github.com/vaniasetia/chkscription.git
```

2. Navigate to the project directory:
```sh
cd chkscription
```

3. Install the required packages:
```sh
pip install -r requirements.txt
```

### Configuration

1. Set up MongoDB and obtain the connection string, for example:
```sh
mongodb://localhost:27017
```

2. Create a `.env` file in the project directory and add the following environment variables:
```sh
MONGO_URI=<your_connection_string>
```

3. Generate the keys by running the following command:
```sh
python backend/utils/key_generator.py
```

### Usage

1. Start the backend server:
```sh
python backend/server.py
```

2. Start the frontend server:
```sh
streamlit run frontend/app.py
```