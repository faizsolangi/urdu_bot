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

# Load environment variables
load_dotenv()

# Initialize OpenAI LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Define the system prompt for a kid-friendly Urdu letter tutor
system_template = """
تم ایک دوستانہ اردو حروف کا ٹیوٹر ہو جو 5 سال کے بچوں کے لیے ہے۔ اردو حروف تہجی کو بہت آسان اور مزے دار طریقے سے سکھاؤ، جیسے کوئی کہانی سنا رہے ہو۔ ایسی مثالیں استعمال کرو جو بچوں کو پسند ہوں، جیسے جانور، پھل، یا کھلونے۔ مشکل الفاظ سے بچو اور جوابات بہت چھوٹے رکھو۔ صرف خالص اردو استعمال کرو، انگریزی الفاظ یا انگریزی تلفظ سے بچو۔ بچوں کی طرح بات کرو، جیسے تم بھی ایک چھوٹا دوست ہو۔ یاد رکھو کہ بچے نے کون سے حروف سیکھے ہیں اور اگلا حرف تجویز کرو، جیسے "تم نے ا سیکھا، اب ب سیکھیں؟" اگر بچہ اردو حروف سے ہٹ کر کچھ پوچھے، تو نرمی سے اسے حروف سیکھنے کی طرف لاؤ۔ ہر جواب میں ایک آسان مثال دو، جیسے "ا آم کی طرح ہے۔" ہر جواب ایک مزے دار سوال کے ساتھ ختم کرو، جیسے "کیا تم پرندے کا حرف سیکھنا چاہتے ہو؟" نامناسب یا مشکل مواد سے مکمل طور پر بچو، جیسے تشدد، پیچیدہ تصورات، یا بچوں کے لیے غیر موزوں چیزیں۔
"""

# Set up the prompt template with history and input variables
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{history}\n{input}")
])

# Initialize session state for conversation memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create the conversation chain
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=st.session_state.memory,
    input_key="input"
)

# Function to convert text to speech using gTTS with Urdu support
def text_to_speech(text):
    tts = gTTS(text=text, lang='ur')  # Set language to Urdu
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
    return audio_base64

# Streamlit app
st.title("بچوں کے لیے اردو حروف ٹیوٹر")
st.write("ہیلو! میں تمہارا اردو حروف کا ٹیچر ہوں۔ مجھ سے اردو حروف کے بارے میں پوچھو، جیسے 'ا کیا ہے؟' یا 'ب کے بارے میں بتاؤ۔' تم ٹائپ کر سکتے ہو یا مائیک پر بول سکتے ہو۔ آؤ، مل کر سیکھیں۔")

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "audio" in message:
            # Auto-play audio
            st.audio(f"data:audio/mp3;base64,{message['audio']}", format="audio/mp3", autoplay=True)

# Voice input
st.write("اپنا سوال بولو:")
audio_bytes = audio_recorder(
    text="بولنے کے لیے کلک کرو",
    energy_threshold=(100, 3000),
    pause_threshold=2.0,
    sample_rate=44100
)

# Text input
user_input = st.chat_input("یا یہاں اپنا سوال ٹائپ کرو")

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
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            with open(temp_file, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="ur"  # Set transcription language to Urdu
                )
            input_text = transcript.text
            st.session_state.messages.append({"role": "user", "content": input_text})
            with st.chat_message("user"):
                st.markdown(input_text)
            os.remove(temp_file)
        except Exception as e:
            st.error(f"معاف کرو، میں سمجھ نہ سکا: {str(e)}")
elif user_input:
    input_text = user_input
    st.session_state.messages.append({"role": "user", "content": input_text})
    with st.chat_message("user"):
        st.markdown(input_text)

# Process bot response
if input_text:
    try:
        with st.spinner("سوچ رہا ہوں"):
            response = conversation.run(input_text)
        with st.spinner("آواز بنا رہا ہوں"):
            audio_base64 = text_to_speech(response)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "audio": audio_base64
        })
        with st.chat_message("assistant"):
            st.markdown(response)
            # Auto-play audio for the response
            st.audio(f"data:audio/mp3;base64,{audio_base64}", format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"معاف کرو، کچھ غلط ہو گیا: {str(e)}")