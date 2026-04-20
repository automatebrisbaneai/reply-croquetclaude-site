// shared/voice-to-text.js — Web Speech API voice input module
// Usage: VoiceToText.init({ target: textarea, cleanUrl: 'optional' })
// Injects its own CSS on first call.
(function(window) {
    var VoiceToText = {};
    var stylesInjected = false;

    function injectStyles() {
        if (stylesInjected) return;
        stylesInjected = true;
        var style = document.createElement('style');
        style.textContent = [
            '.voice-mic-btn {',
            '    position: absolute;',
            '    top: 8px;',
            '    right: 8px;',
            '    width: 36px;',
            '    height: 36px;',
            '    border-radius: 50%;',
            '    border: 1.5px solid #C9C3B6;',
            '    background: #fff;',
            '    color: #4A453D;',
            '    cursor: pointer;',
            '    display: flex;',
            '    align-items: center;',
            '    justify-content: center;',
            '    padding: 0;',
            '    transition: background 0.15s, border-color 0.15s, color 0.15s;',
            '    z-index: 2;',
            '}',
            '.voice-mic-btn:hover { background: #F5F0E8; border-color: #2D6A4F; color: #2D6A4F; }',
            '.voice-mic-btn.voice-mic-active {',
            '    background: #2D6A4F;',
            '    border-color: #2D6A4F;',
            '    color: #fff;',
            '    animation: mic-pulse 1.2s ease-in-out infinite;',
            '}',
            '@keyframes mic-pulse {',
            '    0%, 100% { box-shadow: 0 0 0 0 rgba(45, 106, 79, 0.4); }',
            '    50% { box-shadow: 0 0 0 6px rgba(45, 106, 79, 0); }',
            '}',
            '@media (prefers-reduced-motion: reduce) {',
            '    .voice-mic-btn.voice-mic-active { animation: none; }',
            '}'
        ].join('\n');
        document.head.appendChild(style);
    }

    VoiceToText.init = function(opts) {
        injectStyles();
        var target = opts.target;
        var container = target.parentNode;

        var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) return;

        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'voice-mic-btn';
        btn.setAttribute('aria-label', 'Tap to speak');
        btn.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 10a7 7 0 0 0 14 0"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>';

        container.style.position = 'relative';
        container.appendChild(btn);

        var recognition = null;
        var active = false;

        btn.addEventListener('click', function() {
            if (active) {
                if (recognition) recognition.stop();
                return;
            }

            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-AU';

            var baseText = target.value;

            recognition.onresult = function(e) {
                var interim = '';
                var final = '';
                for (var i = e.resultIndex; i < e.results.length; i++) {
                    if (e.results[i].isFinal) {
                        final += e.results[i][0].transcript;
                    } else {
                        interim += e.results[i][0].transcript;
                    }
                }
                if (final) {
                    baseText = (baseText + (baseText ? ' ' : '') + final).trim();
                    target.value = baseText;
                } else {
                    target.value = (baseText + (baseText ? ' ' : '') + interim).trim();
                }
                target.dispatchEvent(new Event('input'));
            };

            recognition.onstart = function() {
                active = true;
                btn.classList.add('voice-mic-active');
                btn.setAttribute('aria-label', 'Tap to stop recording');
            };

            recognition.onend = function() {
                active = false;
                btn.classList.remove('voice-mic-active');
                btn.setAttribute('aria-label', 'Tap to speak');
            };

            recognition.onerror = function() {
                active = false;
                btn.classList.remove('voice-mic-active');
                btn.setAttribute('aria-label', 'Tap to speak');
            };

            recognition.start();
        });
    };

    window.VoiceToText = VoiceToText;
})(window);
