#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional


@dataclass
class FixPlan:
    key: str
    title: str
    description: str
    files_touched: List[str]
    apply_fn: Optional[Callable[[], bool]] = None  # returns True if applied


def _read(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def fix_failed_parse_url_from_api_plan() -> FixPlan:
    key = "next_failed_parse_url"
    title = "Next.js: 相対URL fetch を絶対URL化"
    description = (
        "Failed to parse URL from /api... に対する修正。apps/web/lib/url.ts を作成し、"
        "SSR/RSC からの fetch に絶対URLを渡すユーティリティを提供します。"
    )
    files = [
        "apps/web/lib/url.ts",
    ]

    def apply() -> bool:
        changed = False
        url_path = "apps/web/lib/url.ts"
        if not os.path.exists(url_path):
            content = (
                "import { headers } from 'next/headers'\n\n"
                "function isAbsoluteUrl(u: string | undefined): u is string {\n"
                "  return !!u && /^https?:\\/\\//i.test(u)\n"
                "}\n\n"
                "export async function siteBaseUrl(): Promise<string> {\n"
                "  const fromEnv = process.env.NEXT_PUBLIC_SITE_URL\n"
                "  if (isAbsoluteUrl(fromEnv)) return fromEnv!\n"
                "  try {\n"
                "    const h = await headers()\n"
                "    const proto = h.get('x-forwarded-proto') ?? 'http'\n"
                "    const host = h.get('x-forwarded-host') ?? h.get('host')\n"
                "    if (host) return `${proto}://${host}`\n"
                "  } catch {}\n"
                "  return 'http://localhost:3000'\n"
                "}\n\n"
                "export async function absolute(path: string): Promise<string> {\n"
                "  const base = await siteBaseUrl()\n"
                "  return `${base.replace(/\\/$/, '')}/${path.replace(/^\\//, '')}`\n"
                "}\n"
            )
            _write(url_path, content)
            changed = True
        return changed

    return FixPlan(key=key, title=title, description=description, files_touched=files, apply_fn=apply)


def fix_register_idempotent_plan() -> FixPlan:
    key = "auth_register_idempotent"
    title = "FastAPI: /auth/register を冪等化"
    description = "Email already registered ログに対し、既存メール時は 200 で {id} を返却する修正。"
    path = "python-api/app/routers/auth.py"

    def apply() -> bool:
        src = _read(path)
        if not src:
            return False
        if "return {\"id\": exists.id}" in src:
            return False  # already fixed
        target = (
            'if exists:\n'
            '        raise HTTPException(status_code=400, detail="Email already registered")'
        )
        if target not in src:
            return False
        patched = src.replace(
            target,
            'if exists:\n        return {"id": exists.id}'
        )
        _write(path, patched)
        return True

    return FixPlan(
        key=key,
        title=title,
        description=description,
        files_touched=[path],
        apply_fn=apply,
    )


RULES: list[tuple[re.Pattern[str], Callable[[], FixPlan]]] = [
    (re.compile(r"Failed to parse URL from /api"), fix_failed_parse_url_from_api_plan),
    (re.compile(r"Email already registered|Unique constraint.*users.*email", re.I), fix_register_idempotent_plan),
]


def make_plans_from_log(text: str) -> list[FixPlan]:
    plans: list[FixPlan] = []
    for pat, factory in RULES:
        if pat.search(text):
            plans.append(factory())
    return plans


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Parse Docker logs and propose/apply fixes")
    p.add_argument("--from-file", dest="from_file", help="log file path; default: stdin", default=None)
    p.add_argument("--apply", action="store_true", help="apply fixes instead of just planning")
    args = p.parse_args(list(argv) if argv is not None else None)

    if args.from_file:
        text = _read(args.from_file)
    else:
        text = sys.stdin.read()
    if not text:
        print("[auto-fix] no log input", file=sys.stderr)
        return 1

    plans = make_plans_from_log(text)
    if not plans:
        print("[auto-fix] no known issues detected.")
        return 0

    print("[auto-fix] detected issues and plans:\n")
    for i, pl in enumerate(plans, 1):
        print(f"{i}. {pl.title} ({pl.key})")
        print(f"   - files: {', '.join(pl.files_touched)}")
        print(f"   - desc : {pl.description}")

    if not args.apply:
        print("\n[auto-fix] run with --apply to modify files.")
        return 0

    print("\n[auto-fix] applying fixes...")
    applied_any = False
    for pl in plans:
        ok = False
        if pl.apply_fn:
            try:
                ok = pl.apply_fn()
            except Exception as e:
                print(f" - {pl.key}: failed to apply: {e}")
        print(f" - {pl.key}: {'applied' if ok else 'skipped'}")
        applied_any = applied_any or ok

    print("[auto-fix] done.")
    return 0 if applied_any else 2


if __name__ == "__main__":
    raise SystemExit(main())
