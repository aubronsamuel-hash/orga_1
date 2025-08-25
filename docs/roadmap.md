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
Jalon 1 - Backend minimal + Observabilite: OK
Jalon 2 - Frontend base: OK
Jalon 3 - Auth v1: EN COURS
- [x] CRUD users + login/refresh/logout
- [x] Hash bcrypt + JWT
- [x] Rate limit actif (fallback memoire)
- [x] 2FA TOTP stub
- [x] Logs securite
- [ ] RBAC fin (plus tard)

Jalon 4 - Missions v1: EN COURS
- [x] CRUD missions/roles/assignments
- [x] Validations dates et overlap
- [x] Audit log
- [x] Tests property dates

Jalon 5 - Disponibilites v1: EN COURS
- [ ] CRUD availabilities OK
- [ ] Conflits detectes
- [ ] Normalisation UTC stricte
- [ ] Stress tests 1000 dispos
- [ ] Vue calendrier (frontend)

Notes:
Ce document prime sur les autres. Proposer patch si divergence.

