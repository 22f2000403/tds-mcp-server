import hashlib
from fastapi import Request
from mcp.server.fastmcp import FastMCP

EMAIL = "22f2000403@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Challenge Server",
    stateless_http=True,
    json_response=True,
)

_request: Request | None = None


@mcp.custom_route("/", methods=["POST"])
async def capture_request(request: Request, call_next):
    global _request
    _request = request
    return await call_next(request)


@mcp.tool()
def solve_challenge() -> str:
    """
    Solve the exam challenge.
    """

    if _request is None:
        return ""

    challenge = _request.headers.get("X-Exam-Challenge", "")

    answer = hashlib.sha256(
        f"{challenge}:{EMAIL.lower().strip()}".encode()
    ).hexdigest()[:16]

    return answer


app = mcp.streamable_http_app()