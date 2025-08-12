"use client";

import { useEffect, useState } from "react";
import { ApiTestResponse } from "../../types/apiResponseTypes";

function ServerMessage() {
  const [message, setMessage] = useState("SSR message");

  useEffect(() => {
    fetch("/api/test")
      .then((response) => response.json())
      .then((data) => setMessage((data as ApiTestResponse).message));
  }, []);

  return (
    <div id="dynamic-message">
      <h3>SSR rendered message</h3>
      <p>{message}</p>
    </div>
  );
}

export default ServerMessage;
