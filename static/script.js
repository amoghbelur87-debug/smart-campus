document.addEventListener('DOMContentLoaded', () => {
    // UI Elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatHistory = document.getElementById('chat-history');
    const voiceBtn = document.getElementById('voice-btn');
    const analyzerResult = document.getElementById('analyzer-result');
    const liveClock = document.getElementById('live-clock');

    // 1. Initial State & Loops
    updateClock();
    setInterval(updateClock, 1000);
    
    fetchSensors();
    setInterval(fetchSensors, 3000); // Poll sensors every 3s

    // 2. Chat Logic
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = userInput.value.trim();
        if (!query) return;

        appendMessage('user', query);
        userInput.value = '';

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            const data = await res.json();
            appendMessage('ai', data.response);
        } catch (err) {
            appendMessage('ai', "System connection interrupted. Retrying...");
        }
    });

    // 3. QR Simulation Logic
    window.simulateScan = async (location) => {
        analyzerResult.innerHTML = '<div class="loader">Analyzing...</div>';
        
        try {
            const res = await fetch('/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location })
            });
            const data = await res.json();
            
            analyzerResult.innerHTML = `
                <div class="analysis-report">
                    <h4 style="color: var(--accent-primary); margin-bottom: 10px;">${location} Insight</h4>
                    <p style="font-size: 0.9rem;">${data.response}</p>
                </div>
            `;
            appendMessage('ai', `Analysis for ${location} complete. Check the viewport.`);
        } catch (err) {
            analyzerResult.innerText = "Analysis failed. Please recalibrate.";
        }
    };

    // 4. Sensor Logic
    async function fetchSensors() {
        try {
            const res = await fetch('/api/sensors');
            const data = await res.json();
            
            updateVal('temp-val', data.temperature);
            updateVal('occupancy-val', data.occupancy);
            updateVal('energy-val', data.energy);
        } catch (err) {
            console.error('Sensor sync failed');
        }
    }

    // 5. Helpers
    function appendMessage(sender, text) {
        const msg = document.createElement('div');
        msg.className = `message ${sender}`;
        msg.innerText = text;
        chatHistory.appendChild(msg);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function updateVal(id, val) {
        const el = document.getElementById(id);
        if (el) el.innerText = val;
    }

    function updateClock() {
        const now = new Date();
        liveClock.innerText = now.toLocaleTimeString();
    }

    // 6. Voice Recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new Recognition();
        
        voiceBtn.onclick = () => {
            voiceBtn.style.color = '#ff0000';
            recognition.start();
        };

        recognition.onresult = (event) => {
            userInput.value = event.results[0][0].transcript;
            voiceBtn.style.color = 'var(--accent-primary)';
            chatForm.dispatchEvent(new Event('submit'));
        };
        
        recognition.onend = () => voiceBtn.style.color = 'var(--accent-primary)';
        recognition.onerror = () => voiceBtn.style.color = 'var(--accent-primary)';
    } else {
        voiceBtn.style.display = 'none';
    }
});
