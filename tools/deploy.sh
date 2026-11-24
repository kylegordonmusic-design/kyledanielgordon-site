#!/bin/bash
# usage: deploy.sh "commit message"
set -e
cd /tmp/site_new
find . -type f ! -name netlify.toml ! -name README.md ! -path './img/*.jpg' -exec cp --parents {} /home/claude/kyledanielgordon-site/public/ \;
{ ls img/share-*.jpg img/kyle-daniel-gordon-orchestrator-share.jpg; grep -rhoE '/img/[^"'"'"' )<]+\.jpg' --include=*.html --include=*.xml . | sed 's#^/##'; } | sort -u | while read f; do [ -f "$f" ] && cp --parents "$f" /home/claude/kyledanielgordon-site/public/; done
cd /home/claude/kyledanielgordon-site
cp /home/claude/kdg_scripts/{gen_lux.py,build_static.py,make_og.py,speed.py,shortlinks.py,assets.json,llms.txt,deploy.sh} tools/; mkdir -p tools/library && cp /home/claude/kdg_scripts/library/gen_library.py tools/library/
git add -A
git commit -qm "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01J4kEb8i43ScNqshKGYvctF" || true
git -c push.negotiate=true push -q
git log --oneline -3
