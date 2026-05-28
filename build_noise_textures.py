"""
build_noise_textures.py

This script is designed to add noise to Minecraft textures.
It scales up all images by x4 and adds a noise pattern to the textures.
"""

import hashlib
import json
import logging
import logging.handlers
import numpy as np
import os
import random
import re
import socket
import sys
import typing
from dataclasses import dataclass, field
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from PIL import Image


logger = logging.getLogger(__name__)

__version__ = "2.0.0"  # Major.Minor.Patch

log_buffer = logging.handlers.MemoryHandler(
    capacity=0,
    flushLevel=logging.CRITICAL,
    target=None,
)

logger.addHandler(log_buffer)
logger.setLevel(logging.DEBUG)


@dataclass
class ScriptSettings:
    assets_dir: Path = Path(r"assets\minecraft\textures")
    scaler_modifier: int = 4
    strength: float = 0.075
    supported_extensions: list[str] = field(default_factory=lambda: [".png"])
    animated_textures: list[dict] = field(default_factory=lambda: [
        {"type": "vanilla_spritesheet", "path": Path(r"block\blast_furnace_front_on.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\copper_lantern.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\exposed_copper_lantern.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\lantern.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\magma.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\oxidized_copper_lantern.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\smoker_front_on.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\soul_lantern.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\stonecutter_saw.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\weathered_copper_lantern.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\campfire_log_lit.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\chain_command_block_back.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\chain_command_block_conditional.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\chain_command_block_front.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\chain_command_block_side.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\command_block_back.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\command_block_conditional.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\command_block_front.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\command_block_side.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\prismarine.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\repeating_command_block_back.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\repeating_command_block_conditional.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\repeating_command_block_front.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\repeating_command_block_side.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk_vein.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\soul_campfire_log_lit.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\crimson_stem.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sea_lantern.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\warped_stem.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\campfire_fire.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk_catalyst_side_bloom.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk_catalyst_top_bloom.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\soul_campfire_fire.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\firefly_bush_emissive.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk_shrieker_can_summon_inner_top.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk_shrieker_inner_top.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk_sensor_tendril_active.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\sculk_sensor_tendril_inactive.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\seagrass.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\tall_seagrass_bottom.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\tall_seagrass_top.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\kelp.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\kelp_plant.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\lava_still.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\fire_0.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\fire_1.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\nether_portal.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\respawn_anchor_top.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\soul_fire_0.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\soul_fire_1.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\water_still.png"), "columns": 1},
        {"type": "vanilla_spritesheet", "path": Path(r"block\lava_flow.png"), "columns": 2},
        {"type": "vanilla_spritesheet", "path": Path(r"block\water_flow.png"), "columns": 2},
        {"type": "image_set", "paths": [Path(r"item\clock_00.png"), Path(r"item\clock_01.png"), Path(r"item\clock_02.png"), Path(r"item\clock_03.png"), Path(r"item\clock_04.png"), Path(r"item\clock_05.png"), Path(r"item\clock_06.png"), Path(r"item\clock_07.png"), Path(r"item\clock_08.png"), Path(r"item\clock_09.png"), Path(r"item\clock_10.png"), Path(r"item\clock_11.png"), Path(r"item\clock_12.png"), Path(r"item\clock_13.png"), Path(r"item\clock_14.png"), Path(r"item\clock_15.png"), Path(r"item\clock_16.png"), Path(r"item\clock_17.png"), Path(r"item\clock_18.png"), Path(r"item\clock_19.png"), Path(r"item\clock_20.png"), Path(r"item\clock_21.png"), Path(r"item\clock_22.png"), Path(r"item\clock_23.png"), Path(r"item\clock_24.png"), Path(r"item\clock_25.png"), Path(r"item\clock_26.png"), Path(r"item\clock_27.png"), Path(r"item\clock_28.png"), Path(r"item\clock_29.png"), Path(r"item\clock_30.png"), Path(r"item\clock_31.png"), Path(r"item\clock_32.png"), Path(r"item\clock_33.png"), Path(r"item\clock_34.png"), Path(r"item\clock_35.png"), Path(r"item\clock_36.png"), Path(r"item\clock_37.png"), Path(r"item\clock_38.png"), Path(r"item\clock_39.png"), Path(r"item\clock_40.png"), Path(r"item\clock_41.png"), Path(r"item\clock_42.png"), Path(r"item\clock_43.png"), Path(r"item\clock_44.png"), Path(r"item\clock_45.png"), Path(r"item\clock_46.png"), Path(r"item\clock_47.png"), Path(r"item\clock_48.png"), Path(r"item\clock_49.png"), Path(r"item\clock_50.png"), Path(r"item\clock_51.png"), Path(r"item\clock_52.png"), Path(r"item\clock_53.png"), Path(r"item\clock_54.png"), Path(r"item\clock_55.png"), Path(r"item\clock_56.png"), Path(r"item\clock_57.png"), Path(r"item\clock_58.png"), Path(r"item\clock_59.png"), Path(r"item\clock_60.png"), Path(r"item\clock_61.png"), Path(r"item\clock_62.png"), Path(r"item\clock_63.png"),]},
        {"type": "image_set", "paths": [Path(r"item\compass_00.png"), Path(r"item\compass_01.png"), Path(r"item\compass_02.png"), Path(r"item\compass_03.png"), Path(r"item\compass_04.png"), Path(r"item\compass_05.png"), Path(r"item\compass_06.png"), Path(r"item\compass_07.png"), Path(r"item\compass_08.png"), Path(r"item\compass_09.png"), Path(r"item\compass_10.png"), Path(r"item\compass_11.png"), Path(r"item\compass_12.png"), Path(r"item\compass_13.png"), Path(r"item\compass_14.png"), Path(r"item\compass_15.png"), Path(r"item\compass_16.png"), Path(r"item\compass_17.png"), Path(r"item\compass_18.png"), Path(r"item\compass_19.png"), Path(r"item\compass_20.png"), Path(r"item\compass_21.png"), Path(r"item\compass_22.png"), Path(r"item\compass_23.png"), Path(r"item\compass_24.png"), Path(r"item\compass_25.png"), Path(r"item\compass_26.png"), Path(r"item\compass_27.png"), Path(r"item\compass_28.png"), Path(r"item\compass_29.png"), Path(r"item\compass_30.png"), Path(r"item\compass_31.png"),]},
        {"type": "image_set", "paths": [Path(r"item\crossbow_arrow.png"), Path(r"item\crossbow_firework.png"), Path(r"item\crossbow_pulling_0.png"), Path(r"item\crossbow_pulling_1.png"), Path(r"item\crossbow_pulling_2.png"), Path(r"item\crossbow_standby.png"),]},
        {"type": "image_set", "paths": [Path(r"item\recovery_compass_00.png"), Path(r"item\recovery_compass_01.png"), Path(r"item\recovery_compass_02.png"), Path(r"item\recovery_compass_03.png"), Path(r"item\recovery_compass_04.png"), Path(r"item\recovery_compass_05.png"), Path(r"item\recovery_compass_06.png"), Path(r"item\recovery_compass_07.png"), Path(r"item\recovery_compass_08.png"), Path(r"item\recovery_compass_09.png"), Path(r"item\recovery_compass_10.png"), Path(r"item\recovery_compass_11.png"), Path(r"item\recovery_compass_12.png"), Path(r"item\recovery_compass_13.png"), Path(r"item\recovery_compass_14.png"), Path(r"item\recovery_compass_15.png"), Path(r"item\recovery_compass_16.png"), Path(r"item\recovery_compass_17.png"), Path(r"item\recovery_compass_18.png"), Path(r"item\recovery_compass_19.png"), Path(r"item\recovery_compass_20.png"), Path(r"item\recovery_compass_21.png"), Path(r"item\recovery_compass_22.png"), Path(r"item\recovery_compass_23.png"), Path(r"item\recovery_compass_24.png"), Path(r"item\recovery_compass_25.png"), Path(r"item\recovery_compass_26.png"), Path(r"item\recovery_compass_27.png"), Path(r"item\recovery_compass_28.png"), Path(r"item\recovery_compass_29.png"), Path(r"item\recovery_compass_30.png"), Path(r"item\recovery_compass_31.png"),]},
        {"type": "image_set", "paths": [Path(r"item\redstone_dust_dot.png"), Path(r"item\redstone_dust_line0.png"), Path(r"item\redstone_dust_line1.png"), Path(r"item\redstone_dust_overlay.png"),]},
    ])


