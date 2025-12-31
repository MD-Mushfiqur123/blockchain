"""
Block compression and optimization
"""
import zlib
import gzip
import json
from typing import Dict, Any


def compress_block(block_data: Dict[str, Any]) -> bytes:
    """Compress block data with multiple algorithms"""
    # Convert to JSON
    json_data = json.dumps(block_data, sort_keys=True).encode('utf-8')
    
    # First compression: zlib
    zlib_compressed = zlib.compress(json_data, level=9)
    
    # Second compression: gzip
    gzip_compressed = gzip.compress(zlib_compressed, compresslevel=9)
    
    return gzip_compressed


def decompress_block(compressed_data: bytes) -> Dict[str, Any]:
    """Decompress block data"""
    # Reverse gzip
    zlib_data = gzip.decompress(compressed_data)
    
    # Reverse zlib
    json_data = zlib.decompress(zlib_data)
    
    # Parse JSON
    return json.loads(json_data.decode('utf-8'))

