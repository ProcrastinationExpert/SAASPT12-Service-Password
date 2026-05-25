import "dotenv/config";
import express from "express";
import { createProxyMiddleware } from "http-proxy-middleware";
import cors from "cors";

const app = express();
app.use(cors());

const PYTHON_SERVICE_URL = process.env.PASSWORD_SERVICE_URL;
if (!PYTHON_SERVICE_URL) {
  console.error(
    "Error: PASSWORD_SERVICE_URL pada environment variable belum di-set.",
  );
  process.exit(1);
}

app.use(
  "/api/gateway/passwords",
  createProxyMiddleware({
    target: PYTHON_SERVICE_URL,
    changeOrigin: true,
    pathRewrite: {
      "^/api/gateway/passwords": "/python-service/passwords",
    },
    logger: console, // Biar kelihatan log traffic-nya di terminal
    on: {
      proxyReq: (proxyReq, req, res) => {
        console.log(
          `[Gateway Proxy] Forwarding ${req.method} request to Python Service`,
        );
      },
    },
  }),
);

const PORT = process.env.PORT;
if (!PORT) {
  console.error("Error: PORT pada environment variable belum di-set.");
  process.exit(1);
}

app.listen(PORT, "0.0.0.0", () =>
  console.log(`Node.js Reverse Proxy Gateway running on port ${PORT}`),
);
