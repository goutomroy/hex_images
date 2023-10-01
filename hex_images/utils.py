def get_thumbnail_photo_path(
    file_name: str, username: str, height: int, width: int
) -> str:
    return "/".join(
        [
            "images",
            username,
            "thumbnails",
            f"{height}_{width}_" + file_name,
        ]
    )
