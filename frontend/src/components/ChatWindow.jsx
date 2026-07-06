function ChatWindow({ answer }) {
  return (
    <div className="chat-window">
      <h2>Chat</h2>

      <div className="answer">
        {answer || "Upload a PDF and ask a question."}
      </div>
    </div>
  );
}

export default ChatWindow;