@dataclass
class LogSettings:
    mode: typing.Literal["per_run", "latest", "per_day", "single_file", "console_only"] = "per_run"
    folder: Path = Path("Logs")
    console_level: int = logging.DEBUG
    file_level: int = logging.DEBUG
    date_format: str = "%Y-%m-%dT%H:%M:%S"
    message_format: str = "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(message)s"
    # message_format: str = "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(module)s:%(funcName)s - %(message)s"
    max_files: int | None = 3
    open_log_after_run: bool = False


@dataclass
class RuntimeSettings:
    pause_on_error: bool = True
    always_pause: bool = False


@dataclass
class Config:
    script_settings: ScriptSettings = field(default_factory=ScriptSettings)
    log_settings: LogSettings = field(default_factory=LogSettings)
    runtime_settings: RuntimeSettings = field(default_factory=RuntimeSettings)


def find_files(root: Path | str, *, recursive: bool = True, include: str | None = None, ignore: str | None = None):
    root = Path(root)
    if not root.exists():
        raise FileNotFoundError(f"Root path does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Expected a directory, got: {root}")

    include_pattern = re.compile(include, re.IGNORECASE) if include else None
    ignore_pattern = re.compile(ignore, re.IGNORECASE) if ignore else None

    iterator = root.rglob("*") if recursive else root.glob("*")

    for path in iterator:
        if not path.is_file():
            continue

        path_str = str(path)

        if ignore_pattern and ignore_pattern.search(path_str):
            continue

        if include_pattern and not include_pattern.search(path_str):
            continue

        yield path


