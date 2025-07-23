import { Router } from "express";

const apiHost = process.env.BE_HOST || "flask-app";
const apiPort = process.env.BE_PORT || 5000;

const router = Router();

router.all("*all", async (req, res) => {
  let redirectUrl = `http://${apiHost}:${apiPort.toString()}${req.originalUrl}`;
  console.log("Forwarding request to Flask BE: " + redirectUrl);
  try {
    const response = await fetch(redirectUrl);
    const data = await response.json();
    res.json(data);
  } catch (e) {
    if (e instanceof Error) {
      console.log(e);
      res.status(500).end(e.message);
    }
  }
});

export default router;
