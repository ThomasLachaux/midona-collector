from subprocess import run, PIPE

import json


def collect():
    # Retreive stats for the whole repo and the latest snapshot
    for snapshot in ["", "latest"]:
        stats = lambda mode: json.loads(
            run(
                ["restic", "stats", "--mode", mode, "--json", snapshot],
                stdout=PIPE,
                text=True,
            ).stdout
        )

        raw_data = stats("raw-data")
        restore_size = stats("restore-size")

        # Define the scope name
        scope = "latest_snapshot"
        if not snapshot:
            scope = "repository"

        yield f'backup,mode=raw_data,scope={scope} total_size={raw_data["total_size"]}u'

        yield f'backup,mode=restore_size,scope={scope} total_size={restore_size["total_size"]}u'
        yield f'backup,mode=restore_size,scope={scope} total_file_count={restore_size["total_file_count"]}u'
