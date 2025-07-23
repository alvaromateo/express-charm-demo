import { StrictMode } from "react";
import { renderToString } from "react-dom/server";
import Head from "./Head";
import Body from "./Body";

export type RenderOutput = {
  head: string;
  body: string;
};

export function render(_url: string): RenderOutput {
  return {
    head: renderToString(
      <StrictMode>
        <Head />
      </StrictMode>
    ),
    body: renderToString(
      <StrictMode>
        <Body />
      </StrictMode>
    ),
  };
}
