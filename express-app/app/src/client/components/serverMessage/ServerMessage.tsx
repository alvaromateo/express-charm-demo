import { useEffect, useState } from "react";
import { ApiTestResponse } from "../../types/apiResponseTypes";

function ServerMessage() {
  const [message, setMessage] = useState("Server message");

  useEffect(() => {
    fetch("/api/test")
      .then((response) => response.json())
      .then((data) => setMessage((data as ApiTestResponse).message));
  }, []);

  return (
    <div id="dynamic-message">
      <h3>Server message</h3>
      <p>{message}</p>
    </div>
  );
}

export default ServerMessage;
