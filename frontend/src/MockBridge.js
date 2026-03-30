console.warn("🚀 MAARGHA Mock Bridge Active: Simulating Backend Responses");

const MOCK_DELAY = 600;
const originalFetch = window.fetch;

// --- Helper for creating fake AI responses ---
const aiRespond = (prompt) => {
    const text = prompt.toLowerCase();
    if (text.includes("react")) return "React is a declarative, component-based library for building user interfaces. Key concepts include Hooks (`useEffect`, `useState`) and the virtual DOM.";
    if (text.includes("docker")) return "Docker uses containers to bundle an application with all its dependencies. It ensures the app runs consistently across different environments.";
    if (text.includes("plan") || text.includes("roadmap")) return "I recommend a 6-month path focusing on: 1. Core JS/CSS. 2. Framework Mastery (React/Next). 3. Cloud Architectures (AWS). 4. AI integration.";
    return `That's an interesting question about "${prompt}". As your Maargha AI architect, I suggest we look into the architectural implications and scalability of that approach.`;
};

window.fetch = async (url, options) => {
    const urlString = typeof url === 'string' ? url : url.toString();
    console.log(`%c[MockBridge Fetch] -> ${urlString}`, "color: #00ff00; font-weight: bold;", options?.body || '');

    // Auth
    if (urlString.includes("/auth/login/")) {
        await new Promise(r => setTimeout(r, MOCK_DELAY));
        const body = JSON.parse(options.body);
        return new Response(JSON.stringify({
            access: "mock_access_token_" + Date.now(),
            refresh: "mock_refresh_token_" + Date.now(),
            user: { id: 1, name: body.username || "Mock Developer", email: body.username + "@maargha.ai" }
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }

    if (urlString.includes("/auth/register/")) {
        await new Promise(r => setTimeout(r, MOCK_DELAY));
        return new Response(JSON.stringify({ message: "Mock account created!", status: "success" }), { status: 201 });
    }

    if (urlString.includes("/auth/logout")) {
        return new Response(JSON.stringify({ message: "Logged out" }), { status: 200 });
    }

    // CV Generation
    if (urlString.includes("/cv/generate")) {
        await new Promise(r => setTimeout(r, 1200));
        if (urlString.endsWith("/pdf") || urlString.endsWith("/pdf/download")) {
            // Return a dummy PDF blob
            const dummyPdf = new Blob(["%PDF-1.4 Mock Content"], { type: 'application/pdf' });
            return new Response(dummyPdf, { status: 200 });
        }
        return new Response(JSON.stringify({
            status: "success",
            cv: "PROFESSIONAL PROFILE: \n Strategic AI developer with expertise in mock bridges..."
        }), { status: 200 });
    }

    // Resume Parser
    if (urlString.includes("/resume/parse")) {
        await new Promise(r => setTimeout(r, 2000));
        return new Response(JSON.stringify({
            entities: {
                Name: "Jinan",
                Skills: ["React", "Python", "FastAPI", "Agentic Workflows"],
                Experience: "3+ Years in Fullstack AI",
                Education: "B.Tech Computer Science",
                Location: "Remote / Bangalore"
            }
        }), { status: 200 });
    }

    // Roadmap
    if (urlString.includes("/roadmap/generate")) {
        await new Promise(r => setTimeout(r, 1500));
        return new Response(JSON.stringify({
            video_url: "https://www.w3schools.com/html/mov_bbb.mp4",
            steps: ["Foundation", "Building UI", "API Integration", "Deployment"]
        }), { status: 200 });
    }

    // Music
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

    // News
    if (urlString.includes("/news/latest")) {
        return new Response(JSON.stringify({
            articles: [
                { title: "AI Revolutionizes Career Mapping", source: "Margha Tech", link: "#" },
                { title: "The Rise of Agentic AI Assistants", source: "Google DeepMind", link: "#" },
                { title: "FastUI: The future of Frontend", source: "Vite Weekly", link: "#" }
            ]
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }

    // Jobs
    if (urlString.includes("/jobs/search") || urlString.includes("/jobs/match")) {
        return new Response(JSON.stringify({
            jobs: [
                { title: "Senior AI Engineer", company: "Margha AI", location: "Remote", desc: "Design premium Agentic UIs...", score: 0.95, source: "LinkedIn", link: "#" },
                { title: "Backend Specialist", company: "CloudScale", location: "Hybrid", desc: "Python, FastAPI & K8s expert needed.", score: 0.88, source: "Indeed", link: "#" },
                { title: "Product Designer", company: "AestheticUI", location: "Bangalore", desc: "Minimalist design and Framer Motion.", score: 0.82, source: "Glassdoor", link: "#" }
            ]
        }), { status: 200 });
    }

    // Defaults to original fetch if not caught
    return originalFetch(url, options);
};

// --- WebSocket Mocking ---
const OriginalWebSocket = window.WebSocket;
window.WebSocket = class MockWebSocket extends EventTarget {
    constructor(url) {
        super();
        this.url = url;
        this.readyState = 0; // CONNECTING
        console.log(`%c[MockBridge WS] Connecting -> ${url}`, "color: #00ccff; font-weight: bold;");

        setTimeout(() => {
            this.readyState = 1; // OPEN
            const openEvent = new Event("open");
            this.dispatchEvent(openEvent);
            if (this.onopen) this.onopen(openEvent);

            // Initial messages for specific WS types
            if (url.includes("/ws/career")) {
                this._sendToClient({ type: "career_question", question: "Do you enjoy working with Visual Designs and Colors?", question_id: 0 });
            }
            if (url.includes("/ws/quiz")) {
              this._sendToClient({ type: "quiz_question", question: "What is the primary purpose of React's useEffect hook?", options: ["Visuals", "Side Effects", "Routing", "Storage"], id: 1 });
            }
        }, 300);
    }

    send(data) {
        console.log(`%c[MockBridge WS Sent] ->`, "color: #ff9900;", data);
        let parsed = data;
        try { parsed = JSON.parse(data); } catch (e) { }
        
        // Simulate thinking delay
        setTimeout(() => {
            this._handleClientMessage(parsed);
        }, 800);
    }

    _handleClientMessage(msg) {
        // Orchestrator Chat / Live
        if (this.url.includes("/ws/chat")) {
            const userQuery = typeof msg === 'string' ? msg : (msg.content || JSON.stringify(msg));
            
            // Check for navigation tokens
            if (userQuery.toLowerCase().includes("job")) {
                this._sendToClient({ type: "CHAT", content: "Navigating you to the Job Board..." });
                this._sendToClient({ navigate: { tool: "JobSearch" } });
                return;
            }

            this._sendToClient({
                type: "CHAT",
                content: aiRespond(userQuery)
            });
        }

        // AI Tutor
        else if (this.url.includes("/ws/tutor")) {
            if (msg.type === "tutor_question") {
                this._sendToClient({
                    type: "tutor_answer",
                    answer: aiRespond(msg.question)
                });
            }
        }

        // Career WS
        else if (this.url.includes("/ws/career")) {
            if (msg.type === "career_answer") {
                this._sendToClient({
                    type: "career_result",
                    careers: [
                        { title: "Frontend Specialist", reason: "Since you love visual design...", skills: ["React", "CSS", "GSAP"] },
                        { title: "System Architect", reason: "Your strategic thinking...", skills: ["K8s", "Microservices"] }
                    ]
                });
            }
        }

        // Quiz WS
        else if (this.url.includes("/ws/quiz")) {
            if (msg.type === "quiz_answer") {
                this._sendToClient({ 
                    type: "quiz_evaluation", 
                    result: { score: 100, feedback: "Perfect! Side effects are the primary use case for useEffect." } 
                });
            }
        }

        // LinkedIn WS
        else if (this.url.includes("/ws/linkedin")) {
            this._sendToClient({ type: "linkedin_reply", message: "Here's a catchy post for your profile: 'Excited to be mastering Agentic AI with Maargha! #AI #FutureOfWork'" });
        }

        else {
            const userText = typeof msg === 'string' ? msg : JSON.stringify(msg);
            this._sendToClient(`[Mock AI] Response: "I received: ${userText}". Frontend looks great!`);
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
        const closeEvent = new Event("close");
        this.dispatchEvent(closeEvent);
        if (this.onclose) this.onclose(closeEvent);
        console.log("%c[MockBridge WS] Closed", "color: #999;");
    }
};

window.WebSocket.CONNECTING = 0;
window.WebSocket.OPEN = 1;
window.WebSocket.CLOSING = 2;
window.WebSocket.CLOSED = 3;
