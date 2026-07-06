import { useState } from "react";
import "./styles/App.css";
import "./styles/Navbar.css";
import "./styles/Upload.css";
import "./styles/Chat.css";
import Navbar from "./components/Navbar";
import UploadBox from "./components/UploadBox";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

function App() {

  const [answer, setAnswer] = useState("");

  return (
    <div className="app">
      <Navbar />
      <UploadBox />
      <ChatWindow answer={answer} />
      <ChatInput setAnswer={setAnswer} />
    </div>
  );
}

export default App;