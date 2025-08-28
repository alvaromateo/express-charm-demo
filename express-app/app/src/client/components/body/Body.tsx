import { ApiSSRResponse } from "../../types/apiResponseTypes";
import Counter from "../counter/Counter";
import ServerMessage from "../serverMessage/ServerMessage";

async function Body() {
  const message = await fetch(
    `http://${process.env.FLASK_BACKEND_HOST}:${process.env.FLASK_BACKEND_PORT}/api/ssr`
  )
    .then((response) => response.json())
    .then((data) => (data as ApiSSRResponse).message);

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
      <Counter />
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
      <div id="ssr-rendered">
        <h3>SSR rendered message</h3>
        <p id="flask-output">{message}</p>
      </div>
      <ServerMessage />
    </>
  );
}

export default Body;
