#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
vector_search.py
----------------

A lightweight, dependency‑aware vector‑search library.

Features
--------
* Store vectors together with optional IDs and user‑defined metadata.
* Exact (brute‑force) search for Euclidean distance or cosine similarity.
* Optional FAISS‑based approximate search for large collections.
* Batch querying, top‑k results, and distance/similarity scores.
* Simple persistence (pickle) for quick save / load.

Typical usage
~~~~~~~~~~~~~

>>> from vector_search import VectorIndex
>>> import numpy as np
>>> # Create an index (cosine similarity by default)
>>> idx = VectorIndex(metric="cosine")
>>> # Add a few vectors
>>> idx.add(np.random.rand(5, 128), ids=["a", "b", "c", "d", "e"])
>>> # Query the 3 nearest neighbours of a new vector
>>> query = np.random.rand(1, 128)
>>> results = idx.search(query, k=3)
>>> for hit in results[0]:
...     print(hit.id, hit.score)

Advanced usage (FAISS)
~~~~~~~~~~~~~~~~~~~~~~
>>> # If you have faiss‑cpu or faiss‑gpu installed the index will
>>> # automatically switch to an approximate index for faster queries.
>>> idx = VectorIndex(metric="l2", use_faiss=True)
"""

from __future__ import annotations

import os
import pickle
import warnings
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np

# --------------------------------------------------------------------------- #
# Optional FAISS import – keep the library optional
# --------------------------------------------------------------------------- #
try:
    import faiss  # type: ignore
    _FAISS_AVAILABLE = True
except Exception:  # pragma: no cover
    _FAISS_AVAILABLE = False


# --------------------------------------------------------------------------- #
# Helper data structures
# --------------------------------------------------------------------------- #
@dataclass
class SearchResult:
    """One hit returned by ``VectorIndex.search``."""
    id: Optional[Any]          # The user supplied ID (or None if not given)
    score: float               # Similarity (cosine) or distance (L2) to query
    vector: np.ndarray         # The stored vector (read‑only view)


# --------------------------------------------------------------------------- #
# Core class
# --------------------------------------------------------------------------- #
class VectorIndex:
    """
    Store vectors and perform nearest‑neighbour search.

    Parameters
    ----------
    metric : {"l2", "cosine"}
        Distance / similarity metric.
        * ``"l2"`` – Euclidean distance (lower is better).
        * ``"cosine"`` – Cosine similarity (higher is better).

    use_faiss : bool, default=False
        If ``True`` and FAISS is installed, an approximate index will be built
        (``IndexFlatIP`` for cosine, ``IndexFlatL2`` for Euclidean).  The
        fallback is a pure‑numpy brute‑force search.

    dtype : np.dtype, default=np.float32
        The numeric type used for the stored vectors.  FAISS requires
        ``float32``; other dtypes will automatically be cast.

    normalize : bool, default=False
        When ``True`` and ``metric="cosine"``, vectors are L2‑normalized on
        insertion so that inner‑product queries are equivalent to cosine
        similarity.  For ``metric="l2"``, this flag is ignored.
    """

    # ------------------------------------------------------------------- #
    # Construction / persistence
    # ------------------------------------------------------------------- #
    def __init__(
        self,
        metric: str = "cosine",
        use_faiss: bool = False,
        dtype: np.dtype = np.float32,
        normalize: bool = False,
    ) -> None:
        metric = metric.lower()
        if metric not in {"l2", "cosine"}:
            raise ValueError("metric must be 'l2' or 'cosine'")
        self.metric = metric
        self.use_faiss = use_faiss and _FAISS_AVAILABLE
        if use_faiss and not _FAISS_AVAILABLE:
            warnings.warn(
                "FAISS requested but not installed – falling back to brute-force.",
                RuntimeWarning,
            )
        self.dtype = np.dtype(dtype)
        self.normalize = normalize and metric == "cosine"

        # Internal storage
        self._vectors: np.ndarray | None = None      # shape (N, D)
        self._ids: List[Any] = []                    # parallel to vectors
        self._metadata: List[Any] = []               # optional extra payload
        self._faiss_index: Any = None                 # type: ignore

    # ------------------------------------------------------------------- #
    # Adding vectors
    # ------------------------------------------------------------------- #
    def add(
        self,
        vectors: Union[np.ndarray, Sequence[Sequence[float]]],
        ids: Optional[Iterable[Any]] = None,
        metadata: Optional[Iterable[Any]] = None,
    ) -> None:
        """
        Append new vectors to the index.

        Parameters
        ----------
        vectors : np.ndarray or array‑like, shape (N, D)
            The vectors to store.

        ids : iterable, optional
            Unique identifiers for each vector (e.g. strings, ints).  If omitted,
            ``None`` is stored for each vector.

        metadata : iterable, optional
            Arbitrary per‑vector payload (e.g. dicts).  If omitted, ``None`` is
            stored.
        """
        vectors = np.asarray(vectors, dtype=self.dtype, order="C")
        if vectors.ndim != 2:
            raise ValueError("vectors must be a 2‑D array (N, D)")

        n_new = vectors.shape[0]

        # Normalization for cosine similarity
        if self.normalize:
            norms = np.linalg.norm(vectors, axis=1, keepdims=True)
            # Avoid division by zero – keep zero vectors as‑is
            norms[norms == 0] = 1.0
            vectors = vectors / norms

        # Prepare IDs / metadata
        if ids is None:
            ids = [None] * n_new
        else:
            ids = list(ids)
            if len(ids) != n_new:
                raise ValueError("ids length must match number of vectors")
        if metadata is None:
            metadata = [None] * n_new
        else:
            metadata = list(metadata)
            if len(metadata) != n_new:
                raise ValueError("metadata length must match number of vectors")

        # Append to internal storage
        if self._vectors is None:
            self._vectors = vectors
        else:
            self._vectors = np.vstack([self._vectors, vectors])
        self._ids.extend(ids)
        self._metadata.extend(metadata)

        # If using FAISS, add to the underlying index
        if self.use_faiss:
            self._ensure_faiss_index()
            self._faiss_index.add(vectors)

    # ------------------------------------------------------------------- #
    # Querying
    # ------------------------------------------------------------------- #
    def search(
        self,
        queries: Union[np.ndarray, Sequence[Sequence[float]]],
        k: int = 5,
        *,
        return_vectors: bool = False,
    ) -> List[List[SearchResult]]:
        """
        Find the `k` nearest neighbours for each query vector.

        Parameters
        ----------
        queries : np.ndarray or array‑like, shape (Q, D)
            One or more query vectors.

        k : int, default=5
            Number of neighbours to return (per query).  If ``k`` exceeds the
            number of indexed vectors, the result is truncated automatically.

        return_vectors : bool, default=False
            If ``True`` the actual stored vectors are included in each
            ``SearchResult`` (adds a small memory copy overhead).

        Returns
        -------
        List[List[SearchResult]]
            Outer list length = number of queries.  Inner list contains up to
            `k` ``SearchResult`` objects sorted by best score first.
        """
        if self._vectors is None or len(self._ids) == 0:
            raise RuntimeError("The index is empty – add vectors before searching.")

        queries = np.asarray(queries, dtype=self.dtype, order="C")
        if queries.ndim != 2:
            raise ValueError("queries must be a 2‑D array (Q, D)")

        if self.normalize and self.metric == "cosine":
            # Normalise queries the same way as stored vectors
            norms = np.linalg.norm(queries, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            queries = queries / norms

        # Clamp k to available size
        effective_k = min(k, len(self._ids))

        if self.use_faiss:
            # FAISS returns (distances, indices)
            distances, indices = self._faiss_index.search(queries, effective_k)
            # For cosine similarity FAISS uses inner‑product, so higher = better.
            # We keep the raw scores and let callers interpret them.
        else:
            # -------- Brute‑force implementation --------
            # Compute pairwise distances / similarities in a vectorised way.
            # This is O(N*D) per query which is fine for <~10k vectors.
            if self.metric == "l2":
                # Euclidean distance: sqrt of summed squared diff.
                # Using broadcasting: (Q,1,D) - (1,N,D) -> (Q,N,D)
                diff = queries[:, None, :] - self._vectors[None, :, :]
                distances = np.linalg.norm(diff, axis=2)  # shape (Q, N)
                # For consistency with FAISS, we keep distances (lower = better)
                indices = np.argsort(distances, axis=1)[:, :effective_k]
                distances = np.take_along_axis(distances, indices, axis=1)
            else:  # cosine similarity (inner product after normalisation)
                # Because vectors are already L2‑normalised, dot product = cosine.
                sims = queries @ self._vectors.T  # shape (Q, N)
                # Higher similarity is better → sort descending.
                indices = np.argsort(-sims, axis=1)[:, :effective_k]
                distances = np.take_along_axis(sims, indices, axis=1)  # actually scores
        # Build SearchResult objects
        results: List[List[SearchResult]] = []
        for q_idx in range(queries.shape[0]):
            cur_res: List[SearchResult] = []
            for rank in range(effective_k):
                idx = int(indices[q_idx, rank])
                score = float(distances[q_idx, rank])
                vec = self._vectors[idx] if return_vectors else None
                cur_res.append(
                    SearchResult(
                        id=self._ids[idx],
                        score=score,
                        vector=vec,
                    )
                )
            results.append(cur_res)
        return results

    # ------------------------------------------------------------------- #
    # FAISS helpers
    # ------------------------------------------------------------------- #
    def _ensure_faiss_index(self) -> None:
        """Create a FAISS index if it does not already exist."""
        if not self.use_faiss:
            return
        if self._faiss_index is not None:
            return

        if self._vectors is None:
            raise RuntimeError("No vectors to build a FAISS index from.")

        dim = self._vectors.shape[1]
        if self.metric == "l2":
            self._faiss_index = faiss.IndexFlatL2(dim)
        else:  # cosine -> inner product
            # FAISS does NOT have a dedicated cosine index; we use inner product
            # after normalising vectors (handled by `self.normalize`).
            self._faiss_index = faiss.IndexFlatIP(dim)

        # Transfer existing vectors to FAISS (required when vectors were added
        # before the first call to `search` with FAISS enabled)
        self._faiss_index.add(self._vectors)

    # ------------------------------------------------------------------- #
    # Persistence
    # ------------------------------------------------------------------- #
    def save(self, path: str, *, overwrite: bool = False) -> None:
        """
        Serialize the index to a file using ``pickle``.

        Parameters
        ----------
        path : str
            Destination file name.  Parent directories are created if needed.

        overwrite : bool, default=False
            If ``True`` an existing file will be replaced; otherwise a
            ``FileExistsError`` is raised.
        """
        if not overwrite and os.path.exists(path):
            raise FileExistsError(f"File '{path}' already exists. Use overwrite=True.")
        os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)

        # FAISS index cannot be pickled directly – we store its binary representation.
        faiss_bytes = None
        if self.use_faiss and self._faiss_index is not None:
            faiss_bytes = faiss.serialize_index(self._faiss_index)

        payload = {
            "metric": self.metric,
            "use_faiss": self.use_faiss,
            "dtype": self
