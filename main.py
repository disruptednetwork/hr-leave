import streamlit as st
from app.auth import initialize_app, authentication_process, get_user_id
from app import db
import logging
import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv


# Load environment variables from a `.env` file
load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
REGION = os.getenv("REGION")

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

def generate(query):
    vertexai.init(project=PROJECT_ID, location=REGION)
    model = GenerativeModel("gemini-1.5-flash-002")
    response = model.generate_content(
        [query],
        generation_config=generation_config,
        stream=False,
    )
    return response.candidates[0].content.parts[0].text

def handle_user_query(query):
    prompt = f"""You are a helpful assistant that classifies user requests related to HR leave. Given the following text, determine the user's intent and respond with only one of the following categories:
    *   get_leave_balance: The user is asking about their leave balance.
    *   submit_leave: The user wants to submit a leave request.
    *   unknown: The user's intent is unclear or not related to leave.

    Here is the user's question:
    {query}"""

    response = generate(prompt)
    logging.info(response)

    # Example of extracting information from Gemini's response
    if "get_leave_balance" in response.lower():
        conn = db.connect_to_db()
        if conn:
            try:
                user_id = get_user_id()
                if user_id:
                    logging.info(f"User ID: {user_id}")
                    leave_balance = db.fetch_user_leave_balance(conn, user_id)
                    if leave_balance:
                        response = "Your leave balance:\n\n"
                        for leave_type, available, used in leave_balance:
                            response += f"- {leave_type}: Available: {available}, Used: {used}\n"
                        return response
                    else:
                        logging.info(f"User ID: {user_id}")
                        return "No leave balance found for your account."
                else:
                    return "User ID not found. Please log in again."
            except Exception as e:
                return f"An error occurred while fetching leave balance: {e}"
            finally:
                conn.close()
        else:
            return "Failed to connect to the database."
    elif "submit_leave" in response.lower():
        return "Submit leave is not yet implemented"
    else:
        return "I can only answer questions about your leave balance at the moment."

def main():
    """
    Main function for the HR Leave Application Streamlit app.
    """
    st.set_page_config(page_title="HR Leave App", page_icon=":date:")
    st.sidebar.title("Login")

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        app = initialize_app()
        if app is not None:
            auth_result = authentication_process(app)
            if auth_result:
                user_data, token = auth_result
                logging.info(f"User data: {user_data}")
                st.session_state["authenticated"] = True
                st.session_state["display_name"] = user_data.get("displayName")
                st.session_state["user_id"] = user_data.get("id")
                st.session_state["token"] = token
                st.rerun()
    else:
        st.sidebar.write(f"Welcome, {st.session_state['display_name']}")

        # Chat Interface
        st.title("HR Leave Chatbot")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you with your leave today?"}]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Enter your query"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            response = handle_user_query(prompt) # Function to handle the query
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)


if __name__ == "__main__":
    main()