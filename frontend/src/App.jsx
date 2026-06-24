import { useState, useRef } from 'react'

const initialMessages = [
  { role: 'assistant', text: 'Welcome! Ask me to book or manage an appointment.' }
]

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState(initialMessages)
  const [input, setInput] = useState('')
  const [status, setStatus] = useState('Ready')
  const [toolEvents, setToolEvents] = useState([])
  const [summary, setSummary] = useState(null)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const mediaRecorderRef = useRef(null)
  const recordingChunksRef = useRef([])
  const audioStreamRef = useRef(null)

  const addMessage = (msg) => setMessages((prev) => [...prev, msg])
  const addToolEvent = (text) => setToolEvents((prev) => [text, ...prev].slice(0, 5))

  const startSession = async () => {
    setStatus('Starting session...')
    const res = await fetch('/api/voice/start-session', { method: 'POST' })
    const data = await res.json()
    setSessionId(data.session_id)
    setStatus('Session started')
    return data.session_id
  }

  const startRecording = async () => {
    if (isRecording) return
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      audioStreamRef.current = stream
      const recorder = new MediaRecorder(stream)
      recordingChunksRef.current = []

      recorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) {
          recordingChunksRef.current.push(event.data)
        }
      })

      recorder.addEventListener('stop', async () => {
        setIsRecording(false)
        setStatus('Processing voice input...')
        const audioBlob = new Blob(recordingChunksRef.current, { type: 'audio/webm' })
        await sendVoiceMessage(audioBlob)
        if (audioStreamRef.current) {
          audioStreamRef.current.getTracks().forEach((track) => track.stop())
          audioStreamRef.current = null
        }
      })

      mediaRecorderRef.current = recorder
      recorder.start()
      setIsRecording(true)
      setStatus('Recording...')
    } catch (error) {
      setStatus('Microphone access denied')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
    }
  }

  const sendVoiceMessage = async (audioBlob) => {
    let sid = sessionId
    if (!sid) {
      sid = await startSession()
    }

    const formData = new FormData()
    formData.append('audio', audioBlob, 'voice.webm')

    const transcribeRes = await fetch('/api/voice/transcribe', {
      method: 'POST',
      body: formData
    })
    const transcriptData = await transcribeRes.json()

    if (!transcribeRes.ok || !transcriptData.text) {
      setStatus('Speech recognition failed')
      return
    }

    addMessage({ role: 'user', text: transcriptData.text })
    await processTextInput(sid, transcriptData.text)
  }

  const synthesizeAudio = async (text) => {
    setStatus('Generating voice output...')
    try {
      const res = await fetch('/api/voice/synthesize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      })

      if (!res.ok) {
        setStatus('Voice playback failed')
        return
      }

      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const audio = new Audio(url)

      return new Promise((resolve) => {
        audio.addEventListener('ended', () => {
          URL.revokeObjectURL(url)
          resolve()
        })
        audio.play().catch(() => {
          URL.revokeObjectURL(url)
          resolve()
        })
      })
    } catch (error) {
      setStatus('Voice playback error')
    }
  }

  const processTextInput = async (sid, text) => {
    setStatus('Sending message...')
    setIsSpeaking(true)

    const res = await fetch('/api/voice/process-message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sid, text })
    })
    const result = await res.json()

    const toolMessage = result.tool_message || (result.tool ? `Tool called: ${result.tool}` : null)
    if (toolMessage) {
      setStatus(toolMessage)
      addToolEvent(toolMessage)
      addMessage({ role: 'assistant', text: toolMessage })
    }

    addMessage({ role: 'assistant', text: result.response })
    await synthesizeAudio(result.response)
    setInput('')
    setIsSpeaking(false)
    setStatus('Ready')
  }

  const sendMessage = async () => {
    if (!input.trim()) return
    let sid = sessionId
    if (!sid) {
      sid = await startSession()
    }
    setStatus('Sending message...')
    setIsSpeaking(true)
    addMessage({ role: 'user', text: input })

    await processTextInput(sid, input)
  }

  const finishSession = async () => {
    if (!sessionId) {
      setStatus('Start a session first')
      return
    }
    setStatus('Ending session...')
    const res = await fetch(`/api/voice/end-session/${sessionId}`, { method: 'POST' })
    const data = await res.json()
    setStatus(data.message || 'Session ended')
    setSummary(data.summary)
    addToolEvent(data.message || 'Session ended')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>Healthcare Front Desk AI</h1>
        <div className={`avatar-card ${isSpeaking ? 'speaking' : ''}`}>
          <div className="avatar-face">
            <div className="avatar-eyes" />
            <div className="avatar-mouth" />
          </div>
          <span>{isSpeaking ? 'Speaking...' : 'Ready'}</span>
        </div>

        <div className="status-card">
          <strong>Status</strong>
          <p>{status}</p>
        </div>

        <div className="tool-log">
          <strong>Tool activity</strong>
          <ul>
            {toolEvents.map((event, index) => (
              <li key={index}>{event}</li>
            ))}
          </ul>
        </div>

        <button className="end-session" onClick={finishSession} disabled={!sessionId}>
          End Session
        </button>
      </aside>

      <main className="chat-panel">
        <div className="messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <span>{msg.role === 'user' ? 'You' : 'Agent'}:</span>
              <p>{msg.text}</p>
            </div>
          ))}
        </div>

        <div className="composer">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                sendMessage()
              }
            }}
            placeholder="Type your request here..."
          />
          <button disabled={!input.trim()} onClick={sendMessage}>Send</button>
          <button
            className={isRecording ? 'recording' : 'record'}
            onClick={isRecording ? stopRecording : startRecording}
          >
            {isRecording ? 'Stop' : 'Voice'}
          </button>
        </div>

        {summary && (
          <section className="session-summary">
            <h2>Session Summary</h2>
            <pre>{summary}</pre>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
