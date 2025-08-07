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
import aiohttp
import streamlit.components.v1 as components

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
تم 5 سال کے بچوں کے لیے اردو حروف کا ٹیوٹر ہو۔ بچہ انگریزی اور اردو ملا کر سوال پوچھ سکتا ہے، جیسے "What is ا?" یا "ب kya hai؟"، لیکن تم صرف آسان اور خالص اردو میں جواب دو۔ حروف تہجی کو بہت آسان اور مزے دار طریقے سے سکھاؤ، جیسے کہانی ہو۔ جانور، پھل یا کھلونوں کی چھوٹی چھوٹی مثالیں دو۔ مشکل الفاظ نہ استعمال کرو، جواب ایک یا دو جملوں میں رکھو۔ بچوں کی طرح چھوٹی چھوٹی باتیں کرو، جیسے "واہ، ا بہت مزے کا ہے!" یاد رکھو کہ بچے نے کون سے حروف سیکھے اور اگلا حرف تجویز کرو، جیسے "ا سیکھ لیا؟ اب ب سیکھیں!" اگر سوال حروف سے ہٹ کر ہو، تو نرمی سے کہو، "آؤ، حروف سیکھیں!" ہر جواب میں ایک مثال دو، جیسے "ا آم کی ہے۔" آخر میں مزے دار سوال پوچھو، جیسے "پرندے کا حرف سیکھیں؟" نامناسب مواد سے بچو، جیسے تشدد، مشکل باتیں، یا کوئی بھی چیز جو بچوں کے لیے ٹھیک نہ ہو۔
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

# Asynchronous function for Whisper transcription
async def async_transcribe_audio(audio_file_path, api_key):
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field('file', open(audio_file_path, 'rb'), filename='audio.wav')
        form.add_field('model', 'whisper-1')
        form.add_field('language', 'ur')
        async with session.post(
            'https://api.openai.com/v1/audio/transcriptions',
            headers={'Authorization': f'Bearer {api_key}'},
            data=form
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result['text']
            else:
                raise Exception(f"Whisper API error: {await response.text()}")

# Custom HTML for auto-playing audio with fallback
def play_audio(audio_base64):
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    components.html(audio_html, height=0)

# Streamlit app
st.title("بچوں کے لیے اردو حروف ٹیوٹر")
st.write("ہیلو! میں تمہارا اردو حروف کا ٹیچر ہوں۔ مجھ سے حروف کے بارے میں پوچھو، جیسے 'ا کیا ہے؟' یا 'What is ب?' بول کر یا ٹائپ کر کے پوچھو۔ آؤ، سیکھیں!")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "audio" in message:
            play_audio(message["audio"])

# Voice input
st.write("اپنا سوال بولو:")
audio_bytes = audio_recorder(
    text="بولنے کے لیے کلک کرو",
    energy_threshold=(100, 3000),
    pause_threshold=2.0,
    sample_rate=44100
)

# Text input
user_input = st.chat_input("یا یہاں سوال ٹائپ کرو")

# Process input (voice or text)
input_text = None
if audio_bytes:
    with st.spinner("تمہاری بات سن رہا ہوں"):
        # Save audio to temporary file
        temp_file = "temp_audio.wav"
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)
        # Use OpenAI Whisper for transcription
        try:
            input_text = asyncio.run(async_transcribe_audio(temp_file, os.getenv("OPENAI_API_KEY")))
            st.session_state.messages.append({"role": "user", "content": input_text})
            with st.chat_message("user"):
                st.markdown(input_text)
            os.remove(temp_file)
        except Exception as e:
            st.error(f"معاف کرو، سمجھ نہ سکا: {str(e)}")
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
                st.markdown(response)
                play_audio(audio_base64)
        else:
            # Stream response
            response_container = st.chat_message("assistant")
            response_text = ""
            with response_container:
                response_placeholder = st.empty()
                for chunk in conversation.stream(input_text):
                    response_text += chunk.get("response", "")
                    response_placeholder.markdown(response_text)
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