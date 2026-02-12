const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

let mainWindow;
let backendProcess;

function getBackendPath() {
  const isPackaged = app.isPackaged;
  if (isPackaged) {
    const platform = process.platform;
    const ext = platform === 'win32' ? '.exe' : '';
    return path.join(process.resourcesPath, 'backend', `server${ext}`);
  }
  return null;
}

function startBackend() {
  const backendPath = getBackendPath();
  if (!backendPath) {
    console.log('Dev mode: backend should be started manually');
    return;
  }

  console.log('Starting backend:', backendPath);
  backendProcess = spawn(backendPath, [], {
    stdio: 'pipe',
    env: { ...process.env }
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`[backend] ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`[backend] ${data}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
  });
}

function waitForBackend(url, timeout = 30000) {
  return new Promise((resolve, reject) => {
    const start = Date.now();

    function check() {
      const req = http.get(url, (res) => {
        resolve();
      });

      req.on('error', () => {
        if (Date.now() - start > timeout) {
          reject(new Error('Backend startup timeout'));
        } else {
          setTimeout(check, 500);
        }
      });

      req.end();
    }

    check();
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 900,
    minHeight: 600,
    title: 'Учёт сотрудников — ГАУК «Брянская областная филармония»',
    icon: path.join(__dirname, '..', 'build', 'icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  mainWindow.loadURL('http://127.0.0.1:8000');

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', async () => {
  startBackend();

  try {
    await waitForBackend('http://127.0.0.1:8000/api/auth/me?token=ping');
  } catch (e) {
    console.error('Failed to start backend:', e.message);
  }

  createWindow();
});

app.on('window-all-closed', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
  app.quit();
});

app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill();
  }
});
