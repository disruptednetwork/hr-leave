## HR Leave Application

This Streamlit application provides an HR chatbot interface for employees to inquire about their leave balance.

See more details in the blog written in Thai language:

[HR APP with Streamlit + Cloud Run + Gemini + Cloud SQL with authentication through Azure AD](https://medium.com/google-cloud-thailand/hr-app-เช็ควันลาแบบลูกทุ่งจานด่วนโดยใช้-streamlit-ผ่าน-cloud-run-gemini-cloud-sql-และทำ-2fbce13ab119)

### Description

The application leverages:

* **Microsoft Azure AD authentication:** Users log in using their Azure AD credentials.
* **Vertex AI Generative Model:** The chatbot classifies user intent related to HR leave (get balance, submit request, etc.).
* **PostgreSQL database:** Stores leave balance information for employees.

### Installation

**Dependencies:**

The project dependencies are listed in `requirements.txt`.

**Installation:**

1. Clone the repository (if you haven't already).
2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Linux/macOS
   .venv\Scripts\activate  # On Windows
   ```
3. Install the required libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in your project directory and set the following environment variables:
    * `CLIENT_ID`: Your Azure AD application client ID.
    * `TENANT_ID`: Your Azure AD tenant ID.
    * `CLIENT_SECRET`: Your Azure AD application client secret.
    * `REDIRECT_URI`: The redirect URI configured for your Azure AD application.
    * `POSTGRES_HOST`: The hostname of your PostgreSQL database server.
    * `POSTGRES_DB`: The name of your PostgreSQL database.
    * `POSTGRES_USER`: The username for your PostgreSQL database.
    * `POSTGRES_PASSWORD`: The password for your PostgreSQL database.
    * `PROJECT_ID`: Your Google Cloud Project ID for Vertex AI.
    * `REGION`: The region where your Vertex AI endpoint is located.
5. See the [blog](https://medium.com/google-cloud-thailand/hr-app-เช็ควันลาแบบลูกทุ่งจานด่วนโดยใช้-streamlit-ผ่าน-cloud-run-gemini-cloud-sql-และทำ-2fbce13ab119) for more details on
   * creating the Postgres database on Cloud SQL
   * packing the image and deploy on Cloud Run

### Usage

1. Run the application using `streamlit run main.py`.
2. Log in using your Azure AD credentials.
3. Type your leave-related questions in the chat interface and press Enter.
4. The chatbot will respond based on your intent and retrieve your leave balance if applicable.

**Note:** Submitting leave requests is not yet implemented in this version.

### References

The Azure AD authentication was inspired by and incorporates ideas from Parham's great blog post:
- [Streamlit login with Azure AD Authentication](https://medium.com/@prhmma/streamlit-login-with-azure-ad-authentication-66ebd1691858)
- [GitHub Repository: Streamlit Authentication with Azure AD](https://github.com/Prhmma/Streamlit_Azure_AD)

