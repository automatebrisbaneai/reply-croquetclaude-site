/* app.js — shared token loader + submit helper for reply.croquetclaude.com */

const PB_BASE = 'https://util.croquetwade.com';
const TOKENS_COLLECTION = 'reply_mission_tokens';
const RESPONSES_COLLECTION = 'reply_mission_responses';

/* ---------- localStorage draft backup helpers ---------- */

const LOCAL_DRAFT_PREFIX = 'replyDraft:';

function _writeLocalDraft(token, blob) {
    try {
        localStorage.setItem(LOCAL_DRAFT_PREFIX + token, JSON.stringify(blob));
    } catch { /* quota exceeded or private mode — silently skip */ }
}

function _readLocalDraft(token) {
    try {
        const raw = localStorage.getItem(LOCAL_DRAFT_PREFIX + token);
        if (!raw) return null;
        const parsed = JSON.parse(raw);
        if (!parsed || !parsed.savedAt) return null;
        return parsed;
    } catch { return null; }
}

function _clearLocalDraft(token) {
    try { localStorage.removeItem(LOCAL_DRAFT_PREFIX + token); }
    catch { /* ignore */ }
}

function _mergeLocalDraft(record) {
    const local = _readLocalDraft(record.token);
    if (!local) return;
    // Compare local.savedAt against the _savedAt embedded in draft_payload.
    // PocketBase does not return updated/created on this collection, so we
    // embed the timestamp in the payload itself when PATCHing (see createAutosave).
    const serverSavedAt = record.draft_payload && record.draft_payload._savedAt
        ? record.draft_payload._savedAt
        : null;
    const serverTime = serverSavedAt ? new Date(serverSavedAt).getTime() : 0;
    const localTime = new Date(local.savedAt).getTime();
    if (localTime > serverTime) {
        record.draft_payload = local.payload;
    }
}

/* ------------------------------------------------------- */

/**
 * Show the link-expired / invalid screen.
 * Replaces #app content with the standard expired message.
 */
function showExpiredScreen() {
    const app = document.getElementById('app');
    if (!app) return;
    app.innerHTML = `
        <div class="expired-screen">
            <h1>This link is no longer active.</h1>
            <p>If you've already submitted your response, thank you — nothing more to do.</p>
            <p>If this is a mistake, reply to the email you received or contact
               <a href="mailto:hello@croquetclaude.com">hello@croquetclaude.com</a>.</p>
        </div>
    `;
}

/**
 * Show a loading indicator while we fetch the token.
 */
function showLoadingScreen() {
    const app = document.getElementById('app');
    if (!app) return;
    app.innerHTML = '<div class="loading-screen">Loading your question…</div>';
}

/**
 * Read ?t= from the current URL.
 * Returns null if not present.
 */
function getTokenParam() {
    const params = new URLSearchParams(window.location.search);
    return params.get('t') || null;
}

/**
 * Fetch and validate the token record from PocketBase.
 * The collection listRule requires ?t=<token> as a query param (not a filter).
 * Returns the record object, or null if invalid/expired/submitted.
 */
async function fetchToken(tokenValue) {
    // Pass token as ?t= query param — the PB listRule is:
    //   token = @request.query.t && revoked = false && submitted_at = null
    const url = `${PB_BASE}/api/collections/${TOKENS_COLLECTION}/records?t=${encodeURIComponent(tokenValue)}&perPage=1&skipTotal=1`;

    let data;
    try {
        const res = await fetch(url);
        if (!res.ok) return null;
        data = await res.json();
    } catch {
        return null;
    }

    if (!data.items || data.items.length === 0) return null;

    const record = data.items[0];

    // Revoked?
    if (record.revoked) return null;

    // Already submitted? (PB returns "" for null datetime)
    if (record.submitted_at && record.submitted_at !== '') return null;

    // Expired?
    if (record.expires_at) {
        const expires = new Date(record.expires_at);
        if (expires < new Date()) return null;
    }

    return record;
}

/**
 * Entry point. Called by mission pages on DOMContentLoaded.
 * Validates the token, then calls renderMission(record) if valid.
 * The mission page must define window.renderMission before calling this.
 */
async function initMission() {
    const params = new URLSearchParams(window.location.search);

    // Edit mode: skip reply-token validation — render page for editing.
    // edit.js handles its own token from the edit_tokens collection.
    if (params.has('edit')) {
        if (typeof window.renderMission === 'function') {
            window.renderMission({ token: 'edit-preview', seed: {} });
        }
        return;
    }

    const tokenValue = getTokenParam();
    if (!tokenValue) {
        showExpiredScreen();
        return;
    }

    showLoadingScreen();

    const record = await fetchToken(tokenValue);
    if (!record) {
        showExpiredScreen();
        return;
    }

    // Merge in newer local draft if present
    _mergeLocalDraft(record);

    if (typeof window.renderMission === 'function') {
        window.renderMission(record);
    }
}

