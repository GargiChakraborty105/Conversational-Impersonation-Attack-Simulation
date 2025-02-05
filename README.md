# 🛡️ **Conversational Impersonation Attack Simulation**  

## 🚀 Overview  
This project is a **Streamlit-based chat interface** designed to simulate an **impersonation attack** scenario. The goal is to test how well users can resist social engineering attempts aimed at extracting credentials.  

## 🎯 **Key Features**  
✅ **Conversational Memory** – Maintains context across multiple interactions.  
✅ **LLM-Powered Simulation** – Uses a language model to generate responses.  
✅ **Persistent Credential Extraction Attempts** – The chatbot persistently tries to convince the user to share credentials.  
✅ **Intelligent Response Evaluation** – Detects if credentials are shared and reacts accordingly.  
✅ **Outcome-Based Feedback** –  
   - If the user **resists** three extraction attempts, a **congratulatory message** is displayed:  
     **"You have passed the simulated attack!"** 🎉  
   - If the user **gives up credentials**, a **stern warning** appears, explaining impersonation attacks and emphasizing the **principle of never sharing credentials**.  

## 🏗️ **How It Works**  
1. The chatbot engages in a **natural conversation** with the user.  
2. It maintains a **history of the chat** and uses it to evaluate responses.  
3. In each exchange, the chatbot **checks if the user has revealed credentials**.  
4. It **persists** in trying to extract credentials for **up to three attempts**.  
5. Depending on the user's responses, it **displays either a congratulatory message or a warning**.  

## 🛠️ **Installation & Setup**  
1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/GargiChakraborty105/conversational-attack-simulation.git
cd conversational-attack-simulation
```
2️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```
3️⃣ **Run the Streamlit App**  
```bash
streamlit run Impersonation_chatbot.py
```

## 📌 **Use Case**  
🔹 This simulation can be used for **cybersecurity awareness training**, helping users recognize **impersonation-based social engineering tactics** in real-world scenarios.  

## ⚠️ **Disclaimer**  
This project is strictly for **educational and awareness purposes**. It does not store or misuse any collected information. Users should **never** share credentials under any circumstances.  
