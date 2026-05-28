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
    assets_dir: Path = Path(r"assets")
    scaler_modifier: int = 4
    strength: float = 0.075
    supported_extensions: list[str] = field(default_factory=lambda: [".png"])
    animated_textures: list[dict] = field(default_factory=lambda: [
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\blast_furnace_front_on.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\copper_lantern.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\exposed_copper_lantern.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\lantern.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\magma.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\oxidized_copper_lantern.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\smoker_front_on.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\soul_lantern.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\stonecutter_saw.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\weathered_copper_lantern.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\campfire_log_lit.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\chain_command_block_back.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\chain_command_block_conditional.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\chain_command_block_front.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\chain_command_block_side.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\command_block_back.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\command_block_conditional.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\command_block_front.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\command_block_side.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\prismarine.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\repeating_command_block_back.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\repeating_command_block_conditional.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\repeating_command_block_front.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\repeating_command_block_side.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk_vein.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\soul_campfire_log_lit.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\crimson_stem.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sea_lantern.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\warped_stem.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\campfire_fire.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk_catalyst_side_bloom.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk_catalyst_top_bloom.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\soul_campfire_fire.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\firefly_bush_emissive.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk_shrieker_can_summon_inner_top.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk_shrieker_inner_top.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk_sensor_tendril_active.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\sculk_sensor_tendril_inactive.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\seagrass.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\tall_seagrass_bottom.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\tall_seagrass_top.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\kelp.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\kelp_plant.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\lava_still.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\fire_0.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\fire_1.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\nether_portal.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\respawn_anchor_top.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\soul_fire_0.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\soul_fire_1.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\water_still.png"),
            "columns": 1
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\lava_flow.png"),
            "columns": 2
        },
        {
            "type": "vanilla_spritesheet",
            "path": Path(r"block\water_flow.png"),
            "columns": 2
        },
        {
            "type": "image_set",
            "paths": [
                Path(r"item\clock_00.png"),
                Path(r"item\clock_01.png"),
                Path(r"item\clock_02.png"),
                Path(r"item\clock_03.png"),
                Path(r"item\clock_04.png"),
                Path(r"item\clock_05.png"),
                Path(r"item\clock_06.png"),
                Path(r"item\clock_07.png"),
                Path(r"item\clock_08.png"),
                Path(r"item\clock_09.png"),
                Path(r"item\clock_10.png"),
                Path(r"item\clock_11.png"),
                Path(r"item\clock_12.png"),
                Path(r"item\clock_13.png"),
                Path(r"item\clock_14.png"),
                Path(r"item\clock_15.png"),
                Path(r"item\clock_16.png"),
                Path(r"item\clock_17.png"),
                Path(r"item\clock_18.png"),
                Path(r"item\clock_19.png"),
                Path(r"item\clock_20.png"),
                Path(r"item\clock_21.png"),
                Path(r"item\clock_22.png"),
                Path(r"item\clock_23.png"),
                Path(r"item\clock_24.png"),
                Path(r"item\clock_25.png"),
                Path(r"item\clock_26.png"),
                Path(r"item\clock_27.png"),
                Path(r"item\clock_28.png"),
                Path(r"item\clock_29.png"),
                Path(r"item\clock_30.png"),
                Path(r"item\clock_31.png"),
                Path(r"item\clock_32.png"),
                Path(r"item\clock_33.png"),
                Path(r"item\clock_34.png"),
                Path(r"item\clock_35.png"),
                Path(r"item\clock_36.png"),
                Path(r"item\clock_37.png"),
                Path(r"item\clock_38.png"),
                Path(r"item\clock_39.png"),
                Path(r"item\clock_40.png"),
                Path(r"item\clock_41.png"),
                Path(r"item\clock_42.png"),
                Path(r"item\clock_43.png"),
                Path(r"item\clock_44.png"),
                Path(r"item\clock_45.png"),
                Path(r"item\clock_46.png"),
                Path(r"item\clock_47.png"),
                Path(r"item\clock_48.png"),
                Path(r"item\clock_49.png"),
                Path(r"item\clock_50.png"),
                Path(r"item\clock_51.png"),
                Path(r"item\clock_52.png"),
                Path(r"item\clock_53.png"),
                Path(r"item\clock_54.png"),
                Path(r"item\clock_55.png"),
                Path(r"item\clock_56.png"),
                Path(r"item\clock_57.png"),
                Path(r"item\clock_58.png"),
                Path(r"item\clock_59.png"),
                Path(r"item\clock_60.png"),
                Path(r"item\clock_61.png"),
                Path(r"item\clock_62.png"),
                Path(r"item\clock_63.png"),
            ]
        },
        {
            "type": "image_set",
            "paths": [
                Path(r"item\compass_00.png"),
                Path(r"item\compass_01.png"),
                Path(r"item\compass_02.png"),
                Path(r"item\compass_03.png"),
                Path(r"item\compass_04.png"),
                Path(r"item\compass_05.png"),
                Path(r"item\compass_06.png"),
                Path(r"item\compass_07.png"),
                Path(r"item\compass_08.png"),
                Path(r"item\compass_09.png"),
                Path(r"item\compass_10.png"),
                Path(r"item\compass_11.png"),
                Path(r"item\compass_12.png"),
                Path(r"item\compass_13.png"),
                Path(r"item\compass_14.png"),
                Path(r"item\compass_15.png"),
                Path(r"item\compass_16.png"),
                Path(r"item\compass_17.png"),
                Path(r"item\compass_18.png"),
                Path(r"item\compass_19.png"),
                Path(r"item\compass_20.png"),
                Path(r"item\compass_21.png"),
                Path(r"item\compass_22.png"),
                Path(r"item\compass_23.png"),
                Path(r"item\compass_24.png"),
                Path(r"item\compass_25.png"),
                Path(r"item\compass_26.png"),
                Path(r"item\compass_27.png"),
                Path(r"item\compass_28.png"),
                Path(r"item\compass_29.png"),
                Path(r"item\compass_30.png"),
                Path(r"item\compass_31.png"),
            ]
        },
        {
            "type": "image_set",
            "paths": [
                Path(r"item\crossbow_arrow.png"),
                Path(r"item\crossbow_firework.png"),
                Path(r"item\crossbow_pulling_0.png"),
                Path(r"item\crossbow_pulling_1.png"),
                Path(r"item\crossbow_pulling_2.png"),
                Path(r"item\crossbow_standby.png"),
            ]
        },
        {
            "type": "image_set",
            "paths": [
                Path(r"item\recovery_compass_00.png"),
                Path(r"item\recovery_compass_01.png"),
                Path(r"item\recovery_compass_02.png"),
                Path(r"item\recovery_compass_03.png"),
                Path(r"item\recovery_compass_04.png"),
                Path(r"item\recovery_compass_05.png"),
                Path(r"item\recovery_compass_06.png"),
                Path(r"item\recovery_compass_07.png"),
                Path(r"item\recovery_compass_08.png"),
                Path(r"item\recovery_compass_09.png"),
                Path(r"item\recovery_compass_10.png"),
                Path(r"item\recovery_compass_11.png"),
                Path(r"item\recovery_compass_12.png"),
                Path(r"item\recovery_compass_13.png"),
                Path(r"item\recovery_compass_14.png"),
                Path(r"item\recovery_compass_15.png"),
                Path(r"item\recovery_compass_16.png"),
                Path(r"item\recovery_compass_17.png"),
                Path(r"item\recovery_compass_18.png"),
                Path(r"item\recovery_compass_19.png"),
                Path(r"item\recovery_compass_20.png"),
                Path(r"item\recovery_compass_21.png"),
                Path(r"item\recovery_compass_22.png"),
                Path(r"item\recovery_compass_23.png"),
                Path(r"item\recovery_compass_24.png"),
                Path(r"item\recovery_compass_25.png"),
                Path(r"item\recovery_compass_26.png"),
                Path(r"item\recovery_compass_27.png"),
                Path(r"item\recovery_compass_28.png"),
                Path(r"item\recovery_compass_29.png"),
                Path(r"item\recovery_compass_30.png"),
                Path(r"item\recovery_compass_31.png"),
            ]
        },
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
    max_files: int | None = 8
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


def get_deterministic_rng(seed_string: str) -> random.Random:
    """
    Creates a deterministic Random instance based on a string (e.g., filename).
    """
    logger.debug("Generating rng...")
    hash_digest = hashlib.md5(seed_string.encode("utf-8")).hexdigest()
    logger.debug("Done")
    return random.Random(int(hash_digest, 16))


def scale_texture_image(file_path: Path, scaler_modifier: int) -> tuple[int, int] | None:
    logger.debug("Scaling x%s...", scaler_modifier)
    try:
        with Image.open(file_path) as image:
            new_width = image.width * scaler_modifier
            new_height = image.height * scaler_modifier
            resized_image = image.resize((new_width, new_height), resample=Image.Resampling.NEAREST)
            resized_image.save(file_path)
            logger.debug("Scaled from %sx%s to %sx%s", image.width, image.height, new_width, new_height)
        return new_width, new_height
    except Exception as e:
        logger.error("An error occurred while scaling media file %s: %s", file_path, e)
        return None


def generate_noise_pattern(width: int, rng: random.Random) -> bytes:
    """
    Generate a square noise texture of size width x width (RGB) using a local RNG.
    Optimized via NumPy to eliminate pure Python loops on high-resolution textures.
    """
    logger.debug("Generating noise pattern...")
    if width <= 0:
        raise ValueError("width must be positive")

    # Pull a 32-bit integer seed from the localized RNG state to stay deterministic
    np_seed = rng.randint(0, 2**32 - 1)

    # Create an isolated NumPy Generator instance so we don't pollute global numpy state
    np_rng = np.random.default_rng(np_seed)

    # Generate the grayscale byte sequence directly (3 channels per pixel)
    # 1. Generate width * width brightness values
    brightness = np_rng.integers(0, 256, size=width * width, dtype=np.uint8)

    # 2. Repeat each brightness value 3 times for RGB alignment, then convert to raw bytes
    # np.repeat is extremely fast and handles the exact layout expected by your frombuffer calls
    noise_bytes = np.repeat(brightness, 3).tobytes()

    logger.debug("Done")
    return noise_bytes


def apply_noise_array(image_path: Path, noise_full: np.ndarray, strength: float) -> None:
    """
    Blends a pre-calculated/tiled noise array onto the target image.
    """
    logger.debug("Applying noise array...")
    try:
        with Image.open(image_path) as img:
            img_rgba = img.convert("RGBA")

        img_arr = np.array(img_rgba).astype(np.float32)

        if img_arr.size == 0 or img_arr.shape[0] == 0 or img_arr.shape[1] == 0:
            logger.warning("Skipping noise application: Image %s has empty dimensions.", image_path)
            return

        if noise_full.shape != img_arr.shape[:2]:
            logger.warning(
                "Skipping noise application: Noise map shape %s does not match image shape %s for %s",
                noise_full.shape, img_arr.shape[:2], image_path
            )
            return

        r, g, b, a = img_arr[..., 0], img_arr[..., 1], img_arr[..., 2], img_arr[..., 3]
        mask = a > 0

        r[mask] = r[mask] * (1 - strength) + r[mask] * noise_full[mask] * strength
        g[mask] = g[mask] * (1 - strength) + g[mask] * noise_full[mask] * strength
        b[mask] = b[mask] * (1 - strength) + b[mask] * noise_full[mask] * strength

        result_arr = np.stack([r, g, b, a], axis=-1).astype(np.uint8)
        logger.debug("Applied.")

        Image.fromarray(result_arr, "RGBA").save(image_path)
        logger.debug("Saved to file.")
    except Exception as e:
        logger.error("Failed to apply noise to %s: %s", image_path, e)


def process_single_image_noise(
    file_path: Path,
    rng: random.Random,
    width: int,
    height: int,
    strength: float,
    columns: int = 1,
) -> None:
    """
    Generates and maps the correct noise layout for a single texture file.
    Handles static textures, vertical sheets, and multi-column layouts safely.
    """
    frame_width = width // columns
    if frame_width == 0:
        frame_width = 1

    noise_bytes = generate_noise_pattern(frame_width, rng)
    noise_arr = np.frombuffer(noise_bytes, dtype=np.uint8).reshape((frame_width, frame_width, 3))
    noise_gray = noise_arr[..., 0] / 255.0

    # Calculate rows required, ensuring it builds at least a 1x1 block framework
    rows = height // frame_width
    if rows == 0:
        rows = 1

    # Tile to cover the potential frame bounds
    noise_full = np.tile(noise_gray, (rows, columns))

    # Crop the tiled matrix down to match the precise image dimensions
    noise_full = noise_full[:height, :width]

    apply_noise_array(file_path, noise_full, strength)


def main(config: Config):
    """
    Processes all Minecraft textures by upscaling them and applying deterministic noise loops.
    """
    settings = config.script_settings
    assets_dir = settings.assets_dir

    if not assets_dir.exists():
        logger.error("Assets directory does not exist: %s", assets_dir)
        return

    logger.info("Scanning for textures in %s", assets_dir)

    valid_exts = {ext.lower() for ext in settings.supported_extensions}

    # 1. Map lookups for quick identification of handled animations
    spritesheet_map = {}
    imageset_first_files = {}
    imageset_siblings = {}

    for anim in settings.animated_textures:
        anim_type = anim.get("type")

        if anim_type == "vanilla_spritesheet":
            spritesheet_map[Path(anim["path"])] = anim.get("columns", 1)

        elif anim_type == "image_set" and anim.get("paths"):
            paths = [Path(p) for p in anim["paths"]]
            first_path = paths[0]
            imageset_first_files[first_path] = paths
            for path in paths:
                imageset_siblings[path] = first_path

    # 2. Gather all valid asset paths relative to the assets folder root
    all_files = [
        f for f in assets_dir.rglob("*")
        if f.is_file() and f.suffix.lower() in valid_exts
    ]

    processed_files = set()

    # 3. First pass: Handle explicitly configured animations to prevent double processing
    for file_path in all_files:
        try:
            rel_path = file_path.relative_to(assets_dir)
        except ValueError:
            continue

        if rel_path in processed_files:
            continue

        logger.debug("Processing %s", file_path)

        # Scenario A: Vanilla Spritesheet
        if rel_path in spritesheet_map:
            columns = spritesheet_map[rel_path]
            scale_res = scale_texture_image(file_path, settings.scaler_modifier)
            if scale_res:
                w, h = scale_res
                rng = get_deterministic_rng(rel_path.as_posix())
                process_single_image_noise(file_path, rng, w, h, settings.strength, columns)
            processed_files.add(rel_path)

        # Scenario B: Image Set (Triggered when encountering the first file of the collection)
        elif rel_path in imageset_first_files:
            all_set_rel_paths = imageset_first_files[rel_path]

            first_absolute_path = assets_dir / rel_path
            scale_res = scale_texture_image(first_absolute_path, settings.scaler_modifier)

            if scale_res:
                w, h = scale_res
                for sibling_rel in all_set_rel_paths[1:]:
                    scale_texture_image(assets_dir / sibling_rel, settings.scaler_modifier)

                rng = get_deterministic_rng(rel_path.as_posix())
                noise_bytes = generate_noise_pattern(w, rng)
                noise_arr = np.frombuffer(noise_bytes, dtype=np.uint8).reshape((w, w, 3))
                noise_gray = noise_arr[..., 0] / 255.0

                # Handle non-square master layouts cleanly
                if h != w:
                    req_rows = h // w
                    if req_rows == 0:
                        req_rows = 1
                    noise_full = np.tile(noise_gray, (req_rows, 1))
                    noise_full = noise_full[:h, :w]
                else:
                    noise_full = noise_gray

                for sibling_rel in all_set_rel_paths:
                    apply_noise_array(assets_dir / sibling_rel, noise_full, settings.strength)
                    processed_files.add(sibling_rel)

        # Scenario C: A sibling file belonging to an image set whose master wasn't hit first
        elif rel_path in imageset_siblings:
            master_rel = imageset_siblings[rel_path]
            if master_rel in processed_files:
                continue

            all_set_rel_paths = imageset_first_files[master_rel]
            scale_res = scale_texture_image(assets_dir / master_rel, settings.scaler_modifier)
            if scale_res:
                w, h = scale_res
                for sibling_rel in all_set_rel_paths:
                    if sibling_rel != master_rel:
                        scale_texture_image(assets_dir / sibling_rel, settings.scaler_modifier)

                rng = get_deterministic_rng(master_rel.as_posix())
                noise_bytes = generate_noise_pattern(w, rng)
                noise_arr = np.frombuffer(noise_bytes, dtype=np.uint8).reshape((w, w, 3))
                noise_gray = noise_arr[..., 0] / 255.0

                if h != w:
                    req_rows = h // w
                    if req_rows == 0:
                        req_rows = 1
                    noise_full = np.tile(noise_gray, (req_rows, 1))
                    noise_full = noise_full[:h, :w]
                else:
                    noise_full = noise_gray

                for sibling_rel in all_set_rel_paths:
                    apply_noise_array(assets_dir / sibling_rel, noise_full, settings.strength)
                    processed_files.add(sibling_rel)

    # 4. Second pass: Process remaining unhandled static images
    for file_path in all_files:
        try:
            rel_path = file_path.relative_to(assets_dir)
        except ValueError:
            continue

        if rel_path in processed_files:
            continue

        scale_res = scale_texture_image(file_path, settings.scaler_modifier)
        if scale_res:
            w, h = scale_res
            rng = get_deterministic_rng(rel_path.as_posix())
            process_single_image_noise(file_path, rng, w, h, settings.strength, columns=1)

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


# import logging
# import pathlib
# import random
# import sys
# import time
# import toml
# import traceback
# import typing
# from datetime import datetime
# from PIL import Image
# import numpy as np

# logger = logging.getLogger(__name__)

# """
# Python Script Template
# """


# def load_config(config_path: str = "config.toml") -> dict:
#     logger.debug("Loading config...")
#     config = toml.load(config_path)

#     logger.debug("Validating config...")
#     required_keys = {
#         "assets_dir": str,
#         "file_extensions": list
#     }
#     for key, expected_type in required_keys.items():
#         if key not in config or not isinstance(config[key], expected_type):
#             raise ValueError(
#                 f"config.toml is missing or has incorrect type for key '{key}' (expected {expected_type.__name__})")
#     if not all(key in config for key in required_keys):
#         raise ValueError(
#             f"config.toml is missing required key(s): {', '.join(sorted(list(set(required_keys) - set(config.keys()))))}")
#     logger.debug("Config loaded successfully.")
#     return config


# def iterate_through_texture_file_paths(config: dict) -> typing.Iterable[pathlib.Path]:
#     assets_dir = pathlib.Path(config["assets_dir"])
#     logger.debug(f"Searching for media files in '{assets_dir}'...")
#     for file_path in assets_dir.rglob("*"):
#         if file_path.is_file():
#             if file_path.suffix[1:] in config["file_extensions"]:
#                 logger.debug(f"Found media file: {file_path}")
#                 yield file_path


# def scale_texture_image(file_path: typing.Union[pathlib.Path, str], scaler_modifier: int) -> typing.Tuple[int, int] | None:
#     file_path = pathlib.Path(file_path)
#     try:
#         logger.debug(f"Scaling media file: {file_path}")
#         from PIL import Image
#         image = Image.open(file_path)
#         new_width = image.width * scaler_modifier
#         new_height = image.height * scaler_modifier
#         image = image.resize((new_width, new_height), resample=Image.NEAREST)
#         image.save(file_path)
#         logger.debug(f"Scaled media file: {file_path}")
#         return (new_width, new_height)
#     except Exception as e:
#         logger.error(f"An error occured while scaling media file: {file_path}\n{traceback.format_exc()}")


# def generate_noise_pattern(width: int) -> bytes:
#     """
#     Generate a square noise texture of size width x width (RGB).
#     :param width: Width and height of the square noise
#     :return: Bytes containing RGB data
#     """
#     if width <= 0:
#         raise ValueError("width must be positive")
#     pixels = bytearray()
#     for _ in range(width * width):
#         brightness = random.randint(0, 255)
#         pixels.extend([brightness, brightness, brightness])
#     return bytes(pixels)


# def apply_noise(image_path, noise_bytes, output_path, strength=0.075):
#     """
#     Apply noise to any image. Treats textures under "textures/block" as vertical strip animations.
#     """
#     logger.debug(f"Applying noise to {image_path}...")
#     img_path = pathlib.Path(image_path)
#     img = Image.open(img_path).convert("RGBA")
#     img_arr = np.array(img).astype(np.float32)
#     height, width = img_arr.shape[:2]

#     # Noise square (width x width)
#     noise_arr = np.frombuffer(noise_bytes, dtype=np.uint8).reshape((width, width, 3))
#     noise_gray = noise_arr[..., 0] / 255.0

#     # Determine if image is animated (block textures) or single-frame
#     if "textures\\block" in str(img_path) or "textures/block" in str(img_path):
#         # Vertical strip animation: tile noise vertically
#         num_tiles = height // width
#         noise_full = np.tile(noise_gray, (num_tiles, 1))
#     else:
#         # Non-animated: just resize noise to match full image
#         noise_img = Image.fromarray((noise_gray * 255).astype(np.uint8), mode="L")
#         noise_full = np.array(noise_img.resize((width, height), resample=Image.NEAREST)) / 255.0

#     # Split channels
#     r, g, b, a = img_arr[..., 0], img_arr[..., 1], img_arr[..., 2], img_arr[..., 3]

#     mask = a > 0

#     # Blend noise
#     r[mask] = r[mask] * (1 - strength) + r[mask] * noise_full[mask] * strength
#     g[mask] = g[mask] * (1 - strength) + g[mask] * noise_full[mask] * strength
#     b[mask] = b[mask] * (1 - strength) + b[mask] * noise_full[mask] * strength

#     result_arr = np.stack([r, g, b, a], axis=-1).astype(np.uint8)
#     logger.debug(f"Saving noised image to {output_path}...")
#     Image.fromarray(result_arr, "RGBA").save(output_path)
#     logger.debug(f"Done applying noise to {image_path}.")


# def main() -> None:
#     config_path = "build_noise_textures.toml"
#     config = load_config(config_path)
#     for texture_file in iterate_through_texture_file_paths(config):
#         scale_result = scale_texture_image(texture_file, 4)
#         if scale_result is None:
#             logger.warning(f"Failed to scale media file: {texture_file}")
#             continue
#         width, height = scale_result
#         noise_pattern = generate_noise_pattern(width)
#         apply_noise(texture_file, noise_pattern, texture_file)


# def setup_logging(
#         logger: logging.Logger,
#         log_file_path: typing.Union[str, pathlib.Path],
#         console_logging_level: int = logging.DEBUG,
#         file_logging_level: int = logging.DEBUG,
#         log_message_format: str = "%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s] [%(name)s]: %(message)s",
#         date_format: str = "%Y-%m-%d %H:%M:%S") -> None:
#     logger.setLevel(file_logging_level)  # Set the overall logging level

#     # File Handler for script-named log file (overwrite each run)
#     file_handler = logging.FileHandler(log_file_path, encoding="utf-8", mode="w")
#     file_handler.setLevel(file_logging_level)
#     file_handler.setFormatter(logging.Formatter(log_message_format, datefmt=date_format))
#     logger.addHandler(file_handler)

#     # Console Handler
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setLevel(console_logging_level)
#     console_handler.setFormatter(logging.Formatter(log_message_format, datefmt=date_format))
#     logger.addHandler(console_handler)

#     # Set specific logging levels if needed
#     # logging.getLogger("requests").setLevel(logging.INFO)


# if __name__ == "__main__":
#     script_name = pathlib.Path(__file__).stem
#     log_file_name = f"{script_name}.log"
#     log_file_path = pathlib.Path(log_file_name)
#     setup_logging(logger, log_file_path, log_message_format="%(asctime)s.%(msecs)03d %(levelname)s [%(funcName)s]: %(message)s")

#     error = 0
#     try:
#         start_time = time.perf_counter()
#         logger.info("Starting operation...")
#         main()
#         end_time = time.perf_counter()
#         duration = end_time - start_time
#         logger.info(f"Completed operation in {duration:.4f}s.")
#     except Exception as e:
#         logger.warning(f"A fatal error has occurred: {repr(e)}\n{traceback.format_exc()}")
#         error = 1
#     finally:
#         sys.exit(error)
