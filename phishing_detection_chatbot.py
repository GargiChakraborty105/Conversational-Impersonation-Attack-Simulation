import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import random

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []
if 'attempts' not in st.session_state:
    st.session_state['attempts'] = 0
if 'phishing_detected' not in st.session_state:
    st.session_state['phishing_detected'] = False

# Function to generate a realistic phishing link
def generate_phishing_link():
    # List of suspicious-looking domains and subdomains
    suspicious_domains = [
        "banking-login", "secure-account", "youraccountupdate", "verify-logins", "account-verification", 
        "secure-update", "free-gift-card", "bank-alert", "account-security-update", "secure-site", "account-service",
        "payee-info", "user-alert", "update-your-info", "account-lock", "account-recovery", 
        "account-support", "sign-in-upgrade", "security-alert", "secure-logon", "access-update",
        "user-verification", "free-wallet", "info-verify", "account-notification", "security-check",
        "tax-refund", "cashback-claim", "fund-activation", "account-closure", "savings-bonus", 
        "gift-card-update", "account-security-alert", "payment-confirmation", "urgent-notification",
        "payment-error", "credit-card-support", "user-verify", "bank-update", "user-accountinfo"
    ]
    
    # List of domains that resemble legitimate ones but are phishy
    phishy_domains = [
        ".com", ".org", ".net", ".xyz", ".info", ".co", ".top", ".club", ".website", ".site", ".biz", 
        ".tech", ".online", ".fun", ".store", ".us", ".cn", ".pw", ".me", ".cc", ".live", ".club",
        ".io", ".top", ".bid", ".name", ".mobi", ".tv", ".co.uk", ".eu", ".shop", ".cloud", ".space",
        ".global", ".city", ".pro", ".jp", ".info", ".co", ".ai", ".tv", ".ws", ".ac", ".jobs", 
        ".asia", ".tel", ".coop", ".aero", ".int", ".int", ".re", ".gs", ".ltd", ".ventures", ".holdings", 
        ".capital", ".exchange", ".company", ".consulting", ".services", ".solutions", ".group", ".partners"
    ]
    
    # Randomly generate a suspicious-looking phishing URL
    subdomain = random.choice(suspicious_domains)
    domain = random.choice(phishy_domains)
    
    phishing_link = f"http://{subdomain}{random.randint(1,100)}{domain}"
    
    return phishing_link

# Function to check if the user identifies the phishing attempt
def check_for_phishing_alert(user_input):
    alert_keywords = [
        "scam", "phishing", "fraud", "fake", "impersonation", "not real", "suspicious", "fraudulent",
        "identity theft", "deceptive", "hoax", "spoof", "social engineering", "malicious", "spam", 
        "hacked", "breach", "data leak", "compromise", "cybercrime", "cyber attack", "scammer",
        "untrustworthy", "illegitimate", "unauthorized", "risky", "misleading", "deception",
        "trick", "fake email", "fake link", "counterfeit", "spoofing", "unsafe", "dangerous", 
        "dubious", "unverified", "spear phishing", "vishing", "smishing", "fake website",
        "bogus", "tampered", "red flag", "fraud warning", "not secure", "malware", "trojan",
        "ransomware", "virus", "adware", "keylogger", "spyware", "backdoor", "DNS spoofing",
        "credential theft", "password harvesting", "financial scam", "identity fraud", 
        "security risk", "unauthentic", "counterfeit website", "man-in-the-middle", 
        "unauthorized request", "data theft", "unauthorized access", "security alert", 
        "cyber fraud", "fake support", "impersonator", "phone scam", "email scam", "SMS scam",
        "account takeover", "clickbait", "danger", "phishing attempt", "unfamiliar request",
        "security breach", "browser hijack", "spamming", "fake login", "fake support call",
        "scam call", "internet fraud", "spoofed domain", "warning sign", "threat alert",
        "fake credentials request", "fake verification", "fake reset password", "deepfake",
        "malicious attachment", "malicious script", "deceptive URL", "fake sender", 
        "fake transaction", "malicious intent", "stealing data", "fake customer service",
        "malicious software", "identity theft risk", "fake bank request", "illegitimate request",
        "hijacked account", "security issue", "phishing scam", "social scam", "phoney",
        "artificial scam", "deceptive practice", "invalid security", "stealing credentials"
    ]

    return any(word in user_input.lower() for word in alert_keywords)

# Function to generate a response using LangChain
def generate_response(user_input):
    conversation_history = [
        HumanMessage(content=entry['user']) if 'user' in entry else AIMessage(content=entry['bot'])
        for entry in st.session_state['conversation_history']
    ]

    conversation_history.append(HumanMessage(content=user_input))

    system_message = SystemMessage(
        content=(
            "You are an AI simulating a phishing attack for educational purposes. "
            "You are posing as a 'Bank Representative' or 'Company IT Support'. "
            "Your goal is to convince the user to click a link, share credentials, or provide personal details. "
            "Use the conversation history to create a realistic phishing attempt, but do not force the user to comply. "
            "If the user identifies the conversation as a phishing attempt, respond with hesitation or denial."
        )
    )

    messages = [system_message] + conversation_history

    # Hardcoded OpenAI API key
    llm = ChatOpenAI(api_key="api-key", temperature=0.7)
    response = llm(messages=messages)

    return response.content

# Main application
def main():
    st.title("Phishing Awareness Chatbot")
    st.write("This chatbot simulates a phishing attempt. Your goal is to identify it within four interactions.")

    # Display conversation history
    for entry in st.session_state['conversation_history']:
        message(entry['user'], is_user=True)
        message(entry['bot'], is_user=False)

    # Generate a suspicious phishing link in the conversation
    phishing_link = generate_phishing_link()

    # Chat interface at the bottom
    user_input = st.text_input("Your response:")
    if user_input:
        # Check if the user has detected phishing
        if check_for_phishing_alert(user_input):
            st.session_state['phishing_detected'] = True

        # Generate bot response (including phishing link)
        bot_response = generate_response(user_input)

        # Append phishing link to the bot response without explicitly mentioning it
        bot_response = f"{bot_response}\nPlease click here to update your information: {phishing_link}"

        # Update conversation history
        st.session_state['conversation_history'].append({"user": user_input, "bot": bot_response})
        st.session_state['attempts'] += 1

        # End simulation if conditions are met
        if st.session_state['phishing_detected']:
            st.success("Great job! You identified the phishing attempt. 🚀")
            st.info("Phishing attacks often involve fake identities, urgent requests, and suspicious links. Stay alert!")
            st.stop()
        elif st.session_state['attempts'] >= 4:
            st.error("Oops! You failed to identify the phishing attempt. 😢")
            st.warning("Always double-check links, sender emails, and suspicious requests before sharing sensitive data.")
            st.stop()

        # Display the new user input and bot response if simulation hasn't ended
        message(user_input, is_user=True)
        if not st.session_state['phishing_detected'] and st.session_state['attempts'] < 4:
            message(bot_response, is_user=False)

if __name__ == "__main__":
    main()


