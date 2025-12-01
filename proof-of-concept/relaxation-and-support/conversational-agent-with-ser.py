import torch
import numpy as np
import asyncio
import tempfile
import io
from groq import Groq
from openai import OpenAI
import pyttsx3
import pyaudio
import librosa
import soundfile as sf
from pydub import AudioSegment
from threading import Lock
import queue
import time
from transformers import pipeline
from datetime import datetime

client = Groq(api_key="")

class EmotionalAgent:
    def __init__(self):
        print("Initializing Emotional Agent...")

