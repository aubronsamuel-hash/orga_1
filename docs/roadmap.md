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

Jalon 0 - Bootstrap:
- [x] Arborescence creee
- [x] Fichiers racine complets
- [x] Workflows CI operatifs
- [x] pre-commit actif
- [x] Dependabot actif

Jalon 1 - Backend minimal + Observabilite de base:
- [ ] FastAPI demarre (/api/v1)
- [ ] Endpoints GET /health, GET /version
- [ ] Middleware request_id + logs JSON
- [ ] CLI Typer "cc"
- [ ] Tests + scripts PS

Jalon 2 - Frontend base:
- [ ] Page /health OK (Loading/OK/KO)
- [ ] Tailwind + UI compatibles shadcn operatifs
- [ ] Lint + build OK
- [ ] Tests vitest OK (+ a11y axe)
- [ ] Storybook OK

Notes:
Ce document prime sur les autres. Proposer patch si divergence.

