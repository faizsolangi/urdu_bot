import streamlit as st
from audio_recorder_streamlit import audio_recorder
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from gtts import gTTS
import base64
from io import BytesIO
import asyncio
import streamlit.components.v1 as components
from openai import OpenAI
import re

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM with streaming enabled
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    streaming=True
)

# Define the system prompt for a kid-friendly Urdu letter tutor
system_template = """
You are a 5-year-old Urdu letter tutor teaching 5-year-old children. Speak like a playful 5-year-old friend in simple, fun Urdu. Follow these instructions exactly:

- Accept questions in mixed English and Urdu, like "What is ا?" or "ب kya hai?", but always respond only in simple, pure Urdu.
- Teach Urdu letters in a fun, story-like way to make learning exciting.
- For every letter, include one short example word using animals, fruits, or toys, like "ا آم کی ہے!".
- Clearly state the letter and the example word in each response so they can be shown in big, bold text.
- Never use difficult words; keep language very simple for 5-year-olds.
- Keep responses to one or two short sentences.
- Talk like a 5-year-old, using playful phrases like "واہ، ا بہت مزے کا ہے!".
- Remember which letters the child has learned and suggest the next letter, like "ا سیکھ لیا؟ اب ب سیکھیں!".
- If a question is not about letters, gently say, "آؤ، حروف سیکھیں!".
- End every answer with a fun question, like "پرندے کا حرف سیکھیں؟".
- Avoid any inappropriate content, such as violence, complex ideas, or anything not suitable for 5-year-olds.
"""

# Set up the prompt template with history and input variables
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{history}\n{input}")
])

# Initialize session state for conversation memory and cache
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "response_cache" not in st.session_state:
    st.session_state.response_cache = {}

# Create the conversation chain
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=st.session_state.memory,
    input_key="input"
)

# Asynchronous function to convert text to speech
async def async_text_to_speech(text):
    loop = asyncio.get_event_loop()
    def generate_audio():
        tts = gTTS(text=text, lang='ur')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return base64.b64encode(audio_bytes.read()).decode('utf-8')
    return await loop.run_in_executor(None, generate_audio)

# Synchronous function for Whisper transcription
def transcribe_audio(audio_file_path, api_key):
    try:
        client = OpenAI(api_key=api_key)
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ur"
            )
        return transcript.text
    except Exception as e:
        raise Exception(f"Whisper transcription failed: {str(e)}")

# Custom HTML for auto-playing audio with fallback
def play_audio(audio_base64):
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    components.html(audio_html, height=0)

# Function to style the letter and example word in big, bold text
def style_response(response_text):
    # Find the letter and example word using regex (assuming single Urdu letter and a word)
    letter_match = re.search(r'[ا-ے]', response_text)
    word_match = re.search(r'\b(?!آؤ|سیکھیں|ہیلو|واہ|مزے|کیا|ہائیں|پرندے|حرف|اب|بہت)\w+\b', response_text)
    
    letter = letter_match.group(0) if letter_match else ""
    word = word_match.group(0) if word_match else ""
    
    # Style the letter and word in big, bold text
    if letter and word:
        styled_response = response_text.replace(
            letter, f"<span style='font-size: 32px; font-weight: bold;'>{letter}</span>"
        ).replace(
            word, f"<span style='font-size: 28px; font-weight: bold;'>{word}</span>"
        )
        return styled_response
    return response_text

# Streamlit app
st.title("بچوں کے لیے اردو حروف ٹیوٹر")
st.write("ہیلو! میں تمہارا 5 سال کا اردو حروف کا ٹیچر ہوں! مجھ سے حروف کے بارے میں پوچھو، جیسے 'ا کیا ہے؟' یا 'What is ب?' بول کر یا ٹائپ کر کے پوچھو۔ آؤ، سیکھیں!")
st.markdown("**نوٹ**: اگر آواز کام نہ کرے، براہ کرم اپنے براؤزر کی مائیک کی اجازت چیک کریں یا سوال ٹائپ کریں۔")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(style_response(message["content"]), unsafe_allow_html=True)
            if "audio" in message:
                play_audio(message["audio"])
        else:
            st.markdown(message["content"])

# Voice input
st.write("اپنا سوال بولو:")
try:
    audio_bytes = audio_recorder(
        text="بولنے کے لیے کلک کرو",
        energy_threshold=(100, 3000),
        pause_threshold=2.0,
        sample_rate=44100
    )
except Exception as e:
    st.error(f"آڈیو ریکارڈر ناکام ہوا: {str(e)}۔ براہ کرم براؤزر کی مائیک اجازت چیک کریں یا سوال ٹائپ کریں۔")

# Text input
user_input = st.chat_input("یا یہاں سوال ٹائپ کرو")

# Process input (voice or text)
input_text = None
if audio_bytes:
    with st.spinner("تمہاری بات سن رہا ہوں"):
        # Save audio to temporary file
        temp_file = "temp_audio.wav"
        try:
            with open(temp_file, "wb") as f:
                f.write(audio_bytes)
            # Use OpenAI Whisper for transcription
            input_text = transcribe_audio(temp_file, os.getenv("OPENAI_API_KEY"))
            st.session_state.messages.append({"role": "user", "content": input_text})
            with st.chat_message("user"):
                st.markdown(input_text)
            os.remove(temp_file)
        except Exception as e:
            st.error(f"معاف کرو، سمجھ نہ سکا: {str(e)}۔ براہ کرم دوبارہ بولنے کی کوشش کریں یا سوال ٹائپ کریں۔")
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
elif user_input:
    input_text = user_input
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)

# Process bot response
if input_text:
    try:
        # Check cache for response
        cache_key = input_text.lower().strip()
        if cache_key in st.session_state.response_cache:
            response, audio_base64 = st.session_state.response_cache[cache_key]
            with st.chat_message("assistant"):
                st.markdown(style_response(response), unsafe_allow_html=True)
                play_audio(audio_base64)
        else:
            # Stream response
            response_container = st.chat_message("assistant")
            response_text = ""
            with response_container:
                response_placeholder = st.empty()
                for chunk in conversation.stream(input_text):
                    response_text += chunk.get("response", "")
                    response_placeholder.markdown(style_response(response_text), unsafe_allow_html=True)
            # Generate audio asynchronously
            with st.spinner("آواز بنا رہا ہوں"):
                audio_base64 = asyncio.run(async_text_to_speech(response_text))
            # Cache response
            st.session_state.response_cache[cache_key] = (response_text, audio_base64)
            # Auto-play audio
            play_audio(audio_base64)
            # Store in session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "audio": audio_base64
            })
    except Exception as e:
        st.error(f"معاف کرو، کچھ غلط ہو گیا: {str(e)}")