import os
from core.util import basic_io

posts_file_path = os.path.join("core", "data", "posts_TheRedPill.json")
posts = basic_io.read_json_to_dict(posts_file_path)
