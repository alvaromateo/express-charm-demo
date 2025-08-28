import { JSX } from "react";
import { renderToPipeableStream } from "react-dom/server";
import { Writable } from "node:stream";

import Head from "./components/head/Head";
import Body from "./components/body/Body";
import { ApiSSRResponse } from "./types/apiResponseTypes";

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
  const data = await fetch(
    `http://${process.env.FLASK_BACKEND_HOST}:${process.env.FLASK_BACKEND_PORT}/api/ssr`
  ).then((response) => response.json() as unknown as ApiSSRResponse);

  return {
    head: (await renderToStringAsync(<Head />)).concat(
      `<script>window.__INITIAL_DATA__=${JSON.stringify(data)}</script>`
    ),
    body: await renderToStringAsync(<Body data={data} />),
  };
}
