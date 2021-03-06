# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog 1.0.0].

## [Unreleased]

2021-02-08
### Added
- cms/blogs/tests.py
- cms/posts/tests.py
- cms/pages/tests.py

### Changed
- cms/atlascasestudies/tests.py
- cms/atlascasestudies/templates/atlascasestudies/atlas_case_study.html
- cms/atlascasestudies/models.py
- cms/blogs/models.py
- cms/blogs/templates/blogs/blog.html
- cms/posts/templates/posts/post.html
- fixtures/testdata.json

2021-02-05
### Added
- cms/publications/tests.py
- cms/atlascasestudies/tests.py

### Changed
- docs where referencing fixtures
2021-02-05
### Changed
- README.md
- docs/application.md
- updated ingress template to use separate secrets for each tls hostname


2021-02-04
### Added
- docs/application.md

### Changed
- README.md
- docs/application.md

2021-02-03
### Added
- developer documentation in /README.md
- documentation folder /docs and moved importer docs there
- requirements.dev to assist with installing dependencies for virtual environments
- Add dependabot.yml file
- Add logging config to cms/settings/base.py
- Specify the Django settings module to use within the Dockerfile for collectstatic

### Changed
- cms/settings/dev.py to serve local static assets
- Update browser-sync to address 3 security advisories

- Document release process for staging

[unreleased]: TODO
[keep a changelog 1.0.0]: https://keepachangelog.com/en/1.0.0/