def generate_seeded_random_generator(seed_string: str) -> random.Random:
    """
    Creates a deterministic Random instance based on a string (e.g., filename).
    """
    logger.debug("Generating rng...")
    hash_digest = hashlib.md5(seed_string.encode("utf-8")).hexdigest()
    rng = random.Random(int(hash_digest, 16))
    logger.debug("Done. %s", rng)
    return rng


def scale_image(file_path: Path, multiplier: int, resampling_mode: int = Image.Resampling.NEAREST) -> tuple[int, int] | None:
    logger.debug("Scaling x%s...", multiplier)
    try:
        with Image.open(file_path) as image:
            new_width = image.width * multiplier
            new_height = image.height * multiplier
            resized_image = image.resize((new_width, new_height), resample=resampling_mode)
            resized_image.save(file_path)
            logger.debug("Scaled from %sx%s to %sx%s", image.width, image.height, new_width, new_height)
        return new_width, new_height
    except Exception as e:
        logger.error("An error occurred while scaling media file %s: %s", file_path, e)
        return None


def generate_monochrome_noise_bytes(width: int, height: int, rng: random.Random) -> bytes:
    logger.debug("Generating noise pattern...")
    if width <= 0 or height <= 0:
        raise ValueError("Dimensions must be positive values")

    np_seed = rng.randint(0, 2**32 - 1)
    np_rng = np.random.default_rng(np_seed)

    brightness = np_rng.integers(0, 256, size=width * height, dtype=np.uint8)
    noise_bytes = np.repeat(brightness, 3).tobytes()

    logger.debug("Done")
    return noise_bytes


