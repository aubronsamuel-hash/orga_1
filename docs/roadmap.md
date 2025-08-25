# Roadmap (source de verite)

Vision:
SaaS de gestion des techniciens: missions, plannings, disponibilites, comptabilite, notifications.

Objectifs:
Qualite, securite, Windows-first, CI verte, scalabilite, observabilite, RGPD, tests.

Conventions:
- OS: Windows 10/11 PowerShell
- Repos: backend/, frontend/, infra/, docs/, PS1/, .github/
- Qualite: ruff+mypy, eslint+tsc
- CI: GitHub Actions matrix Python 3.12/3.13, Node 20/22
- Logs JSON correles (request_id)
- RGPD: export, droit a l oubli, retention 30j dev/stage, 90j prod

Jalon 0 - Bootstrap: OK
- [x] Arborescence creee
- [x] Fichiers racine complets
- [x] Workflows CI operatifs
- [x] pre-commit actif
- [x] Dependabot actif

Jalon 1 - Backend minimal + Observabilite de base: EN COURS
- [x] FastAPI demarre (/api/v1)
- [x] Endpoints GET /health, GET /version
- [x] Middleware request_id + logs JSON
- [x] CLI Typer "cc"
- [x] Tests + scripts PS

Jalon 2 - Frontend base: EN COURS
- [x] Page /health OK (Loading/OK/KO)
- [x] Tailwind + UI compatibles shadcn operatifs
- [x] Lint + build OK
- [x] Tests vitest OK (+ a11y axe)
- [x] Storybook OK

Jalon 3 - Auth v1: EN COURS
- [ ] CRUD users + login/refresh/logout OK
- [ ] Hash bcrypt + JWT OK
- [ ] Rate limit actif (Redis ou memoire)
- [ ] 2FA TOTP stub
- [ ] Logs securite + lock progressif
- [ ] Pages FE Login/Register/Profil + guards

Notes:
Ce document prime sur les autres. Proposer patch si divergence.
