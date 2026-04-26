from pydantic import BaseModel


class GraphNode(BaseModel):
    id: str
    type: str
    label: str
    status: str
    metadata: dict = {}


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
