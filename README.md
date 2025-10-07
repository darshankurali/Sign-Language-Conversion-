# Sign Language Translation System

An intelligent, real-time sign language interpretation system that facilitates seamless communication between individuals with hearing or speech impairments and the general public.

## 📖 Overview

This project bridges communication gaps by translating sign language gestures into readable text and audible speech, while also converting voice input into text. The system supports both American Sign Language (ASL) and Indian Sign Language (ISL), handling both static gestures (alphabets) and dynamic gestures (words/phrases).

## ✨ Key Features

- **Real-time Translation**: Converts sign language gestures to text and speech instantly
- **Dual Modality**: Supports both gesture-to-text/speech and voice-to-text conversion
- **Multi-Gesture Support**: Handles both static (alphabets) and dynamic (words) gestures
- **Bidirectional Communication**: Enables two-way interaction between signers and non-signers
- **Multi-Language Support**: Works with ASL and ISL
- **User-Friendly Interface**: Simple GUI for easy interaction

## 🛠️ Technology Stack

### Machine Learning & Deep Learning
- **Convolutional Neural Networks (CNN)** - Static gesture recognition
- **Long Short-Term Memory (LSTM)** - Dynamic gesture sequence recognition
- **Random Forest Classifier** - Lightweight gesture classification
- **TensorFlow/Keras** - Model training and deployment

### Computer Vision
- **OpenCV** - Image processing and video capture
- **MediaPipe** - Real-time hand landmark detection
- **NumPy & Pandas** - Data handling and numerical operations

### Speech Processing
- **Google Speech Recognition API** - Voice-to-text conversion
- **Google Text-to-Speech (gTTS)** - Text-to-speech synthesis
- **SpeechRecognition Library** - Audio input processing

### Programming
- **Python 3.8+** - Core programming language

## 📋 Requirements

### Hardware
- **Processor**: Intel Core i5 or higher
- **RAM**: Minimum 8 GB
- **Webcam**: HD (720p or higher)
- **Microphone**: Built-in or external
- **Storage**: Minimum 100 MB free space
- **GPU**: Recommended for faster processing (optional)

### Software
- Python 3.8 or above
- OpenCV
- MediaPipe
- TensorFlow/Keras
- SpeechRecognition
- gTTS or pyttsx3
- NumPy and Pandas

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/sign-language-translation.git
   cd sign-language-translation
   ```

2. **Set up virtual environment (optional)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install opencv-python mediapipe tensorflow speechrecognition gtts numpy pandas scikit-learn
   ```

## 🎯 Usage

### Gesture to Text/Speech Translation
```bash
python src/main.py --mode gesture
```
- Position your hand in front of the webcam
- Perform ASL/ISL gestures
- View translated text and hear audio output

### Voice to Text Conversion
```bash
python src/main.py --mode voice
```
- Speak into the microphone
- View transcribed text on screen

### Training Custom Models
```bash
python src/train_model.py --dataset path/to/dataset --model_type cnn
```

## 📊 Performance

The system achieves:
- **95.2% accuracy** for static ASL alphabet recognition (CNN)
- **100% accuracy** for dynamic ISL gestures (LSTM)
- **92% accuracy** with Random Forest classifier
- **98-99% accuracy** for speech recognition
- **<500ms latency** for real-time processing

## 🔧 Customization

### Adding New Gestures
1. Collect gesture data using data collection script
2. Retrain models with extended dataset
3. Update gesture mapping dictionary

### Supporting New Languages
1. Add language-specific datasets
2. Update text preprocessing for the language
3. Configure TTS for language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Future Enhancements

- Sentence-level gesture recognition
- Multi-language input/output support
- Facial expression and body posture integration
- Mobile application deployment
- Offline functionality
- User personalization mode
