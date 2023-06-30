"""
webhook.py

An ansible-rulebook event source module for receiving logicmonitor alerts via a webhook.

Arguments:
    host: The hostname to listen to. Set to 0.0.0.0 to listen on all
          interfaces. Defaults to 127.0.0.1
    port: The TCP port to listen to.  Defaults to 5000
    vault_pass: vault password which was used during encryption
    Vault_path: path to vault file containing ansible_token generated in logicmonitor

Usage in a rulebook:
- name: collector down mitigation
  hosts: localhost
  sources:
    - logicmonitor.integration.webhook:
        hosts: 127.0.0.1
        port: 5000
        vault_pass: '{{vault_pass}}'
        vault_path: '{{vault_path}}'
  rules:
    - name: start collector
      condition: event.payload.type == "agentDownAlert"
      action:
        run_playbook:
          name: logicmonitor.integration.start_lm-collector
"""

import asyncio
import sys
import yaml
import logging

from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import VaultLib, VaultSecret
from typing import Any, Dict
from aiohttp import web

routes = web.RouteTableDef()

ANSIBLE_TOKEN = "ansible_token"
_token = None

logger = logging.getLogger("logicmonitor.integration.webhook")


@routes.post(r"/{endpoint:.*}")
async def webhook(request: web.Request):
    payload = await request.json()
    endpoint = request.match_info["endpoint"]

    headers = dict(map(lambda kv: (kv[0].lower(), kv[1]), request.headers.items()))

    header_token = headers.pop(ANSIBLE_TOKEN, None)
    if not header_token:
        logger.warning("Ansible token not provided")
        return web.Response(status=403, text="Unauthorized! Token not provided")
    data = {
        "payload": payload,
        "meta": {"endpoint": endpoint, "headers": headers},
    }

    if header_token == _token:
        auth_message = "Request authenticated! Alert: type=%s, status=%s, host=%s"
        logger.info(auth_message, payload.get("type"), payload.get("status"), payload.get("host"))
        await request.app["queue"].put(data)  # adding data to queue
        return web.Response(text="success")
    logger.warning("Unauthorised Request! wrong %s provided.", ANSIBLE_TOKEN)
    return web.Response(status=403, text="Unauthorized! Wrong token provided")


async def main(queue: asyncio.Queue, args: Dict[str, Any]):
    logger.info("Starting webhook")

    vault_path = args.get("vault_path")
    vault_pass = args.get("vault_pass")
    if not vault_pass:
        logger.error("vault_pass is required")
        raise ValueError("Missing required argument: vault_pass")
    if not vault_path:
        logger.error("vault_path is required")
        raise ValueError("Missing required argument: vault_path")

    try:
        # init vaultlib
        logger.info("Reading vault content")
        vault = VaultLib([(DEFAULT_VAULT_ID_MATCH, VaultSecret(vault_pass.encode()))])
        vault_dict = yaml.safe_load(vault.decrypt(open(vault_path).read()))
        logger.info("Successfully read vault content")
    except FileNotFoundError:
        logger.error("File %s doesn't exist!!!", vault_path)
        raise
    except Exception:
        logger.exception("Error decrypting and reading vault content. Please check vault password and vault content.")
        raise

    global _token
    _token = vault_dict.get(ANSIBLE_TOKEN)
    if not _token:
        logger.error("Vault doesn't have the required variable: %s", ANSIBLE_TOKEN)
        raise ValueError("Vault doesn't have the required variable: " + ANSIBLE_TOKEN)

    app = web.Application()
    app["queue"] = queue

    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner, args.get("host") or "localhost", args.get("port") or 5000
    )
    await site.start()

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.error("Plugin Task Cancelled")
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    class MockQueue:
        async def put(self, event):
            logger.info(event)

    args = {"host": "127.0.0.1", "port": 5000, "vault_pass": "secret", "vault_path": "path"}

    asyncio.run(main(MockQueue(), args))
