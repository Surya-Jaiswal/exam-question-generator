import re
import smtplib
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
)


# ---------------- CONFIGURATION ----------------

MODEL_NAME = "gemini-3.8-flash"

GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(
    page_title="ExamBuddy",
    page_icon="📚",
    layout="centered",
)


# ---------------- GEMINI CLIENT ----------------

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


def create_chat():
    return gemini_client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )


def ask_gemini(parts):
    """Return Gemini's response and an optional error."""

    try:
        response = st.session_state.chat.send_message(parts)

        if not response.text:
            return None, "Gemini returned an empty response. Please try again."

        return response.text, None

    except Exception:
        return (
            None,
            "Gemini could not process your request. "
            "Please check your API key, model name, and connection.",
        )


# ---------------- EMAIL ----------------

def send_email(to_address, subject, body):
    """Send an email using Gmail SMTP."""

    try:
        message = MIMEText(body, "plain", "utf-8")
        message["Subject"] = subject
        message["From"] = GMAIL_ADDRESS
        message["To"] = to_address

        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465, timeout=30
        ) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.send_message(message)

        return True, "Email sent successfully."

    except (smtplib.SMTPException, OSError):
        return (
            False,
            "Email delivery failed. Check your Gmail App Password "
            "and internet connection.",
        )


def is_valid_email(address):
    """Basic email format validation."""

    return bool(
        re.fullmatch(
            r"[^@\s]+@[^@\s]+\.[^@\s]+",
            address.strip(),
        )
    )


# ---------------- CHAT HISTORY ----------------

def render_message(message):
    with st.chat_message(message["role"]):

        if message["kind"] == "text":
            st.write(message["content"])

        elif message["kind"] == "image":
            st.image(message["content"], width="stretch")


def add_message(role, kind, content):
    message = {
        "role": role,
        "kind": kind,
        "content": content,
    }

    st.session_state.messages.append(message)
    render_message(message)


# ---------------- SESSION STATE ----------------

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if not st.session_state.onboarded:

    st.title("ExamBuddy 📚")
    st.subheader("Your Personal AI Exam Question Generator")

    st.write(
        "Upload your study material and turn it into "
        "practice questions, quizzes, and answer keys."
    )

    with st.form("onboarding_form"):

        name = st.text_input("Your name")
        recipient_email = st.text_input("Your email address")

        submitted = st.form_submit_button(
            "Let's Prepare 📝",
            use_container_width=True,
        )

        if submitted:

            if not name.strip():
                st.error("Please enter your name.")

            elif not is_valid_email(recipient_email):
                st.error("Please enter a valid email address.")

            else:
                st.session_state.name = name.strip()
                st.session_state.email = recipient_email.strip()
                st.session_state.chat = create_chat()
                st.session_state.messages = []
                st.session_state.has_study_material = False
                st.session_state.onboarded = True

                st.rerun()

    st.stop()


# ---------------- MAIN INTERFACE ----------------

header_col, button_col = st.columns(
    [0.65, 0.35],
    vertical_alignment="center",
)

with header_col:
    st.title("ExamBuddy 📚")

with button_col:
    if st.button(
        "📩 Email My Practice Test",
        disabled=not st.session_state.has_study_material,
        use_container_width=True,
    ):

        with st.spinner("Preparing your practice test..."):

            summary, error = ask_gemini(
                [SUMMARY_REQUEST_PROMPT]
            )

            if error:
                st.error(error)

            else:
                success, info = send_email(
                    st.session_state.email,
                    "Your ExamBuddy Practice Test",
                    summary,
                )

                if success:
                    st.success(
                        "Practice test emailed successfully! 📩"
                    )
                else:
                    st.error(info)


st.caption(
    f"Welcome, {st.session_state.name}! "
    "Upload notes, textbook pages, or diagrams to get started."
)


# ---------------- DISPLAY HISTORY ----------------

if not st.session_state.messages:

    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        ),
    )

else:

    for message in st.session_state.messages:
        render_message(message)


# ---------------- USER INPUT ----------------

user_input = st.chat_input(
    "Upload study material or ask a question...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)


if user_input:

    photo = user_input.files[0] if user_input.files else None
    text = user_input.text.strip() if user_input.text else ""

    parts = []

    # Add the image to Gemini's request.
    if photo is not None:

        photo_bytes = photo.getvalue()

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type or "image/jpeg",
            )
        )

    # Add the user's text to the same request.
    if text:
        parts.append(text)

    elif photo is not None:
        parts.append(
            "Analyze this study material. Identify its main "
            "topics and generate relevant practice questions. "
            "Explain important concepts clearly."
        )

    if not parts:
        st.warning("Please enter a question or upload an image.")

    else:

        # Display the user's input.
        if photo is not None:
            add_message("user", "image", photo_bytes)

        if text:
            add_message("user", "text", text)

        # Generate Gemini's response.
        with st.spinner("ExamBuddy is analyzing your material..."):

            answer, error = ask_gemini(parts)

        if error:
            st.error(error)
        else:
            add_message("assistant", "text", answer)

            # Enable email only after Gemini responds successfully.
            st.session_state.has_study_material = True
            st.rerun()