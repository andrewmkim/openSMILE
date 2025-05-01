from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import opensmile
import numpy as np
import librosa
import tempfile
import os
import json

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_voice(audio: UploadFile = File(...)):
    """
    Analyze voice recording using openSMILE
    """
    try:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_filename = temp_file.name
            # Write the uploaded file to the temporary file
            temp_file.write(await audio.read())
        
        # Load the audio file with librosa
        y, sr = librosa.load(temp_filename, sr=None)
        
        # Initialize openSMILE with eGeMAPSv02 feature set
        smile = opensmile.Smile(
            feature_set=opensmile.FeatureSet.eGeMAPSv02,
            feature_level=opensmile.FeatureLevel.Functionals,
        )
        
        # Extract features
        features = smile.process_signal(y, sr)
        
        # Extract specific metrics we're interested in
        # Note: These are approximate mappings to the eGeMAPSv02 feature set
        # In a real implementation, you would need to map these more precisely
        pitch_mean = float(features.loc[0, 'F0semitoneFrom27.5Hz_sma3nz_amean'])
        # Convert semitones to Hz (approximate)
        pitch_hz = 27.5 * (2 ** (pitch_mean / 12))
        
        jitter = float(features.loc[0, 'jitterLocal_sma3nz_amean'])
        shimmer = float(features.loc[0, 'shimmerLocaldB_sma3nz_amean'])
        hnr = float(features.loc[0, 'HNRdBACF_sma3nz_amean'])
        loudness = float(features.loc[0, 'loudness_sma3_amean'])
        
        # Clean up the temporary file
        os.unlink(temp_filename)
        
        # Return the metrics
        return {
            "pitch": pitch_hz,
            "jitter": jitter,
            "shimmer": shimmer,
            "hnr": hnr,
            "loudness": loudness
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing audio: {str(e)}")

@app.get("/")
async def root():
    return {"message": "openSMILE Voice Analysis API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
