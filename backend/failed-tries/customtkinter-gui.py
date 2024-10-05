import customtkinter as ctk
import os
import random
import colorsys
import threading
from PIL import Image, ImageDraw, ImageChops
from tkinter import filedialog


class ArtGeneratorGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("NFT Art Generator")
        self.window.geometry("500x500")

        # Input fields
        self.collection_name = ctk.CTkEntry(
            self.window, placeholder_text="Collection name", width=350
        )
        self.collection_name.pack(pady=25)

        self.num_images = ctk.CTkEntry(
            self.window, placeholder_text="Number of images", width=350
        )
        self.num_images.insert(0, "1")
        self.num_images.pack(pady=25)

        # Output directory
        self.output_dir = ctk.CTkEntry(
            self.window, placeholder_text="Output directory", width=350
        )
        self.output_dir.insert(0, os.getcwd())
        self.output_dir.pack(pady=25)

        browse_button = ctk.CTkButton(
            self.window, text="Browse path", command=self.browse_output_dir
        )
        browse_button.pack(pady=10)

        # Generate button
        generate_button = ctk.CTkButton(
            self.window, text="Generate art", command=self.generate_art
        )
        generate_button.pack(pady=10)

        # Status label
        self.status_label = ctk.CTkLabel(self.window, text="")
        self.status_label.pack(pady=10)

    def browse_output_dir(self):
        dir_path = filedialog.askdirectory()
        self.output_dir.delete(0, "end")
        self.output_dir.insert(0, dir_path)

    def generate_art(self):
        collection_name = self.collection_name.get()
        num_images = int(self.num_images.get())
        output_dir = self.output_dir.get()

        if not collection_name:
            error_window = ctk.CTkToplevel(self.window)
            error_window.title("Error")
            error_label = ctk.CTkLabel(
                error_window, text="Please enter a collection name."
            )
            error_label.pack()
            error_window.configure(width=200, height=100)
            error_window.resizable(False, False)
            return

        self.status_label.configure(text="Generating art...")

        # Run art generation in separate thread to avoid blocking GUI
        thread = threading.Thread(
            target=self.run_art_generation,
            args=(collection_name, num_images, output_dir),
        )
        thread.start()

    def run_art_generation(self, collection_name, num_images, output_dir):
        for i in range(num_images):
            self.status_label.configure(
                text=f"Generating image(s): {i+1} of {num_images}..."
            )

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
            max_y = max([p[1] for p in points])

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

        self.status_label.configure("Art generation completed!")

        def random_color(self):
            hue = random.random()
            saturation = random.uniform(0.5, 1.0)
            value = random.uniform(0.5, 1.0)
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            return (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = ArtGeneratorGUI()
    gui.run()
