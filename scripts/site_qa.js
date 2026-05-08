#!/usr/bin/env node
/**
 * Mitra AI Life · public site QA
 *
 * Checks for:
 *   - missing local href targets (ignoring external URLs)
 *   - in-page anchor fragments (#id) that do not resolve to an element
 *   - SEO basics on every public HTML page (title, description, canonical,
 *     og:title, og:description, og:image, viewport, lang attribute)
 *   - og:image / twitter:image files served from this site exist on disk
 *   - JSON-LD blocks parse as valid JSON
 *   - sitemap.xml coverage of the public top-level pages
 *
 * Usage:
 *   node scripts/site_qa.js
 *
 * Exits with code 1 if any issue is found.
 */

const fs = require('fs');
const path = require('path');

const SITE_DIR = path.resolve(__dirname, '..', 'site');
const SITEMAP = path.join(SITE_DIR, 'sitemap.xml');

// Pages excluded from SEO checks (utility / non-public-index pages)
const SEO_EXCLUDE = new Set(['404.html', 'logo-options.html']);

// Pages excluded from sitemap coverage check
const SITEMAP_EXCLUDE = new Set([
  '404.html',
  'pitch-deck.html',
  'index-te.html',
  'logo-options.html',
]);

function listHtmlFiles() {
  return fs
    .readdirSync(SITE_DIR)
    .filter((f) => f.endsWith('.html'))
    .sort();
}

function readFile(rel) {
  return fs.readFileSync(path.join(SITE_DIR, rel), 'utf8');
}

function checkLinks(file, html) {
  const issues = [];
  const hrefs = [...html.matchAll(/href="([^"]+)"/g)].map((m) => m[1]);
  for (let href of hrefs) {
    if (/^(https?:|mailto:|tel:)/.test(href)) continue;
    if (href.startsWith('#')) continue; // handled by checkAnchors
    href = href.split('#')[0];
    if (!href) continue;
    const target = path.normalize(
      path.join(path.dirname(path.join(SITE_DIR, file)), href),
    );
    if (!fs.existsSync(target)) {
      issues.push(`broken local link: ${href}`);
    }
  }
  return issues;
}

function checkAnchors(file, html) {
  const issues = [];
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]),
  );
  const fragments = [...html.matchAll(/href="#([^"]+)"/g)].map((m) => m[1]);
  for (const frag of fragments) {
    if (!ids.has(frag)) {
      issues.push(`broken anchor: #${frag}`);
    }
  }
  return issues;
}

function checkLocalAssets(file, html) {
  const issues = [];
  const SITE_ORIGIN = 'https://mitraailife.com';
  const metas = [
    ...html.matchAll(/<meta\s+(?:property|name)="(?:og:image|twitter:image)"\s+content="([^"]+)"/gi),
  ].map((m) => m[1]);
  for (const url of metas) {
    if (!url.startsWith(SITE_ORIGIN + '/')) continue; // skip external (e.g. S3)
    const rel = url.slice(SITE_ORIGIN.length).replace(/^\//, '');
    const target = path.join(SITE_DIR, rel);
    if (!fs.existsSync(target)) {
      issues.push(`og/twitter image missing on disk: ${rel}`);
    }
  }
  return issues;
}

function checkJsonLd(file, html) {
  const issues = [];
  const blocks = [
    ...html.matchAll(/<script\s+type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi),
  ].map((m) => m[1]);
  blocks.forEach((raw, i) => {
    try {
      JSON.parse(raw.trim());
    } catch (err) {
      issues.push(`JSON-LD block #${i + 1} invalid: ${err.message}`);
    }
  });
  return issues;
}

function checkSeo(file, html) {
  if (SEO_EXCLUDE.has(file)) return [];
  const issues = [];
  const checks = [
    ['<html', /<html[^>]*\blang="[a-zA-Z-]+"/, 'missing <html lang="...">'],
    ['<title>', /<title>[^<]+<\/title>/, 'missing or empty <title>'],
    ['viewport', /<meta\s+name="viewport"[^>]+>/i, 'missing viewport meta'],
    [
      'description',
      /<meta\s+name="description"\s+content="[^"]+"/i,
      'missing meta description',
    ],
    [
      'canonical',
      /<link\s+rel="canonical"\s+href="https?:\/\/[^"]+"/i,
      'missing canonical link',
    ],
    [
      'og:title',
      /<meta\s+property="og:title"\s+content="[^"]+"/i,
      'missing og:title',
    ],
    [
      'og:description',
      /<meta\s+property="og:description"\s+content="[^"]+"/i,
      'missing og:description',
    ],
    [
      'og:image',
      /<meta\s+property="og:image"\s+content="https?:\/\/[^"]+"/i,
      'missing og:image',
    ],
  ];
  for (const [, regex, message] of checks) {
    if (!regex.test(html)) issues.push(message);
  }
  return issues;
}

function checkSitemapCoverage(files) {
  if (!fs.existsSync(SITEMAP)) {
    return ['sitemap.xml is missing'];
  }
  const sitemap = fs.readFileSync(SITEMAP, 'utf8');
  const issues = [];
  for (const file of files) {
    if (SITEMAP_EXCLUDE.has(file)) continue;
    const expected = file === 'index.html' ? '/' : `/${file}`;
    const tail = expected === '/' ? '/' : expected;
    if (!sitemap.includes(tail)) {
      issues.push(`sitemap.xml does not list ${file}`);
    }
  }
  return issues;
}

function main() {
  const files = listHtmlFiles();
  let problems = 0;

  for (const file of files) {
    const html = readFile(file);
    const issues = [
      ...checkLinks(file, html),
      ...checkAnchors(file, html),
      ...checkLocalAssets(file, html),
      ...checkJsonLd(file, html),
      ...checkSeo(file, html),
    ];
    if (issues.length) {
      problems += issues.length;
      console.log(`\n${file}`);
      for (const issue of issues) console.log(`  - ${issue}`);
    }
  }

  const sitemapIssues = checkSitemapCoverage(files);
  if (sitemapIssues.length) {
    problems += sitemapIssues.length;
    console.log('\nsitemap.xml');
    for (const issue of sitemapIssues) console.log(`  - ${issue}`);
  }

  if (problems) {
    console.log(`\nFAIL: ${problems} issue(s) across ${files.length} pages.`);
    process.exit(1);
  }
  console.log(`OK: ${files.length} pages, links and SEO basics validated.`);
}

main();