/**
 * Format a past date as a human-readable relative time string.
 * e.g. "2 hours ago", "just now", "3 days ago"
 */
function relativeTime(dateStr) {
    if (!dateStr) return null;
    const then = new Date(dateStr);
    if (isNaN(then.getTime())) return null;
    const diffMs = Date.now() - then.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return diffMins + ' minute' + (diffMins === 1 ? '' : 's') + ' ago';
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return diffHours + ' hour' + (diffHours === 1 ? '' : 's') + ' ago';
    const diffDays = Math.floor(diffHours / 24);
    return diffDays + ' day' + (diffDays === 1 ? '' : 's') + ' ago';
}

/**
 * Create a draft autosave controller bound to a specific token record.
 *
 * Returns { save(payloadFn), showSavedIndicator() }
 *
 * @param {object} tokenRecord - the full PB token record (needs .id)
 * @param {Function} buildPayload - called with no args, returns the current partial payload
 * @returns {{ save: Function }}
 */
function createAutosave(tokenRecord, buildPayload) {
    let debounceTimer = null;
    let lastSaveFailed = false;

    async function _doSave() {
        const payload = buildPayload();
        const savedAt = new Date().toISOString();

        // Local backup first — survives network failures
        _writeLocalDraft(tokenRecord.token, { payload, savedAt });

        // Embed savedAt inside draft_payload so the server copy carries a
        // freshness timestamp. _mergeLocalDraft compares against this field.
        // renderMission only reads .cards and .general_notes so the extra
        // _savedAt field is harmless there.
        const patchPayload = Object.assign({}, payload, { _savedAt: savedAt });

        try {
            const res = await fetch(
                `${PB_BASE}/api/collections/${TOKENS_COLLECTION}/records/${tokenRecord.id}`,
                {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ draft_payload: patchPayload })
                }
            );
            if (!res.ok) {
                console.warn('[autosave] PATCH returned', res.status);
                lastSaveFailed = true;
                return;
            }
            lastSaveFailed = false;
            _showSavedIndicator();
        } catch (err) {
            console.warn('[autosave] Network error:', err);
            lastSaveFailed = true;
        }
    }

    function _showSavedIndicator() {
        const el = document.getElementById('draft-saved-indicator');
        if (!el) return;
        el.classList.add('visible');
        clearTimeout(el._hideTimer);
        el._hideTimer = setTimeout(function() {
            el.classList.remove('visible');
        }, 2500);
    }

    function save() {
        // If last save failed, attempt immediately (silent retry on next interaction)
        if (lastSaveFailed) {
            lastSaveFailed = false;
            _doSave();
            return;
        }
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(_doSave, 400);
    }

    return { save: save };
}

/**
 * Show the draft-restored notice above the form.
 * Inserts a small banner into the container.
 *
 * @param {HTMLElement} container - the container element to prepend the notice to
 * @param {string} savedAt - ISO date string of when the draft was last saved
 */
function showDraftRestoredNotice(container, savedAt) {
    const rel = relativeTime(savedAt) || 'earlier';
    const notice = document.createElement('div');
    notice.className = 'draft-restored-notice';
    notice.textContent = 'Draft from ' + rel + ' restored.';
    container.insertBefore(notice, container.firstChild);
}

/**
 * Submit the mission response.
 *
 * @param {object} tokenRecord  — the full PB token record (needs .id and .token and .mission)
 * @param {object} responsePayload — the JSON payload to store
 * @param {string} respondentName — for the thank-you message
 * @returns {Promise<boolean>} — true on success
 */
async function submitMission(tokenRecord, responsePayload, respondentName) {
    // 1. POST the response
    const postBody = JSON.stringify({
        token: tokenRecord.token,
        mission: tokenRecord.mission,
        payload: responsePayload,
        user_agent: navigator.userAgent,
        submitted_at: new Date().toISOString()
    });

    let postOk = false;
    try {
        const res = await fetch(`${PB_BASE}/api/collections/${RESPONSES_COLLECTION}/records`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: postBody
        });
        postOk = res.ok;
    } catch {
        postOk = false;
    }

    if (!postOk) {
        return false;
    }

    // Clear local backup — response is safely on the server
    _clearLocalDraft(tokenRecord.token);

    // 2. PATCH the token to mark as submitted
    try {
        await fetch(`${PB_BASE}/api/collections/${TOKENS_COLLECTION}/records/${tokenRecord.id}`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ submitted_at: new Date().toISOString() })
        });
    } catch {
        // Best-effort — response is saved, PATCH failure is non-fatal
    }

    // 3. Show thank-you screen
    const firstName = (respondentName || 'there').split(' ')[0].split(',')[0];
    const app = document.getElementById('app');
    if (app) {
        app.innerHTML = `
            <div class="thankyou-screen visible">
                <img src="/assets/party-claude.png" alt="" class="thankyou-claude">
                <h1>Thanks ${firstName} — I'll get your reply right away.</h1>
                <p>You don't need to do anything else.</p>
            </div>
        `;
    }

    return true;
}

