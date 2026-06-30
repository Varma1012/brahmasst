import os
import uuid


BASE_UPLOAD = "uploads"

PARENT1 = os.path.join(
    BASE_UPLOAD,
    "parent1"
)

PARENT2 = os.path.join(
    BASE_UPLOAD,
    "parent2"
)


def save_uploaded_file(
    file,
    folder="parent1"
):

    target = (
        PARENT1
        if folder == "parent1"
        else PARENT2
    )

    os.makedirs(
        target,
        exist_ok=True
    )

    print("\n====================")
    print("[DEBUG] UPLOAD START")
    print("====================")

    print(
        "[DEBUG] Folder:",
        target
    )

    print(
        "[DEBUG] File:",
        file.filename
    )

    # remove only target folder files
    for old in os.listdir(target):

        old_path = os.path.join(
            target,
            old
        )

        try:

            os.remove(
                old_path
            )

            print(
                "[DEBUG] Removed:",
                old
            )

        except Exception as e:

            print(
                "[DEBUG] Remove failed:",
                e
            )

    ext = (
        os.path.splitext(
            file.filename
        )[1]
        or ".gff"
    )

    filename = (
        str(uuid.uuid4())
        + ext
    )

    path = os.path.join(
        target,
        filename
    )

    size = 0

    with open(
        path,
        "wb"
    ) as f:

        for chunk in file.stream:

            size += len(chunk)

            f.write(
                chunk
            )

    print(
        "[DEBUG] Saved:",
        path
    )

    print(
        "[DEBUG] Size:",
        round(
            size / 1024,
            2
        ),
        "KB"
    )

    print("====================\n")

    return path