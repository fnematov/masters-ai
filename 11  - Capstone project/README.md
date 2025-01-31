# 🚗 AI-Powered Car Sales Manager

## 📌 Project Overview
This project is an **AI-powered car sales system** built with **Streamlit** and **AutoGen**, integrating **multi-agent AI** to assist customers in finding the perfect car. The system includes a **data dashboard** and a **conversational AI assistant** that helps users with car recommendations, financing, and compliance.

---

## 📊 Features
### **🔹 AI Sales Manager (Multi-Agent System)**
✔ **Conversational AI** using OpenAI-powered AutoGen Agents  
✔ **Retrieval-Augmented Generation (RAG)** for FAQ & policy queries  
✔ **Car recommendations** based on customer preferences  
✔ **Pricing & negotiation assistance**  
✔ **Order tracking & deal finalization**  

### **📊 Data Dashboard**
✔ **Top-rated cars visualization**  
✔ **Most ordered cars statistics**  
✔ **Interactive bar charts with insights**  

### **📂 SQLite Database**
✔ Stores **car listings**, **orders**, and **customer interactions**  
✔ Auto-incremented `id` column for database consistency  
✔ Dynamic filtering & search queries  

---

## ⚙️ Installation & Setup

### **🔹 1. Clone the Repository**
```bash
git clone https://github.com/fnematov/masters-ai
cd masters-ai/11 - Capstone project
```

### **🔹 2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **🔹 3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **🔹 4. Set Up API Keys**
Create a `.env` file in the project root and add your **OpenAI API key**:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🚀 Running the Application

### **🔹 1. Load the Car Data**
When you run system, all dataset will be downloaded from data sources and saved to the database.
Data sources are:
- [mohitkumar282/used-car-dataset](https://www.kaggle.com/mohitkumar282/used-car-dataset)
- [CooperUnion/cardataset](https://www.kaggle.com/CooperUnion/cardataset)
- [asinow/car-price-dataset](https://www.kaggle.com/asinow/car-price-dataset)

### **🔹 2. Start the AI Sales System**
```bash
streamlit run main.py
```

---

## 🏗️ System Architecture
The system consists of two primary components:  

### **🔹 1. AI Multi-Agent System (AutoGen)**
- **User Proxy Agent** → Handles user input  
- **Sales Lead Agent** → Guides the conversation  
- **Product Expert Agent** → Fetches cars from the database  
- **Compliance Agent (RAG)** → Answers FAQ & policy questions  
- **Closing Agent** → Finalizes deals  
- **Objection Handler** → Addresses customer concerns  

### **🔹 2. Streamlit Dashboard**
- **Top 10 Highly Rated Cars**
- **Top 5 Most Ordered Cars**
- **AI Chat Interface**

---

## 🔍 Example AI Conversations

### **User:**  
_"Hi, I'm Smit. I want to buy Mercedes. My budget is about 40k. Do you have any offers?"_

### **AI Response:**  
_"You've chosen a 2017 Mercedes-Benz C-Class, fitting perfectly within your budget at a discounted price of $37,857.50. To finalize the purchase, please provide your first name, last name, email, and phone number"_

### **User:**  
_"Do you have any discounts?"_

### **Compliance Agent:**  
_"No, all sales are final. However, we offer a limited exchange policy under certain conditions."_  

---

## 🛠️ Troubleshooting
### **1. API Key Issues**
Ensure you have an OpenAI API key stored in `.env`.  
Run:
```bash
echo $OPENAI_API_KEY  # On Windows: echo %OPENAI_API_KEY%
```

### **2. Database Not Found**
If you get a **database error**, ensure you have **run `save_csv_to_db()`** before launching the app.

### **3. FAQ Retrieval Not Working**
If `RetrieveUserProxyAgent` is not retrieving answers:
```python
compliance_agent.retrieve("Do you offer financing?")
```
Expected output:
```json
[{"question": "Do you offer financing?", "answer": "Yes, we partner with banks and financial institutions to offer financing options."}]
```

---

🚀 **Built with Python, Streamlit, AutoGen & OpenAI!**  
