/**
 * MockBridge.js
 * Intercepts all backend calls (Fetch and WebSockets)
 * and simulates responses locally.
 *
 * TO REMOVE: Just delete the import of this file in main.jsx
 */

console.warn("🚀 MAARGHA Mock Bridge Active: Simulating Backend Responses");

const MOCK_DELAY = 600;

// --- 1. MOCK FETCH INTERCEPTOR ---
const originalFetch = window.fetch;
window.fetch = async (url, options) => {
    const urlString = typeof url === 'string' ? url : url.toString();

    console.log(`[MockBridge Fetch] -> ${urlString}`, options?.body || '');

    // AUTH
    if (urlString.includes("/auth/login/")) {
        await new Promise(r => setTimeout(r, MOCK_DELAY));
        return new Response(JSON.stringify({
            access: "mock_access_token_" + Date.now(),
            refresh: "mock_refresh_token_" + Date.now(),
            user: { id: 1, full_name: "Mock Developer", email: "dev@maargha.ai" }
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }

    if (urlString.includes("/auth/register/")) {
        await new Promise(r => setTimeout(r, MOCK_DELAY));
        return new Response(JSON.stringify({ message: "Mock account created!" }), { status: 201 });
    }

    if (urlString.includes("/auth/logout")) {
        return new Response(JSON.stringify({ message: "Logged out" }), { status: 200 });
    }

    // ROADMAP
    if (urlString.includes("/roadmap/generate")) {
        await new Promise(r => setTimeout(r, 1500));
        return new Response(JSON.stringify({
            video_url: "https://www.w3schools.com/html/mov_bbb.mp4"
        }), { status: 200 });
    }

    // MUSIC
    if (urlString.includes("/music/recommend")) {
        await new Promise(r => setTimeout(r, 1000));
        return new Response(JSON.stringify({
            song: {
                title: "Mock Chill Vibes",
                song_emotions: ["Relaxed", "Happy"],
                audio_url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            }
        }), { status: 200 });
    }

    // NEWS
    if (urlString.includes("/news/latest")) {
        return new Response(JSON.stringify([
            { title: "AI Revolutionizes Career Mapping", summary: "New techniques in LLMs allow...", link: "#" },
            { title: "FastAPI 0.124 Released", summary: "Performance benchmarks show 20% gain...", link: "#" }
        ]), { status: 200 });
    }

    // JOBS
    if (urlString.includes("/jobs/search")) {
        return new Response(JSON.stringify([
            { title: "Frontend Developer", company: "AI Startup", location: "Remote", description: "Design premium UIs..." },
            { title: "Backend Engineer", company: "Tech Giant", location: "Hybrid", description: "Python & FastAPI..." }
        ]), { status: 200 });
    }

    return originalFetch(url, options);
};

// --- 2. MOCK WEBSOCKET INTERCEPTOR ---
const OriginalWebSocket = window.WebSocket;
window.WebSocket = class MockWebSocket extends EventTarget {
    constructor(url) {
        super();
        this.url = url;
        this.readyState = 0; // CONNECTING
        console.log(`[MockBridge WS] Opening to ${url}`);

        setTimeout(() => {
            this.readyState = 1; // OPEN
            this.dispatchEvent(new Event("open"));
            if (this.onopen) this.onopen();

            // Initial triggers
            if (url.includes("/ws/career")) {
                this._sendToClient({ type: "career_question", question: "Do you enjoy working with Visual Designs and Colors?", question_id: 0 });
            }
        }, 150);
    }

    send(data) {
        console.log(`[MockBridge WS Client Sent] -> ${data}`);
        let parsed = data;
        try { parsed = JSON.parse(data); } catch (e) { }

        setTimeout(() => {
            this._handleClientMessage(parsed);
        }, 800);
    }

    _handleClientMessage(msg) {
        // Career
        if (this.url.includes("/ws/career")) {
            if (msg.type === "career_answer") {
                this._sendToClient({
                    type: "career_result",
                    careers: [
                        { title: "Frontend Specialist", reason: "Since you love visual design...", skills: ["React", "CSS", "GSAP"] },
                        { title: "Product Designer", reason: "Your interest in user experience...", skills: ["Figma", "Design Systems"] }
                    ]
                });
            }
            if (msg.type === "select_career") {
                this._sendToClient({ type: "career_saved", career: msg.career });
            }
        }

        // Quiz
        else if (this.url.includes("/ws/quiz")) {
            if (msg.type === "start_quiz") {
                this._sendToClient({ type: "quiz_question", question: "What is the primary purpose of React's useEffect hook?" });
            } else {
                this._sendToClient({ type: "quiz_evaluation", result: { score: 90, feedback: "Excellent!" } });
            }
        }

        // LinkedIn
        else if (this.url.includes("/ws/linkedin")) {
            this._sendToClient({ type: "linkedin_reply", message: "That's a great profile query! Here are 3 tips for your LinkedIn summary..." });
        }

        // Chat / Orchestrator / Emotional Support
        else {
            const userText = typeof msg === 'string' ? msg : JSON.stringify(msg);
            this._sendToClient(`[Mock AI] Simulated Response: "I received your message: ${userText}". Everything is working perfectly on the frontend!`);
        }
    }

    _sendToClient(data) {
        const event = new MessageEvent("message", {
            data: typeof data === 'string' ? data : JSON.stringify(data)
        });
        this.dispatchEvent(event);
        if (this.onmessage) this.onmessage(event);
    }

    close() {
        this.readyState = 3; // CLOSED
        this.dispatchEvent(new Event("close"));
        if (this.onclose) this.onclose();
        console.log("[MockBridge WS] Closed");
    }
};

window.WebSocket.CONNECTING = 0;
window.WebSocket.OPEN = 1;
window.WebSocket.CLOSING = 2;
window.WebSocket.CLOSED = 3;
