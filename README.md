# 📚 ExamBuddy — AI Exam Question Generator

ExamBuddy is an AI-powered study assistant built with **Python, Streamlit, and Google Gemini**. It transforms textbook photos, handwritten notes, diagrams, and study topics into practice questions, quizzes, and explanations.

Students can interact with the AI, generate a complete practice test, and email the test with an answer key for convenient revision.

## ✨ Features

* 📸 **Image-Based Learning:** Upload photos of textbook pages, handwritten notes, and diagrams.
* 💬 **AI Study Assistant:** Ask questions and explore concepts through an interactive chat.
* 📝 **Practice Question Generation:** Generate multiple-choice, short-answer, and long-answer questions.
* 🎯 **Flexible Difficulty:** Request easy, medium, or challenging questions.
* ✅ **Answer Keys & Explanations:** Review correct answers and understand important concepts.
* 📧 **Email Practice Tests:** Send a generated practice test to your email for later revision.
* 🔐 **Secure Configuration:** Store API keys and email credentials using Streamlit secrets.

## 🛠️ Tech Stack

* **Python** — Application logic
* **Streamlit** — Web interface
* **Google Gemini API** — Image understanding and AI-generated responses
* **Gmail SMTP** — Email delivery

## 📁 Project Structure

```text
ExamBuddy/
│
├── app.py                 # Main Streamlit application
├── prompts.py             # Gemini system and summary prompts
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
│
├── .streamlit/
│   └── secrets.toml       # API keys and email credentials
│
├── .gitignore             # Files excluded from Git
└── venv/                  # Local virtual environment (not committed)
```

## 🚀 Getting Started

### 1. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/YOUR_USERNAME/ExamBuddy.git
cd ExamBuddy
```

Replace `YOUR_USERNAME` with your GitHub username and `ExamBuddy` with your repository name if different.

### 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the application using the virtual environment's Python executable directly instead.

For macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

If you haven't created `requirements.txt`, add:

```text
streamlit
google-genai
```

The Python standard library already includes the email and SMTP modules.

### 4. Configure Your API Keys

Create a folder named `.streamlit` in your project directory.

Inside it, create a file named `secrets.toml`:

```toml
GEMINI_API_KEY = "your-gemini-api-key"
GMAIL_ADDRESS = "your-email@gmail.com"
GMAIL_APP_PASSWORD = "your-16-character-app-password"
```

Replace the example values with your actual credentials.

**Get your Gemini API key:**

1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Generate an API key.
3. Add the key to `secrets.toml`.

**Configure Gmail SMTP:**

1. Sign in to your Google account.
2. Enable 2-Step Verification.
3. Visit [Google App Passwords](https://myaccount.google.com/apppasswords).
4. Generate an App Password.
5. Use the generated password in `GMAIL_APP_PASSWORD`.

Use a Gmail App Password, not your regular Google account password. App Passwords may not be available for some account configurations.

### 5. Run the Application

With your virtual environment activated, execute:

```bash
streamlit run app.py
```

Your browser should open the ExamBuddy interface. If it doesn't, open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 📖 How to Use ExamBuddy

1. **Enter your details:** Provide your name and email address.
2. **Upload study material:** Submit a JPG or PNG image of your textbook, notes, or diagram, or type a study topic.
3. **Chat with ExamBuddy:** Ask for practice questions, concept explanations, or specific question types.
4. **Generate your practice test:** Click **Email My Practice Test** after successfully processing study material.
5. **Review and revise:** Open the email and use the questions and answer key to prepare for your exam.

## 🔒 Security Best Practices

Never commit API keys, Gmail App Passwords, or other credentials to GitHub.

Add the following to your `.gitignore` file:

```gitignore
# Python virtual environments
venv/
.venv/

# Secrets and environment variables
.streamlit/secrets.toml
.env

# Python cache files
__pycache__/
*.py[cod]

# Editor and operating system files
.vscode/
.idea/
.DS_Store
Thumbs.db
```

If you accidentally publish a credential, revoke or rotate it immediately. Removing it from a commit does not guarantee that it is no longer accessible.

## 🧰 Troubleshooting

**Gemini API or model error**

* Check that `GEMINI_API_KEY` is correct.
* Confirm that your API key has access to the selected model.
* Verify the model name configured in `app.py`.
* Check your internet connection and API usage limits.

**Gmail authentication failure**

* Confirm that 2-Step Verification is enabled.
* Verify that you are using a valid Gmail App Password.
* Check that the sending Gmail address matches your configuration.

**Missing secrets error**

* Ensure `.streamlit/secrets.toml` exists in the project root.
* Check that all three required settings are present and correctly named.

**PowerShell cannot activate the virtual environment**

* Confirm that the environment was created successfully.
* Check that `venv\Scripts\Activate.ps1` exists.
* Alternatively, run:

```powershell
.\venv\Scripts\python.exe -m streamlit run app.py
```

**Email button remains disabled**

* Upload study material or submit a topic and wait for a successful AI response.
* Check the terminal for Gemini errors.
* Confirm that the app updates its session state after processing the material.

## ⚠️ Limitations

* AI-generated questions and answers may contain errors. Verify important information against your course materials.
* Blurry images, incomplete notes, and complex diagrams may reduce accuracy.
* Email delivery requires valid Gmail SMTP credentials and an internet connection.
* Conversation history is held in Streamlit session state and is not permanently stored.
* Emailing a practice test does not automatically schedule future reminders.

## 🔮 Future Enhancements

* 📄 PDF upload support
* 🎓 Subject and exam-specific question generation
* ⏱️ Timed mock tests and scoring
* 📊 Student performance tracking
* 📅 Study plans and scheduled reminders
* 📚 Saved question banks and revision history

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request describing your improvements.

## 📄 License

This project is available under the MIT License if you choose to distribute it under those terms. Add a `LICENSE` file containing the MIT License text before claiming that the repository is MIT-licensed.

---

**Built with Python, Streamlit, and Google Gemini.**

*Study smarter. Practice better. Prepare with confidence.*
