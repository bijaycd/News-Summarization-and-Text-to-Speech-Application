from setuptools import find_packages, setup

setup(
    name="News-Summarization-and-Text-to-Speech-Application",
    version="0.0.1",
    author="bijay",
    author_email="bjaydasiitb@gmail.com",
    packages=find_packages(),
    install_requires=["SpeechRecognition","pipwin","pyaudio","gTTS","google-generativeai","python-dotenv","streamlit"]
)