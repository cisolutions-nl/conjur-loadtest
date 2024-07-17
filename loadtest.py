import argparse
import asyncio
import base64
import time
import urllib.parse

import httpx
from getpass import getpass

parser = argparse.ArgumentParser(
    prog="Conjur Load Test",
    description="Load Test for consuming secrets from Cyberark Conjur.",
)
parser.add_argument(
    "-c",
    "--concurrency",
    type=str,
    help="Number of concurrent requests to make to Conjur.",
    required=True,
)
parser.add_argument("-b", "--base-url", type=str, help="Base URL", required=True)
parser.add_argument(
    "-a", "--account", type=str, help="Account", required=True
)
parser.add_argument(
    "-u", "--user-name", type=str, help="User name", required=True
)
parser.add_argument(
    "-k", "--api-key", type=str, help="API key"
)
parser.add_argument(
    "-s", "--secret-id", type=str, help="Secret id", required=True
)

args = parser.parse_args()

CONJUR_API_KEY = args.api_key or getpass("Enter Conjur API key:")
DEFAULT_HEADERS = {"Content-Type": "text/plain", "Accept-Encoding": "base64"}


def timeit(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        response = await func(*args, **kwargs)
        return response, time.time() - start

    return wrapper


@timeit
async def fetch():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f"{args.base_url}/authn/{args.account}/{args.user_name}/authenticate/",
            headers=DEFAULT_HEADERS,
            data=CONJUR_API_KEY,
        )
        token = base64.b64encode(response.content).decode("utf-8")

        parsed_secret_id = urllib.parse.quote(args.secret_id, safe="")
        path = f"{args.base_url}/secrets/{args.account}/variable/{parsed_secret_id}"

        response = await client.get(
            url=path,
            headers=DEFAULT_HEADERS
            | {
                "Authorization": 'Token token="{}"'.format(token),
            },
        )
        return response


async def main(
    concurrent_requests: int,
):
    tasks = [fetch() for _ in range(0, concurrent_requests)]

    responses = await asyncio.gather(*tasks)
    times = [seconds for response, seconds in responses]
    print(
        f"Finished {len(times)} requests. Average response time: {sum(times) / len(times)}"
    )


if __name__ == "__main__":
    for i in range(0, 10):
        asyncio.run(main(
            concurrent_requests=int(args.concurrency),
        ))
