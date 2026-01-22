let audioContext = null;
let processor = null;
let source = null;
let streamRef = null;
let silenceTimer = null;
let micEnabled = true;
const SILENCE_THRESHOLD = 0.01;
const SILENCE_TIMEOUT = 2500;
export function muteMic() {
  micEnabled = false;
}
export function unmuteMic() {
  micEnabled = true;
}
export function startMicStream(ws, onVolume) {
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    streamRef = stream;
    audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
    source = audioContext.createMediaStreamSource(stream);
    processor = audioContext.createScriptProcessor(4096, 1, 1);
    source.connect(processor);
    processor.connect(audioContext.destination);
    processor.onaudioprocess = e => {
      if (!micEnabled) return;
      if (ws.readyState !== WebSocket.OPEN) return;
      const input = e.inputBuffer.getChannelData(0);
      ws.send(input.buffer);
      const volume =
        input.reduce((s, v) => s + Math.abs(v), 0) / input.length;

      if (onVolume) onVolume(volume);

      if (volume > SILENCE_THRESHOLD) {
        if (silenceTimer) {
          clearTimeout(silenceTimer);
          silenceTimer = null;
        }
      } else {
        if (!silenceTimer) {
          silenceTimer = setTimeout(() => {
            ws.send("STOP");
            silenceTimer = null;
          }, SILENCE_TIMEOUT);
        }
      }
    };
  });
}
export function stopMicStream() {
  micEnabled = false;
  if (processor) processor.disconnect();
  if (source) source.disconnect();
  if (audioContext) audioContext.close();
  streamRef?.getTracks().forEach(t => t.stop());
  processor = source = audioContext = streamRef = null;
  silenceTimer = null;
}


