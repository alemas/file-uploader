def format_file_size(size_in_bytes: int):
    size_str = f'{size_in_bytes:n}' + " B"
    if size_in_bytes > 1024**3:
        size_str = f'{int(size_in_bytes/1024**3):n}' + " GB"
    elif size_in_bytes > 1024**2:
        size_str = f'{int(size_in_bytes/1024**2):n}' + " MB"
    elif size_in_bytes > 1024:
        size_str = f'{int(size_in_bytes/1024):n}' + " KB"
    return size_str