#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration file with embedded secrets for testing secret detection.
"""

# API key - should be detected
API_KEY = "sk-1234567890abcdef1234567890abcdef"

# AWS credentials - should be detected
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Database password - should be detected
DB_PASSWORD = "MyS3cr3tP@ssw0rd!"

# GitHub token - should be detected
GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz12"

# Normal configuration (non-secret)
DEBUG = True
TIMEOUT = 30
MAX_RETRIES = 3
