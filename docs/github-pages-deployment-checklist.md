# GitHub Pages Deployment Checklist

Use this checklist before and after public website changes for `mitraailife.com`.

## Before Editing

- Run `git status --short` and note unrelated files before making changes.
- Keep large generated media outside GitHub. Upload videos and heavy assets to S3/object storage.
- Keep public site files under `site/` unless there is a clear reason to change structure.
- Keep lesson source content under `content/english/` first, then translate or localize.
- Do not change the free-first, English-first, Telugu-next strategy unless the founder explicitly decides it.

## Before Commit

- Check that all new local links point to existing files.
- Check that top navigation still uses the shared order:
  Home, AI for Daily Life, AI for Students, AI Tuition, Spoken English, AI Project Kits, AI for Small Business, AI for Teachers, Contact.
- Check mobile layout for Home and at least one track page.
- Check that `site/sitemap.xml` includes any new public top-level page.
- Check that `site/robots.txt` still points to `https://mitraailife.com/sitemap.xml`.
- Check that public pages do not promise guaranteed AI accuracy.
- Check that child-facing or school-facing pages avoid collecting sensitive child data.

## Recommended Local Checks

Run a local link check from the repository root:

```bash
node - <<'NODE'
const fs=require('fs'), path=require('path');
const files=fs.readdirSync('site').filter(f=>f.endsWith('.html')).map(f=>path.join('site',f));
let missing=[];
for(const file of files){
  const html=fs.readFileSync(file,'utf8');
  for(const m of html.matchAll(/href=["']([^"']+)["']/g)){
    const href=m[1];
    if(/^(https?:|mailto:|#)/.test(href)) continue;
    const clean=href.split('#')[0];
    if(!clean) continue;
    const target=path.normalize(path.join(path.dirname(file), clean));
    if(!fs.existsSync(target)) missing.push(`${file} -> ${href} (${target})`);
  }
}
if(missing.length){ console.log(missing.join('\n')); process.exit(1); }
console.log(`Checked ${files.length} HTML files. No missing local href targets.`);
NODE
```

Optional browser checks:

- Open `site/index.html` locally.
- Open `site/contact.html` locally.
- Open `site/404.html` locally.
- Confirm no horizontal scrolling on mobile-width viewports.
- Confirm primary buttons go to the expected track or contact page.

## Commit And Push

- Stage only the files related to the current task.
- Use a clear commit message, such as `feat: add track page`, `fix: tighten mobile layout`, or `docs: update deployment checklist`.
- Push to `main` after validation.

```bash
git push origin main
```

## After Push

- Wait for GitHub Pages to update.
- Visit `https://mitraailife.com/`.
- Check the changed page directly by URL.
- Check `https://mitraailife.com/sitemap.xml` when sitemap changes.
- Check a missing URL once in a while to confirm `404.html` is served.
- If video or image assets were changed, verify that the S3 URL loads in a browser.

## Current Hosting Notes

- Public site source lives in `site/`.
- Domain is `mitraailife.com`.
- Large media assets are stored outside GitHub.
- Current S3 asset base is `https://mitra-ai-life-assets.s3.us-west-2.amazonaws.com/`.
- Current Google Analytics ID is `G-QGY0LH6W93`.
