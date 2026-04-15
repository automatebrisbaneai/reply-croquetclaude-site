/* app.js — shared token loader + submit helper for reply.croquetclaude.com */

const PB_BASE = 'https://pb.croquetwade.com';
const TOKENS_COLLECTION = 'reply_mission_tokens';
const RESPONSES_COLLECTION = 'reply_mission_responses';

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
 * Returns the record object, or null if invalid/expired/submitted.
 */
async function fetchToken(tokenValue) {
    const filter = encodeURIComponent(`token="${tokenValue}"`);
    const url = `${PB_BASE}/api/collections/${TOKENS_COLLECTION}/records?filter=${filter}&perPage=1&skipTotal=1`;

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

    // Already submitted?
    if (record.submitted_at) return null;

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

    if (typeof window.renderMission === 'function') {
        window.renderMission(record);
    }
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
        user_agent: navigator.userAgent
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
                <div class="tick">&#10003;</div>
                <h1>Thanks ${firstName} — Wade will see your answers right away.</h1>
                <p>You don't need to do anything else.</p>
            </div>
        `;
    }

    return true;
}

// Expose for inline scripts
window.initMission = initMission;
window.submitMission = submitMission;
