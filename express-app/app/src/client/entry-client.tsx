import "./index.css";
import { hydrateRoot } from "react-dom/client";
import Body from "./components/body/Body";
import { StrictMode } from "react";

hydrateRoot(
  document.getElementById("root") as HTMLElement,
  <StrictMode>
    <Body data={window.__INITIAL_DATA__} />
  </StrictMode>
);
