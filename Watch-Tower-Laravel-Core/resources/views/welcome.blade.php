<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Watch Tower</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Nunito', sans-serif;
            background: #000000;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 800px;
            background: #2b2929;
            border-radius: 12px;
            padding: 48px 56px 40px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04), 0 4px 12px rgba(0, 0, 0, 0.02);
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
        }

        .header .logo {
            font-weight: 800;
            font-size: 32px;
            color: #ffffff;
            letter-spacing: 1px;
        }

        .header .logo span {
            color: #e53e3e;
        }

        .header .sub {
            font-size: 14px;
            color: #718096;
            margin-top: 4px;
            font-weight: 400;
        }

        .header .status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 12px;
            font-size: 12px;
            color: #48bb78;
            font-weight: 600;
        }

        .header .status .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #48bb78;
            animation: dotPulse 2s infinite;
        }

        @keyframes dotPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.2; }
        }

        .terminal {
            background: #1a202c;
            border-radius: 10px;
            padding: 20px 24px 16px;
            margin-bottom: 24px;
        }

        .terminal-bar {
            display: flex;
            align-items: center;
            gap: 10px;
            padding-bottom: 14px;
            border-bottom: 1px solid #2d3748;
            margin-bottom: 14px;
        }

        .terminal-bar .dots {
            display: flex;
            gap: 6px;
        }

        .terminal-bar .dots span {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: block;
        }

        .terminal-bar .dots span:nth-child(1) { background: #fc8181; }
        .terminal-bar .dots span:nth-child(2) { background: #f6ad55; }
        .terminal-bar .dots span:nth-child(3) { background: #68d391; }

        .terminal-bar .path {
            font-family: 'Courier New', monospace;
            font-size: 11px;
            color: #a0aec0;
            letter-spacing: 0.5px;
        }

        .terminal-bar .version {
            margin-left: auto;
            font-family: 'Courier New', monospace;
            font-size: 10px;
            color: #4a5568;
        }

        #output {
            max-height: 280px;
            overflow-y: auto;
            margin-bottom: 12px;
            padding-right: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.8;
        }

        #output::-webkit-scrollbar {
            width: 4px;
        }

        #output::-webkit-scrollbar-track {
            background: transparent;
        }

        #output::-webkit-scrollbar-thumb {
            background: #4a5568;
            border-radius: 10px;
        }

        .line {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 1px 0;
        }

        .line .prompt {
            color: #68d391;
            flex-shrink: 0;
            user-select: none;
            min-width: 14px;
        }

        .line .text {
            color: #e2e8f0;
            word-break: break-word;
        }

        .line .text.green { color: #68d391; }
        .line .text.blue { color: #63b3ed; }
        .line .text.red { color: #fc8181; }
        .line .text.yellow { color: #f6ad55; }
        .line .text.muted { color: #4a5568; }
        .line .text.bold { color: #ffffff; font-weight: 600; }

        .input-row {
            display: flex;
            align-items: center;
            gap: 10px;
            padding-top: 12px;
            border-top: 1px solid #2d3748;
            font-family: 'Courier New', monospace;
        }

        .input-row .prompt {
            color: #68d391;
            flex-shrink: 0;
            font-size: 13px;
            user-select: none;
            min-width: 14px;
        }

        .input-row .wrap {
            flex: 1;
            display: flex;
            align-items: center;
            min-height: 24px;
            position: relative;
        }

        .input-row .wrap #cmd-text {
            color: #f6ad55;
            font-size: 13px;
            white-space: pre-wrap;
            word-break: break-all;
        }

        .input-row .wrap .cursor {
            display: inline-block;
            width: 8px;
            height: 18px;
            background: #68d391;
            animation: blink 1s step-end infinite;
            margin-left: 2px;
            flex-shrink: 0;
            border-radius: 1px;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }

        .input-row .wrap .suggestion {
            position: absolute;
            left: 0;
            top: 0;
            color: #4a5568;
            font-size: 13px;
            pointer-events: none;
            white-space: pre;
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
            text-align: center;
            padding-top: 20px;
            border-top: 1px solid #edf2f7;
        }

        .footer .links {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: center;
            gap: 4px 20px;
            margin-bottom: 12px;
        }

        .footer .links a {
            color: #718096;
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            transition: color 0.2s ease;
        }

        .footer .links a:hover {
            color: #2d3748;
        }

        .footer .links .sep {
            color: #e2e8f0;
        }

        .footer .copy {
            color: #a0aec0;
            font-size: 12px;
        }

        @media (max-width: 640px) {
            .container { padding: 24px 16px 20px; }
            .header .logo { font-size: 24px; }
            .terminal { padding: 14px 14px 12px; }
            .line { font-size: 11px; gap: 6px; }
            .input-row .prompt { font-size: 11px; }
            .input-row .wrap #cmd-text { font-size: 11px; }
            #output { max-height: 160px; }
            .footer .links a { font-size: 11px; }
            .footer .links { gap: 2px 12px; }
        }
    </style>
</head>
<body>

<div class="container">

    <div class="header">
        <div class="logo">WATCH <span>TOWER</span></div>
        <div class="sub">monitoring infrastructure</div>
        <div class="status">
            <span class="dot"></span>
            system ready
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
            <div class="line"><span class="prompt">></span><span class="text muted">initializing system...</span></div>
            <div class="line"><span class="prompt">></span><span class="text green">+ kernel loaded</span></div>
            <div class="line"><span class="prompt">></span><span class="text blue">+ network interface active</span></div>
            <div class="line"><span class="prompt">></span><span class="text green">+ user authenticated</span></div>
            <div class="line"><span class="prompt">></span><span class="text bold">welcome to watch tower</span></div>
            <div class="line"><span class="prompt">#</span><span class="text muted">type "help" for commands | Tab for autocomplete</span></div>
        </div>

        <div class="input-row">
            <span class="prompt">></span>
            <div class="wrap">
                <span id="cmd-text"></span>
                <span class="cursor"></span>
                <span id="suggestion" class="suggestion"></span>
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
            <span class="sep">|</span>
            <span style="color:#a0aec0;font-size:13px;font-weight:600;">v2.1.0</span>
        </div>
        <div class="copy">© 2026 Watch Tower · All rights reserved</div>
    </div>

</div>

<input type="text" id="hidden-input" autofocus>

<script>
(function() {

    const COMMANDS = [
        'help', 'clear', 'status', 'version', 'whoami', 'date', 
        'github', 'docs', 'exit', 'history', 'echo'
    ];

    const output = document.getElementById('output');
    const cmdText = document.getElementById('cmd-text');
    const suggestionEl = document.getElementById('suggestion');
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
        div.innerHTML = `<span class="prompt">></span><span class="text ${type}">${text}</span>`;
        output.appendChild(div);
        output.scrollTop = output.scrollHeight;
    }

    function clearTerminal() {
        output.innerHTML = '';
        print('terminal cleared', 'muted');
        print('type "help" for commands', 'muted');
    }

    function showHelp() {
        print(' ─── commands ───', 'yellow');
        print(' help      show this help', '');
        print(' clear     clear terminal', '');
        print(' status    system status', '');
        print(' version   api version', '');
        print(' whoami    current user', '');
        print(' date      current date', '');
        print(' github    repository url', '');
        print(' docs      documentation url', '');
        print(' echo      echo text', '');
        print(' exit      exit (just for fun)', '');
        print(' history   show command history', '');
        print(' ─────────────────', 'yellow');
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
                print('build: 2026-08-06', 'muted');
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
                history.forEach((h, i) => print(`  ${i+1}  ${h}`, 'muted'));
                break;
            default:
                print(`unknown: ${c}`, 'red');
                print('type "help" for commands', 'muted');
        }
    }

    function getSuggestions(input) {
        if (!input) return [];
        const lower = input.toLowerCase();
        return COMMANDS.filter(cmd => cmd.startsWith(lower));
    }

    function showSuggestion(suggestions) {
        if (suggestions.length === 1 && suggestions[0] !== currentInput) {
            const full = suggestions[0];
            const partial = currentInput;
            if (full.startsWith(partial)) {
                suggestionEl.textContent = full.slice(partial.length);
                return;
            }
        }
        suggestionEl.textContent = '';
    }

    function applySuggestion() {
        const sug = suggestionEl.textContent;
        if (sug) {
            currentInput = currentInput + sug;
            cmdText.textContent = currentInput;
            suggestionEl.textContent = '';
            hidden.value = currentInput;
        }
    }

    hidden.addEventListener('input', function() {
        currentInput = this.value;
        cmdText.textContent = currentInput;
        suggestionEl.textContent = '';
        const suggestions = getSuggestions(currentInput);
        showSuggestion(suggestions);
    });

    hidden.addEventListener('keydown', function(e) {

        if (e.ctrlKey && e.key === 'c') {
            e.preventDefault();
            currentInput = '';
            this.value = '';
            cmdText.textContent = '';
            suggestionEl.textContent = '';
            print('^C', 'red');
            print('type "help" for commands', 'muted');
            return;
        }

        if (e.key === 'Tab') {
            e.preventDefault();
            const suggestions = getSuggestions(currentInput);
            if (suggestions.length > 0) {
                if (suggestions.length === 1) {
                    applySuggestion();
                } else {
                    print(`  ${suggestions.join('  ')}`, 'muted');
                    const first = suggestions[0];
                    currentInput = first;
                    cmdText.textContent = first;
                    hidden.value = first;
                    suggestionEl.textContent = '';
                }
            }
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
            suggestionEl.textContent = '';
            output.scrollTop = output.scrollHeight;
        }

        if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (history.length > 0 && historyIdx > 0) {
                historyIdx--;
                this.value = history[historyIdx];
                currentInput = this.value;
                cmdText.textContent = currentInput;
                suggestionEl.textContent = '';
            }
        }

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIdx < history.length - 1) {
                historyIdx++;
                this.value = history[historyIdx];
                currentInput = this.value;
                cmdText.textContent = currentInput;
                suggestionEl.textContent = '';
            } else {
                historyIdx = history.length;
                this.value = '';
                currentInput = '';
                cmdText.textContent = '';
                suggestionEl.textContent = '';
            }
        }

        if (e.key === 'Escape') {
            this.value = '';
            currentInput = '';
            cmdText.textContent = '';
            suggestionEl.textContent = '';
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