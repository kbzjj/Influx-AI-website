#!/bin/sh
PATH='/Users/gztd-03-02687/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin':"$PATH"
export PATH
exec /Users/gztd-03-02687/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/pnpm dlx vercel@65.2.0 "$@"
