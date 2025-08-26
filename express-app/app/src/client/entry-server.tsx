import { JSX, StrictMode } from "react";
import { renderToPipeableStream } from "react-dom/server";
import { Writable } from "node:stream";

import Head from "./components/head/Head";
import Body from "./components/body/Body";

export type RenderOutput = {
  head: string;
  body: string;
};

async function renderToStringAsync(jsx: JSX.Element): Promise<string> {
  return new Promise((resolve, reject) => {
    let html = "";
    const writable = new Writable({
      write(chunk, _encoding, callback) {
        html += chunk.toString();
        callback();
      },
    });

    const { pipe } = renderToPipeableStream(jsx, {
      onAllReady() {
        pipe(writable);
      },
      onError(err) {
        reject(err);
      },
    });

    writable.on("finish", () => resolve(html));
    writable.on("error", reject);
  });
}

export async function render(_url: string): Promise<RenderOutput> {
  return {
    head: await renderToStringAsync(
      <StrictMode>
        <Head />
      </StrictMode>
    ),
    body: await renderToStringAsync(
      <StrictMode>
        <Body />
      </StrictMode>
    ),
  };
}
