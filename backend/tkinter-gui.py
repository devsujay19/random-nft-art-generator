import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import colorsys
from PIL import Image, ImageDraw, ImageChops
import threading


class ArtGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Art Generator")
        self.root.config(background="#2b2b2b")
        self.root.geometry("500x400")

        # Input fields
        self.input_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.input_frame.pack(pady=20)

        self.collection_label = tk.Label(
            self.input_frame, text="Collection Name:", fg="#fff", bg="#2b2b2b"
        )
        self.collection_label.pack()
        self.collection_name = tk.Entry(
            self.input_frame, width=50, font=("Arial", 12), bg="#3b3b3b", fg="#fff"
        )
        self.collection_name.pack()

        self.num_images_label = tk.Label(
            self.input_frame, text="Number of Images:", fg="#fff", bg="#2b2b2b"
        )
        self.num_images_label.pack()
        self.num_images = tk.Entry(
            self.input_frame, width=10, font=("Arial", 12), bg="#3b3b3b", fg="#fff"
        )
        self.num_images.insert(0, "1")
        self.num_images.pack()

        # Buttons
        self.button_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.button_frame.pack(pady=20)

        self.generate_button = tk.Button(
            self.button_frame,
            text="Generate Art",
            command=self.generate_art,
            bg="#4CAF50",
            fg="#fff",
            font=("Arial", 12),
        )
        self.generate_button.pack(side=tk.LEFT, padx=10)

        self.browse_button = tk.Button(
            self.button_frame,
            text="Browse Output Directory",
            command=self.browse_output_dir,
            bg="#4CAF50",
            fg="#fff",
            font=("Arial", 12),
        )
        self.browse_button.pack(side=tk.LEFT, padx=10)

        # Output directory
        self.output_dir_label = tk.Label(
            self.root, text="Output Directory:", fg="#fff", bg="#2b2b2b"
        )
        self.output_dir_label.pack()
        self.output_dir = tk.Entry(
            self.root, width=50, font=("Arial", 12), bg="#3b3b3b", fg="#fff"
        )
        self.output_dir.insert(0, os.getcwd())
        self.output_dir.pack()

        # Status label
        self.status_label = tk.Label(self.root, text="", fg="#fff", bg="#2b2b2b")
        self.status_label.pack()

    def browse_output_dir(self):
        dir_path = filedialog.askdirectory()
        self.output_dir.delete(0, tk.END)
        self.output_dir.insert(0, dir_path)

    def generate_art(self):
        collection_name = self.collection_name.get()
        num_images = int(self.num_images.get())
        output_dir = self.output_dir.get()

        if not collection_name:
            messagebox.showerror("Error", "Please enter a collection name")
            return

        self.status_label.config(text="Generating art...")

        # Run art generation in separate thread to avoid blocking GUI
        thread = threading.Thread(
            target=self.run_art_generation,
            args=(collection_name, num_images, output_dir),
        )
        thread.start()

    def run_art_generation(self, collection_name, num_images, output_dir):
        for i in range(num_images):
            self.status_label.config(text=f"Generating image {i+1} of {num_images}...")

            # Set size parameters.
            rescale = 2
            image_size_px = 128 * rescale
            padding = 12 * rescale

            # Create the directory and base image.
            image_path = os.path.join(
                output_dir, collection_name, f"{collection_name}_art_{i}.png"
            )
            os.makedirs(os.path.join(output_dir, collection_name), exist_ok=True)
            bg_color = (0, 0, 0)
            image = Image.new("RGB", (image_size_px, image_size_px), bg_color)

            # How many lines do we want to draw?
            num_lines = 10
            points = []

            # Pick the colors.
            start_color = self.random_color()
            end_color = self.random_color()

            # Generate points to draw.
            for _ in range(num_lines):
                point = (
                    self.random_point(image_size_px, padding),
                    self.random_point(image_size_px, padding),
                )
                points.append(point)

            # Center image.
            # Find the bounding box.
            min_x = min([p[0] for p in points])
            max_x = max([p[0] for p in points])
            min_y = min([p[1] for p in points])
            max_y = min([p[1] for p in points])

            # Find offsets.
            x_offset = (min_x - padding) - (image_size_px - padding - max_x)
            y_offset = (min_y - padding) - (image_size_px - padding - max_y)

            # Move all points by offset.
            for j, point in enumerate(points):
                points[j] = (point[0] - x_offset // 2, point[1] - y_offset // 2)

            # Draw the points.
            current_thickness = 1 * rescale
            n_points = len(points) - 1
            for j, point in enumerate(points):

                # Create the overlay.
                overlay_image = Image.new(
                    "RGB", (image_size_px, image_size_px), (0, 0, 0)
                )
                overlay_draw = ImageDraw.Draw(overlay_image)

                if j == n_points:
                    # Connect the last point back to the first.
                    next_point = points[0]
                else:
                    # Otherwise connect it to the next element.
                    next_point = points[j + 1]

                # Find the right color.
                factor = j / n_points
                line_color = self.interpolate(start_color, end_color, factor=factor)

                # Draw the line.
                overlay_draw.line(
                    [point, next_point], fill=line_color, width=current_thickness
                )

                # Increase the thickness.
                current_thickness += rescale

                # Add the overlay channel.
                image = ImageChops.add(image, overlay_image)

            # Image is done! Now resize it to be smooth.
            image = image.resize(
                (image_size_px // rescale, image_size_px // rescale),
                resample=Image.Resampling.LANCZOS,
            )

            # Save the image.
            image.save(image_path)

        self.status_label.config(text="Art generation complete!")

    def random_point(self, image_size_px: int, padding: int):
        return random.randint(padding, image_size_px - padding)

    def random_color(self):

        # I want a bright, vivid color, so max V and S and only randomize HUE.
        h = random.random()
        s = 1
        v = 1
        float_rbg = colorsys.hsv_to_rgb(h, s, v)

        # Return as integer RGB.
        return (
            int(float_rbg[0] * 255),
            int(float_rbg[1] * 255),
            int(float_rbg[2] * 255),
        )

    def interpolate(self, start_color, end_color, factor: float):
        # Find the color that is exactly factor (0.0 - 1.0) between the two colors.
        new_color_rgb = []
        for i in range(3):
            new_color_value = factor * end_color[i] + (1 - factor) * start_color[i]
            new_color_rgb.append(int(new_color_value))

        return tuple(new_color_rgb)


if __name__ == "__main__":
    root = tk.Tk()
    gui = ArtGeneratorGUI(root)
    root.mainloop()
