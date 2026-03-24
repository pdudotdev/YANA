# RAG Workflow — Concrete Example

This document walks through exactly what happens when you ask netKB a question, using real data from the project.

## The Question

```
"Why is my OSPF neighbor stuck in INIT?"
```

## Step 1: Ingestion (One-Time Setup)

Before any question can be answered, the knowledge base must be built. This happens once when you run `python ingest.py`.

### 1a. Loading

`ingest.py` reads all `.md` files from `docs/` plus `INTENT.json` and `NETWORK.json` from `core/legacy/`. Each file becomes a LangChain `Document` object with metadata derived from its filename.

Example — `rfc2328_summary.md` gets metadata:
```json
{"vendor": "all", "topic": "rfc", "source": "rfc2328_summary.md"}
```

### 1b. Chunking

The `RecursiveCharacterTextSplitter` breaks each document into ~800 character chunks, splitting at section headers and paragraphs to keep chunks coherent.

The full `rfc2328_summary.md` (~4000 chars) becomes multiple chunks. One of them is:

```
- **DOWN**: No Hello packets received from this neighbor. Initial state.
- **INIT**: A Hello was received but the local router's ID was not in the
  neighbor's Hello. One-way communication only.
- **2WAY**: Bidirectional communication confirmed. Both routers see each
  other's Router ID in Hello packets...
- **EXSTART**: Master/slave negotiation for Database Description (DD)
  exchange begins...
```

This chunk is 731 characters. It inherited the metadata `{source: "rfc2328_summary.md", topic: "rfc", vendor: "all"}`.

### 1c. Embedding

The `all-MiniLM-L6-v2` model (running locally, no API call) reads that chunk and produces a vector of 384 numbers:

```
[-0.0302, -0.0195, 0.0166, -0.0345, 0.0212, -0.0464, -0.0415, -0.0128, -0.0797, 0.0049, ... ]
(384 dimensions total)
```

These numbers encode the *meaning* of the text in a mathematical space. Text about similar topics produces similar vectors.

### 1d. Storage

ChromaDB stores the chunk as a record:

```
ID:        1181ff8e-1983-4b59-a772-3374a3b6baa1
Text:      "- **DOWN**: No Hello packets received..."  (731 chars)
Metadata:  {"source": "rfc2328_summary.md", "topic": "rfc", "vendor": "all"}
Vector:    [-0.0302, -0.0195, 0.0166, ...]  (384 floats)
```

This happens for all 75 chunks across all documents. The database is now ready.

## Step 2: Query (Every Time You Ask)

Now you ask: `"Why is my OSPF neighbor stuck in INIT?"`

### 2a. Question → Vector

The same embedding model converts your question into a 384-dim vector:

```
Question: "Why is my OSPF neighbor stuck in INIT"
Vector:   [0.0193, -0.0532, 0.0135, -0.0071, 0.1528, 0.0054, -0.0898, -0.0029, -0.0993, 0.0045, ...]
```

### 2b. Similarity Search

ChromaDB compares the question vector against all 75 stored chunk vectors using distance calculation (cosine distance). Lower distance = more similar meaning.

Results ranked by relevance:

```
Distance: 0.9453  →  rfc2328_summary.md  — "Common Stuck States and Causes" table
Distance: 1.0184  →  vendor_cisco_ios.md  — Cisco IOS OSPF configuration syntax
Distance: 1.0490  →  vendor_arista_eos.md — Arista EOS VRF configuration
```

The top result (distance 0.9453) is the "Common Stuck States and Causes" chunk — which directly explains INIT, EXSTART, and other stuck states. The system found the right answer even though the question used different words than the stored text.

### 2c. Return to Claude

The top 5 chunks (text + metadata) are returned to Claude Code via the MCP tool response. Claude now has relevant documentation context.

## Step 3: Claude Synthesizes

Claude reads the CLAUDE.md skill, which tells it to:

1. Use the KB results to understand the theory (INIT = one-way communication, common causes)
2. Optionally query live devices if a specific device was mentioned
3. Combine both into a grounded answer citing sources

## Why This Works

The key insight is that the embedding model maps both *"INIT state means Hello one-way"* and *"Why is my neighbor stuck in INIT"* to nearby points in 384-dimensional space — because they're about the same concept. A keyword search would miss this (the word "stuck" doesn't appear in the RFC text), but vector similarity catches the semantic relationship.

## Summary

```
Ingestion (one-time):
  Docs → Chunks (text splitter) → Vectors (embedding model) → ChromaDB

Query (every question):
  Question → Vector (same embedding model) → Similarity search → Top chunks returned

Synthesis:
  Claude reads chunks + optionally queries live devices → Grounded answer
```
