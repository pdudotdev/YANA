"""Pydantic input models for MCP tools."""
import json
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

_VRF_RE = re.compile(r'^[a-zA-Z0-9_-]{1,32}$')


class BaseParamsModel(BaseModel):
    """Base class with JSON string parsing and VRF validation."""

    @model_validator(mode='before')
    @classmethod
    def parse_string_input(cls, v):
        if isinstance(v, str):
            try:
                obj, _ = json.JSONDecoder().raw_decode(v.strip())
                return obj
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Could not parse params as JSON: {v!r}") from e
        return v

    @field_validator('vrf', mode='before', check_fields=False)
    @classmethod
    def _validate_vrf(cls, v):
        if v is None:
            return v
        if not _VRF_RE.match(str(v)):
            raise ValueError(f"vrf must be alphanumeric with underscores/dashes, max 32 chars. Got: {v!r}")
        return v


class OspfQuery(BaseParamsModel):
    device: str = Field(..., description="Device name from inventory")
    query: Literal["neighbors", "database", "borders", "config", "interfaces", "details"] = Field(
        ..., description="neighbors | database | borders | config | interfaces | details"
    )
    vrf: str | None = Field(None, description="Optional VRF name (default: device VRF or global)")


class InterfacesQuery(BaseParamsModel):
    device: str = Field(..., description="Device name from inventory")


class KBQuery(BaseParamsModel):
    query: str = Field(..., description="Search question for the OSPF knowledge base", max_length=500)
    vendor: Literal["cisco_ios", "arista_eos", "juniper_junos", "aruba_aoscx", "mikrotik_ros"] | None = Field(
        None, description="Filter by vendor: cisco_ios | arista_eos | juniper_junos | aruba_aoscx | mikrotik_ros"
    )
    topic: Literal["rfc", "vendor_guide", "intent", "inventory"] | None = Field(
        None, description="Filter by topic: rfc | vendor_guide | intent | inventory"
    )
    top_k: int = Field(5, description="Number of results to return (1-10)", ge=1, le=10)
