const { app, BrowserWindow, dialog } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const http = require('http');
const fs = require('fs');

let mainWindow;
let backendProcess;

function getBackendPath() {
  if (app.isPackaged) {
    const ext = process.platform === 'win32' ? '.exe' : '';
    const p = path.join(process.resourcesPath, 'backend', `server${ext}`);
    return p;
  }
  return null;
}

function startBackend() {
  const backendPath = getBackendPath();
  if (!backendPath) {
    console.log('Dev mode: backend should be started manually');
    return;
  }

  if (!fs.existsSync(backendPath)) {
    console.error('Backend binary not found at:', backendPath);
    dialog.showErrorBox('Ошибка запуска', `Не найден файл сервера:\n${backendPath}`);
    return;
  }

  console.log('Starting backend:', backendPath);
  backendProcess = spawn(backendPath, [], {
    stdio: 'pipe',
    cwd: path.dirname(backendPath),
    env: { ...process.env }
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`[backend] ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`[backend] ${data}`);
  });

  backendProcess.on('error', (err) => {
    console.error('Failed to start backend process:', err);
    dialog.showErrorBox('Ошибка', `Не удалось запустить сервер:\n${err.message}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`Backend process exited with code ${code}`);
    if (code !== 0 && code !== null) {
      dialog.showErrorBox('Ошибка сервера', `Сервер завершился с кодом ${code}`);
    }
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

  mainWindow.webContents.on('did-fail-load', (event, errorCode, errorDesc) => {
    console.error('Page failed to load:', errorCode, errorDesc);
    mainWindow.loadURL('http://127.0.0.1:8000');
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', async () => {
  startBackend();

  try {
    await waitForBackend('http://127.0.0.1:8000/api/departments');
  } catch (e) {
    console.error('Failed to start backend:', e.message);
    dialog.showErrorBox(
      'Ошибка запуска',
      'Сервер не запустился за 30 секунд.\nПриложение может работать некорректно.'
    );
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
