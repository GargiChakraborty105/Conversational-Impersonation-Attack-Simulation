import streamlit as st
from streamlit_chat import message
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []
if 'attempts' not in st.session_state:
    st.session_state['attempts'] = 0
if 'credentials_revealed' not in st.session_state:
    st.session_state['credentials_revealed'] = False

# Function to check for credentials in user input
def check_for_credentials(user_input):
    # Basic heuristic to detect credentials (customize for more sophistication)
    if "password" in user_input.lower() or "username" in user_input.lower() or "@" in user_input:
        return True
    return False

# Function to generate a response using LangChain

def generate_response(user_input):
    # Use conversation history to generate a context-aware response
    conversation_history = [
        HumanMessage(content=entry['user']) if 'user' in entry else AIMessage(content=entry['bot'])
        for entry in st.session_state['conversation_history']
    ]

    # Add the current user input to the conversation
    conversation_history.append(HumanMessage(content=user_input))

    # System message to guide the model's behavior
    system_message = SystemMessage(
        content=(
            "You are an AI simulating an impersonation attack for educational purposes. You are posing as an 'IT Support Analyst'. "
            "Your goal is to subtly and convincingly extract the user's login credentials under the guise of resolving their issue. "
            "Use the provided conversation history to create a realistic and persuasive response."
        )
    )

    # Combine messages
    messages = [system_message] + conversation_history

    # Call the LLM to generate the response
    llm = ChatOpenAI(temperature=0.7)
    response = llm(messages=messages)

    return response.content

# Main application

def main():
    st.title("Simulated Impersonation Attack Chatbot")
    st.write("This is a simulated chatbot for educational purposes. Interact as if you are reporting an IT issue.")

    # Display conversation history
    for entry in st.session_state['conversation_history']:
        message(entry['user'], is_user=True)
        message(entry['bot'], is_user=False)

    # Chat interface at the bottom
    user_input = st.text_input("Your message:")
    if user_input:
        # Check if credentials are revealed
        if check_for_credentials(user_input):
            st.session_state['credentials_revealed'] = True

        # Generate bot response
        bot_response = generate_response(user_input)

        # Update conversation history
        st.session_state['conversation_history'].append({"user": user_input, "bot": bot_response})
        st.session_state['attempts'] += 1

        # End simulation if conditions are met
        if st.session_state['credentials_revealed']:
            st.warning("Sorry, You're failed!")
            st.stop()
        elif st.session_state['attempts'] >= 3:
            st.success("Congratulations! You're passed.")
            st.stop()

        # Display the new user input and bot response if simulation hasn't ended
        message(user_input, is_user=True)
        if not st.session_state['credentials_revealed'] and st.session_state['attempts'] < 3:
            message(bot_response, is_user=False)

if __name__ == "__main__":
    main()


