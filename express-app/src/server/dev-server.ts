import fs from "node:fs/promises";
import path from "path";
import { ViteDevServer, createServer } from "vite";
import { Express } from "express";
import { RenderOutput } from "../client/entry-server";

let vite: ViteDevServer | undefined;

export async function setUpDevServer(app: Express): Promise<void> {
  if (!vite) {
    vite = await createServer({
      publicDir: "public",
      logLevel: "info",
      server: {
        middlewareMode: true,
        hmr: false,
      },
      appType: "custom",
      root: process.cwd(),
    });
  }

  app.use(vite.middlewares);
}

export async function serveDevHTML(app: Express) {
  if (!vite) {
    await setUpDevServer(app);
  }

  // this has to be the last rule
  app.use("*all", async (req, res) => {
    try {
      const url = req.originalUrl;
      let template = await fs.readFile(
        path.join(process.cwd(), "index.html"),
        "utf-8"
      );

      template = await vite!.transformIndexHtml(url, template);
      let render: (url: string) => RenderOutput = (
        await vite!.ssrLoadModule("src/client/entry-server.tsx")
      ).render;

      const rendered = await render(url);
      const html = template
        .replace(`<!--app-head-->`, rendered.head ?? "")
        .replace(`<!--app-html-->`, rendered.body ?? "");

      res.status(200).set({ "Content-Type": "text/html" }).send(html);
    } catch (e) {
      if (e instanceof Error) {
        vite?.ssrFixStacktrace(e);
        console.log(e.stack);
        res.status(500).end(e.stack);
      }
    }
  });
}
