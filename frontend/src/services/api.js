import axios from "axios";

const API = axios.create({
    baseURL: "https://ai-research-assistant-g1b1.vercel.app/"
});

export default API;