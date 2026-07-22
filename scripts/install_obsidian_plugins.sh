#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLUGIN_DIR="${ROOT_DIR}/.obsidian/plugins"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

download_file() {
  local url="$1"
  local expected="$2"
  local output="$3"

  curl --fail --location --silent --show-error "${url}" --output "${output}"

  local actual
  actual="$(shasum -a 256 "${output}" | awk '{print $1}')"
  if [[ "${actual}" != "${expected}" ]]; then
    echo "Checksum mismatch for ${url}" >&2
    echo "Expected: ${expected}" >&2
    echo "Actual:   ${actual}" >&2
    exit 1
  fi
}

install_plugin() {
  local plugin_id="$1"
  local base_url="$2"
  local main_hash="$3"
  local manifest_hash="$4"
  local styles_hash="$5"
  local stage="${TMP_DIR}/${plugin_id}"
  local target="${PLUGIN_DIR}/${plugin_id}"

  mkdir -p "${stage}" "${target}"
  download_file "${base_url}/main.js" "${main_hash}" "${stage}/main.js"
  download_file "${base_url}/manifest.json" "${manifest_hash}" "${stage}/manifest.json"
  download_file "${base_url}/styles.css" "${styles_hash}" "${stage}/styles.css"

  install -m 0644 "${stage}/main.js" "${target}/main.js"
  install -m 0644 "${stage}/manifest.json" "${target}/manifest.json"
  install -m 0644 "${stage}/styles.css" "${target}/styles.css"
  echo "Installed ${plugin_id}"
}

install_plugin \
  "obsidian-tasks-plugin" \
  "https://github.com/obsidian-tasks-group/obsidian-tasks/releases/download/8.2.2" \
  "5c68dd0f4e1838f3bd263df39aa508d66ed94e85cc4a48bb338170be2955e077" \
  "db6fe0eb4f033955cdae3e545a39f69748c87262ea8b352805662c4ccbcb714b" \
  "32b3d394b697a058f2dcaef0d38476b3c3e585aea63549a816bcc237cf3e3872"

install_plugin \
  "quickadd" \
  "https://github.com/chhoumann/quickadd/releases/download/2.12.3" \
  "a0c59ebed18ab870e7b9dc5f70b84e5730bb15116dba673c8fd6ce90f0aeaf90" \
  "60625157623a60e143aa26ab1823fd10e2361d12b2eb946792a555839231e7d5" \
  "7198c40b23c4b1ba825156f376855e6122ed8a7f8792e6bd813ebb86534e133e"

install_plugin \
  "obsidian-kanban" \
  "https://github.com/obsidian-community/obsidian-kanban/releases/download/2.0.51" \
  "a7e3bd4cf25f9b7f53a841c44ce990db0ef5f7954ebcab17ae6dca80310c39ac" \
  "24976787097ead467969e014a35654e7a80e4db49a977689a48afadfa15e1854" \
  "ecf6dd31f1727c441cce6f54794b0d3916dcfffc87fa17b855c79ba04a85d9a7"

echo "Obsidian plugins installed and verified."
