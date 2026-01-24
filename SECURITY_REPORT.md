# Security Vulnerability Report

**Generated on:** Sat Jan 24 20:56:01 CET 2026
**Scan Tool:** Safety CLI

## Summary

This report contains security vulnerabilities found in the project dependencies.

## Vulnerabilities Found

```json


+===========================================================================================================================================================================================+


DEPRECATED: this command (`check`) has been DEPRECATED, and will be unsupported beyond 01 June 2024.


We highly encourage switching to the new `scan` command which is easier to use, more powerful, and can be set up to mimic the deprecated command if required.


+===========================================================================================================================================================================================+


{
    "report_meta": {
        "scan_target": "environment",
        "scanned": [
            "/opt/homebrew/Cellar/python@3.13/3.13.11_1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload",
            "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor",
            "/opt/homebrew/Cellar/python@3.13/3.13.11_1/Frameworks/Python.framework/Versions/3.13/lib/python313.zip",
            "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages",
            "/opt/homebrew/Cellar/python@3.13/3.13.11_1/Frameworks/Python.framework/Versions/3.13/lib/python3.13",
            "/Users/martin/.local/pipx/venvs/safety/bin",
            "/Users/martin/.local/pipx/shared/lib/python3.13/site-packages",
            "/opt/homebrew/opt/python-tk@3.13/libexec"
        ],
        "scanned_full_path": [
            "/Users/martin/.local/pipx/venvs/safety/bin",
            "/opt/homebrew/Cellar/python@3.13/3.13.11_1/Frameworks/Python.framework/Versions/3.13/lib/python313.zip",
            "/opt/homebrew/Cellar/python@3.13/3.13.11_1/Frameworks/Python.framework/Versions/3.13/lib/python3.13",
            "/opt/homebrew/Cellar/python@3.13/3.13.11_1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload",
            "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages",
            "/Users/martin/.local/pipx/shared/lib/python3.13/site-packages",
            "/opt/homebrew/opt/python-tk@3.13/libexec",
            "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
        ],
        "target_languages": [
            "python"
        ],
        "policy_file": null,
        "policy_file_source": "local",
        "audit_and_monitor": false,
        "api_key": false,
        "account": "martin@bondit.dk",
        "local_database_path": null,
        "safety_version": "3.6.1",
        "timestamp": "2026-01-24 20:55:58",
        "packages_found": 58,
        "vulnerabilities_found": 11,
        "vulnerabilities_ignored": 0,
        "remediations_recommended": 5,
        "telemetry": {
            "safety_options": {
                "json": {
                    "--json": 1
                }
            },
            "safety_version": "3.6.1",
            "safety_source": "cli",
            "os_type": "Darwin",
            "os_release": "25.2.0",
            "os_description": "macOS-26.2-arm64-arm-64bit-Mach-O",
            "python_version": "3.13.11",
            "safety_command": "check"
        },
        "git": {
            "branch": "main",
            "tag": "",
            "commit": "678e0748f192cbcf50b9e73e1398011396573fc4",
            "dirty": "False",
            "origin": "https://github.com/MaBoNi/homeassistant-tracker.git"
        },
        "project": null,
        "json_version": "1.1",
        "remediations_attempted": 0,
        "remediations_completed": 0,
        "remediation_mode": "NON_INTERACTIVE"
    },
    "scanned_packages": {
        "markupsafe": {
            "name": "markupsafe",
            "version": "3.0.2",
            "requirements": [
                {
                    "raw": "markupsafe==3.0.2",
                    "extras": [],
                    "marker": null,
                    "name": "markupsafe",
                    "specifier": "==3.0.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "annotated-types": {
            "name": "annotated-types",
            "version": "0.7.0",
            "requirements": [
                {
                    "raw": "annotated-types==0.7.0",
                    "extras": [],
                    "marker": null,
                    "name": "annotated-types",
                    "specifier": "==0.7.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "anyio": {
            "name": "anyio",
            "version": "4.10.0",
            "requirements": [
                {
                    "raw": "anyio==4.10.0",
                    "extras": [],
                    "marker": null,
                    "name": "anyio",
                    "specifier": "==4.10.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "authlib": {
            "name": "authlib",
            "version": "1.6.4",
            "requirements": [
                {
                    "raw": "authlib==1.6.4",
                    "extras": [],
                    "marker": null,
                    "name": "authlib",
                    "specifier": "==1.6.4",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "certifi": {
            "name": "certifi",
            "version": "2025.8.3",
            "requirements": [
                {
                    "raw": "certifi==2025.8.3",
                    "extras": [],
                    "marker": null,
                    "name": "certifi",
                    "specifier": "==2025.8.3",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "cffi": {
            "name": "cffi",
            "version": "2.0.0",
            "requirements": [
                {
                    "raw": "cffi==2.0.0",
                    "extras": [],
                    "marker": null,
                    "name": "cffi",
                    "specifier": "==2.0.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "charset-normalizer": {
            "name": "charset-normalizer",
            "version": "3.4.3",
            "requirements": [
                {
                    "raw": "charset-normalizer==3.4.3",
                    "extras": [],
                    "marker": null,
                    "name": "charset-normalizer",
                    "specifier": "==3.4.3",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "click": {
            "name": "click",
            "version": "8.3.0",
            "requirements": [
                {
                    "raw": "click==8.3.0",
                    "extras": [],
                    "marker": null,
                    "name": "click",
                    "specifier": "==8.3.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "cryptography": {
            "name": "cryptography",
            "version": "46.0.1",
            "requirements": [
                {
                    "raw": "cryptography==46.0.1",
                    "extras": [],
                    "marker": null,
                    "name": "cryptography",
                    "specifier": "==46.0.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "dparse": {
            "name": "dparse",
            "version": "0.6.4",
            "requirements": [
                {
                    "raw": "dparse==0.6.4",
                    "extras": [],
                    "marker": null,
                    "name": "dparse",
                    "specifier": "==0.6.4",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "filelock": {
            "name": "filelock",
            "version": "3.19.1",
            "requirements": [
                {
                    "raw": "filelock==3.19.1",
                    "extras": [],
                    "marker": null,
                    "name": "filelock",
                    "specifier": "==3.19.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "h11": {
            "name": "h11",
            "version": "0.16.0",
            "requirements": [
                {
                    "raw": "h11==0.16.0",
                    "extras": [],
                    "marker": null,
                    "name": "h11",
                    "specifier": "==0.16.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "httpcore": {
            "name": "httpcore",
            "version": "1.0.9",
            "requirements": [
                {
                    "raw": "httpcore==1.0.9",
                    "extras": [],
                    "marker": null,
                    "name": "httpcore",
                    "specifier": "==1.0.9",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "httpx": {
            "name": "httpx",
            "version": "0.28.1",
            "requirements": [
                {
                    "raw": "httpx==0.28.1",
                    "extras": [],
                    "marker": null,
                    "name": "httpx",
                    "specifier": "==0.28.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "idna": {
            "name": "idna",
            "version": "3.10",
            "requirements": [
                {
                    "raw": "idna==3.10",
                    "extras": [],
                    "marker": null,
                    "name": "idna",
                    "specifier": "==3.10",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "jinja2": {
            "name": "jinja2",
            "version": "3.1.6",
            "requirements": [
                {
                    "raw": "jinja2==3.1.6",
                    "extras": [],
                    "marker": null,
                    "name": "jinja2",
                    "specifier": "==3.1.6",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "joblib": {
            "name": "joblib",
            "version": "1.5.2",
            "requirements": [
                {
                    "raw": "joblib==1.5.2",
                    "extras": [],
                    "marker": null,
                    "name": "joblib",
                    "specifier": "==1.5.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "markdown-it-py": {
            "name": "markdown-it-py",
            "version": "4.0.0",
            "requirements": [
                {
                    "raw": "markdown-it-py==4.0.0",
                    "extras": [],
                    "marker": null,
                    "name": "markdown-it-py",
                    "specifier": "==4.0.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "marshmallow": {
            "name": "marshmallow",
            "version": "4.0.1",
            "requirements": [
                {
                    "raw": "marshmallow==4.0.1",
                    "extras": [],
                    "marker": null,
                    "name": "marshmallow",
                    "specifier": "==4.0.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "mdurl": {
            "name": "mdurl",
            "version": "0.1.2",
            "requirements": [
                {
                    "raw": "mdurl==0.1.2",
                    "extras": [],
                    "marker": null,
                    "name": "mdurl",
                    "specifier": "==0.1.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "nltk": {
            "name": "nltk",
            "version": "3.9.1",
            "requirements": [
                {
                    "raw": "nltk==3.9.1",
                    "extras": [],
                    "marker": null,
                    "name": "nltk",
                    "specifier": "==3.9.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "packaging": {
            "name": "packaging",
            "version": "25.0",
            "requirements": [
                {
                    "raw": "packaging==25.0",
                    "extras": [],
                    "marker": null,
                    "name": "packaging",
                    "specifier": "==25.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "psutil": {
            "name": "psutil",
            "version": "7.1.0",
            "requirements": [
                {
                    "raw": "psutil==7.1.0",
                    "extras": [],
                    "marker": null,
                    "name": "psutil",
                    "specifier": "==7.1.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "pycparser": {
            "name": "pycparser",
            "version": "2.23",
            "requirements": [
                {
                    "raw": "pycparser==2.23",
                    "extras": [],
                    "marker": null,
                    "name": "pycparser",
                    "specifier": "==2.23",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "pydantic": {
            "name": "pydantic",
            "version": "2.9.2",
            "requirements": [
                {
                    "raw": "pydantic==2.9.2",
                    "extras": [],
                    "marker": null,
                    "name": "pydantic",
                    "specifier": "==2.9.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "pydantic-core": {
            "name": "pydantic-core",
            "version": "2.23.4",
            "requirements": [
                {
                    "raw": "pydantic-core==2.23.4",
                    "extras": [],
                    "marker": null,
                    "name": "pydantic-core",
                    "specifier": "==2.23.4",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "pygments": {
            "name": "pygments",
            "version": "2.19.2",
            "requirements": [
                {
                    "raw": "pygments==2.19.2",
                    "extras": [],
                    "marker": null,
                    "name": "pygments",
                    "specifier": "==2.19.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "regex": {
            "name": "regex",
            "version": "2025.9.18",
            "requirements": [
                {
                    "raw": "regex==2025.9.18",
                    "extras": [],
                    "marker": null,
                    "name": "regex",
                    "specifier": "==2025.9.18",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "requests": {
            "name": "requests",
            "version": "2.32.5",
            "requirements": [
                {
                    "raw": "requests==2.32.5",
                    "extras": [],
                    "marker": null,
                    "name": "requests",
                    "specifier": "==2.32.5",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "rich": {
            "name": "rich",
            "version": "14.1.0",
            "requirements": [
                {
                    "raw": "rich==14.1.0",
                    "extras": [],
                    "marker": null,
                    "name": "rich",
                    "specifier": "==14.1.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "ruamel.yaml": {
            "name": "ruamel.yaml",
            "version": "0.18.15",
            "requirements": [
                {
                    "raw": "ruamel.yaml==0.18.15",
                    "extras": [],
                    "marker": null,
                    "name": "ruamel.yaml",
                    "specifier": "==0.18.15",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "ruamel.yaml.clib": {
            "name": "ruamel.yaml.clib",
            "version": "0.2.12",
            "requirements": [
                {
                    "raw": "ruamel.yaml.clib==0.2.12",
                    "extras": [],
                    "marker": null,
                    "name": "ruamel.yaml.clib",
                    "specifier": "==0.2.12",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "safety": {
            "name": "safety",
            "version": "3.6.1",
            "requirements": [
                {
                    "raw": "safety==3.6.1",
                    "extras": [],
                    "marker": null,
                    "name": "safety",
                    "specifier": "==3.6.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "safety-schemas": {
            "name": "safety-schemas",
            "version": "0.0.14",
            "requirements": [
                {
                    "raw": "safety-schemas==0.0.14",
                    "extras": [],
                    "marker": null,
                    "name": "safety-schemas",
                    "specifier": "==0.0.14",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "setuptools": {
            "name": "setuptools",
            "version": "80.9.0",
            "requirements": [
                {
                    "raw": "setuptools==80.9.0",
                    "extras": [],
                    "marker": null,
                    "name": "setuptools",
                    "specifier": "==80.9.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "shellingham": {
            "name": "shellingham",
            "version": "1.5.4",
            "requirements": [
                {
                    "raw": "shellingham==1.5.4",
                    "extras": [],
                    "marker": null,
                    "name": "shellingham",
                    "specifier": "==1.5.4",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "sniffio": {
            "name": "sniffio",
            "version": "1.3.1",
            "requirements": [
                {
                    "raw": "sniffio==1.3.1",
                    "extras": [],
                    "marker": null,
                    "name": "sniffio",
                    "specifier": "==1.3.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "tenacity": {
            "name": "tenacity",
            "version": "9.1.2",
            "requirements": [
                {
                    "raw": "tenacity==9.1.2",
                    "extras": [],
                    "marker": null,
                    "name": "tenacity",
                    "specifier": "==9.1.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "tomlkit": {
            "name": "tomlkit",
            "version": "0.13.3",
            "requirements": [
                {
                    "raw": "tomlkit==0.13.3",
                    "extras": [],
                    "marker": null,
                    "name": "tomlkit",
                    "specifier": "==0.13.3",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "tqdm": {
            "name": "tqdm",
            "version": "4.67.1",
            "requirements": [
                {
                    "raw": "tqdm==4.67.1",
                    "extras": [],
                    "marker": null,
                    "name": "tqdm",
                    "specifier": "==4.67.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "typer": {
            "name": "typer",
            "version": "0.19.1",
            "requirements": [
                {
                    "raw": "typer==0.19.1",
                    "extras": [],
                    "marker": null,
                    "name": "typer",
                    "specifier": "==0.19.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "typing-extensions": {
            "name": "typing-extensions",
            "version": "4.15.0",
            "requirements": [
                {
                    "raw": "typing-extensions==4.15.0",
                    "extras": [],
                    "marker": null,
                    "name": "typing-extensions",
                    "specifier": "==4.15.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "urllib3": {
            "name": "urllib3",
            "version": "2.5.0",
            "requirements": [
                {
                    "raw": "urllib3==2.5.0",
                    "extras": [],
                    "marker": null,
                    "name": "urllib3",
                    "specifier": "==2.5.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ]
        },
        "pip": {
            "name": "pip",
            "version": "25.2",
            "requirements": [
                {
                    "raw": "pip==25.2",
                    "extras": [],
                    "marker": null,
                    "name": "pip",
                    "specifier": "==25.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/shared/lib/python3.13/site-packages"
                }
            ]
        },
        "autocommand": {
            "name": "autocommand",
            "version": "2.2.2",
            "requirements": [
                {
                    "raw": "autocommand==2.2.2",
                    "extras": [],
                    "marker": null,
                    "name": "autocommand",
                    "specifier": "==2.2.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "backports.tarfile": {
            "name": "backports.tarfile",
            "version": "1.2.0",
            "requirements": [
                {
                    "raw": "backports.tarfile==1.2.0",
                    "extras": [],
                    "marker": null,
                    "name": "backports.tarfile",
                    "specifier": "==1.2.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "importlib-metadata": {
            "name": "importlib-metadata",
            "version": "8.0.0",
            "requirements": [
                {
                    "raw": "importlib-metadata==8.0.0",
                    "extras": [],
                    "marker": null,
                    "name": "importlib-metadata",
                    "specifier": "==8.0.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "inflect": {
            "name": "inflect",
            "version": "7.3.1",
            "requirements": [
                {
                    "raw": "inflect==7.3.1",
                    "extras": [],
                    "marker": null,
                    "name": "inflect",
                    "specifier": "==7.3.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "jaraco.collections": {
            "name": "jaraco.collections",
            "version": "5.1.0",
            "requirements": [
                {
                    "raw": "jaraco.collections==5.1.0",
                    "extras": [],
                    "marker": null,
                    "name": "jaraco.collections",
                    "specifier": "==5.1.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "jaraco.context": {
            "name": "jaraco.context",
            "version": "5.3.0",
            "requirements": [
                {
                    "raw": "jaraco.context==5.3.0",
                    "extras": [],
                    "marker": null,
                    "name": "jaraco.context",
                    "specifier": "==5.3.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "jaraco.functools": {
            "name": "jaraco.functools",
            "version": "4.0.1",
            "requirements": [
                {
                    "raw": "jaraco.functools==4.0.1",
                    "extras": [],
                    "marker": null,
                    "name": "jaraco.functools",
                    "specifier": "==4.0.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "jaraco.text": {
            "name": "jaraco.text",
            "version": "3.12.1",
            "requirements": [
                {
                    "raw": "jaraco.text==3.12.1",
                    "extras": [],
                    "marker": null,
                    "name": "jaraco.text",
                    "specifier": "==3.12.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "more-itertools": {
            "name": "more-itertools",
            "version": "10.3.0",
            "requirements": [
                {
                    "raw": "more-itertools==10.3.0",
                    "extras": [],
                    "marker": null,
                    "name": "more-itertools",
                    "specifier": "==10.3.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "platformdirs": {
            "name": "platformdirs",
            "version": "4.2.2",
            "requirements": [
                {
                    "raw": "platformdirs==4.2.2",
                    "extras": [],
                    "marker": null,
                    "name": "platformdirs",
                    "specifier": "==4.2.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "tomli": {
            "name": "tomli",
            "version": "2.0.1",
            "requirements": [
                {
                    "raw": "tomli==2.0.1",
                    "extras": [],
                    "marker": null,
                    "name": "tomli",
                    "specifier": "==2.0.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "typeguard": {
            "name": "typeguard",
            "version": "4.3.0",
            "requirements": [
                {
                    "raw": "typeguard==4.3.0",
                    "extras": [],
                    "marker": null,
                    "name": "typeguard",
                    "specifier": "==4.3.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "wheel": {
            "name": "wheel",
            "version": "0.45.1",
            "requirements": [
                {
                    "raw": "wheel==0.45.1",
                    "extras": [],
                    "marker": null,
                    "name": "wheel",
                    "specifier": "==0.45.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        },
        "zipp": {
            "name": "zipp",
            "version": "3.19.2",
            "requirements": [
                {
                    "raw": "zipp==3.19.2",
                    "extras": [],
                    "marker": null,
                    "name": "zipp",
                    "specifier": "==3.19.2",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ]
        }
    },
    "affected_packages": {
        "wheel": {
            "name": "wheel",
            "version": "0.45.1",
            "requirements": [
                {
                    "raw": "wheel==0.45.1",
                    "extras": [],
                    "marker": null,
                    "name": "wheel",
                    "specifier": "==0.45.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                }
            ],
            "found": null,
            "insecure_versions": [
                "0.1",
                "0.10.0",
                "0.10.1",
                "0.10.2",
                "0.10.3",
                "0.11.0",
                "0.12.0",
                "0.13.0",
                "0.14.0",
                "0.15.0",
                "0.16.0",
                "0.17.0",
                "0.18.0",
                "0.19.0",
                "0.2",
                "0.21.0",
                "0.22.0",
                "0.23.0",
                "0.24.0",
                "0.25.0",
                "0.26.0",
                "0.27.0",
                "0.28.0",
                "0.29.0",
                "0.3",
                "0.30.0",
                "0.30.0a0",
                "0.31.0",
                "0.31.1",
                "0.32.0",
                "0.32.1",
                "0.32.2",
                "0.32.3",
                "0.33.0",
                "0.33.1",
                "0.33.4",
                "0.33.5",
                "0.33.6",
                "0.34.0",
                "0.34.1",
                "0.34.2",
                "0.35.0",
                "0.35.1",
                "0.36.0",
                "0.36.1",
                "0.36.2",
                "0.37.0",
                "0.37.1",
                "0.38.0",
                "0.38.1",
                "0.38.2",
                "0.38.3",
                "0.38.4",
                "0.4",
                "0.40.0",
                "0.4.1",
                "0.41.0",
                "0.41.1",
                "0.41.2",
                "0.41.3",
                "0.4.2",
                "0.42.0",
                "0.43.0",
                "0.44.0",
                "0.45.0",
                "0.45.1",
                "0.46.0",
                "0.46.1",
                "0.5",
                "0.6",
                "0.7",
                "0.8",
                "0.9",
                "0.9.1",
                "0.9.2",
                "0.9.3",
                "0.9.4",
                "0.9.5",
                "0.9.6",
                "0.9.7"
            ],
            "secure_versions": [
                "0.46.3",
                "0.46.2"
            ],
            "latest_version_without_known_vulnerabilities": "0.46.3",
            "latest_version": "0.46.3",
            "more_info_url": "https://data.safetycli.com/p/pypi/wheel/eda/"
        },
        "urllib3": {
            "name": "urllib3",
            "version": "2.5.0",
            "requirements": [
                {
                    "raw": "urllib3==2.5.0",
                    "extras": [],
                    "marker": null,
                    "name": "urllib3",
                    "specifier": "==2.5.0",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ],
            "found": null,
            "insecure_versions": [
                "0.2",
                "0.3",
                "0.3.1",
                "0.4.0",
                "0.4.1",
                "1.0",
                "1.0.1",
                "1.0.2",
                "1.1",
                "1.10",
                "1.10.1",
                "1.10.2",
                "1.10.3",
                "1.10.4",
                "1.11",
                "1.12",
                "1.13",
                "1.13.1",
                "1.14",
                "1.15",
                "1.15.1",
                "1.16",
                "1.17",
                "1.18",
                "1.18.1",
                "1.19",
                "1.19.1",
                "1.2",
                "1.20",
                "1.21",
                "1.2.1",
                "1.21.1",
                "1.22",
                "1.2.2",
                "1.23",
                "1.24",
                "1.24.1",
                "1.24.2",
                "1.24.3",
                "1.25",
                "1.25.1",
                "1.25.10",
                "1.25.11",
                "1.25.2",
                "1.25.3",
                "1.25.4",
                "1.25.5",
                "1.25.6",
                "1.25.7",
                "1.25.8",
                "1.25.9",
                "1.26.0",
                "1.26.1",
                "1.26.10",
                "1.26.11",
                "1.26.12",
                "1.26.13",
                "1.26.14",
                "1.26.15",
                "1.26.16",
                "1.26.17",
                "1.26.18",
                "1.26.19",
                "1.26.2",
                "1.26.20",
                "1.26.3",
                "1.26.4",
                "1.26.5",
                "1.26.6",
                "1.26.7",
                "1.26.8",
                "1.26.9",
                "1.3",
                "1.4",
                "1.5",
                "1.6",
                "1.7",
                "1.7.1",
                "1.8",
                "1.8.2",
                "1.8.3",
                "1.9",
                "1.9.1",
                "2.0.0",
                "2.0.0a1",
                "2.0.0a2",
                "2.0.0a3",
                "2.0.0a4",
                "2.0.1",
                "2.0.2",
                "2.0.3",
                "2.0.4",
                "2.0.5",
                "2.0.6",
                "2.0.7",
                "2.1.0",
                "2.2.0",
                "2.2.1",
                "2.2.2",
                "2.2.3",
                "2.3.0",
                "2.4.0",
                "2.5.0",
                "2.6.0",
                "2.6.1",
                "2.6.2"
            ],
            "secure_versions": [
                "2.6.3"
            ],
            "latest_version_without_known_vulnerabilities": "2.6.3",
            "latest_version": "2.6.3",
            "more_info_url": "https://data.safetycli.com/p/pypi/urllib3/eda/"
        },
        "marshmallow": {
            "name": "marshmallow",
            "version": "4.0.1",
            "requirements": [
                {
                    "raw": "marshmallow==4.0.1",
                    "extras": [],
                    "marker": null,
                    "name": "marshmallow",
                    "specifier": "==4.0.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ],
            "found": null,
            "insecure_versions": [
                "0.1.0",
                "0.2.0",
                "0.2.1",
                "0.3.0",
                "0.3.1",
                "0.4.0",
                "0.4.1",
                "0.5.0",
                "0.5.1",
                "0.5.2",
                "0.5.3",
                "0.5.4",
                "0.5.5",
                "0.6.0",
                "0.7.0",
                "1.0.0",
                "1.0.0a0",
                "1.0.1",
                "1.1.0",
                "1.2.0",
                "1.2.1",
                "1.2.2",
                "1.2.3",
                "1.2.4",
                "1.2.5",
                "1.2.6",
                "2.0.0",
                "2.0.0a1",
                "2.0.0b1",
                "2.0.0b2",
                "2.0.0b3",
                "2.0.0b4",
                "2.0.0b5",
                "2.0.0rc1",
                "2.0.0rc2",
                "2.1.0",
                "2.10.0",
                "2.10.1",
                "2.10.2",
                "2.10.3",
                "2.10.4",
                "2.10.5",
                "2.1.1",
                "2.11.0",
                "2.11.1",
                "2.1.2",
                "2.12.0",
                "2.12.1",
                "2.12.2",
                "2.1.3",
                "2.13.0",
                "2.13.1",
                "2.13.2",
                "2.13.3",
                "2.13.4",
                "2.13.5",
                "2.13.6",
                "2.14.0",
                "2.15.0",
                "2.2.0",
                "2.2.1",
                "2.3.0",
                "2.4.0",
                "2.4.1",
                "2.4.2",
                "2.5.0",
                "2.6.0",
                "2.6.1",
                "2.7.0",
                "2.7.1",
                "2.7.2",
                "2.7.3",
                "2.8.0",
                "2.9.0",
                "2.9.1",
                "3.0.0",
                "3.0.0a1",
                "3.0.0b1",
                "3.0.0b2",
                "3.0.0b3",
                "3.0.0b4",
                "3.0.0b5",
                "3.0.0b6",
                "3.0.0b7",
                "3.0.0b8",
                "3.0.0rc1",
                "3.0.0rc2",
                "3.0.0rc3",
                "3.0.0rc4",
                "3.0.0rc5",
                "3.0.0rc6",
                "3.0.0rc7",
                "3.0.0rc8",
                "3.0.0rc9",
                "3.0.1",
                "3.0.2",
                "3.0.3",
                "3.0.4",
                "3.0.5",
                "3.1.0",
                "3.10.0",
                "3.1.1",
                "3.11.0",
                "3.11.1",
                "3.12.0",
                "3.12.1",
                "3.12.2",
                "3.13.0",
                "3.14.0",
                "3.14.1",
                "3.15.0",
                "3.16.0",
                "3.17.0",
                "3.17.1",
                "3.18.0",
                "3.19.0",
                "3.2.0",
                "3.20.0",
                "3.20.1",
                "3.20.2",
                "3.2.1",
                "3.21.0",
                "3.21.1",
                "3.21.2",
                "3.21.3",
                "3.2.2",
                "3.22.0",
                "3.23.0",
                "3.23.1",
                "3.23.2",
                "3.23.3",
                "3.24.0",
                "3.24.1",
                "3.24.2",
                "3.25.0",
                "3.25.1",
                "3.26.0",
                "3.26.1",
                "3.3.0",
                "3.4.0",
                "3.5.0",
                "3.5.1",
                "3.5.2",
                "3.6.0",
                "3.6.1",
                "3.7.0",
                "3.7.1",
                "3.8.0",
                "3.9.0",
                "3.9.1",
                "4.0.0",
                "4.0.1",
                "4.1.0",
                "4.1.1"
            ],
            "secure_versions": [
                "4.2.1",
                "4.2.0",
                "4.1.2",
                "3.26.2",
                "3.0.0b20",
                "3.0.0b19",
                "3.0.0b18",
                "3.0.0b17",
                "3.0.0b16",
                "3.0.0b15",
                "3.0.0b14",
                "3.0.0b13",
                "3.0.0b12",
                "3.0.0b11",
                "3.0.0b10",
                "3.0.0b9",
                "2.21.0",
                "2.20.5",
                "2.20.4",
                "2.20.3",
                "2.20.2",
                "2.20.1",
                "2.20.0",
                "2.19.5",
                "2.19.4",
                "2.19.3",
                "2.19.2",
                "2.19.1",
                "2.19.0",
                "2.18.1",
                "2.18.0",
                "2.17.0",
                "2.16.3",
                "2.16.2",
                "2.16.1",
                "2.16.0",
                "2.15.6",
                "2.15.5",
                "2.15.4",
                "2.15.3",
                "2.15.2",
                "2.15.1"
            ],
            "latest_version_without_known_vulnerabilities": "4.2.1",
            "latest_version": "4.2.1",
            "more_info_url": "https://data.safetycli.com/p/pypi/marshmallow/eda/"
        },
        "filelock": {
            "name": "filelock",
            "version": "3.19.1",
            "requirements": [
                {
                    "raw": "filelock==3.19.1",
                    "extras": [],
                    "marker": null,
                    "name": "filelock",
                    "specifier": "==3.19.1",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ],
            "found": null,
            "insecure_versions": [
                "0.2.0",
                "0.2.1",
                "0.2.2",
                "1.0.0",
                "1.0.1",
                "1.0.2",
                "1.0.3",
                "2.0.0",
                "2.0.1",
                "2.0.10",
                "2.0.11",
                "2.0.12",
                "2.0.13",
                "2.0.4",
                "2.0.5",
                "2.0.6",
                "2.0.7",
                "2.0.8",
                "2.0.9",
                "3.0.0",
                "3.0.10",
                "3.0.12",
                "3.0.2",
                "3.0.3",
                "3.0.4",
                "3.0.6",
                "3.0.8",
                "3.0.9",
                "3.1.0",
                "3.10.0",
                "3.10.1",
                "3.10.2",
                "3.10.3",
                "3.10.4",
                "3.10.5",
                "3.10.6",
                "3.10.7",
                "3.11.0",
                "3.12.0",
                "3.12.1",
                "3.12.2",
                "3.12.3",
                "3.12.4",
                "3.13.0",
                "3.13.1",
                "3.13.2",
                "3.13.3",
                "3.13.4",
                "3.14.0",
                "3.15.0",
                "3.15.1",
                "3.15.2",
                "3.15.3",
                "3.15.4",
                "3.16.0",
                "3.16.1",
                "3.17.0",
                "3.18.0",
                "3.19.1",
                "3.2.0",
                "3.20.0",
                "3.20.1",
                "3.20.2",
                "3.2.1",
                "3.3.0",
                "3.3.1",
                "3.3.2",
                "3.4.0",
                "3.4.1",
                "3.4.2",
                "3.5.0",
                "3.5.1",
                "3.6.0",
                "3.7.0",
                "3.7.1",
                "3.8.0",
                "3.8.1",
                "3.8.2",
                "3.9.0",
                "3.9.1"
            ],
            "secure_versions": [
                "3.20.3"
            ],
            "latest_version_without_known_vulnerabilities": "3.20.3",
            "latest_version": "3.20.3",
            "more_info_url": "https://data.safetycli.com/p/pypi/filelock/eda/"
        },
        "authlib": {
            "name": "authlib",
            "version": "1.6.4",
            "requirements": [
                {
                    "raw": "authlib==1.6.4",
                    "extras": [],
                    "marker": null,
                    "name": "authlib",
                    "specifier": "==1.6.4",
                    "url": null,
                    "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                }
            ],
            "found": null,
            "insecure_versions": [
                "0.1",
                "0.10",
                "0.11",
                "0.12",
                "0.12.1",
                "0.13",
                "0.14",
                "0.14.1",
                "0.14.2",
                "0.14.3",
                "0.15",
                "0.15.1",
                "0.15.2",
                "0.15.3",
                "0.15.4",
                "0.15.5",
                "0.15.6",
                "0.1rc0",
                "0.2",
                "0.2.1",
                "0.3",
                "0.4",
                "0.4.1",
                "0.5",
                "0.5.1",
                "0.6",
                "0.7",
                "0.8",
                "0.9",
                "1.0.0",
                "1.0.0a1",
                "1.0.0a2",
                "1.0.0b1",
                "1.0.0b2",
                "1.0.0rc1",
                "1.0.1",
                "1.1.0",
                "1.2.0",
                "1.2.1",
                "1.3.0",
                "1.3.1",
                "1.3.2",
                "1.4.0",
                "1.4.1",
                "1.5.0",
                "1.5.1",
                "1.5.2",
                "1.6.0",
                "1.6.1",
                "1.6.2",
                "1.6.3",
                "1.6.4",
                "1.6.5"
            ],
            "secure_versions": [
                "1.6.6"
            ],
            "latest_version_without_known_vulnerabilities": "1.6.6",
            "latest_version": "1.6.6",
            "more_info_url": "https://data.safetycli.com/p/pypi/authlib/eda/"
        }
    },
    "announcements": [],
    "vulnerabilities": [
        {
            "vulnerability_id": "84961",
            "package_name": "wheel",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                "<0.46.2"
            ],
            "all_vulnerable_specs": [
                "<0.46.2"
            ],
            "analyzed_version": "0.45.1",
            "analyzed_requirement": {
                "raw": "wheel==0.45.1",
                "extras": [],
                "marker": null,
                "name": "wheel",
                "specifier": "==0.45.1",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
            },
            "advisory": "Affected versions of the wheel package are vulnerable to Path Traversal due to applying extracted file permissions using an unsanitized archive pathname. The vulnerable logic is in wheel.cli.unpack.unpack (and setuptools._vendor.wheel.cli.unpack.unpack), where the code calls wf.extract(zinfo, destination) but then performs destination.joinpath(zinfo.filename).chmod(permissions) using zinfo.filename directly, allowing dot-dot-slash sequences to escape the intended directory.",
            "is_transitive": false,
            "published_date": "2026-Jan-22",
            "fixed_versions": [
                "0.46.2"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/84961/eda",
                "https://github.com/pypa/wheel/commit/7a7d2de96b22a9adf9208afcc9547e1001569fef",
                "https://github.com/advisories/GHSA-8rrh-rw8j-w5fx",
                "https://pypi.org/project/wheel",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-24049"
            ],
            "CVE": "CVE-2026-24049",
            "severity": null,
            "affected_versions": [
                "0.46.1",
                "0.46.0",
                "0.45.1",
                "0.45.0",
                "0.44.0",
                "0.43.0",
                "0.42.0",
                "0.41.3",
                "0.41.2",
                "0.41.1",
                "0.41.0",
                "0.40.0",
                "0.38.4",
                "0.38.3",
                "0.38.2",
                "0.38.1",
                "0.38.0",
                "0.37.1",
                "0.37.0",
                "0.36.2",
                "0.36.1",
                "0.36.0",
                "0.35.1",
                "0.35.0",
                "0.34.2",
                "0.34.1",
                "0.34.0",
                "0.33.6",
                "0.33.5",
                "0.33.4",
                "0.33.1",
                "0.33.0",
                "0.32.3",
                "0.32.2",
                "0.32.1",
                "0.32.0",
                "0.31.1",
                "0.31.0",
                "0.30.0",
                "0.30.0a0",
                "0.29.0",
                "0.28.0",
                "0.27.0",
                "0.26.0",
                "0.25.0",
                "0.24.0",
                "0.23.0",
                "0.22.0",
                "0.21.0",
                "0.19.0",
                "0.18.0",
                "0.17.0",
                "0.16.0",
                "0.15.0",
                "0.14.0",
                "0.13.0",
                "0.12.0",
                "0.11.0",
                "0.10.3",
                "0.10.2",
                "0.10.1",
                "0.10.0",
                "0.9.7",
                "0.9.6",
                "0.9.5",
                "0.9.4",
                "0.9.3",
                "0.9.2",
                "0.9.1",
                "0.9",
                "0.8",
                "0.7",
                "0.6",
                "0.5",
                "0.4.2",
                "0.4.1",
                "0.4",
                "0.3",
                "0.2",
                "0.1"
            ],
            "more_info_url": "https://data.safetycli.com/v/84961/eda"
        },
        {
            "vulnerability_id": "84031",
            "package_name": "urllib3",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                ">=1.22,<2.6.3"
            ],
            "all_vulnerable_specs": [
                ">=1.22,<2.6.3"
            ],
            "analyzed_version": "2.5.0",
            "analyzed_requirement": {
                "raw": "urllib3==2.5.0",
                "extras": [],
                "marker": null,
                "name": "urllib3",
                "specifier": "==2.5.0",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of the urllib3 package are vulnerable to Denial of Service (DoS) due to redirect handling that drains connections by decompressing redirect response bodies without enforcing streaming read limits. The issue occurs when using urllib3\u2019s streaming mode (for example, preload_content=False) while allowing redirects, because urllib3.response.HTTPResponse.drain_conn() would call HTTPResponse.read() in a way that decoded/decompressed the entire redirect response body even before any streaming reads were performed, effectively bypassing decompression-bomb safeguards.",
            "is_transitive": false,
            "published_date": "2026-Jan-08",
            "fixed_versions": [
                "2.6.3"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/84031/eda",
                "https://github.com/urllib3/urllib3/commit/8864ac407bba8607950025e0979c4c69bc7abc7b",
                "https://github.com/advisories/GHSA-38jv-5279-wg99",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-21441"
            ],
            "CVE": "CVE-2026-21441",
            "severity": null,
            "affected_versions": [
                "2.6.2",
                "2.6.1",
                "2.6.0",
                "2.5.0",
                "2.4.0",
                "2.3.0",
                "2.2.3",
                "2.2.2",
                "2.2.1",
                "2.2.0",
                "2.1.0",
                "2.0.7",
                "2.0.6",
                "2.0.5",
                "2.0.4",
                "2.0.3",
                "2.0.2",
                "2.0.1",
                "2.0.0",
                "2.0.0a4",
                "2.0.0a3",
                "2.0.0a2",
                "2.0.0a1",
                "1.26.20",
                "1.26.19",
                "1.26.18",
                "1.26.17",
                "1.26.16",
                "1.26.15",
                "1.26.14",
                "1.26.13",
                "1.26.12",
                "1.26.11",
                "1.26.10",
                "1.26.9",
                "1.26.8",
                "1.26.7",
                "1.26.6",
                "1.26.5",
                "1.26.4",
                "1.26.3",
                "1.26.2",
                "1.26.1",
                "1.26.0",
                "1.25.11",
                "1.25.10",
                "1.25.9",
                "1.25.8",
                "1.25.7",
                "1.25.6",
                "1.25.5",
                "1.25.4",
                "1.25.3",
                "1.25.2",
                "1.25.1",
                "1.25",
                "1.24.3",
                "1.24.2",
                "1.24.1",
                "1.24",
                "1.23",
                "1.22"
            ],
            "more_info_url": "https://data.safetycli.com/v/84031/eda"
        },
        {
            "vulnerability_id": "82332",
            "package_name": "urllib3",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                ">=1.0,<2.6.0"
            ],
            "all_vulnerable_specs": [
                ">=1.0,<2.6.0"
            ],
            "analyzed_version": "2.5.0",
            "analyzed_requirement": {
                "raw": "urllib3==2.5.0",
                "extras": [],
                "marker": null,
                "name": "urllib3",
                "specifier": "==2.5.0",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of the urllib3 package are vulnerable to Denial of Service (DoS) due to improper handling of highly compressed HTTP response bodies during streaming decompression. The urllib3.HTTPResponse methods stream(), read(), read1(), read_chunked(), and readinto() may fully decompress a minimal but highly compressed payload based on the Content-Encoding header into an internal buffer instead of limiting the decompressed output to the requested chunk size, causing excessive CPU usage and massive memory allocation on the client side.",
            "is_transitive": false,
            "published_date": "2025-Dec-08",
            "fixed_versions": [
                "2.6.0"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/82332/eda",
                "https://github.com/advisories/GHSA-2xpw-w6gg-jr37",
                "https://github.com/urllib3/urllib3/commit/c19571de34c47de3a766541b041637ba5f716ed7",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-66471"
            ],
            "CVE": "CVE-2025-66471",
            "severity": {
                "source": "CVE-2025-66471",
                "cvssv2": null,
                "cvssv3": {
                    "base_score": 7.5,
                    "impact_score": 3.6,
                    "base_severity": "HIGH",
                    "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"
                }
            },
            "affected_versions": [
                "2.5.0",
                "2.4.0",
                "2.3.0",
                "2.2.3",
                "2.2.2",
                "2.2.1",
                "2.2.0",
                "2.1.0",
                "2.0.7",
                "2.0.6",
                "2.0.5",
                "2.0.4",
                "2.0.3",
                "2.0.2",
                "2.0.1",
                "2.0.0",
                "2.0.0a4",
                "2.0.0a3",
                "2.0.0a2",
                "2.0.0a1",
                "1.26.20",
                "1.26.19",
                "1.26.18",
                "1.26.17",
                "1.26.16",
                "1.26.15",
                "1.26.14",
                "1.26.13",
                "1.26.12",
                "1.26.11",
                "1.26.10",
                "1.26.9",
                "1.26.8",
                "1.26.7",
                "1.26.6",
                "1.26.5",
                "1.26.4",
                "1.26.3",
                "1.26.2",
                "1.26.1",
                "1.26.0",
                "1.25.11",
                "1.25.10",
                "1.25.9",
                "1.25.8",
                "1.25.7",
                "1.25.6",
                "1.25.5",
                "1.25.4",
                "1.25.3",
                "1.25.2",
                "1.25.1",
                "1.25",
                "1.24.3",
                "1.24.2",
                "1.24.1",
                "1.24",
                "1.23",
                "1.22",
                "1.21.1",
                "1.21",
                "1.20",
                "1.19.1",
                "1.19",
                "1.18.1",
                "1.18",
                "1.17",
                "1.16",
                "1.15.1",
                "1.15",
                "1.14",
                "1.13.1",
                "1.13",
                "1.12",
                "1.11",
                "1.10.4",
                "1.10.3",
                "1.10.2",
                "1.10.1",
                "1.10",
                "1.9.1",
                "1.9",
                "1.8.3",
                "1.8.2",
                "1.8",
                "1.7.1",
                "1.7",
                "1.6",
                "1.5",
                "1.4",
                "1.3",
                "1.2.2",
                "1.2.1",
                "1.2",
                "1.1",
                "1.0.2",
                "1.0.1",
                "1.0"
            ],
            "more_info_url": "https://data.safetycli.com/v/82332/eda"
        },
        {
            "vulnerability_id": "82331",
            "package_name": "urllib3",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                ">=1.24,<2.6.0"
            ],
            "all_vulnerable_specs": [
                ">=1.24,<2.6.0"
            ],
            "analyzed_version": "2.5.0",
            "analyzed_requirement": {
                "raw": "urllib3==2.5.0",
                "extras": [],
                "marker": null,
                "name": "urllib3",
                "specifier": "==2.5.0",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of the urllib3 package are vulnerable to Denial of Service (DoS) due to allowing an unbounded number of content-encoding decompression steps for HTTP responses. The HTTPResponse content decoding pipeline in urllib3 follows the Content-Encoding header and applies each advertised compression algorithm in sequence without enforcing a maximum chain length or effective output size, so a malicious peer can send a response with a very long encoding chain that triggers excessive CPU use and massive memory allocation during decompression.",
            "is_transitive": false,
            "published_date": "2025-Dec-08",
            "fixed_versions": [
                "2.6.0"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/82331/eda",
                "https://github.com/advisories/GHSA-gm62-xv2j-4w53",
                "https://github.com/urllib3/urllib3/commit/24d7b67eac89f94e11003424bcf0d8f7b72222a8",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-66418"
            ],
            "CVE": "CVE-2025-66418",
            "severity": {
                "source": "CVE-2025-66418",
                "cvssv2": null,
                "cvssv3": {
                    "base_score": 7.5,
                    "impact_score": 3.6,
                    "base_severity": "HIGH",
                    "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"
                }
            },
            "affected_versions": [
                "2.5.0",
                "2.4.0",
                "2.3.0",
                "2.2.3",
                "2.2.2",
                "2.2.1",
                "2.2.0",
                "2.1.0",
                "2.0.7",
                "2.0.6",
                "2.0.5",
                "2.0.4",
                "2.0.3",
                "2.0.2",
                "2.0.1",
                "2.0.0",
                "2.0.0a4",
                "2.0.0a3",
                "2.0.0a2",
                "2.0.0a1",
                "1.26.20",
                "1.26.19",
                "1.26.18",
                "1.26.17",
                "1.26.16",
                "1.26.15",
                "1.26.14",
                "1.26.13",
                "1.26.12",
                "1.26.11",
                "1.26.10",
                "1.26.9",
                "1.26.8",
                "1.26.7",
                "1.26.6",
                "1.26.5",
                "1.26.4",
                "1.26.3",
                "1.26.2",
                "1.26.1",
                "1.26.0",
                "1.25.11",
                "1.25.10",
                "1.25.9",
                "1.25.8",
                "1.25.7",
                "1.25.6",
                "1.25.5",
                "1.25.4",
                "1.25.3",
                "1.25.2",
                "1.25.1",
                "1.25",
                "1.24.3",
                "1.24.2",
                "1.24.1",
                "1.24"
            ],
            "more_info_url": "https://data.safetycli.com/v/82331/eda"
        },
        {
            "vulnerability_id": "83159",
            "package_name": "marshmallow",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                ">=4.0.0,<4.1.2"
            ],
            "all_vulnerable_specs": [
                ">=3.0.0rc1,<3.26.2",
                ">=4.0.0,<4.1.2"
            ],
            "analyzed_version": "4.0.1",
            "analyzed_requirement": {
                "raw": "marshmallow==4.0.1",
                "extras": [],
                "marker": null,
                "name": "marshmallow",
                "specifier": "==4.0.1",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of the marshmallow package are vulnerable to Denial of Service (DoS) due to inefficient merging of validation error structures when deserializing collections with many=True. Specifically, Schema.load(data, many=True) can trigger repeated ErrorStore.store_error() calls that rely on marshmallow.error_store.merge_errors(), performing costly list concatenation and dictionary copying during deep merges, causing disproportionate CPU consumption for moderately sized inputs.",
            "is_transitive": false,
            "published_date": "2025-Dec-23",
            "fixed_versions": [
                "3.26.2",
                "4.1.2"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/83159/eda",
                "https://github.com/marshmallow-code/marshmallow/commit/d24a0c9df061c4daa92f71cf85aca25b83eee508",
                "https://github.com/advisories/GHSA-428g-f7cq-pgp5",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-68480"
            ],
            "CVE": "CVE-2025-68480",
            "severity": {
                "source": "CVE-2025-68480",
                "cvssv2": null,
                "cvssv3": {
                    "base_score": 7.5,
                    "impact_score": 4.7,
                    "base_severity": "HIGH",
                    "vector_string": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:N"
                }
            },
            "affected_versions": [
                "4.1.1",
                "4.1.0",
                "4.0.1",
                "4.0.0",
                "3.26.1",
                "3.26.0",
                "3.25.1",
                "3.25.0",
                "3.24.2",
                "3.24.1",
                "3.24.0",
                "3.23.3",
                "3.23.2",
                "3.23.1",
                "3.23.0",
                "3.22.0",
                "3.21.3",
                "3.21.2",
                "3.21.1",
                "3.21.0",
                "3.20.2",
                "3.20.1",
                "3.20.0",
                "3.19.0",
                "3.18.0",
                "3.17.1",
                "3.17.0",
                "3.16.0",
                "3.15.0",
                "3.14.1",
                "3.14.0",
                "3.13.0",
                "3.12.2",
                "3.12.1",
                "3.12.0",
                "3.11.1",
                "3.11.0",
                "3.10.0",
                "3.9.1",
                "3.9.0",
                "3.8.0",
                "3.7.1",
                "3.7.0",
                "3.6.1",
                "3.6.0",
                "3.5.2",
                "3.5.1",
                "3.5.0",
                "3.4.0",
                "3.3.0",
                "3.2.2",
                "3.2.1",
                "3.2.0",
                "3.1.1",
                "3.1.0",
                "3.0.5",
                "3.0.4",
                "3.0.3",
                "3.0.2",
                "3.0.1",
                "3.0.0",
                "3.0.0rc9",
                "3.0.0rc8",
                "3.0.0rc7",
                "3.0.0rc6",
                "3.0.0rc5",
                "3.0.0rc4",
                "3.0.0rc3",
                "3.0.0rc2",
                "3.0.0rc1"
            ],
            "more_info_url": "https://data.safetycli.com/v/83159/eda"
        },
        {
            "vulnerability_id": "82754",
            "package_name": "filelock",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                "<3.20.1"
            ],
            "all_vulnerable_specs": [
                "<3.20.1"
            ],
            "analyzed_version": "3.19.1",
            "analyzed_requirement": {
                "raw": "filelock==3.19.1",
                "extras": [],
                "marker": null,
                "name": "filelock",
                "specifier": "==3.19.1",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of this package are vulnerable to a TOCTOU (Time-of-Check to Time-of-Use) symlink vulnerability due to improper handling of symlinks during lock file creation. The vulnerability exists because the package does not adequately check for symlink manipulation between the time the lock file path is checked and the time it is used. An attacker can exploit this vulnerability by creating a malicious symlink, potentially leading to unauthorized access or modification of files, which could compromise the integrity and security of the system.",
            "is_transitive": false,
            "published_date": "2025-Dec-05",
            "fixed_versions": [
                "3.20.1"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/82754/eda",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-68146"
            ],
            "CVE": "CVE-2025-68146",
            "severity": {
                "source": "CVE-2025-68146",
                "cvssv2": null,
                "cvssv3": {
                    "base_score": 6.3,
                    "impact_score": 5.2,
                    "base_severity": "MEDIUM",
                    "vector_string": "CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:H/A:H"
                }
            },
            "affected_versions": [
                "3.20.0",
                "3.19.1",
                "3.18.0",
                "3.17.0",
                "3.16.1",
                "3.16.0",
                "3.15.4",
                "3.15.3",
                "3.15.2",
                "3.15.1",
                "3.15.0",
                "3.14.0",
                "3.13.4",
                "3.13.3",
                "3.13.2",
                "3.13.1",
                "3.13.0",
                "3.12.4",
                "3.12.3",
                "3.12.2",
                "3.12.1",
                "3.12.0",
                "3.11.0",
                "3.10.7",
                "3.10.6",
                "3.10.5",
                "3.10.4",
                "3.10.3",
                "3.10.2",
                "3.10.1",
                "3.10.0",
                "3.9.1",
                "3.9.0",
                "3.8.2",
                "3.8.1",
                "3.8.0",
                "3.7.1",
                "3.7.0",
                "3.6.0",
                "3.5.1",
                "3.5.0",
                "3.4.2",
                "3.4.1",
                "3.4.0",
                "3.3.2",
                "3.3.1",
                "3.3.0",
                "3.2.1",
                "3.2.0",
                "3.1.0",
                "3.0.12",
                "3.0.10",
                "3.0.9",
                "3.0.8",
                "3.0.6",
                "3.0.4",
                "3.0.3",
                "3.0.2",
                "3.0.0",
                "2.0.13",
                "2.0.12",
                "2.0.11",
                "2.0.10",
                "2.0.9",
                "2.0.8",
                "2.0.7",
                "2.0.6",
                "2.0.5",
                "2.0.4",
                "2.0.1",
                "2.0.0",
                "1.0.3",
                "1.0.2",
                "1.0.1",
                "1.0.0",
                "0.2.2",
                "0.2.1",
                "0.2.0"
            ],
            "more_info_url": "https://data.safetycli.com/v/82754/eda"
        },
        {
            "vulnerability_id": "84415",
            "package_name": "filelock",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                "<3.20.3"
            ],
            "all_vulnerable_specs": [
                "<3.20.3"
            ],
            "analyzed_version": "3.19.1",
            "analyzed_requirement": {
                "raw": "filelock==3.19.1",
                "extras": [],
                "marker": null,
                "name": "filelock",
                "specifier": "==3.19.1",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of the filelock package are vulnerable to a Time-of-Check Time-of-Use (TOCTOU) Race Condition due to a race window between a write-permission check and lock file creation that does not prevent symlink substitution. The flaw is in filelock.SoftFileLock in src/filelock/_soft.py, where _acquire() calls raise_on_not_writable_file() and then performs os.open() on the lock path, allowing the filesystem state to change between the check and the use.",
            "is_transitive": false,
            "published_date": "2026-Jan-14",
            "fixed_versions": [
                "3.20.3"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/84415/eda",
                "https://github.com/advisories/GHSA-qmgc-5h2g-mvrw",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-22701"
            ],
            "CVE": "CVE-2026-22701",
            "severity": null,
            "affected_versions": [
                "3.20.2",
                "3.20.1",
                "3.20.0",
                "3.19.1",
                "3.18.0",
                "3.17.0",
                "3.16.1",
                "3.16.0",
                "3.15.4",
                "3.15.3",
                "3.15.2",
                "3.15.1",
                "3.15.0",
                "3.14.0",
                "3.13.4",
                "3.13.3",
                "3.13.2",
                "3.13.1",
                "3.13.0",
                "3.12.4",
                "3.12.3",
                "3.12.2",
                "3.12.1",
                "3.12.0",
                "3.11.0",
                "3.10.7",
                "3.10.6",
                "3.10.5",
                "3.10.4",
                "3.10.3",
                "3.10.2",
                "3.10.1",
                "3.10.0",
                "3.9.1",
                "3.9.0",
                "3.8.2",
                "3.8.1",
                "3.8.0",
                "3.7.1",
                "3.7.0",
                "3.6.0",
                "3.5.1",
                "3.5.0",
                "3.4.2",
                "3.4.1",
                "3.4.0",
                "3.3.2",
                "3.3.1",
                "3.3.0",
                "3.2.1",
                "3.2.0",
                "3.1.0",
                "3.0.12",
                "3.0.10",
                "3.0.9",
                "3.0.8",
                "3.0.6",
                "3.0.4",
                "3.0.3",
                "3.0.2",
                "3.0.0",
                "2.0.13",
                "2.0.12",
                "2.0.11",
                "2.0.10",
                "2.0.9",
                "2.0.8",
                "2.0.7",
                "2.0.6",
                "2.0.5",
                "2.0.4",
                "2.0.1",
                "2.0.0",
                "1.0.3",
                "1.0.2",
                "1.0.1",
                "1.0.0",
                "0.2.2",
                "0.2.1",
                "0.2.0"
            ],
            "more_info_url": "https://data.safetycli.com/v/84415/eda"
        },
        {
            "vulnerability_id": "84183",
            "package_name": "filelock",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                "<3.20.3"
            ],
            "all_vulnerable_specs": [
                "<3.20.3"
            ],
            "analyzed_version": "3.19.1",
            "analyzed_requirement": {
                "raw": "filelock==3.19.1",
                "extras": [],
                "marker": null,
                "name": "filelock",
                "specifier": "==3.19.1",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of this package are vulnerable to Time-of-Check Time-of-Use (TOCTOU) Race Condition. The file locking mechanism in SoftFileLock._acquire() performs permission validation before file creation without using the O_NOFOLLOW flag, leading to a race window where attackers with local access can create symlinks that redirect lock operations to arbitrary files. An attacker can exploit this vulnerability by creating a malicious symlink during the brief window between permission check and file creation, causing the lock to operate on unintended target files and potentially enabling unauthorized access or file corruption.",
            "is_transitive": false,
            "published_date": "2026-Jan-09",
            "fixed_versions": [
                "3.20.3"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/84183/eda",
                "https://pypi.org/project/filelock",
                "https://data.safetycli.com/changelogs/filelock/"
            ],
            "CVE": null,
            "severity": null,
            "affected_versions": [
                "3.20.2",
                "3.20.1",
                "3.20.0",
                "3.19.1",
                "3.18.0",
                "3.17.0",
                "3.16.1",
                "3.16.0",
                "3.15.4",
                "3.15.3",
                "3.15.2",
                "3.15.1",
                "3.15.0",
                "3.14.0",
                "3.13.4",
                "3.13.3",
                "3.13.2",
                "3.13.1",
                "3.13.0",
                "3.12.4",
                "3.12.3",
                "3.12.2",
                "3.12.1",
                "3.12.0",
                "3.11.0",
                "3.10.7",
                "3.10.6",
                "3.10.5",
                "3.10.4",
                "3.10.3",
                "3.10.2",
                "3.10.1",
                "3.10.0",
                "3.9.1",
                "3.9.0",
                "3.8.2",
                "3.8.1",
                "3.8.0",
                "3.7.1",
                "3.7.0",
                "3.6.0",
                "3.5.1",
                "3.5.0",
                "3.4.2",
                "3.4.1",
                "3.4.0",
                "3.3.2",
                "3.3.1",
                "3.3.0",
                "3.2.1",
                "3.2.0",
                "3.1.0",
                "3.0.12",
                "3.0.10",
                "3.0.9",
                "3.0.8",
                "3.0.6",
                "3.0.4",
                "3.0.3",
                "3.0.2",
                "3.0.0",
                "2.0.13",
                "2.0.12",
                "2.0.11",
                "2.0.10",
                "2.0.9",
                "2.0.8",
                "2.0.7",
                "2.0.6",
                "2.0.5",
                "2.0.4",
                "2.0.1",
                "2.0.0",
                "1.0.3",
                "1.0.2",
                "1.0.1",
                "1.0.0",
                "0.2.2",
                "0.2.1",
                "0.2.0"
            ],
            "more_info_url": "https://data.safetycli.com/v/84183/eda"
        },
        {
            "vulnerability_id": "84339",
            "package_name": "authlib",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                "<1.6.6"
            ],
            "all_vulnerable_specs": [
                "<1.6.6"
            ],
            "analyzed_version": "1.6.4",
            "analyzed_requirement": {
                "raw": "authlib==1.6.4",
                "extras": [],
                "marker": null,
                "name": "authlib",
                "specifier": "==1.6.4",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of the Authlib package are vulnerable to Cross-Site Request Forgery (CSRF) due to cache-backed OAuth state storage not being bound to the initiating user session. In authlib/integrations/base_client/framework_integration.py, FrameworkIntegration.set_state_data stores state under a cache key like _state_{app}_{state} and FrameworkIntegration.get_state_data retrieves it without validating the caller\u2019s session, allowing authorize_access_token in authlib/integrations/flask_client/apps.py (via the oauth_token parameter) to accept a state value from a different browser session.",
            "is_transitive": false,
            "published_date": "2026-Jan-12",
            "fixed_versions": [
                "1.6.6"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/84339/eda",
                "https://github.com/advisories/GHSA-fg6f-75jq-6523",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-68158"
            ],
            "CVE": "CVE-2025-68158",
            "severity": null,
            "affected_versions": [
                "1.6.5",
                "1.6.4",
                "1.6.3",
                "1.6.2",
                "1.6.1",
                "1.6.0",
                "1.5.2",
                "1.5.1",
                "1.5.0",
                "1.4.1",
                "1.4.0",
                "1.3.2",
                "1.3.1",
                "1.3.0",
                "1.2.1",
                "1.2.0",
                "1.1.0",
                "1.0.1",
                "1.0.0",
                "1.0.0rc1",
                "1.0.0b2",
                "1.0.0b1",
                "1.0.0a2",
                "1.0.0a1",
                "0.15.6",
                "0.15.5",
                "0.15.4",
                "0.15.3",
                "0.15.2",
                "0.15.1",
                "0.15",
                "0.14.3",
                "0.14.2",
                "0.14.1",
                "0.14",
                "0.13",
                "0.12.1",
                "0.12",
                "0.11",
                "0.10",
                "0.9",
                "0.8",
                "0.7",
                "0.6",
                "0.5.1",
                "0.5",
                "0.4.1",
                "0.4",
                "0.3",
                "0.2.1",
                "0.2",
                "0.1",
                "0.1rc0"
            ],
            "more_info_url": "https://data.safetycli.com/v/84339/eda"
        },
        {
            "vulnerability_id": "81132",
            "package_name": "authlib",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                "<1.6.5"
            ],
            "all_vulnerable_specs": [
                "<1.6.5"
            ],
            "analyzed_version": "1.6.4",
            "analyzed_requirement": {
                "raw": "authlib==1.6.4",
                "extras": [],
                "marker": null,
                "name": "authlib",
                "specifier": "==1.6.4",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions (< 1.6.5) of the Authlib package are vulnerable to Denial of Service (DoS) due to unbounded DEFLATE decompression in JWE zip=DEF handling. In the JOSE implementation, the JWE decode path (authlib/jose/rfc7516/jwe.py) passes decryptable ciphertexts with zip=DEF to DeflateZipAlgorithm.decompress in authlib/jose/rfc7518/jwe_zips.py, which calls zlib.decompress without an output size limit, allowing tiny inputs to expand massively.",
            "is_transitive": false,
            "published_date": "2025-Nov-03",
            "fixed_versions": [
                "1.6.5"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/81132/eda",
                "https://github.com/advisories/GHSA-g7f3-828f-7h7m",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-62706"
            ],
            "CVE": "CVE-2025-62706",
            "severity": {
                "source": "CVE-2025-62706",
                "cvssv2": null,
                "cvssv3": {
                    "base_score": 6.5,
                    "impact_score": 3.4,
                    "base_severity": "MEDIUM",
                    "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:L"
                }
            },
            "affected_versions": [
                "1.6.4",
                "1.6.3",
                "1.6.2",
                "1.6.1",
                "1.6.0",
                "1.5.2",
                "1.5.1",
                "1.5.0",
                "1.4.1",
                "1.4.0",
                "1.3.2",
                "1.3.1",
                "1.3.0",
                "1.2.1",
                "1.2.0",
                "1.1.0",
                "1.0.1",
                "1.0.0",
                "1.0.0rc1",
                "1.0.0b2",
                "1.0.0b1",
                "1.0.0a2",
                "1.0.0a1",
                "0.15.6",
                "0.15.5",
                "0.15.4",
                "0.15.3",
                "0.15.2",
                "0.15.1",
                "0.15",
                "0.14.3",
                "0.14.2",
                "0.14.1",
                "0.14",
                "0.13",
                "0.12.1",
                "0.12",
                "0.11",
                "0.10",
                "0.9",
                "0.8",
                "0.7",
                "0.6",
                "0.5.1",
                "0.5",
                "0.4.1",
                "0.4",
                "0.3",
                "0.2.1",
                "0.2",
                "0.1",
                "0.1rc0"
            ],
            "more_info_url": "https://data.safetycli.com/v/81132/eda"
        },
        {
            "vulnerability_id": "80401",
            "package_name": "authlib",
            "ignored": {},
            "ignored_reason": null,
            "ignored_expires": null,
            "vulnerable_spec": [
                "<1.6.5"
            ],
            "all_vulnerable_specs": [
                "<1.6.5"
            ],
            "analyzed_version": "1.6.4",
            "analyzed_requirement": {
                "raw": "authlib==1.6.4",
                "extras": [],
                "marker": null,
                "name": "authlib",
                "specifier": "==1.6.4",
                "url": null,
                "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
            },
            "advisory": "Affected versions of the Authlib package are vulnerable to Denial of Service due to unbounded JOSE (JWS/JWT) segment sizes. The vulnerability occurs because Authlib\u2019s util.extract_segment (for the header) and _extract_signature (for the signature) accept base64url-encoded data of arbitrary size and then fully decode and parse it without early limits.",
            "is_transitive": false,
            "published_date": "2025-Oct-13",
            "fixed_versions": [
                "1.6.5"
            ],
            "closest_versions_without_known_vulnerabilities": [],
            "resources": [
                "https://pyup.io/v/80401/eda",
                "https://github.com/authlib/authlib/commit/867e3f87b072347a1ae9cf6983cc8bbf88447e5e",
                "https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-61920"
            ],
            "CVE": "CVE-2025-61920",
            "severity": {
                "source": "CVE-2025-61920",
                "cvssv2": null,
                "cvssv3": {
                    "base_score": 7.5,
                    "impact_score": 3.6,
                    "base_severity": "HIGH",
                    "vector_string": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"
                }
            },
            "affected_versions": [
                "1.6.4",
                "1.6.3",
                "1.6.2",
                "1.6.1",
                "1.6.0",
                "1.5.2",
                "1.5.1",
                "1.5.0",
                "1.4.1",
                "1.4.0",
                "1.3.2",
                "1.3.1",
                "1.3.0",
                "1.2.1",
                "1.2.0",
                "1.1.0",
                "1.0.1",
                "1.0.0",
                "1.0.0rc1",
                "1.0.0b2",
                "1.0.0b1",
                "1.0.0a2",
                "1.0.0a1",
                "0.15.6",
                "0.15.5",
                "0.15.4",
                "0.15.3",
                "0.15.2",
                "0.15.1",
                "0.15",
                "0.14.3",
                "0.14.2",
                "0.14.1",
                "0.14",
                "0.13",
                "0.12.1",
                "0.12",
                "0.11",
                "0.10",
                "0.9",
                "0.8",
                "0.7",
                "0.6",
                "0.5.1",
                "0.5",
                "0.4.1",
                "0.4",
                "0.3",
                "0.2.1",
                "0.2",
                "0.1",
                "0.1rc0"
            ],
            "more_info_url": "https://data.safetycli.com/v/80401/eda"
        }
    ],
    "ignored_vulnerabilities": [],
    "remediations": {
        "wheel": {
            "requirements": {
                "==0.45.1": {
                    "vulnerabilities_found": 1,
                    "version": "0.45.1",
                    "requirement": {
                        "raw": "wheel==0.45.1",
                        "extras": [],
                        "marker": null,
                        "name": "wheel",
                        "specifier": "==0.45.1",
                        "url": null,
                        "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages/setuptools/_vendor"
                    },
                    "more_info_url": "https://data.safetycli.com/p/pypi/wheel/eda/?from=0.45.1&to=0.46.2",
                    "closest_secure_version": {
                        "upper": "0.46.2",
                        "lower": null
                    },
                    "recommended_version": "0.46.2",
                    "other_recommended_versions": [
                        "0.46.3"
                    ]
                }
            },
            "current_version": null,
            "vulnerabilities_found": null,
            "recommended_version": null,
            "other_recommended_versions": [],
            "more_info_url": null
        },
        "urllib3": {
            "requirements": {
                "==2.5.0": {
                    "vulnerabilities_found": 3,
                    "version": "2.5.0",
                    "requirement": {
                        "raw": "urllib3==2.5.0",
                        "extras": [],
                        "marker": null,
                        "name": "urllib3",
                        "specifier": "==2.5.0",
                        "url": null,
                        "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                    },
                    "more_info_url": "https://data.safetycli.com/p/pypi/urllib3/eda/?from=2.5.0&to=2.6.3",
                    "closest_secure_version": {
                        "upper": "2.6.3",
                        "lower": null
                    },
                    "recommended_version": "2.6.3",
                    "other_recommended_versions": []
                }
            },
            "current_version": null,
            "vulnerabilities_found": null,
            "recommended_version": null,
            "other_recommended_versions": [],
            "more_info_url": null
        },
        "marshmallow": {
            "requirements": {
                "==4.0.1": {
                    "vulnerabilities_found": 1,
                    "version": "4.0.1",
                    "requirement": {
                        "raw": "marshmallow==4.0.1",
                        "extras": [],
                        "marker": null,
                        "name": "marshmallow",
                        "specifier": "==4.0.1",
                        "url": null,
                        "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                    },
                    "more_info_url": "https://data.safetycli.com/p/pypi/marshmallow/eda/?from=4.0.1&to=4.1.2",
                    "closest_secure_version": {
                        "upper": "4.1.2",
                        "lower": "3.26.2"
                    },
                    "recommended_version": "4.1.2",
                    "other_recommended_versions": [
                        "4.2.1",
                        "4.2.0",
                        "3.26.2",
                        "3.0.0b20",
                        "3.0.0b19",
                        "3.0.0b18",
                        "3.0.0b17",
                        "3.0.0b16",
                        "3.0.0b15",
                        "3.0.0b14",
                        "3.0.0b13",
                        "3.0.0b12",
                        "3.0.0b11",
                        "3.0.0b10",
                        "3.0.0b9",
                        "2.21.0",
                        "2.20.5",
                        "2.20.4",
                        "2.20.3",
                        "2.20.2",
                        "2.20.1",
                        "2.20.0",
                        "2.19.5",
                        "2.19.4",
                        "2.19.3",
                        "2.19.2",
                        "2.19.1",
                        "2.19.0",
                        "2.18.1",
                        "2.18.0",
                        "2.17.0",
                        "2.16.3",
                        "2.16.2",
                        "2.16.1",
                        "2.16.0",
                        "2.15.6",
                        "2.15.5",
                        "2.15.4",
                        "2.15.3",
                        "2.15.2",
                        "2.15.1"
                    ]
                }
            },
            "current_version": null,
            "vulnerabilities_found": null,
            "recommended_version": null,
            "other_recommended_versions": [],
            "more_info_url": null
        },
        "filelock": {
            "requirements": {
                "==3.19.1": {
                    "vulnerabilities_found": 3,
                    "version": "3.19.1",
                    "requirement": {
                        "raw": "filelock==3.19.1",
                        "extras": [],
                        "marker": null,
                        "name": "filelock",
                        "specifier": "==3.19.1",
                        "url": null,
                        "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                    },
                    "more_info_url": "https://data.safetycli.com/p/pypi/filelock/eda/?from=3.19.1&to=3.20.3",
                    "closest_secure_version": {
                        "upper": "3.20.3",
                        "lower": null
                    },
                    "recommended_version": "3.20.3",
                    "other_recommended_versions": []
                }
            },
            "current_version": null,
            "vulnerabilities_found": null,
            "recommended_version": null,
            "other_recommended_versions": [],
            "more_info_url": null
        },
        "authlib": {
            "requirements": {
                "==1.6.4": {
                    "vulnerabilities_found": 3,
                    "version": "1.6.4",
                    "requirement": {
                        "raw": "authlib==1.6.4",
                        "extras": [],
                        "marker": null,
                        "name": "authlib",
                        "specifier": "==1.6.4",
                        "url": null,
                        "found": "/Users/martin/.local/pipx/venvs/safety/lib/python3.13/site-packages"
                    },
                    "more_info_url": "https://data.safetycli.com/p/pypi/authlib/eda/?from=1.6.4&to=1.6.6",
                    "closest_secure_version": {
                        "upper": "1.6.6",
                        "lower": null
                    },
                    "recommended_version": "1.6.6",
                    "other_recommended_versions": []
                }
            },
            "current_version": null,
            "vulnerabilities_found": null,
            "recommended_version": null,
            "other_recommended_versions": [],
            "more_info_url": null
        }
    },
    "remediations_results": {
        "vulnerabilities_fixed": [],
        "remediations_applied": {},
        "remediations_skipped": {}
    }
}


+===========================================================================================================================================================================================+


DEPRECATED: this command (`check`) has been DEPRECATED, and will be unsupported beyond 01 June 2024.


We highly encourage switching to the new `scan` command which is easier to use, more powerful, and can be set up to mimic the deprecated command if required.


+===========================================================================================================================================================================================+
```

## Recommended Actions

1. Review the vulnerabilities listed above
2. Update affected packages to the recommended versions
3. Test the application after updates
4. Consider adding version pinning for critical dependencies

## Next Steps

- [ ] Review each vulnerability
- [ ] Test application functionality
- [ ] Update any additional dependencies if needed
- [ ] Merge this PR after review
