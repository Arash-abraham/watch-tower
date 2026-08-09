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
            background: #0b0d0f;
            border-radius: 18px;
            padding: 16px 20px 12px;
            border: 1px solid rgba(255, 255, 255, 0.03);
            box-shadow: inset 0 4px 12px rgba(0, 0, 0, 0.6);
            margin-bottom: 22px;
        }

        .terminal-bar {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
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

        .line .text {
            color: #d4dcec;
            word-break: break-word;
        }

        .line .text.green {
            color: #6fcf97;
        }
        .line .text.blue {
            color: #7bb3e6;
        }
        .line .text.red {
            color: #f28b82;
        }
        .line .text.yellow {
            color: #f5c542;
        }
        .line .text.muted {
            color: #5c6b7e;
        }
        .line .text.bold {
            color: #eef2f8;
            font-weight: 500;
        }
        .line .text.cyan {
            color: #5fc8e8;
        }

        .help-grid {
            display: grid;
            grid-template-columns: 80px 1fr;
            gap: 2px 20px;
            padding: 4px 0;
        }

        .help-grid .cmd {
            color: #f5c542;
            font-weight: 500;
        }

        .help-grid .desc {
            color: #8a9bb0;
        }

        .input-row {
            display: flex;
            align-items: center;
            gap: 12px;
            padding-top: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
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

        .input-row .wrap {
            flex: 1;
            display: flex;
            align-items: center;
            min-height: 26px;
        }

        .input-row .wrap #cmd-text {
            color: #f5c542;
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
            border-top: 1px solid rgba(255, 255, 255, 0.03);
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
        }

        .footer .links a:hover {
            color: #d4dcec;
            border-bottom-color: #e53e3e;
        }

        .footer .links .sep {
            color: #2a3344;
            font-weight: 300;
        }

        .footer .copy {
            color: #3f4a5a;
            font-size: 11px;
            font-weight: 400;
            letter-spacing: 0.2px;
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
                grid-template-columns: 70px 1fr;
                gap: 1px 14px;
                font-size: 11px;
            }
        }
    </style>
</head>
<body>

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
            <div class="badge-status">
                <span class="dot-pulse"></span>
                <span>system ready</span>
            </div>
        </div>

        <div class="terminal">

            <div class="terminal-bar">
                <div class="dots">
                    <span></span><span></span><span></span>
                </div>
                <span class="path">root@watch-tower</span>
                <span class="version">v2.1.0</span>
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
                <a href="#" onclick="return false;">Repository</a>
                <span class="sep">|</span>
                <a href="#" onclick="return false;">Commits</a>
                <span class="sep">|</span>
                <a href="#" onclick="return false;">Telegram</a>
                <span class="sep">|</span>
                <a href="#" onclick="return false;">Email</a>
            </div>
            <div style="display:flex;align-items:center;gap:16px;">
                <span class="version-tag">v2.1.0</span>
                <span class="copy">© 2026 · Watch Tower</span>
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

            function focus() { hidden.focus(); }
            document.addEventListener('click', focus);
            document.addEventListener('touchstart', focus);
            setTimeout(focus, 400);

            function print(text, type = '') {
                const div = document.createElement('div');
                div.className = 'line';
                div.innerHTML = `<span class="text ${type}">${text}</span>`;
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
                    'version': 'show API version',
                    'whoami': 'current user',
                    'date': 'current date & time',
                    'github': 'repository URL',
                    'docs': 'documentation link',
                    'echo': 'echo text back',
                    'exit': 'exit (just for fun)',
                    'history': 'show command history'
                };

                print('╭─ available commands ─╮', 'cyan');
                printHelpGrid(commands);
                print('╰─────────────────────╯', 'cyan');
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
                        print('version: 2.1.0', '');
                        break;
                    case 'version':
                        print('watch tower api v2.1.0', 'blue');
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
                            history.forEach((h, i) => print(`  ${String(i+1).padStart(2,' ')}  ${h}`, 'muted'));
                        }
                        break;
                    default:
                        print(`unknown: ${c}`, 'red');
                        print('type "help" for commands', 'muted');
                }
            }

            hidden.addEventListener('input', function() {
                currentInput = this.value;
                cmdText.textContent = currentInput;
            });

            hidden.addEventListener('keydown', function(e) {

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
                        const div = document.createElement('div');
                        div.className = 'line';
                        div.innerHTML = `<span class="prompt">></span><span class="text yellow">${val}</span>`;
                        output.appendChild(div);
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

            console.log('%c WATCH TOWER ', 'background:#1a202c;color:#68d391;font-size:14px;font-weight:700;padding:6px 16px;');
            console.log('%c https://github.com/AryaKhorasan/watch-tower ', 'color:#718096;font-size:11px;');

        })();
    </script>

</body>
</html>