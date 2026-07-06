import { useState } from "react";
import API from "../services/api";

function ChatInput({ setAnswer }) {

    const [question, setQuestion] = useState("");
    const [loading, setLoading] = useState(false);

    async function sendQuestion() {

    if (!question.trim()) return;

    try {

        setLoading(true);

        const response = await API.post("/ask", {
            question: question
        });

        setAnswer(response.data.answer);

        setQuestion("");

    } catch (e) {

        setAnswer("Something went wrong.");

    } finally {

        setLoading(false);

    }
}
    return (
        <div className="chat-input">

            <input
    type="text"
    value={question}
    disabled={loading}
    placeholder="Ask anything about the document..."
    onChange={(e) => setQuestion(e.target.value)}
    onKeyDown={(e) => {
        if (e.key === "Enter") {
            sendQuestion();
        }
    }}
/>

            <button onClick={sendQuestion} disabled={loading}>
                {loading ? "Thinking..." : "Send"}
            </button>

        </div>
    );
}

export default ChatInput;