def blend_noise_overlay_on_image(image_path: Path, noise_mask: np.ndarray, strength: float) -> None:
    logger.debug("Applying noise array...")
    try:
        with Image.open(image_path) as img:
            img_rgba = img.convert("RGBA")

        img_arr = np.array(img_rgba).astype(np.float32)

        if img_arr.size == 0 or img_arr.shape[0] == 0 or img_arr.shape[1] == 0:
            logger.warning("Skipping noise application: Image %s has empty dimensions.", image_path)
            return

        if noise_mask.shape != img_arr.shape[:2]:
            logger.warning("Skipping noise application: Noise map shape %s does not match image shape %s for %s", noise_mask.shape, img_arr.shape[:2], image_path)
            return

        # Separate channels while preserving the 2D spatial dimensions
        r = img_arr[..., 0]
        g = img_arr[..., 1]
        b = img_arr[..., 2]
        a = img_arr[..., 3]

        # Create the mask but keep spatial geometry intact
        mask = a > 0

        # Calculate the noise adjustment for the entire image plane first
        r_noise = r * (1 - strength) + r * noise_mask * strength
        g_noise = g * (1 - strength) + g * noise_mask * strength
        b_noise = b * (1 - strength) + b * noise_mask * strength

        # Use the mask to selectively overwrite only the non-transparent pixels
        r[mask] = r_noise[mask]
        g[mask] = g_noise[mask]
        b[mask] = b_noise[mask]

        result_arr = np.stack([r, g, b, a], axis=-1).astype(np.uint8)
        logger.debug("Applied.")

        Image.fromarray(result_arr, "RGBA").save(image_path)
        logger.debug("Saved to file.")
    except Exception as e:
        logger.error("Failed to apply noise to %s: %s", image_path, e)


def create_and_apply_noise_grid(file_path: Path, rng: random.Random, width: int, height: int, strength: float, *, columns: int = 1, rows: int = 1) -> np.ndarray | None:
    frame_width = width // columns
    frame_height = height // rows

    if frame_width == 0:
        frame_width = 1
    if frame_height == 0:
        frame_height = 1

    noise_bytes = generate_monochrome_noise_bytes(frame_width, frame_height, rng)
    noise_arr = np.frombuffer(noise_bytes, dtype=np.uint8).reshape((frame_height, frame_width, 3))
    noise_gray = noise_arr[..., 0] / 255.0

    noise_full = np.tile(noise_gray, (rows, columns))
    noise_full = noise_full[:height, :width]

    blend_noise_overlay_on_image(file_path, noise_full, strength)
    return noise_full


def main(config: Config):
    settings = config.script_settings
    assets_dir = settings.assets_dir

    if not assets_dir.exists():
        logger.error("Assets directory does not exist: %s", assets_dir)
        return

    logger.info("Scanning for textures in %s", assets_dir)

    # Join extensions into a single valid regex pattern string matching any of them at the end of a path
    include_pattern_str = "|".join(re.escape(ext) + r"$" for ext in settings.supported_extensions)

    spritesheet_configs = {}
    imageset_first_files = {}
    imageset_siblings = {}

    for anim in settings.animated_textures:
        anim_type = anim.get("type")
        if anim_type == "vanilla_spritesheet":
            spritesheet_configs[Path(anim["path"])] = anim.get("columns", 1)
        elif anim_type == "image_set" and anim.get("paths"):
            paths = [Path(p) for p in anim["paths"]]
            first_path = paths[0]
            imageset_first_files[first_path] = paths
            for path in paths:
                imageset_siblings[path] = first_path

    processed_files = set()

    for file_path in find_files(assets_dir, include=include_pattern_str):
        try:
            rel_path = file_path.relative_to(assets_dir)
        except ValueError:
            continue

        if rel_path in processed_files:
            continue

        logger.debug("Processing %s", file_path)

        # Case A: Vanilla Spritesheet (Assume frames are square grid-tiled)
        if rel_path in spritesheet_configs:
            cols = spritesheet_configs[rel_path]
            scale_res = scale_image(file_path, settings.scaler_modifier, Image.Resampling.NEAREST)
            if scale_res:
                w, h = scale_res
                frame_w = w // cols
                calculated_rows = h // frame_w if frame_w > 0 else 1
                if calculated_rows == 0:
                    calculated_rows = 1

                rng = generate_seeded_random_generator(rel_path.as_posix())
                create_and_apply_noise_grid(file_path, rng, w, h, settings.strength, columns=cols, rows=calculated_rows)
            processed_files.add(rel_path)

        # Case B: First file encountered matches the master profile of an Image Set collection
        elif rel_path in imageset_first_files:
            all_set_rel_paths = imageset_first_files[rel_path]
            scale_res = scale_image(file_path, settings.scaler_modifier, Image.Resampling.NEAREST)
            if scale_res:
                w, h = scale_res
                for sibling_rel in all_set_rel_paths[1:]:
                    scale_image(assets_dir / sibling_rel, settings.scaler_modifier, Image.Resampling.NEAREST)

                rng = generate_seeded_random_generator(rel_path.as_posix())
                noise_matrix = create_and_apply_noise_grid(file_path, rng, w, h, settings.strength, columns=1, rows=1)

                if noise_matrix is not None:
                    for sibling_rel in all_set_rel_paths[1:]:
                        blend_noise_overlay_on_image(assets_dir / sibling_rel, noise_matrix, settings.strength)

                for sibling_rel in all_set_rel_paths:
                    processed_files.add(sibling_rel)

        # Case C: Sibling image set element hit out of sequence before its master record
        elif rel_path in imageset_siblings:
            master_rel = imageset_siblings[rel_path]
            if master_rel in processed_files:
                continue

            all_set_rel_paths = imageset_first_files[master_rel]
            master_abs_path = assets_dir / master_rel
            scale_res = scale_image(master_abs_path, settings.scaler_modifier, Image.Resampling.NEAREST)
            if scale_res:
                w, h = scale_res
                for sibling_rel in all_set_rel_paths:
                    if sibling_rel != master_rel:
                        scale_image(assets_dir / sibling_rel, settings.scaler_modifier, Image.Resampling.NEAREST)

                rng = generate_seeded_random_generator(master_rel.as_posix())
                noise_matrix = create_and_apply_noise_grid(master_abs_path, rng, w, h, settings.strength, columns=1, rows=1)

                if noise_matrix is not None:
                    for sibling_rel in all_set_rel_paths:
                        if sibling_rel != master_rel:
                            blend_noise_overlay_on_image(assets_dir / sibling_rel, noise_matrix, settings.strength)

                for sibling_rel in all_set_rel_paths:
                    processed_files.add(sibling_rel)

        # Case D: Standard raw layout (Fallback generic handling)
        else:
            scale_res = scale_image(file_path, settings.scaler_modifier, Image.Resampling.NEAREST)
            if scale_res:
                w, h = scale_res
                rng = generate_seeded_random_generator(rel_path.as_posix())
                create_and_apply_noise_grid(file_path, rng, w, h, settings.strength, columns=1, rows=1)
            processed_files.add(rel_path)


