import asyncio
import io
import json
import aiohttp
import pytest

from extensions.eda.plugins.event_source.webhook import main as webhook_main


async def start_server(queue, args):
    await webhook_main(queue, args)


async def post_code(server_task, info):
    url = f'http://{info["host"]}/{info["endpoint"]}'
    payload = info["payload"]

    async with aiohttp.ClientSession() as session:
        headers = {"ansible_token": info["ansible_token"]}
        async with session.post(url, json=payload, headers=headers) as resp:
            print("\nResponse status ", resp.status)

    server_task.cancel()


async def cancel_code(server_task):
    server_task.cancel()


@pytest.mark.asyncio
async def test_missing_argument_vault_pass():
    queue = asyncio.Queue()

    args = {"host": "127.0.0.1", "port": 8001}
    plugin_task = asyncio.create_task(start_server(queue, args))
    cancel_task = asyncio.create_task(cancel_code(plugin_task))

    with pytest.raises(ValueError):
        await asyncio.gather(plugin_task, cancel_task)


@pytest.mark.asyncio
async def test_missing_argument_vault_path():
    queue = asyncio.Queue()

    args = {"host": "127.0.0.1", "port": 8001, "vault_pass": "secret"}
    plugin_task = asyncio.create_task(start_server(queue, args))
    cancel_task = asyncio.create_task(cancel_code(plugin_task))

    with pytest.raises(ValueError):
        await asyncio.gather(plugin_task, cancel_task)


@pytest.mark.asyncio
async def test_cancel(mocker):
    queue = asyncio.Queue()

    mock_vault_data = json.dumps({"ansible_token": "test"}).encode('utf-8')
    mocker.patch("pathlib.Path.open", return_value=io.StringIO("mock stream"))
    mocker.patch("ansible.parsing.vault.VaultLib.decrypt", return_value=mock_vault_data)

    args = {"host": "127.0.0.1", "port": 8002, "vault_pass": "secret", "vault_path": "mocked"}
    plugin_task = asyncio.create_task(start_server(queue, args))
    cancel_task = asyncio.create_task(cancel_code(plugin_task))

    with pytest.raises(asyncio.CancelledError):
        await asyncio.gather(plugin_task, cancel_task)


@pytest.mark.asyncio
async def test_file_not_found(mocker):
    queue = asyncio.Queue()

    mocker.patch("pathlib.Path.open", side_effect=FileNotFoundError("mocked error"))

    args = {"host": "127.0.0.1", "port": 8003, "vault_pass": "ansible", "vault_path": "mocked"}
    plugin_task = asyncio.create_task(start_server(queue, args))

    with pytest.raises(FileNotFoundError):
        await asyncio.gather(plugin_task)


@pytest.mark.asyncio
async def test_no_token_in_vault(mocker):
    queue = asyncio.Queue()

    mock_vault_data = json.dumps({"ansible_no_token": "test"}).encode('utf-8')
    mocker.patch("pathlib.Path.open", return_value=io.StringIO("mock stream"))
    mocker.patch("ansible.parsing.vault.VaultLib.decrypt", return_value=mock_vault_data)

    args = {"host": "127.0.0.1", "port": 8004, "vault_pass": "ansible", "vault_path": "mocked"}
    plugin_task = asyncio.create_task(start_server(queue, args))

    with pytest.raises(ValueError):
        await asyncio.gather(plugin_task)


@pytest.mark.asyncio
async def test_post_endpoint_success(mocker):
    queue = asyncio.Queue()

    mock_vault_data = json.dumps({"ansible_token": "test"}).encode('utf-8')
    mocker.patch("pathlib.Path.open", return_value=io.StringIO("mock stream"))
    mocker.patch("ansible.parsing.vault.VaultLib.decrypt", return_value=mock_vault_data)

    args = {"host": "127.0.0.1", "port": 8005, "vault_pass": "ansible", "vault_path": "mocked"}
    plugin_task = asyncio.create_task(start_server(queue, args))

    task_info = {
        "payload": {"type": "alert", "status": "update", "host": "server_a"},
        "endpoint": "test",
        "host": f'{args["host"]}:{args["port"]}',
        "ansible_token": "test"
    }

    post_task = asyncio.create_task(post_code(plugin_task, task_info))

    await asyncio.gather(plugin_task, post_task)

    data = await queue.get()
    assert data["payload"] == task_info["payload"]
    assert data["meta"]["endpoint"] == task_info["endpoint"]
    assert data["meta"]["headers"]["host"] == task_info["host"]


@pytest.mark.asyncio
async def test_post_endpoint_wrong_token(mocker):
    queue = asyncio.Queue()

    mock_vault_data = json.dumps({"ansible_token": "test"}).encode('utf-8')
    mocker.patch("pathlib.Path.open", return_value=io.StringIO("mock stream"))
    mocker.patch("ansible.parsing.vault.VaultLib.decrypt", return_value=mock_vault_data)

    args = {"host": "127.0.0.1", "port": 8006, "vault_pass": "ansible", "vault_path": "mocked"}
    plugin_task = asyncio.create_task(start_server(queue, args))

    task_info = {
        "payload": {"src_path": "https://example.com/payload"},
        "endpoint": "test",
        "host": f'{args["host"]}:{args["port"]}',
        "ansible_token": "Wrong token"
    }

    post_task = asyncio.create_task(post_code(plugin_task, task_info))

    await asyncio.gather(plugin_task, post_task)

    assert queue.qsize() == 0
