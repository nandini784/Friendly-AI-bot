import streamlit as st
import ollama

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Friendly AI Bot",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* ---------- PROFESSIONAL BACKGROUND ---------- */
.stApp {
    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #172554 45%,
            #1e3a8a 100%
        );

    min-height: 100vh;
}

/* ---------- TITLE ---------- */
.main-title {
    text-align: center;
    color: white;
    font-size: 50px;
    font-weight: 800;
    margin-top: 25px;
    letter-spacing: 1px;

    text-shadow:
        0 4px 15px rgba(0,0,0,0.35);
}

/* ---------- SUBTITLE ---------- */
.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
    margin-top: 8px;
    margin-bottom: 45px;
}

/* ---------- QUESTION TITLE ---------- */
.question-title {
    color: white;
    font-size: 27px;
    font-weight: 700;
    margin-bottom: 15px;
}

/* ---------- INPUT LABEL ---------- */
label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* ---------- INPUT BOX ---------- */
.stTextInput input {
    background: #ffffff !important;
    color: #1e293b !important;

    border: 2px solid #93c5fd !important;
    border-radius: 14px !important;

    padding: 14px !important;
    font-size: 17px !important;

    box-shadow:
        0 6px 20px rgba(0,0,0,0.20);
}

.stTextInput input:focus {
    border: 2px solid #38bdf8 !important;

    box-shadow:
        0 0 15px rgba(56,189,248,0.35);
}

/* ---------- ASK BUTTON ---------- */
.stButton button {
    background: linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    ) !important;

    color: white !important;

    border: none !important;
    border-radius: 12px !important;

    padding: 12px 30px !important;

    font-size: 17px !important;
    font-weight: 700 !important;

    box-shadow:
        0 6px 18px rgba(0,0,0,0.25);

    transition: 0.3s ease;
}

/* ---------- BUTTON HOVER ---------- */
.stButton button:hover {
    background: linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb
    ) !important;

    transform: translateY(-2px);

    box-shadow:
        0 9px 25px rgba(37,99,235,0.35);
}

/* ---------- RESPONSE TITLE ---------- */
.response-title {
    color: white;
    font-size: 28px;
    font-weight: 700;

    margin-top: 40px;
    margin-bottom: 18px;
}

/* ---------- RESPONSE CARD ---------- */
.response-card {
    background: rgba(255,255,255,0.97);

    color: #1e293b;

    padding: 25px;

    border-radius: 18px;

    border: 1px solid rgba(255,255,255,0.8);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.25);

    font-size: 17px;

    line-height: 1.8;
}

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;

    color: #cbd5e1;

    margin-top: 50px;

    font-size: 14px;

    opacity: 0.8;
}

/* ---------- ALERT ---------- */
.stAlert {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🤖 Friendly AI Bot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '✨ Smart • Simple • Friendly • Powered by Ollama ✨'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- QUESTION SECTION ----------------
st.markdown(
    '<div class="question-title">💬 Ask me anything!</div>',
    unsafe_allow_html=True
)

question = st.text_input(
    "Enter your question",
    placeholder="Example: Explain Python in simple words..."
)


# ---------------- ASK AI ----------------
if st.button("🚀 Ask AI"):

    if not question.strip():

        st.warning("⚠️ Please enter a question first!")

    else:

        # Response heading
        st.markdown(
            '<div class="response-title">🤖 AI Response</div>',
            unsafe_allow_html=True
        )

        # Placeholder for streaming response
        response_placeholder = st.empty()

        try:

            # Connect to Ollama
            stream = ollama.chat(
                model="llama3.2",

                messages=[
                    {
                        "role": "system",
                        "content": """
You are a friendly and helpful AI assistant.

Rules:
- Answer in simple language.
- Keep answers clear and easy to understand.
- Be friendly and encouraging.
- Use examples when helpful.
- Avoid unnecessarily long answers.
"""
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],

                # Show answer while it is being generated
                stream=True,

                # Keep model loaded for faster next questions
                keep_alive="10m",

                options={
                    "temperature": 0.4,
                    "num_predict": 180
                }
            )

            answer = ""

            # Display answer word-by-word
            for chunk in stream:

                text = chunk["message"]["content"]

                answer += text

                response_placeholder.markdown(
                    f"""
                    <div class="response-card">
                        {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:

            response_placeholder.error(
                "❌ Could not connect to Ollama. "
                "Please make sure Ollama is running and "
                "the llama3.2 model is installed."
            )


# ---------------- FOOTER ----------------
st.markdown(
    '<div class="footer">'
    '💜 Built with Python • Streamlit • Ollama'
    '</div>',
    unsafe_allow_html=True
)