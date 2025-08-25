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
- [ ] Middleware request_id (header X-Request-ID) + logs JSON correles
- [ ] Gestion erreurs JSON standardisee
- [ ] CLI Typer "cc": --version, env, check [--json], ping
- [ ] Tests OK/KO backend et CLI
- [ ] Scripts PowerShell: dev_up, dev_down, smoke
- [ ] CI backend installe requirements.txt et run tests

Notes:
Ce document prime sur les autres. Proposer patch si divergence.

