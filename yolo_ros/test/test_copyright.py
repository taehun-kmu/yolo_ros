# Copyright 2015 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adjusted to recognize GPL headers with (C) or (c).

import re
from pathlib import Path

import pytest


def _extract_leading_comment_block(text: str) -> str:
    lines = text.splitlines()
    # Skip shebang / coding declarations
    i = 0
    while i < len(lines) and (
        lines[i].startswith("#!/") or
        lines[i].lstrip().startswith("# -*- coding")
    ):
        i += 1
    # Collect leading comment lines (allow blank lines between)
    block_lines = []
    while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith('#')):
        block_lines.append(lines[i])
        i += 1
    return "\n".join(block_lines)


def _has_gpl_header(comment_block: str) -> bool:
    # Accept both (C) and (c) and optional comma after year(s)
    copyright_re = re.compile(
        r"^\s*#\s*Copyright(?:\s+\((?:C|c)\))?\s+\d{4}(?:[-,]\s*\d{4})*\s+.+$",
        re.MULTILINE,
    )
    required_phrases = [
        "This program is free software",
        "GNU General Public License",
        "You should have received a copy of the GNU General Public License",
    ]
    if not copyright_re.search(comment_block):
        return False
    return all(phrase in comment_block for phrase in required_phrases)


@pytest.mark.linter
def test_gpl_headers_present():
    pkg_root = Path(__file__).resolve().parents[1]
    src_dir = pkg_root / "yolo_ros"
    py_files = [f for f in sorted(src_dir.glob("*.py")) if f.name != "__init__.py"]

    missing = []
    for f in py_files:
        text = f.read_text(encoding="utf-8")
        comment_block = _extract_leading_comment_block(text)
        if not _has_gpl_header(comment_block):
            missing.append(str(f.relative_to(pkg_root)))

    assert not missing, (
        "Missing or unrecognized GPL headers in files: " + ", ".join(missing)
    )
