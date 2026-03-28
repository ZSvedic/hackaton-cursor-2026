#!/usr/bin/env bash
# #Human
usage() {
  echo "  Usage: stirr-check.sh <codex|claude> PATH1 [PATH2 ...]\n"
  echo "  - Calls \`stirr-tree.py\` on provided paths, pipes output to a string."
  echo "  - Constructs a validation prompt, including the tree output."
  echo "  - Calls either Codex or Claude with a given prompt, no tools allowed."
  exit 1
}

set -euo pipefail

[ "$#" -ge 2 ] || usage

AGENT="$1"
shift
PATHS=("$@")

TREE_OUTPUT=$($(dirname "$0")/stirr-tree.py "${PATHS[@]}")

RULES="$(< "$(dirname "$0")/../stirr-skill/SKILL.md")"

PROMPT=$(cat <<EOF
You are a project compliance checker that: 
- Can read and search files in the project paths. 
- Can read test logs. 
- Can\'t modify files, execute tests or code, or access files outside the project paths. 
Below are the STIRR rules and the CLI output of stirr-tree.py for the specified paths. 
Check if the code structure and files comply with the STIRR rules. 
You should output pure text for console, no Markdown. 
Answer within 45 seconds (e.g. use \`date\` at the start). 

=== STIRR rules (from SKILL.md):
\`\`\`md
$RULES
\`\`\`

=== PATHS:
${PATHS[*]}

=== stirr-tree.py output: 
\`\`\`console
$TREE_OUTPUT
\`\`\`
EOF
)

case "$AGENT" in
  codex)
    echo "Running Codex..."
    codex -a never -s workspace-write exec "$PROMPT" \
      2>&1 | awk '/^=== PATHS:/,0' # Codex is a bit verbose, display only after path part.
    ;;
  claude)
    echo "Running Claude..."
    claude -p "$PROMPT" 
    ;;
  *)
    usage
    ;;
esac