def enforce_max_log_count(dir_path: Path, max_count: int, script_name: str) -> None:
    """
    Enforce a maximum number of log files for this script.

    Rules:
    - Only affects files ending with `.log`
    - Only affects logs that contain the script name
    - Sorting is performed lexicographically by filename
    """
    if max_count <= 0:
        return

    if not dir_path.exists():
        return

    log_files = [f for f in dir_path.glob("*.log") if script_name in f.name]
    if len(log_files) <= max_count:
        return
    log_files.sort(key=lambda p: p.name)
    to_delete = log_files[:-max_count]
    for file in to_delete:
        try:
            file.unlink()
            logger.debug("Removed old log %s", file)
        except OSError as e:
            logger.debug("Failed removing old log %s: %s", file, e)


def build_log_path(log_settings: LogSettings) -> Path | None:
    """
    Builds the final log file path based on logging mode.
    """
    if log_settings.mode == "console_only":
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    day_stamp = datetime.now().strftime("%Y%m%d")

    script_name = Path(__file__).stem
    pc_name = socket.gethostname()

    log_dir = Path(log_settings.folder).expanduser().resolve()

    match log_settings.mode:
        case "per_run":
            filename = f"{timestamp}__{script_name}__{pc_name}.log"
        case "latest":
            filename = f"latest_{script_name}__{pc_name}.log"
        case "per_day":
            filename = f"{day_stamp}__{script_name}__{pc_name}.log"
        case "single_file":
            filename = f"{script_name}__{pc_name}.log"
        case _:
            filename = f"{timestamp}__{script_name}__{pc_name}.log"

    return log_dir / filename


