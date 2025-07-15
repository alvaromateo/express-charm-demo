import { Router } from "express";

const router = Router();

router.all("/", (req, res, next) => {
  console.log("Forwarding request to Flask BE...");
  next();
});

export default router;
