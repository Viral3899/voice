import React, { useEffect, useState, useRef } from 'react';

const API_BASE = 'http://localhost:5000';

const Avatar = ({ speaking }) => (
  <div style={{display:'flex',alignItems:'center',gap:16}}>
    <div style={{width:120,height:120,background:'#eee',borderRadius:12,display:'flex',alignItems:'center',justifyContent:'center',flexDirection:'column'}}>
      <div style={{width:64,height:64,borderRadius:32,background:'#b5d0ff'}} />
      <div style={{width:40,height:10,marginTop:8,background:'#111',borderRadius:6,transform: speaking ? 'scaleY(1.6)' : 'scaleY(1)',transition:'transform 0.08s linear'}} />
    </div>
    <div>
      <strong>Agent Avatar</strong>
      <div style={{fontSize:12,color:'#666'}}>{speaking ? 'Speaking...' : 'Idle'}</div>
    </div>
  </div>
)

const App = () => {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [messages, setMessages] = useState([]);
  const [speaking, setSpeaking] = useState(false);
  const [slots, setSlots] = useState([]);
  const recognitionRef = useRef(null);

  useEffect(() => {
    // init speech recognition if available
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    const r = new SpeechRecognition();
    r.lang = 'en-US';
    r.interimResults = false;
    r.onresult = (e) => {
      const text = Array.from(e.results).map(r => r[0].transcript).join('');
      setTranscript(text);
      appendMessage({from:'user', text});
      handleUserText(text);
    };
    r.onend = () => setListening(false);
    recognitionRef.current = r;
  }, []);

  const appendMessage = (m) => setMessages(prev => [...prev, {...m, time: new Date().toISOString()}]);

  const startListening = () => {
    if (recognitionRef.current) {
      setTranscript('');
      setListening(true);
      recognitionRef.current.start();
    } else {
      alert('SpeechRecognition not supported in this browser');
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) recognitionRef.current.stop();
    setListening(false);
  };

  const speak = (text) => {
    if (!window.speechSynthesis) return;
    setSpeaking(true);
    const u = new SpeechSynthesisUtterance(text);
    u.onend = () => setSpeaking(false);
    window.speechSynthesis.speak(u);
  };

  async function handleUserText(text) {
    // simple intent detection for demo
    const lower = text.toLowerCase();
    if (lower.includes('slots') || lower.includes('available')) {
      appendMessage({from:'system', text:'Fetching slots...' });
      const res = await fetch(`${API_BASE}/fetch_slots`);
      const data = await res.json();
      setSlots(data.slots || []);
      appendMessage({from:'system', text:'Slots fetched.'});
      speak('I found available slots.');
      return;
    }

    if (lower.includes('book') || lower.includes('appointment')) {
      // Try to extract date/time/phone via naive patterns
      const payload = { text };
      appendMessage({from:'system', text:'Booking appointment...' });
      // For demo use identify_user first
      // Ask for phone if not present
      const phoneMatch = (text.match(/\+?\d[\d\-\s]{6,}\d/) || [])[0];
      const phone = phoneMatch ? phoneMatch.replace(/[^0-9+]/g,'') : null;
      const nameMatch = text.match(/name is ([A-Z][a-z]+)/i);
      const name = nameMatch ? nameMatch[1] : 'Guest';
      // naive date/time in yyyy-mm-dd and HH:MM
      const dateMatch = text.match(/(\d{4}-\d{2}-\d{2})/);
      const timeMatch = text.match(/(\d{1,2}:\d{2})/);
      const body = { phone, name, date: dateMatch?dateMatch[1]:null, time: timeMatch?timeMatch[1]:null };
      const res = await fetch(`${API_BASE}/book_appointment`, {method:'POST',headers:{'content-type':'application/json'},body: JSON.stringify(body)});
      const data = await res.json();
      if (res.ok) {
        appendMessage({from:'system', text:`Booking confirmed ✅ ${data.date} ${data.time}`});
        speak('Your appointment is confirmed.');
      } else {
        appendMessage({from:'system', text:`Booking failed: ${data.error || 'unknown'}`});
        speak('I could not book that slot.');
      }
      return;
    }

    // Fallback echo
    appendMessage({from:'system', text:'I heard: '+text});
    speak('You said: ' + text);
  }

  return (
    <main style={{padding:20,fontFamily:'Arial, sans-serif'}}>
      <h1>Voice AI Agent</h1>
      <div style={{display:'flex',gap:24}}>
        <div style={{flex:1}}>
          <Avatar speaking={speaking} />
          <div style={{marginTop:16}}>
            <button onClick={startListening} disabled={listening} style={{marginRight:8}}>Start Listening</button>
            <button onClick={stopListening} disabled={!listening}>Stop</button>
          </div>
          <div style={{marginTop:12}}><strong>Transcript:</strong> {transcript}</div>
          <div style={{marginTop:12}}>
            <strong>Messages:</strong>
            <div style={{border:'1px solid #eee',padding:8,maxHeight:240,overflow:'auto'}}>
              {messages.map((m,i)=> (
                <div key={i} style={{padding:6,background:m.from==='user'? '#f1f8ff':'#f6f6f6',marginBottom:6}}>
                  <div style={{fontSize:12,color:'#666'}}>{m.time}</div>
                  <div>{m.text}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div style={{width:320}}>
          <h3>Slots</h3>
          <div style={{border:'1px solid #eee',padding:8}}>
            {slots.length===0 && <div>No slots fetched yet.</div>}
            {slots.map((s,idx)=> (
              <div key={idx} style={{marginBottom:8}}>
                <div style={{fontWeight:600}}>{s.date}</div>
                <div style={{display:'flex',gap:8,flexWrap:'wrap'}}>{s.times.map(t=> <div key={t} style={{padding:'4px 8px',border:'1px solid #ddd',borderRadius:6}}>{t}</div>)}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

export default App;
