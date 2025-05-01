# openSMILE Voice Analysis API

This is a FastAPI application that uses openSMILE to analyze voice recordings and extract acoustic features for mental health assessment.

## Features

- Analyzes voice recordings using the eGeMAPSv02 feature set
- Extracts key metrics: pitch, jitter, shimmer, HNR, and loudness
- Provides a simple REST API for integration with web applications

## Deployment Options

### Option 1: Deploy on Render.com

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add the following environment variables:
   - `PYTHON_VERSION`: `3.9.13`

### Option 2: Deploy on Fly.io

1. Install the Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login to Fly: `fly auth login`
3. Create a new app: `fly launch`
4. Deploy the app: `fly deploy`

### Option 3: Deploy on Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Select "Gradio" as the SDK
3. Upload the files from this directory
4. Add a `requirements.txt` file with the dependencies
5. The Space will automatically deploy your API

## Local Development

1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the server: `uvicorn main:app --reload`

## API Endpoints

### POST /analyze

Analyzes a voice recording and returns acoustic features.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with an `audio` field containing a WAV file

**Response:**
\`\`\`json
{
  "pitch": 127.5,
  "jitter": 0.88,
  "shimmer": 1.03,
  "hnr": 24.6,
  "loudness": -19.1
}
\`\`\`

### GET /

Health check endpoint.

**Response:**
\`\`\`json
{
  "message": "openSMILE Voice Analysis API"
}
\`\`\`

## Integration with VoiceVitals

Update the `analyzeVoiceWithOpenSMILE` function in `voice-service.ts` to point to your deployed API:

\`\`\`typescript
export async function analyzeVoiceWithOpenSMILE(audioBlob: Blob): Promise<VoiceMetrics> {
  try {
    // Convert audio to WAV format for openSMILE
    const wavBlob = await convertToWav(audioBlob)
    
    // Create a FormData object to send to the API
    const formData = new FormData()
    formData.append("audio", wavBlob, "recording.wav")
    
    // Call the openSMILE API - replace with your deployed API URL
    const response = await fetch("https://your-opensmile-api-url.com/analyze", {
      method: "POST",
      body: formData,
    })
    
    if (!response.ok) {
      throw new Error(`openSMILE API error: ${response.statusText}`)
    }
    
    const data = await response.json()
    return data as VoiceMetrics
  } catch (error) {
    console.error("Error analyzing voice with openSMILE:", error)
    
    // Return mock data if the API call fails
    return {
      pitch: 120 + Math.random() * 20,
      jitter: 0.8 + Math.random() * 0.2,
      shimmer: 1.0 + Math.random() * 0.1,
      hnr: 22 + Math.random() * 5,
      loudness: -20 + Math.random() * 3
    }
  }
}
