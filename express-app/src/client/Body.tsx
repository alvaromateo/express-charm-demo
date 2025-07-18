import { useEffect, useState } from "react";

type ApiTestResponse = {
  message: string;
};

function Body() {
  const [count, setCount] = useState(0);
  const [message, setMessage] = useState("SSR message");

  useEffect(() => {
    fetch("/api/test")
      .then((response) => response.json())
      .then((data) => setMessage((data as ApiTestResponse).message));
  }, []);

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src="/vite.svg" className="logo" alt="Vite logo" />
        </a>
        <a href="https://reactjs.org" target="_blank">
          <img src="/react.svg" className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <p id="flask-output">{message}</p>
    </>
  );
}

export default Body;