// Expose for inline scripts
window.initMission = initMission;
window.submitMission = submitMission;
window.createAutosave = createAutosave;
window.showDraftRestoredNotice = showDraftRestoredNotice;

// Voice input is now handled by /shared/voice-to-text.js (Phase 2 swap, 2026-04-19).
// Templates call VoiceToText.init({ target: ta, cleanUrl: null }) directly after
// creating each textarea. No DOMContentLoaded auto-attach needed here.

// KILL SWITCH: uncomment if shared voice-to-text.js regresses.
// Delete after one deploy cycle (post 2026-04-21).
//
// function attachVoiceInput(textarea) {
//     const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
//     if (!SpeechRecognition) return;
//
//     // Wrap the textarea in a positioning container
//     const wrapper = document.createElement('div');
//     wrapper.className = 'voice-textarea-wrapper';
//     textarea.parentNode.insertBefore(wrapper, textarea);
//     wrapper.appendChild(textarea);
//
//     // Build the mic button
//     const btn = document.createElement('button');
//     btn.type = 'button';
//     btn.className = 'voice-btn';
//     btn.setAttribute('aria-label', 'Start voice input');
//     btn.setAttribute('title', 'Start voice input');
//     btn.innerHTML = `<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
//         <rect x="9" y="2" width="6" height="12" rx="3" stroke-width="1.75"/>
//         <path d="M5 11a7 7 0 0 0 14 0" stroke-width="1.75" stroke-linecap="round"/>
//         <line x1="12" y1="18" x2="12" y2="22" stroke-width="1.75" stroke-linecap="round"/>
//         <line x1="9" y1="22" x2="15" y2="22" stroke-width="1.75" stroke-linecap="round"/>
//     </svg>`;
//     wrapper.appendChild(btn);
//
//     // Interim preview element
//     const preview = document.createElement('div');
//     preview.className = 'voice-interim';
//     wrapper.after(preview);
//
//     let recognition = null;
//     let silenceTimer = null;
//     let isRecording = false;
//
//     function startRecording() {
//         recognition = new SpeechRecognition();
//         recognition.continuous = true;
//         recognition.interimResults = true;
//         recognition.lang = 'en-AU';
//
//         recognition.onresult = function(event) {
//             // Reset silence timer on any result
//             clearTimeout(silenceTimer);
//             silenceTimer = setTimeout(stopRecording, 3000);
//
//             let interim = '';
//             for (let i = event.resultIndex; i < event.results.length; i++) {
//                 const result = event.results[i];
//                 if (result.isFinal) {
//                     textarea.value = (textarea.value ? textarea.value + ' ' : '') + result[0].transcript.trim();
//                     // Trigger input event so autosave and other listeners fire
//                     textarea.dispatchEvent(new Event('input', { bubbles: true }));
//                 } else {
//                     interim += result[0].transcript;
//                 }
//             }
//             preview.textContent = interim;
//         };
//
//         recognition.onend = function() {
//             // onend fires when recognition stops — clean up if not intentional
//             if (isRecording) {
//                 stopRecording();
//             }
//         };
//
//         recognition.onerror = function() {
//             stopRecording();
//         };
//
//         recognition.start();
//         isRecording = true;
//         btn.classList.add('voice-active');
//         btn.setAttribute('aria-label', 'Stop voice input');
//         btn.setAttribute('title', 'Stop voice input');
//
//         // Arm 3-second silence timer immediately
//         silenceTimer = setTimeout(stopRecording, 3000);
//     }
//
//     function stopRecording() {
//         clearTimeout(silenceTimer);
//         isRecording = false;
//         preview.textContent = '';
//         btn.classList.remove('voice-active');
//         btn.setAttribute('aria-label', 'Start voice input');
//         btn.setAttribute('title', 'Start voice input');
//         if (recognition) {
//             try { recognition.stop(); } catch (_) { /* already stopped */ }
//             recognition = null;
//         }
//     }
//
//     btn.addEventListener('click', function() {
//         if (isRecording) {
//             stopRecording();
//         } else {
//             startRecording();
//         }
//     });
// }
//
// // Auto-attach on page load for any textarea with data-voice="true"
// document.addEventListener('DOMContentLoaded', function() {
//     document.querySelectorAll('textarea[data-voice="true"]').forEach(function(ta) {
//         attachVoiceInput(ta);
//     });
// });
//
// window.attachVoiceInput = attachVoiceInput;
