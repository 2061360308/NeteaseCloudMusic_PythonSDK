import os
import subprocess

# Bump version
subprocess.check_call(['bumpversion', 'patch'])

# Push changes to remote
subprocess.check_call(['git', 'push'])
subprocess.check_call(['git', 'push', '--tags'])

# Run towncrier
subprocess.check_call(['towncrier', '--yes'])