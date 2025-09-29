"""webhook.py.

An ansible-rulebook event source module for receiving logicmonitor alerts via a webhook.

Arguments:
---------
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
from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any

import aiofiles
import yaml
from aiohttp import web
from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import VaultLib, VaultSecret

MISSING_VAULT_ARGUMENT_PATH = "Missing required argument: vault_path"

MISSING_VAULT_ARGUMENT_PASS = "Missing required argument: vault_pass"  # noqa: S105

routes = web.RouteTableDef()

ANSIBLE_KEY = "ansible_token"

logger = logging.getLogger("logicmonitor.integration.webhook")


@routes.post(r"/{endpoint:.*}")
async def webhook(request: web.Request) -> web.Response:
    """Webhook endpoint route.

    Parameters
    ----------
    request : web.Request
        incoming web request

    Returns
    -------
    web.Request
        contains status code and message

    """
    payload = await request.json()
    endpoint = request.match_info["endpoint"]

    headers = {k.lower(): v for (k, v) in request.headers.items()}

    header_token = headers.pop(ANSIBLE_KEY, None)
    if not header_token:
        logger.warning("Ansible token not provided")
        return web.Response(status=403, text="Unauthorized! Token not provided")
    data = {
        "payload": payload,
        "meta": {"endpoint": endpoint, "headers": headers},
    }

    if header_token == request.app["token"]:
        auth_message = "Request authenticated! Alert: type=%s, status=%s, host=%s"
        logger.info(auth_message, payload.get("type"),
                    payload.get("status"), payload.get("host"))
        await request.app["queue"].put(data)  # adding data to queue
        return web.Response(text="success")
    logger.warning("Unauthorised Request! wrong %s provided.", ANSIBLE_KEY)
    return web.Response(status=403, text="Unauthorized! Wrong token provided")


async def main(queue: asyncio.Queue, args: dict[str, Any]) -> None:
    """Initialise the event source.

    Parameters
    ----------
    queue : asyncio.Queue
        event queue
    args : dict
        dictionary object containing arguments from rulebook

    Raises
    ------
    Exception
        If not able to read vault content
    FileNotFoundError
        If the vault file is missing
    ValueError
        If vault_path or vault_pass are missing

    """
    logger.info("Starting webhook")

    vault_path = args.get("vault_path")
    vault_pass = args.get("vault_pass")
    if not vault_pass:
        logger.error("vault_pass is required")
        raise ValueError(MISSING_VAULT_ARGUMENT_PASS)
    if not vault_path:
        logger.error("vault_path is required")
        raise ValueError(MISSING_VAULT_ARGUMENT_PATH)

    try:
        # init vaultlib
        logger.info("Reading vault content")
        vault = VaultLib([(DEFAULT_VAULT_ID_MATCH, VaultSecret(vault_pass.encode()))])
        async with aiofiles.open(vault_path, encoding="utf-8") as vault_file:
            vault_content = await vault_file.read()
            vault_dict = yaml.safe_load(vault.decrypt(vault_content))
        logger.info("Successfully read vault content")
    except FileNotFoundError:
        logger.exception("File %s doesn't exist!!!", vault_path)
        raise
    except Exception:
        logger.exception("Error decrypting and reading vault content. "
                         "Please check vault password and vault content.")
        raise

    token = vault_dict.get(ANSIBLE_KEY)
    if not token:
        logger.error("Vault doesn't have the required variable: %s", ANSIBLE_KEY)
        raise ValueError("Vault doesn't have the required variable: " + ANSIBLE_KEY)

    app = web.Application()
    app["queue"] = queue
    app["token"] = token

    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner, args.get("host") or "localhost", args.get("port") or 5000,
    )
    await site.start()

    try:
        await asyncio.Future()
    except asyncio.CancelledError:
        logger.exception("Plugin Task Cancelled")
    finally:
        await runner.cleanup()


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    class MockQueue:  # pylint: disable=R0903
        """A fake queue."""

        async def put(self: MockQueue, event: dict[str, Any]) -> None:
            """Print the event.

            Parameters
            ----------
            event : dict
                event details

            """
            logger.info(event)

    params = {"host": "127.0.0.1", "port": 5000,
              "vault_pass": "secret", "vault_path": "path"}

    asyncio.run(main(MockQueue(), params))
