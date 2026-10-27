#!/usr/bin/env python3
"""
Generate an SVG visualisation of a GNU Make build profile.
Uses the drawsvg library.
"""

import sys
import re
import csv
from collections import defaultdict
import drawsvg as draw
from profile import Profile

# --- Visualization Logic ---


class TargetType:
    """Determines color and short name for a build target."""

    # Configuration list: (regex_pattern, description, color_hex)
    CLASSES = [
        (r".*\.h$", "generated C header", "#FFFF00"),  # Yellow
        (r".*\.c$", "generated C source", "#6A5ACD"),  # SlateBlue
        (r".*\.o$", "compiled object file", "#FF6347"),  # Tomato
        (r"^make$", "make", "#F5DEB3"),  # Wheat
        (r".*", "unknown", "#32CD32"),  # LimeGreen
    ]

    SHORTNAME_RE = re.compile(r".*/([^/]+)$")

    @classmethod
    def get_style(cls, target: str):
        """Returns (color, short_text) for the given target."""
        clean_target = target.split()[0] if " " in target else target

        for pattern_str, desc, color_hex in cls.CLASSES:
            if re.match(pattern_str, clean_target):
                # Extract filename from path
                match = cls.SHORTNAME_RE.search(clean_target)
                short_name = match.group(1) if match else clean_target
                return color_hex, short_name

        # Fallback
        return "#FFFFFF", target


def generate_svg(
    profile: Profile, output_filename: str, width_px: int = 2000, height_px: int = 1000
):
    """Generates the SVG file using drawsvg."""

    if not profile.notional_cpus:
        print("No data to visualize.")
        return

    num_cpus = len(profile.notional_cpus)
    time_range = profile.end_time - profile.start_time

    if time_range <= 0:
        print("Invalid time range.")
        return

    # Margins for axes and labels
    margin_left = 50
    margin_top = 40
    margin_bottom = 50
    margin_right = 20

    plot_width = width_px - margin_left - margin_right
    plot_height = height_px - margin_top - margin_bottom

    # Y-axis scaling: each CPU gets a row
    row_height = plot_height / num_cpus

    # X-axis scaling: time to pixels
    scale_x = plot_width / time_range

    # Create Drawing object
    d = draw.Drawing(width_px, height_px)

    # Background
    d.append(draw.Rectangle(0, 0, width_px, height_px, fill="#FFFFFF"))

    # Title
    d.append(
        draw.Text(
            "GNU Make Build Profile",
            18,
            margin_left,
            20,
            fill="black",
            font_family="sans-serif",
        )
    )

    for cpu_idx, tasks in enumerate(profile.notional_cpus):
        y_base = margin_top + (cpu_idx * row_height)
        y_label_center = y_base + (row_height / 2)

        # CPU Label on Y-axis
        d.append(
            draw.Text(
                f"CPU {cpu_idx}",
                14,
                0,
                y_label_center,
                fill="gray",
                font_family="sans-serif",
                text_anchor="end",
            )
        )

        for start, duration, target in tasks:
            # Calculate X position and Width
            rel_time = start - profile.start_time
            x_pos = margin_left + (rel_time * scale_x)
            bar_width = max(0, duration * scale_x)

            # Height of the bar (with some padding within the row)
            padding = 5
            bar_height = max(2, row_height - padding)
            y_pos = y_base + (padding / 2)

            # Get Color and Text
            color, short_text = TargetType.get_style(target)

            # Draw Rectangle
            rect = draw.Rectangle(
                x_pos,
                y_pos,
                bar_width,
                bar_height,
                fill=color,
                stroke="#000000",
                stroke_width=1,
            )
            d.append(rect)

            # Draw Text (Target Name)
            # Only draw text if the bar is wide enough to avoid clutter
            font_size = 12
            if bar_width > 40:
                # Ensure text doesn't overflow visually too badly, though SVG handles it
                d.append(
                    draw.Text(
                        short_text,
                        font_size,
                        x_pos + 5,  # slight offset from left edge
                        y_pos + (bar_height / 2) + 5,  # vertical center approx
                        fill="black",
                        stroke="black",
                        stroke_width=0.5,
                        font_family="sans-serif",
                    )
                )

    # Save the SVG
    d.save_svg(output_filename)
    print(f"Saved profile visualization to {output_filename}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python make_profile_svg.py <csv_file> [output.svg]")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "profile.svg"

    try:
        profile = Profile.from_file(csv_file)
        generate_svg(profile, output_file)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
