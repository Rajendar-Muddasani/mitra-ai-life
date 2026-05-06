// ─── Mitra AI Life · Supabase Auth + Progress ────────────────────────────
// The anon key is safe to expose in client-side code.
// It is a public key — all data access is controlled by Row Level Security.

const SUPABASE_URL  = 'https://kuriwaysdlqnzqqzabts.supabase.co';
const SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1cml3YXlzZGxxbnpxcXphYnRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgwNTE5NzYsImV4cCI6MjA5MzYyNzk3Nn0.UA2AgEmnA6r_evrAyXz0MTVhohziKdspkjuB6wHD6fw';

// Wait for supabase SDK to be available (loaded via CDN before this script)
const _sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON);

// ─── Auth helpers ──────────────────────────────────────────────────────────

async function signInWithGoogle() {
  // Strip trailing slash so https://mitraailife.com/ → https://mitraailife.com
  // which matches the Supabase Site URL exactly. Deep paths (/content/...) are kept as-is.
  const path = window.location.pathname.replace(/\/$/, '');
  const redirectTo = window.location.origin + (path || '');
  const { error } = await _sb.auth.signInWithOAuth({
    provider: 'google',
    options: { redirectTo }
  });
  if (error) console.error('Sign-in error:', error.message);
}

async function signOut() {
  await _sb.auth.signOut();
  window.location.reload();
}

async function getCurrentUser() {
  const { data: { session } } = await _sb.auth.getSession();
  return session ? session.user : null;
}

// ─── Progress helpers ──────────────────────────────────────────────────────

// levelId: 'level-01' | 'level-02' etc.
async function saveProgress(levelId, quizScore) {
  const user = await getCurrentUser();
  if (!user) return;                    // not logged in — silent no-op
  const { error } = await _sb.from('user_progress').upsert(
    { user_id: user.id, level_id: levelId, quiz_score: quizScore, completed_at: new Date().toISOString() },
    { onConflict: 'user_id,level_id' }
  );
  if (error) console.error('saveProgress error:', error.message);
}

async function getProgress() {
  const user = await getCurrentUser();
  if (!user) return [];
  const { data, error } = await _sb.from('user_progress').select('*').eq('user_id', user.id);
  if (error) { console.error('getProgress error:', error.message); return []; }
  return data || [];
}

// ─── Nav UI ────────────────────────────────────────────────────────────────

// authNavArea: a DOM element to inject the login/user button into
async function renderAuthUI(authNavArea) {
  if (!authNavArea) return;
  const user = await getCurrentUser();

  if (!user) {
    authNavArea.innerHTML =
      '<button onclick="signInWithGoogle()" style="'
      + 'display:flex;align-items:center;gap:7px;'
      + 'background:white;border:1.5px solid #dadce0;border-radius:22px;'
      + 'padding:6px 14px 6px 10px;cursor:pointer;font-size:0.82rem;font-weight:700;'
      + 'color:#3c4043;white-space:nowrap;box-shadow:0 1px 3px rgba(0,0,0,0.12);'
      + '">'
      + '<svg width="16" height="16" viewBox="0 0 48 48"><path fill="#4285F4" d="M46.1 24.6c0-1.6-.1-3.1-.4-4.6H24v8.7h12.4c-.5 2.7-2.1 5-4.5 6.5v5.4h7.3c4.3-3.9 6.9-9.7 6.9-16z"/><path fill="#34A853" d="M24 47c6.5 0 11.9-2.1 15.9-5.8l-7.3-5.4c-2.2 1.5-5 2.3-8.6 2.3-6.6 0-12.2-4.5-14.2-10.5H2.2v5.6C6.2 41.9 14.5 47 24 47z"/><path fill="#FBBC05" d="M9.8 27.6A14.9 14.9 0 0 1 9.8 20.4V14.8H2.2A23 23 0 0 0 1 24c0 3.2.5 6.3 1.2 9.2l7.6-5.6z"/><path fill="#EA4335" d="M24 9.5c3.7 0 7 1.3 9.6 3.8l7.2-7.2C36.9 2.1 31.5 0 24 0 14.5 0 6.2 5.1 2.2 12.8l7.6 5.6C11.8 12 17.4 9.5 24 9.5z"/></svg>'
      + 'Sign in with Google'
      + '</button>';
  } else {
    const name    = user.user_metadata?.full_name || user.email || 'Learner';
    const avatar  = user.user_metadata?.avatar_url;
    const initials = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

    authNavArea.innerHTML =
      '<div style="display:flex;align-items:center;gap:8px;">'
      + (avatar
          ? '<img src="' + avatar + '" alt="" style="width:30px;height:30px;border-radius:50%;object-fit:cover;border:2px solid #2563eb;">'
          : '<div style="width:30px;height:30px;border-radius:50%;background:#2563eb;color:white;display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:800;">' + initials + '</div>')
      + '<span style="font-size:0.82rem;font-weight:700;color:#1e3a5f;max-width:100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + name.split(' ')[0] + '</span>'
      + '<button onclick="signOut()" style="font-size:0.75rem;padding:4px 10px;border:1px solid #e2e8f0;border-radius:14px;background:transparent;cursor:pointer;color:#64748b;">Sign out</button>'
      + '</div>';
  }
}

// ─── Progress badges on index page ────────────────────────────────────────

async function renderProgressBadges() {
  const progress = await getProgress();
  if (!progress.length) return;

  const done = new Set(progress.map(r => r.level_id));

  // Level cards on index.html have data-level-id attributes
  document.querySelectorAll('[data-level-id]').forEach(card => {
    const lid = card.dataset.levelId;
    if (done.has(lid)) {
      // Add a ✓ Done badge if not already there
      if (!card.querySelector('.progress-done-badge')) {
        const badge = document.createElement('div');
        badge.className = 'progress-done-badge';
        badge.style.cssText =
          'position:absolute;top:10px;right:10px;background:#10b981;color:white;'
          + 'font-size:0.7rem;font-weight:800;padding:3px 10px;border-radius:12px;'
          + 'letter-spacing:0.5px;';
        badge.textContent = '✓ Done';
        // card needs position:relative
        card.style.position = 'relative';
        card.appendChild(badge);
      }
    }
  });
}

// ─── Auto-init on DOMContentLoaded ────────────────────────────────────────

document.addEventListener('DOMContentLoaded', async () => {
  // Render auth button in every element with id="auth-nav-area"
  renderAuthUI(document.getElementById('auth-nav-area'));

  // Render progress badges if on index page
  if (document.getElementById('levels-grid')) {
    renderProgressBadges();
  }

  // Listen for auth state changes (e.g. after OAuth redirect)
  _sb.auth.onAuthStateChange((_event, _session) => {
    renderAuthUI(document.getElementById('auth-nav-area'));
    if (document.getElementById('levels-grid')) renderProgressBadges();
  });
});
