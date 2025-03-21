
# A Voice Interface for AI

Point-and-click user interfaces will soon be a thing of the past. The main user interface of the near future will be entirely voice-based.

Speechbot is a platform that aims to enable seamless two-way verbal communication with AI models. It works in both desktop and mobile browsers and currently supports Gemini models, with support for open models under development.



## Usage
To interact with Chatbot, simply start speaking after navigating to the app in your browser. Speechbot will listen to your voice input, process it using an AI model, and provide a synthesized speech response. You can have a natural, continuous conversation with the AI by speaking and listening to its responses.

## Run it Locally  
1. Clone the repo
```bash
git clone 
```
2. Change directory to speechbot
```bash
cd speechbot
```
3. Build Docker image
```bash
docker build -t speechbot .
``` 
or if on arm64 architecture (including Apple Silicon): 
```bash
docker buildx build --platform linux/arm64 -t aiui .
```
4. Create Docker container from image
```bash
docker run -d -e OPENAI_API_KEY=key -e TTS_PROVIDER=googleTTS -p 8000:80 speechbot
```
5. Navigate to `localhost:8000` in a modern browser

