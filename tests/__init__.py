#!/usr/bin/python3
"""Test_AirBnb"""
import os
from typing import TextIO
from models.engine.file_storage import FileStorage


def clear_stream(stream: TextIO):
    """Test_AirBnb"""
    if stream.seekable():
        stream.seek(0)
        stream.truncate(0)


def Test_AirBnb_reset_store(store: FileStorage, file_path='file.json'):
    """Test_AirBnb"""
    with open(file_path, mode='w') as f:
        f.write('{}')
        if store is not None:
            store.reload()


def Test_AirBnb_delete_file(file_path: str):
    """Test_AirBnb"""
    if os.path.isfile(file_path):
        os.unlink(file_path)


def Test_AirBnb_write_text_file(file_name, text):
    """Test_AirBnb"""
    with open(file_name, mode='w') as f:
        f.write(text)


def Test_AirBnb_read_text_file(file_name):
    """Test_AirBnb"""
    lines = []
    if os.path.isfile(file_name):
        with open(file_name, mode='r') as f:
            for line in f.readlines():
                lines.append(line)
    return ''.join(lines)