class JsonArgsFilter(logging.Filter):
    """
    Automatically formats log arguments using JSON serialization rules.
    Guarantees double quotes around strings and paths without manual formatting.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if record.args:
            # Normalize arguments into a flat list for processing
            raw_args = list(record.args) if isinstance(record.args, tuple) else [record.args]
            processed_args: list[str] = []

            for val in raw_args:
                if isinstance(val, Path):
                    processed_args.append(json.dumps(val.as_posix(), default=str))
                elif isinstance(val, str):
                    processed_args.append(json.dumps(val))
                else:
                    processed_args.append(json.dumps(val, default=str))

            # Cast back to tuple so the logger can unpack it safely
            record.args = tuple(processed_args)
        return True


def setup_logging(logger_obj: logging.Logger, log_settings: LogSettings) -> Path | None:
    """
    Set up console and file logging.
    """
    logger_obj.handlers.clear()
    logger_obj.setLevel(logging.DEBUG)
    logger_obj.propagate = False

    # Attach the automatic JSON formatting filter
    logger_obj.addFilter(JsonArgsFilter())

    log_path = build_log_path(log_settings)

    formatter = logging.Formatter(
        log_settings.message_format,
        datefmt=log_settings.date_format,
    )

    if log_path:
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)

        except OSError as e:
            raise RuntimeError(f"Failed creating log directory {log_path.parent}") from e

        file_handler: logging.Handler

        match log_settings.mode:
            case "per_day":
                file_handler = TimedRotatingFileHandler(filename=log_path, when="midnight", interval=1, backupCount=log_settings.max_files or 0, encoding="utf-8")
            case "single_file":
                file_handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
            case _:
                file_handler = logging.FileHandler(log_path, mode="w", encoding="utf-8")

        file_handler.setLevel(log_settings.file_level)
        file_handler.setFormatter(formatter)
        logger_obj.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_settings.console_level)
    console_handler.setFormatter(formatter)

    logger_obj.addHandler(console_handler)

    write_banner(logger_obj)

    if log_buffer:
        class _ForwardToLogger(logging.Handler):
            def emit(self, record):
                logger_obj.handle(record)

        forward_handler = _ForwardToLogger()
        log_buffer.setTarget(forward_handler)
        log_buffer.flush()
        log_buffer.close()

    if (log_settings.max_files and log_path and log_settings.mode not in ("per_day", "console_only")):
        enforce_max_log_count(dir_path=log_path.parent, max_count=log_settings.max_files, script_name=Path(__file__).stem)

    return log_path


def write_banner(logger_obj: logging.Logger):
    """
    Writes a clean session banner without log prefixes.
    """
    separator = "-" * 80

    banner = (
        f"{separator}\n"
        f"SCRIPT     | {json.dumps(Path(__file__).resolve().as_posix())}\n"
        f"VERSION    | {__version__}\n"
        f"START TIME | {datetime.now().isoformat(timespec='milliseconds')}\n"
        f"USER       | {os.getlogin()}\n"
        f"HOST       | {socket.gethostname()}\n"
        f"RUNTIME    | Python {sys.version.split()[0]}\n"
        f"{separator}"
    )

    original_formatters = {}

    class RawFormatter(logging.Formatter):
        """
        Formatter that outputs only the log message with no prefixes.
        """

        def format(self, record):
            return record.getMessage()

    try:
        for handler in logger_obj.handlers:
            original_formatters[handler] = handler.formatter
            handler.setFormatter(RawFormatter())

        logger_obj.info(banner)

    finally:
        for handler, formatter in original_formatters.items():
            handler.setFormatter(formatter)


def bootstrap():
    exit_code = 0
    log_path: Path | None = None
    config = Config()

    try:
        log_path = setup_logging(logger_obj=logger, log_settings=config.log_settings)
        main(config)

    except KeyboardInterrupt:
        logger.warning("Operation interrupted by user.")
        exit_code = 130

    except Exception as e:
        logger.exception("A fatal error has occurred: %s", e)
        exit_code = 1

    if (config.log_settings.open_log_after_run and log_path and log_path.exists()):
        try:
            match sys.platform:
                case plat if plat.startswith("win"):
                    os.startfile(log_path)
                case "darwin":
                    os.system(f'open "{log_path}"')
                case _:
                    os.system(f'xdg-open "{log_path}"')

        except Exception as e:
            logger.warning("Failed to open log file: %s", e)

    if (config.runtime_settings.always_pause or (config.runtime_settings.pause_on_error and exit_code != 0)):
        input("Press Enter to exit...")

    return exit_code


if __name__ == "__main__":
    sys.exit(bootstrap())
