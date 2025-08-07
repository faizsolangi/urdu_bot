# Urdu Letter Tutor Bot for Kids

This is a fun and friendly Urdu letter tutor bot designed for 5-year-old kids. It teaches Urdu letters (حروف تہجی) in a simple way, using stories and examples like animals, fruits, or toys. The bot supports voice input (via microphone) and voice output (in Urdu), making it engaging for young learners. It uses Streamlit for the web interface, LangChain with OpenAI for conversation management, and tracks learning progress to suggest the next letter.

## Features
- Teaches Urdu letters with simple, kid-friendly explanations (e.g., "ا is for آم, which means mango!").
- Supports voice input using OpenAI's Whisper for Urdu transcription.
- Provides voice output in Urdu using gTTS.
- Tracks progress with conversation memory, suggesting the next letter (e.g., ب after ا).
- Gently redirects off-topic questions to Urdu letter learning.
- Deployable on Render as a web app.

## Prerequisites
- Python 3.8 or higher
- A GitHub account for deployment
- An OpenAI API key (get it from https://platform.openai.com)
- A Render account (sign up at https://render.com)

## Setup
1. **Clone the Repository**:
   ```bash
   git clone <your-repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

## Local Testing
1. Run the Streamlit app locally:
   ```bash
   streamlit run urdu_tutor_bot.py
   ```
2. Open the provided URL (e.g., `http://localhost:8501`) in your browser.
3. Test by typing a question like "What is ا?" or using the microphone to ask. The bot will respond with text and audio, e.g., "ا is for آم, which means mango! Want to learn ب for a bird?"

## Deployment on Render
1. **Push to GitHub**:
   - Create a GitHub repository and push your code:
     ```bash
     git add .
     git commit -m "Initial commit"
     git push origin main
     ```

2. **Create a Render Web Service**:
   - Sign in to https://render.com and create a new Web Service.
   - Connect your GitHub repository.
   - Set the runtime to `Python 3`.
   - Set the build command: `pip install -r requirements.txt`.
   - Set the start command: `streamlit run urdu_tutor_bot.py --server.port $PORT --server.headless true`.
   - Add the environment variable `OPENAI_API_KEY` with your OpenAI API key in Render's dashboard.

3. **Deploy**:
   - Trigger deployment in Render.
   - Access the bot via the provided URL (e.g., `https://your-app.onrender.com`).

## Usage
- Open the deployed URL in a browser.
- Type a question (e.g., "What is ب?") or click the microphone to record a question in Urdu.
- The bot transcribes voice input, responds with a simple explanation (e.g., "ب is for بلبل, which is a bird! Want to learn the next letter?"), and plays the response in Urdu audio.
- The bot remembers learned letters and suggests the next one in the Urdu alphabet.

## Files
- `urdu_tutor_bot.py`: Main application script with Streamlit, LangChain, and audio processing.
- `.env`: Stores the OpenAI API key (not committed to Git).
- `requirements.txt`: Lists dependencies (`streamlit`, `audio-recorder-streamlit`, `python-dotenv`, `langchain`, `langchain-openai`, `gTTS`, `openai`).

## Troubleshooting
- **Audio issues**: Ensure your OpenAI API key has credits for Whisper transcription. Check Render logs for errors.
- **Dependency errors**: Verify all packages in `requirements.txt` are compatible with your Python version.
- **Deployment failures**: Confirm the start command and environment variables are set correctly in Render.

## Notes
- Designed for 5-year-olds, using very simple language and examples like fruits or animals.
- Uses OpenAI's Whisper for Urdu voice transcription and gTTS for Urdu audio output.
- Tracks progress with LangChain's `ConversationBufferMemory` to suggest the next letter.
- Ensure a stable internet connection for voice input/output and API calls.
