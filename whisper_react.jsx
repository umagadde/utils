// React Frontend (VoiceRecorder.js)
import React, { useState, useRef } from 'react';
import axios from 'axios';

const VoiceRecorder = () => {
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const toggleRecording = async () => {
    if (isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    } else {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        audioChunksRef.current.push(e.data);
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/mp3' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.mp3');

        // const response = await axios.post('http://localhost:8000/transcribe', formData);
        var text="sent to backend";
        setTranscript(text);
      };

      mediaRecorder.start();
      setIsRecording(true);
    }
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <button onClick={toggleRecording} style={{ fontSize: '20px', padding: '10px 20px' }}>
        {isRecording ? '🎙️ Recording... Click to Stop' : '🎤 Start Recording'}
      </button>
      <div style={{ marginTop: '20px' }}>
        <strong>Transcript:</strong>
        <p>{transcript}</p>
      </div>
    </div>
  );
};

export default VoiceRecorder;
