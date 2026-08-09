<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watch Tower · terminal</title>
    <script src="https://cdn.tailwindcss.com">
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800&display=swap');

        :root {
            --bg-terminal: #0b0d0f;
            --text-primary: #d4dcec;
            --text-muted: #5c6b7e;
            --text-green: #6fcf97;
            --text-blue: #7bb3e6;
            --text-red: #f28b82;
            --text-yellow: #f5c542;
            --text-cyan: #5fc8e8;
            --border-color: rgba(255, 255, 255, 0.04);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(circle at 30% 10%, #111 0%, #030303 95%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            transition: background 0.3s ease;
        }

        body.light-theme {
            background: radial-gradient(circle at 30% 10%, #e8ecf1 0%, #d5dae3 95%);
        }

        body.light-theme .glass {
            background: rgba(245, 247, 250, 0.85);
            border: 1px solid rgba(0, 0, 0, 0.06);
            box-shadow: 0 25px 50px -8px rgba(0, 0, 0, 0.15), inset 0 0 0 1px rgba(255, 255, 255, 0.5);
        }

        body.light-theme .terminal {
            background: #f0f2f5;
            border: 1px solid rgba(0, 0, 0, 0.06);
            box-shadow: inset 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        body.light-theme .brand .logo {
            color: #1a202c;
        }

        body.light-theme .terminal-bar .path {
            color: #4a5568;
            background: rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(0, 0, 0, 0.06);
        }

        body.light-theme .terminal-bar .version {
            color: #718096;
            background: rgba(0, 0, 0, 0.04);
        }

        body.light-theme .line .text {
            color: #2d3748;
        }

        body.light-theme .line .text.muted {
            color: #718096;
        }

        body.light-theme .line .text.green {
            color: #2f855a;
        }

        body.light-theme .line .text.blue {
            color: #2b6cb0;
        }

        body.light-theme .line .text.red {
            color: #c53030;
        }

        body.light-theme .line .text.yellow {
            color: #b7791f;
        }

        body.light-theme .line .text.cyan {
            color: #2c7a7a;
        }

        body.light-theme .line .text.bold {
            color: #1a202c;
        }

        body.light-theme .input-row .wrap #cmd-text {
            color: #b7791f;
        }

        body.light-theme .input-row .wrap .cursor {
            background: #2d3748;
        }

        body.light-theme .badge-status {
            background: rgba(47, 133, 90, 0.08);
            border: 1px solid rgba(47, 133, 90, 0.12);
        }

        body.light-theme .badge-status span {
            color: #2f855a;
        }

        body.light-theme .footer .links a {
            color: #4a5568;
        }

        body.light-theme .footer .links a:hover {
            color: #1a202c;
        }

        body.light-theme .footer .links .sep {
            color: #a0aec0;
        }

        body.light-theme .footer .copy {
            color: #718096;
        }

        body.light-theme .footer .version-tag {
            background: rgba(229, 62, 62, 0.08);
            color: #c53030;
            border: 1px solid rgba(229, 62, 62, 0.12);
        }

        .glass {
            background: rgba(20, 20, 22, 0.75);
            backdrop-filter: blur(12px) saturate(180%);
            -webkit-backdrop-filter: blur(12px) saturate(180%);
            border: 1px solid rgba(255, 255, 255, 0.04);
            box-shadow: 0 25px 50px -8px rgba(0, 0, 0, 0.8), inset 0 0 0 1px rgba(255, 255, 255, 0.02);
        }

        .container {
            width: 100%;
            max-width: 820px;
            border-radius: 28px;
            padding: 32px 40px 32px;
            transition: all 0.2s ease;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 28px;
            flex-wrap: wrap;
            gap: 12px 8px;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #1a1a1e, #2a2a2e);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(229, 62, 62, 0.15);
            box-shadow: 0 4px 12px -4px rgba(229, 62, 62, 0.15);
            position: relative;
            flex-shrink: 0;
        }

        body.light-theme .brand-icon {
            background: linear-gradient(135deg, #e2e8f0, #cbd5e0);
            border: 1px solid rgba(229, 62, 62, 0.2);
        }

        .tower-icon {
            position: relative;
            width: 24px;
            height: 28px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-end;
        }

        .tower-body {
            position: relative;
            width: 18px;
            height: 20px;
            background: linear-gradient(180deg, #e53e3e 0%, #b91c1c 100%);
            border-radius: 3px 3px 0 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 2px;
            padding-top: 2px;
            box-shadow: 0 0 12px rgba(229, 62, 62, 0.2);
        }

        body.light-theme .tower-body {
            background: linear-gradient(180deg, #e53e3e 0%, #c53030 100%);
        }

        .tower-window {
            width: 10px;
            height: 4px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 1px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .tower-window:last-child {
            width: 6px;
            height: 3px;
        }

        .tower-antenna {
            position: absolute;
            top: -6px;
            left: 50%;
            transform: translateX(-50%);
            width: 2px;
            height: 6px;
            background: #e53e3e;
            border-radius: 1px;
        }

        .tower-antenna::after {
            content: '';
            position: absolute;
            top: -4px;
            left: 50%;
            transform: translateX(-50%);
            width: 4px;
            height: 4px;
            background: #e53e3e;
            border-radius: 50%;
            opacity: 0.6;
            animation: radar-pulse 2s ease-in-out infinite;
        }

        @keyframes radar-pulse {
            0%,
            100% {
                opacity: 0.3;
                transform: translateX(-50%) scale(0.8);
            }
            50% {
                opacity: 1;
                transform: translateX(-50%) scale(1.2);
            }
        }

        .radar-wave {
            position: absolute;
            top: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 12px;
            height: 12px;
            border: 1.5px solid rgba(229, 62, 62, 0.1);
            border-radius: 50%;
            animation: radar-wave 3s ease-out infinite;
        }

        .radar-wave:nth-child(2) {
            animation-delay: 0.5s;
            width: 18px;
            height: 18px;
        }

        .radar-wave:nth-child(3) {
            animation-delay: 1s;
            width: 24px;
            height: 24px;
        }

        @keyframes radar-wave {
            0% {
                opacity: 0.6;
                transform: translateX(-50%) scale(0.5);
            }
            100% {
                opacity: 0;
                transform: translateX(-50%) scale(1.8);
            }
        }

        .tower-base {
            width: 22px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(229, 62, 62, 0.3), transparent);
            border-radius: 2px;
            margin-top: 1px;
        }

        .brand .logo {
            font-weight: 700;
            font-size: 24px;
            letter-spacing: -0.3px;
            color: #f1f5f9;
        }

        .brand .logo span {
            color: #e53e3e;
            font-weight: 800;
        }

        .badge-status {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(72, 187, 120, 0.08);
            padding: 4px 14px 4px 10px;
            border-radius: 40px;
            border: 1px solid rgba(72, 187, 120, 0.12);
        }

        .badge-status .dot-pulse {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #48bb78;
            box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.5);
            animation: pulse-dot 2.2s infinite;
        }

        @keyframes pulse-dot {
            0% {
                box-shadow: 0 0 0 0 rgba(72, 187, 120, 0.5);
            }
            70% {
                box-shadow: 0 0 0 6px rgba(72, 187, 120, 0);
            }
            100% {
                box-shadow: 0 0 0 0 rgba(72, 187, 120, 0);
            }
        }

        .badge-status span {
            font-size: 12px;
            font-weight: 500;
            color: #b0f0c0;
            letter-spacing: 0.2px;
        }

        .terminal {
            background: var(--bg-terminal);
            border-radius: 18px;
            padding: 16px 20px 12px;
            border: 1px solid var(--border-color);
            box-shadow: inset 0 4px 12px rgba(0, 0, 0, 0.6);
            margin-bottom: 22px;
            transition: all 0.3s ease;
        }

        .terminal-bar {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 12px;
        }

        .terminal-bar .dots {
            display: flex;
            gap: 7px;
        }

        .terminal-bar .dots span {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: block;
        }

        .terminal-bar .dots span:nth-child(1) {
            background: #fc8181;
        }
        .terminal-bar .dots span:nth-child(2) {
            background: #f6ad55;
        }
        .terminal-bar .dots span:nth-child(3) {
            background: #68d391;
        }

        .terminal-bar .path {
            font-family: 'Menlo', 'Courier New', monospace;
            font-size: 11px;
            color: #6b7a8f;
            letter-spacing: 0.2px;
            background: rgba(255, 255, 255, 0.02);
            padding: 2px 12px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.03);
        }

        .terminal-bar .version {
            margin-left: auto;
            font-family: 'Menlo', monospace;
            font-size: 10px;
            color: #3f4a5a;
            background: rgba(255, 255, 255, 0.02);
            padding: 2px 12px;
            border-radius: 30px;
        }

        #output {
            max-height: 280px;
            overflow-y: auto;
            margin-bottom: 10px;
            padding-right: 4px;
            font-family: 'Menlo', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.9;
        }

        #output::-webkit-scrollbar {
            width: 5px;
        }

        #output::-webkit-scrollbar-track {
            background: transparent;
        }

        #output::-webkit-scrollbar-thumb {
            background: #2a3344;
            border-radius: 20px;
        }

        body.light-theme #output::-webkit-scrollbar-thumb {
            background: #a0aec0;
        }

        .line {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 2px 0;
        }

        .line .prompt {
            color: #68d391;
            flex-shrink: 0;
            user-select: none;
            min-width: 16px;
            font-weight: 500;
        }

        body.light-theme .line .prompt {
            color: #2f855a;
        }

        .line .text {
            color: var(--text-primary);
            word-break: break-word;
        }

        .line .text.green {
            color: var(--text-green);
        }
        .line .text.blue {
            color: var(--text-blue);
        }
        .line .text.red {
            color: var(--text-red);
        }
        .line .text.yellow {
            color: var(--text-yellow);
        }
        .line .text.muted {
            color: var(--text-muted);
        }
        .line .text.bold {
            color: #eef2f8;
            font-weight: 500;
        }
        .line .text.cyan {
            color: var(--text-cyan);
        }

        body.light-theme .line .text.bold {
            color: #1a202c;
        }

        .help-grid {
            display: grid;
            grid-template-columns: 100px 1fr;
            gap: 2px 24px;
            padding: 4px 0;
        }

        .help-grid .cmd {
            color: var(--text-yellow);
            font-weight: 500;
        }

        .help-grid .desc {
            color: var(--text-muted);
        }

        body.light-theme .help-grid .cmd {
            color: #b7791f;
        }

        body.light-theme .help-grid .desc {
            color: #4a5568;
        }

        .input-row {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-top: 12px;
            border-top: 1px solid var(--border-color);
            font-family: 'Menlo', 'Courier New', monospace;
        }

        .input-row .prompt {
            color: #68d391;
            flex-shrink: 0;
            font-size: 13px;
            user-select: none;
            min-width: 16px;
            font-weight: 500;
        }

        body.light-theme .input-row .prompt {
            color: #2f855a;
        }

        .input-row .wrap {
            flex: 1;
            display: flex;
            align-items: center;
            min-height: 26px;
        }

        .input-row .wrap #cmd-text {
            color: var(--text-yellow);
            font-size: 13px;
            white-space: pre-wrap;
            word-break: break-all;
        }

        .input-row .wrap .cursor {
            display: inline-block;
            width: 9px;
            height: 20px;
            background: #68d391;
            animation: blink 1s step-end infinite;
            margin-left: 2px;
            flex-shrink: 0;
            border-radius: 2px;
            opacity: 0.9;
        }

        body.light-theme .input-row .wrap .cursor {
            background: #2d3748;
        }

        @keyframes blink {
            0%,
            100% {
                opacity: 1;
            }
            50% {
                opacity: 0.1;
            }
        }

        #hidden-input {
            position: fixed;
            top: -9999px;
            left: -9999px;
            opacity: 0;
            width: 0;
            height: 0;
        }

        .footer {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            padding-top: 14px;
            border-top: 1px solid var(--border-color);
            gap: 12px 16px;
        }

        .footer .links {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 4px 18px;
        }

        .footer .links a {
            color: #7e8b9f;
            text-decoration: none;
            font-size: 12px;
            font-weight: 500;
            transition: color 0.2s ease;
            letter-spacing: 0.2px;
            border-bottom: 1px solid transparent;
            cursor: pointer;
        }

        .footer .links a:hover {
            color: #d4dcec;
            border-bottom-color: #e53e3e;
        }

        body.light-theme .footer .links a:hover {
            color: #1a202c;
        }

        .footer .links .sep {
            color: #2a3344;
            font-weight: 300;
        }

        body.light-theme .footer .links .sep {
            color: #a0aec0;
        }

        .footer .copy {
            color: #3f4a5a;
            font-size: 11px;
            font-weight: 400;
            letter-spacing: 0.2px;
        }

        body.light-theme .footer .copy {
            color: #718096;
        }

        .footer .version-tag {
            background: rgba(229, 62, 62, 0.08);
            color: #e53e3e;
            font-size: 11px;
            font-weight: 600;
            padding: 2px 12px;
            border-radius: 40px;
            border: 1px solid rgba(229, 62, 62, 0.12);
        }

        .matrix-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            display: none;
        }

        .matrix-container.active {
            display: block;
        }

        .matrix-container canvas {
            width: 100%;
            height: 100%;
            display: block;
        }

        .theme-toggle {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            color: #7e8b9f;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'Inter', sans-serif;
        }

        .theme-toggle:hover {
            color: #d4dcec;
            border-color: rgba(255, 255, 255, 0.08);
        }

        body.light-theme .theme-toggle {
            background: rgba(0, 0, 0, 0.04);
            color: #4a5568;
            border-color: rgba(0, 0, 0, 0.06);
        }

        body.light-theme .theme-toggle:hover {
            color: #1a202c;
            border-color: rgba(0, 0, 0, 0.1);
        }

        .todo-item {
            color: var(--text-primary);
            padding: 2px 0;
        }

        .todo-item.done {
            text-decoration: line-through;
            color: var(--text-muted);
        }

        body.light-theme .todo-item {
            color: #2d3748;
        }

        body.light-theme .todo-item.done {
            color: #718096;
        }

        @media (max-width: 640px) {
            .container {
                padding: 20px 14px 18px;
            }
            .brand .logo {
                font-size: 20px;
            }
            .brand-icon {
                width: 34px;
                height: 34px;
            }
            .tower-icon {
                transform: scale(0.85);
            }
            .header {
                margin-bottom: 18px;
            }
            .terminal {
                padding: 12px 12px 10px;
            }
            .line {
                font-size: 11px;
                gap: 6px;
            }
            .input-row .prompt {
                font-size: 11px;
            }
            .input-row .wrap #cmd-text {
                font-size: 11px;
            }
            #output {
                max-height: 140px;
            }
            .footer .links a {
                font-size: 11px;
            }
            .footer .links {
                gap: 2px 12px;
            }
            .footer {
                flex-direction: column;
                align-items: flex-start;
            }
            .help-grid {
                grid-template-columns: 80px 1fr;
                gap: 1px 14px;
                font-size: 11px;
            }
        }
    </style>
