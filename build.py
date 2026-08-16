from build_utils import prepare_skill_images, assemble_workspace_video, build_skill_zip, list_assets

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build and assemble video assets for the project.")
    parser.add_argument(
        "command",
        nargs="?",
        default="all",
        choices=["prepare_skill_images", "assemble_video", "build_skill_zip", "list_assets", "all"],
        help="Command to run.",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=None,
        help="Override the output video FPS for assemble_video.",
    )
    parser.add_argument(
        "--scene-seconds",
        type=float,
        default=None,
        help="Override the duration in seconds for each scene.",
    )
    args = parser.parse_args()

    if args.command == "prepare_skill_images":
        prepare_skill_images()
    elif args.command == "assemble_video":
        assemble_workspace_video(
            video_fps=args.fps if args.fps is not None else None,
            scene_seconds=args.scene_seconds if args.scene_seconds is not None else None,
        )
    elif args.command == "build_skill_zip":
        build_skill_zip()
    elif args.command == "list_assets":
        list_assets()
    elif args.command == "all":
        prepare_skill_images()
        assemble_workspace_video(
            video_fps=args.fps if args.fps is not None else None,
            scene_seconds=args.scene_seconds if args.scene_seconds is not None else None,
        )
    if args.command == "all":
        build_skill_zip()
