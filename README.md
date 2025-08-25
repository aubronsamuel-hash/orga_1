# Coulisses Crew (monorepo)

Vision:
SaaS de gestion des techniciens: missions, plannings, disponibilites, comptabilite, notifications.

Objectifs:
Qualite, securite, Windows-first, CI verte, scalabilite, observabilite, conformite RGPD, tests beton.

Conventions globales:
- OS cible: Windows 10/11. Shell: PowerShell.
- Repertoires: backend/, frontend/, infra/, docs/, PS1/, .github/
- Branch naming: feat/-, fix/, chore/
- Commits: Conventional Commits
- Envs: .env, .env.example (sans secrets), .env.test, .env.staging, .env.prod
- Qualite: ruff + mypy (py), eslint + tsc (ts), pip-audit, npm audit, trivy (images), bandit (py sec), k6 (charge)
- Observabilite: logs JSON correles (request_id), Prometheus, Grafana, Loki, OpenTelemetry
- CI/CD: GitHub Actions, matrix Python 3.12/3.13 + Node 20/22, artefacts coverage, dependabot, caches npm/pip
- Tests: unit, integration, E2E (Cypress), smoke/load (k6), snapshot exports, fuzz, property-based (hypothesis)
- Securite: SAST, DAST (OWASP ZAP), dependabot, secret scanning, PR gates, 2FA optionnel
- Conformite: RGPD (droit a l oubli, export), retention logs 30j dev/staging, 90j prod

Jalon 0 (Bootstrap) - criteres d acceptation:
- CI backend/frontend verte (lint + tests vides)
- Scripts PowerShell executables
- pre-commit installe
- dependabot actif

Demenrage rapide (Windows PowerShell):
1) Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
2) .\PS1\init_repo.ps1
3) .\PS1\lint_all.ps1
4) .\PS1\test_all.ps1

Arborescence (extrait):
- backend: pyproject, tests, conf ruff/mypy
- frontend: React+TS+Vite minimal
- docs: roadmap.md (source de verite)
- PS1: scripts Windows-first
