import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession


async def main():
    server = StdioServerParameters(
        command="python",
        args=["-m", "mcp_server.server"]
    )

    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            result = await session.call_tool(
                "update_pbi_state",
                {
                    "input": {
                        "pbi_id": "PBI-102",
                        "new_state": "Done"
                    }
                }
            )

            print(result)


if __name__ == "__main__":
    asyncio.run(main())
