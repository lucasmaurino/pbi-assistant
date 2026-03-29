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

            print("\n--- TEST: update_pbi_state ---")
            result = await session.call_tool(
                "update_pbi_state",
                {
                    "input": {
                        "pbi_id": "PBI-102",
                        "new_state": "Active"
                    }
                }
            )
            print(result)

            print("\n--- TEST: assign_pbi ---")
            result = await session.call_tool(
                "assign_pbi",
                {
                    "input": {
                        "pbi_id": "PBI-102",
                        "person_name": "Bob"
                    }
                }
            )
            print(result)

            print("\n--- TEST: add_comment ---")
            result = await session.call_tool(
                "add_comment",
                {
                    "input": {
                        "pbi_id": "PBI-102",
                        "comment": "Status updated to Active and assigned to Bob."
                    }
                }
            )
            print(result)

            print("\n--- TEST: add_comment ---")
            result = await session.call_tool(
                "add_comment",
                {
                    "input": {
                        "pbi_id": "PBI-103",
                        "comment": "Test to validate PBI verification (PBI-103 does not exist)."
                    }
                }
            )
            print(result)


if __name__ == "__main__":
    asyncio.run(main())
