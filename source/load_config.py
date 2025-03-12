# *---------------------------------------------------------------------------------------------
# *  Copyright (c). All rights reserved.
# *  Licensed under the LICENSE-APACHE. See License.txt in the project root for license information.
# *--------------------------------------------------------------------------------------------*


import os
import json

from config import CONFIG_FILE


def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as file:
            json.dump(
                {
                    "version": "0.0.1",
                    "analysis": {
                        "refactor": True,
                        "security": False,
                        "viewTree": False,
                    },
                    "ignore": ["packages", "venv", ".git", "__pycache__", ".husky"],
                },
                file,
                indent=4,
            )

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
