#!/usr/bin/env python3
"""Minimal YouQuant extension API helper bundled with the skill."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


API_BASE = "https://www.youquant.com/api/v1"


def get_credentials(args: argparse.Namespace) -> tuple[str, str]:
    access_key = args.access_key or os.environ.get("YOUQUANT_ACCESS_KEY")
    secret_key = args.secret_key or os.environ.get("YOUQUANT_SECRET_KEY")
    if not access_key or not secret_key:
        raise SystemExit(
            "Missing credentials. Set YOUQUANT_ACCESS_KEY / YOUQUANT_SECRET_KEY "
            "or pass --access-key / --secret-key."
        )
    return access_key, secret_key


def call_api(access_key: str, secret_key: str, method: str, api_args: list) -> dict:
    query = urllib.parse.urlencode(
        {
            "access_key": access_key,
            "secret_key": secret_key,
            "method": method,
            "args": json.dumps(api_args, ensure_ascii=False),
        }
    )
    req = urllib.request.Request(
        f"{API_BASE}?{query}",
        headers={"User-Agent": "codex-youquant-skill/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def cmd_call(args: argparse.Namespace) -> int:
    access_key, secret_key = get_credentials(args)
    result = call_api(access_key, secret_key, args.method, json.loads(args.args_json))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_list_strategies(args: argparse.Namespace) -> int:
    access_key, secret_key = get_credentials(args)
    result = call_api(access_key, secret_key, "GetStrategyList", [])
    strategies = (((result.get("data") or {}).get("result") or {}).get("strategies") or [])
    if args.name:
        strategies = [item for item in strategies if args.name in item.get("name", "")]
    print(json.dumps(strategies, ensure_ascii=False, indent=2))
    return 0


def cmd_list_robots(args: argparse.Namespace) -> int:
    access_key, secret_key = get_credentials(args)
    result = call_api(access_key, secret_key, "GetRobotList", [])
    robots = (((result.get("data") or {}).get("result") or {}).get("robots") or [])
    print(json.dumps(robots, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="YouQuant extension API helper")
    parser.add_argument("--access-key")
    parser.add_argument("--secret-key")

    sub = parser.add_subparsers(dest="command", required=True)

    call_parser = sub.add_parser("call", help="Call a raw API method")
    call_parser.add_argument("method")
    call_parser.add_argument("args_json", nargs="?", default="[]")
    call_parser.set_defaults(func=cmd_call)

    strategies_parser = sub.add_parser("list-strategies", help="List strategies")
    strategies_parser.add_argument("--name")
    strategies_parser.set_defaults(func=cmd_list_strategies)

    robots_parser = sub.add_parser("list-robots", help="List robots")
    robots_parser.set_defaults(func=cmd_list_robots)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
