import os
import cv2
import glob
import imageio.v2 as imageio  # pip install imageio

def stitched_image_to_gif(
    input_folder="./static/video1/",
    output_folder="./output_gifs/",
    frames_per_strip=10,
    fps=2,
):
    """
    Converts each stitched strip image in input_folder into a GIF animation.

    Assumptions:
      - Each image is a horizontal concat of `frames_per_strip` frames.
      - Layout: [frame0 | frame1 | ... | frame9] left -> right.
      - All subframes have same height and width.
    """

    os.makedirs(output_folder, exist_ok=True)

    # grab common image formats
    exts = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tif", "*.tiff")
    image_paths = []
    for ext in exts:
        image_paths.extend(glob.glob(os.path.join(input_folder, ext)))

    if not image_paths:
        print(f"[WARN] No images found in {input_folder}")
        return

    for img_path in sorted(image_paths):
        stitched = cv2.imread(img_path)
        if stitched is None:
            print(f"[ERROR] Failed to read {img_path}, skipping.")
            continue

        H, W_total, C = stitched.shape

        if W_total % frames_per_strip != 0:
            print(f"[WARN] {img_path}: total width {W_total} not divisible by {frames_per_strip}")

        frame_W = W_total // frames_per_strip

        frames = []
        for i in range(frames_per_strip):
            x0 = i * frame_W
            x1 = x0 + frame_W
            frame = stitched[:, x0:x1, :]

            # Convert from BGR (OpenCV) to RGB (for GIF)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)

        base_name = os.path.splitext(os.path.basename(img_path))[0]
        out_path = os.path.join(output_folder, f"{base_name}.gif")

        # Duration per frame = 1 / fps seconds
        imageio.mimsave(out_path, frames, duration=1 / fps)
        print(f"[OK] Wrote {out_path} ({len(frames)} frames, {frame_W}x{H}@{fps}fps)")

if __name__ == "__main__":
    stitched_image_to_gif(
        input_folder="./static/video1/",
        output_folder="./output_gifs/",
        frames_per_strip=10,
        fps=2,
    )
