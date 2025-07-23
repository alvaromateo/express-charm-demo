import fs from "node:fs/promises";
import path from "path";
import express from "express";

import apiRoute from "./routes/api";

// Constants
const isProduction = process.env.NODE_ENV === "production";
const port = process.env.PORT || 3000;
const base = process.env.BASE || "/";

// Cache production assets
const templateHtml = await fs.readFile(
  path.join(process.cwd(), "index.html"),
  "utf-8"
);

// Create http server
const app = express();

if (isProduction) {
  const compression = (await import("compression")).default;
  const sirv = (await import("sirv")).default;
  app.use(compression());
  app.use(
    base,
    sirv(path.join(process.cwd(), "dist", "client"), { extensions: [] })
  );
}

app.use("/api", apiRoute);

// Serve HTML for all other routes
// This has to be the last 'use' to catch all paths
if (!isProduction) {
  const serveDevHTML = (await import("./dev-server")).serveDevHTML;
  serveDevHTML(app);
} else {
  app.use("*all", async (req, res) => {
    try {
      const url = req.originalUrl;
      let template = templateHtml;
      let render = (await import("../client/entry-server")).render;

      const rendered = await render(url);
      console.log(rendered);
      const html = template
        .replace(`<!--app-head-->`, rendered.head ?? "")
        .replace(`<!--app-html-->`, rendered.body ?? "");

      res.status(200).set({ "Content-Type": "text/html" }).send(html);
    } catch (e) {
      if (e instanceof Error) {
        console.log(e.stack);
        res.status(500).end(e.stack);
      }
    }
  });
}

// Start http server
app.listen(port, () => {
  console.log(`Server started at http://localhost:${port}`);
});