</head>
<body>

    <div class="matrix-container" id="matrixContainer">
        <canvas id="matrixCanvas"></canvas>
    </div>

    <div class="container glass">

        <div class="header">
            <div class="brand">
                <div class="brand-icon">
                    <div class="tower-icon">
                        <div class="radar-wave"></div>
                        <div class="radar-wave"></div>
                        <div class="radar-wave"></div>
                        <div class="tower-body">
                            <div class="tower-antenna"></div>
                            <div class="tower-window"></div>
                            <div class="tower-window"></div>
                            <div class="tower-window" style="width:6px;height:3px;"></div>
                        </div>
                        <div class="tower-base"></div>
                    </div>
                </div>
                <div class="logo">WATCH <span>TOWER</span></div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;">
                <button class="theme-toggle" id="themeToggle">toggle theme</button>
                <div class="badge-status">
                    <span class="dot-pulse"></span>
                    <span>system ready</span>
                </div>
            </div>
        </div>

        <div class="terminal">

            <div class="terminal-bar">
                <div class="dots">
                    <span></span><span></span><span></span>
                </div>
                <span class="path">root@watch-tower</span>
                <span class="version">v3.0.0</span>
            </div>

            <div id="output">
                <div class="line"><span class="text muted">initializing system...</span></div>
                <div class="line"><span class="text green">+ kernel loaded</span></div>
                <div class="line"><span class="text blue">+ network interface active</span></div>
                <div class="line"><span class="text green">+ user authenticated</span></div>
                <div class="line"><span class="text bold">welcome to watch tower</span></div>
                <div class="line"><span class="prompt">#</span><span class="text muted">type "help" for commands</span></div>
            </div>

            <div class="input-row">
                <span class="prompt">></span>

                <div class="wrap">
                    <span id="cmd-text"></span>
                    <span class="cursor"></span>
                </div>
            </div>

        </div>

        <div class="footer">
            <div class="links">
                <a onclick="return false;">Repository</a>
                <span class="sep">|</span>
                <a onclick="return false;">Commits</a>
                <span class="sep">|</span>
                <a onclick="return false;">Telegram</a>
                <span class="sep">|</span>
                <a onclick="return false;">Email</a>
            </div>
            <div style="display:flex;align-items:center;gap:16px;">
                <span class="version-tag">v3.0.0</span>
                <span class="copy">2026 Watch Tower</span>
            </div>
        </div>

    </div>

    <input type="text" id="hidden-input" autofocus>

    <script>
        (function() {

            const output = document.getElementById('output');
            const cmdText = document.getElementById('cmd-text');
            const hidden = document.getElementById('hidden-input');

            let history = [];
            let historyIdx = -1;
            let currentInput = '';
            let todoList = [];
            let matrixRunning = false;
            let matrixInterval = null;

            const COMMANDS = [
                'help', 'clear', 'status', 'version', 'whoami', 'date',
                'github', 'docs', 'exit', 'history', 'echo', 'theme',
                'calc', 'info', 'dashboard', 'ping', 'todo', 'matrix'
            ];

            function focus() { hidden.focus(); }
            document.addEventListener('click', focus);
            document.addEventListener('touchstart', focus);
            setTimeout(focus, 400);

            function print(text, type = '') {
                const div = document.createElement('div');
                div.className = 'line';
                if (type === 'no-prompt') {
                    div.innerHTML = `<span class="text">${text}</span>`;
                } else {
                    div.innerHTML = `<span class="text ${type}">${text}</span>`;
                }
                output.appendChild(div);
                output.scrollTop = output.scrollHeight;
            }

            function printWithPrompt(text, type = '') {
                const div = document.createElement('div');
                div.className = 'line';
                div.innerHTML = `<span class="prompt">></span><span class="text ${type}">${text}</span>`;
                output.appendChild(div);
                output.scrollTop = output.scrollHeight;
            }

            function printHelpGrid(commands) {
                const div = document.createElement('div');
                div.className = 'line';

                let html = `<div class="help-grid">`;
                const sorted = Object.entries(commands).sort((a, b) => a[0].localeCompare(b[0]));
                sorted.forEach(([cmd, desc]) => {
                    html += `<span class="cmd">${cmd}</span><span class="desc">${desc}</span>`;
                });
                html += `</div>`;

                div.innerHTML = `<span class="text"></span>`;
                div.querySelector('.text').innerHTML = html;
                output.appendChild(div);
                output.scrollTop = output.scrollHeight;
            }

            function clearTerminal() {
                output.innerHTML = '';
                print('terminal cleared', 'muted');
                print('type "help" for commands', 'muted');
            }

            function showHelp() {
                const commands = {
                    'help': 'show available commands',
                    'clear': 'clear terminal screen',
                    'status': 'display system status',
                    'version': 'show version information',
                    'whoami': 'current user',
                    'date': 'current date and time',
                    'github': 'repository URL',
                    'docs': 'documentation link',
                    'echo': 'echo text back',
                    'exit': 'exit (just for fun)',
                    'history': 'show command history',
                    'theme': 'toggle dark/light theme',
                    'calc': 'calculate expression (e.g., calc 2+2)',
                    'info': 'show system information',
                    'dashboard': 'show system dashboard',
                    'ping': 'ping a host (e.g., ping google.com)',
                    'todo': 'manage todo list (add/remove/list)',
                    'matrix': 'show matrix rain effect'
                };
                print('+-----------------------------------------------------+', 'cyan');
                print('|                  AVAILABLE COMMANDS                  |', 'cyan');
                print('+-----------------------------------------------------+', 'cyan');
                printHelpGrid(commands);
                print('+-----------------------------------------------------+', 'cyan');
            }

            function showDashboard() {
                print('+-----------------------------------------------------+', 'cyan');
                print('|                  SYSTEM DASHBOARD                    |', 'cyan');
                print('+-----------------------------------------------------+', 'cyan');
                print('|  CPU Usage:     23%                                  |', '');
                print('|  Memory:        1.2 GB / 8.0 GB                     |', '');
                print('|  Disk:          45%                                 |', '');
                print('|  Uptime:        12 days, 4 hours                    |', '');
                print('|  Connections:   3                                   |', '');
                print('|  Processes:     42                                  |', '');
                print('|  Load Average:  0.23, 0.45, 0.67                   |', '');
                print('+-----------------------------------------------------+', 'cyan');
            }

            function showInfo() {
                print('+-----------------------------------------------------+', 'cyan');
                print('|                  SYSTEM INFORMATION                  |', 'cyan');
                print('+-----------------------------------------------------+', 'cyan');
                print('|  OS:            Watch Tower OS v3.0.0               |', '');
                print('|  Kernel:        6.8.0-watchtower                   |', '');
                print('|  Architecture:  x86_64                              |', '');
                print('|  Shell:         watch-sh 3.0                        |', '');
                print('|  Terminal:      Web Terminal                        |', '');
                print('|  CPU:           Intel Core i9-13900K               |', '');
                print('|  GPU:           NVIDIA RTX 4090                     |', '');
                print('+-----------------------------------------------------+', 'cyan');
            }

            function calculate(expr) {
                try {
                    const sanitized = expr.replace(/[^0-9+\-*/(). ]/g, '');
                    const result = Function('"use strict"; return (' + sanitized + ')')();
                    return result;
                } catch (e) {
                    return null;
                }
            }

            function pingHost(host) {
                if (!host) {
                    print('usage: ping <host>', 'red');
                    return;
                }
                print(`PING ${host} (simulated)...`, 'blue');
                setTimeout(() => {
                    const latency = Math.floor(Math.random() * 50) + 10;
                    print(`64 bytes from ${host}: icmp_seq=1 ttl=64 time=${latency} ms`, 'green');
                }, 300);
                setTimeout(() => {
                    const latency = Math.floor(Math.random() * 50) + 10;
                    print(`64 bytes from ${host}: icmp_seq=2 ttl=64 time=${latency} ms`, 'green');
                }, 600);
                setTimeout(() => {
                    const latency = Math.floor(Math.random() * 50) + 10;
                    print(`64 bytes from ${host}: icmp_seq=3 ttl=64 time=${latency} ms`, 'green');
                }, 900);
                setTimeout(() => {
                    print(`--- ${host} ping statistics ---`, '');
                    print('3 packets transmitted, 3 received, 0% packet loss', '');
                }, 1200);
            }

            function showTodo() {
                if (todoList.length === 0) {
                    print('todo list is empty', 'muted');
                    return;
                }
                print('+-----------------------------------------------------+', 'cyan');
                print('|                     TODO LIST                       |', 'cyan');
                print('+-----------------------------------------------------+', 'cyan');
                todoList.forEach((item, index) => {
                    const status = item.done ? '[X]' : '[ ]';
                    const className = item.done ? 'muted' : '';
                    print(`  ${index + 1}. ${status} ${item.text}`, className);
                });
                print('+-----------------------------------------------------+', 'cyan');
            }

            function addTodo(text) {
                if (!text) {
                    print('usage: todo add <task>', 'red');
                    return;
                }
                todoList.push({ text: text, done: false });
                print(`added: "${text}"`, 'green');
            }

            function removeTodo(index) {
                const idx = parseInt(index) - 1;
                if (isNaN(idx) || idx < 0 || idx >= todoList.length) {
                    print('invalid todo index', 'red');
                    return;
                }
                const removed = todoList.splice(idx, 1);
                print(`removed: "${removed[0].text}"`, 'green');
            }

            function toggleTodo(index) {
                const idx = parseInt(index) - 1;
                if (isNaN(idx) || idx < 0 || idx >= todoList.length) {
                    print('invalid todo index', 'red');
                    return;
                }
                todoList[idx].done = !todoList[idx].done;
                const status = todoList[idx].done ? 'completed' : 'uncompleted';
                print(`todo ${status}: "${todoList[idx].text}"`, 'green');
            }

            function startMatrix() {
                const container = document.getElementById('matrixContainer');
                const canvas = document.getElementById('matrixCanvas');
                const ctx = canvas.getContext('2d');

                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;

                const columns = Math.floor(canvas.width / 14);
                const drops = [];
                for (let i = 0; i < columns; i++) {
                    drops[i] = Math.floor(Math.random() * -100);
                }

                const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:,.<>?/';

                container.classList.add('active');
                matrixRunning = true;

                if (matrixInterval) {
                    clearInterval(matrixInterval);
                }

                matrixInterval = setInterval(() => {
                    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);

                    ctx.fillStyle = '#0F0';
                    ctx.font = '14px monospace';

                    for (let i = 0; i < drops.length; i++) {
                        const char = chars[Math.floor(Math.random() * chars.length)];
                        const x = i * 14;
                        const y = drops[i] * 14;

                        ctx.fillText(char, x, y);

                        if (y > canvas.height && Math.random() > 0.975) {
                            drops[i] = 0;
                        }

                        drops[i]++;
                    }
                }, 33);
            }

            function stopMatrix() {
                const container = document.getElementById('matrixContainer');
                container.classList.remove('active');
                matrixRunning = false;
                if (matrixInterval) {
                    clearInterval(matrixInterval);
                    matrixInterval = null;
                }
                print('matrix effect stopped', 'muted');
            }

            function toggleTheme() {
                document.body.classList.toggle('light-theme');
                const isLight = document.body.classList.contains('light-theme');
                print(`theme switched to ${isLight ? 'light' : 'dark'} mode`, 'green');
            }

            function run(cmd) {
                const c = cmd.trim();
                if (!c) return;

                history.push(c);
                historyIdx = history.length;

                const parts = c.split(' ');
                const name = parts[0].toLowerCase();
                const args = parts.slice(1);

                switch (name) {
                    case 'help':
                        showHelp();
                        break;
                    case 'clear':
                        clearTerminal();
                        break;
                    case 'status':
                        print('system: operational', 'green');
                        print('uptime: 99.9%', '');
                        print('connections: 0', '');
                        print('version: 3.0.0', '');
                        break;
                    case 'version':
                        print('watch tower api v3.0.0', 'blue');
                        print('build: 2026-08-09', 'muted');
                        break;
                    case 'whoami':
                        print('root@watch-tower', 'green');
                        break;
                    case 'date':
                        print(new Date().toString(), '');
                        break;
                    case 'github':
                        print('https://github.com/AryaKhorasan/watch-tower', 'blue');
                        break;
                    case 'docs':
                        print('/api/documentation', 'blue');
                        break;
                    case 'echo':
                        print(args.join(' ') || '', '');
                        break;
                    case 'exit':
                        print('exiting... just kidding, this is a web terminal.', 'muted');
                        break;
                    case 'history':
                        if (history.length === 0) {
                            print('no commands in history', 'muted');
                        } else {
                            print('+-----------------------------------------------------+', 'cyan');
                            print('|                   COMMAND HISTORY                   |', 'cyan');
                            print('+-----------------------------------------------------+', 'cyan');
                            history.forEach((h, i) => {
                                const num = String(i + 1).padStart(2, ' ');
                                print(`  ${num}.  ${h}`, 'muted');
                            });
                            print('+-----------------------------------------------------+', 'cyan');
                        }
                        break;
                    case 'theme':
                        toggleTheme();
                        break;
                    case 'calc':
                        if (args.length === 0) {
                            print('usage: calc <expression> (e.g., calc 2+2)', 'red');
                        } else {
                            const result = calculate(args.join(''));
                            if (result !== null && !isNaN(result)) {
                                print(`${args.join('')} = ${result}`, 'green');
                            } else {
                                print('invalid expression', 'red');
                            }
                        }
                        break;
                    case 'info':
                        showInfo();
                        break;
                    case 'dashboard':
                        showDashboard();
                        break;
                    case 'ping':
                        pingHost(args[0]);
                        break;
                    case 'todo':
                        if (args.length === 0) {
                            showTodo();
                        } else if (args[0] === 'add') {
                            addTodo(args.slice(1).join(' '));
                        } else if (args[0] === 'remove' || args[0] === 'rm') {
                            removeTodo(args[1]);
                        } else if (args[0] === 'toggle' || args[0] === 'done') {
                            toggleTodo(args[1]);
                        } else if (args[0] === 'list') {
                            showTodo();
                        } else if (args[0] === 'clear') {
                            todoList = [];
                            print('todo list cleared', 'green');
                        } else {
                            print('usage: todo [add|remove|toggle|list|clear]', 'red');
                        }
                        break;
                    case 'matrix':
                        if (args[0] === 'stop') {
                            stopMatrix();
                        } else if (matrixRunning) {
                            print('matrix effect is already running', 'muted');
                            print('use "matrix stop" to stop', 'muted');
                        } else {
                            startMatrix();
                            print('matrix effect started', 'green');
                            print('use "matrix stop" to stop', 'muted');
                        }
                        break;
                    default:
                        print(`unknown command: ${c}`, 'red');
                        print('type "help" for commands', 'muted');
                }
            }

            hidden.addEventListener('input', function() {
                currentInput = this.value;
                cmdText.textContent = currentInput;

                // Auto-complete suggestion
                if (currentInput && !currentInput.includes(' ')) {
                    const match = COMMANDS.find(cmd => cmd.startsWith(currentInput.toLowerCase()));
                    if (match && match !== currentInput) {
                        // Show suggestion but don't auto-complete
                    }
                }
            });

            hidden.addEventListener('keydown', function(e) {
                // Tab completion
                if (e.key === 'Tab') {
                    e.preventDefault();
                    const current = this.value.trim();
                    if (current) {
                        const match = COMMANDS.find(cmd => cmd.startsWith(current.toLowerCase()));
                        if (match) {
                            this.value = match;
                            currentInput = match;
                            cmdText.textContent = match;
                        }
                    }
                }

                if (e.ctrlKey && e.key === 'c') {
                    e.preventDefault();
                    currentInput = '';
                    this.value = '';
                    cmdText.textContent = '';
                    print('^C', 'red');
                    print('type "help" for commands', 'muted');
                    return;
                }

                if (e.key === 'Enter') {
                    e.preventDefault();
                    const val = this.value;

                    if (val.trim()) {
                        printWithPrompt(val, 'yellow');
                    }

                    run(val);

                    this.value = '';
                    currentInput = '';
                    cmdText.textContent = '';
                    output.scrollTop = output.scrollHeight;
                }

                if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    if (history.length > 0 && historyIdx > 0) {
                        historyIdx--;
                        this.value = history[historyIdx];
                        currentInput = this.value;
                        cmdText.textContent = currentInput;
                    } else if (historyIdx === -1 && history.length > 0) {
                        historyIdx = history.length - 1;
                        this.value = history[historyIdx];
                        currentInput = this.value;
                        cmdText.textContent = currentInput;
                    }
                }

                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    if (historyIdx < history.length - 1) {
                        historyIdx++;
                        this.value = history[historyIdx];
                        currentInput = this.value;
                        cmdText.textContent = currentInput;
                    } else {
                        historyIdx = history.length;
                        this.value = '';
                        currentInput = '';
                        cmdText.textContent = '';
                    }
                }

                if (e.key === 'Escape') {
                    this.value = '';
                    currentInput = '';
                    cmdText.textContent = '';
                }
            });

            hidden.addEventListener('blur', function() {
                setTimeout(focus, 10);
            });

            // Theme toggle button
            document.getElementById('themeToggle').addEventListener('click', function() {
                toggleTheme();
            });

            // Matrix resize
            window.addEventListener('resize', function() {
                const canvas = document.getElementById('matrixCanvas');
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            });

            console.log('%c WATCH TOWER ', 'background:#1a202c;color:#68d391;font-size:14px;font-weight:700;padding:6px 16px;');
            console.log('%c https://github.com/AryaKhorasan/watch-tower ', 'color:#718096;font-size:11px;');

            // Load saved theme preference
            if (localStorage.getItem('watchtower-theme') === 'light') {
                document.body.classList.add('light-theme');
            }

            // Save theme preference
            const origToggle = toggleTheme;
            toggleTheme = function() {
                origToggle();
                const isLight = document.body.classList.contains('light-theme');
                localStorage.setItem('watchtower-theme', isLight ? 'light' : 'dark');
            };

            // Restore theme toggle function
            window.toggleTheme = toggleTheme;

            // Load saved todo list
            try {
                const saved = localStorage.getItem('watchtower-todo');
                if (saved) {
                    todoList = JSON.parse(saved);
                }
            } catch (e) {}

            // Save todo list on changes
            const origAdd = addTodo;
            const origRemove = removeTodo;
            const origToggleTodo = toggleTodo;
            const origClear = function() {};

            function saveTodo() {
                localStorage.setItem('watchtower-todo', JSON.stringify(todoList));
            }

            addTodo = function(text) {
                origAdd(text);
                saveTodo();
            };

            removeTodo = function(index) {
                origRemove(index);
                saveTodo();
            };

            toggleTodo = function(index) {
                origToggleTodo(index);
                saveTodo();
            };

            // Override todo clear
            const todoClear = function() {
                todoList = [];
                print('todo list cleared', 'green');
                saveTodo();
            };

            // Patch todo command
            const origRun = run;
            run = function(cmd) {
                const c = cmd.trim();
                if (!c) return;

                const parts = c.split(' ');
                const name = parts[0].toLowerCase();
                const args = parts.slice(1);

                if (name === 'todo' && args[0] === 'clear') {
                    todoClear();
                    return;
                }
                origRun(cmd);
            };

            console.log('Watch Tower v3.0.0 loaded successfully');
            print('system ready - type "help" for commands', 'muted');

        })();
    </script>

</body>
</html>