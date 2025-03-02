# ---
# KazLabs Media Group
# Made with ♥ by Liam Sorensen - AI Assisted by Cursor.AI.
# Version 0.1.3 - 2025-03-03
# ---

"""
Texture Normaliser - Main Entry Point

This is the main entry point for the Texture Normaliser application.
It imports the app from the src directory and runs it.
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the app from the src directory
from src.config import config
from src.logger import logger

def main():
    """Main entry point for the application."""
    try:
        # Import the app here to avoid circular imports
        from src.texture_processor import processor
        
        # Log startup information
        logger.info(f"Texture Normaliser v0.1.3 starting up")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Operating system: {sys.platform}")
        
        # Create the app and run it
        import tkinter as tk
        from tkinter import filedialog, messagebox
        import customtkinter as ctk
        from PIL import Image, ImageTk
        
        # Set appearance mode and default color theme
        ctk.set_appearance_mode(config.get("theme", "dark"))
        ctk.set_default_color_theme("blue")
        
        # Create and run the app
        class TextureNormaliserApp(ctk.CTk):
            """
            Main application class for the Texture Normaliser.
            
            # This is the main UI class. It's a mess of widgets and callbacks.
            # But hey, at least it looks pretty. That's what matters, right?
            """
            
            def __init__(self):
                """Initialize the application."""
                super().__init__()
                
                # Configure the window
                self.title("Texture Normaliser")
                self.geometry("1000x800")
                self.minsize(900, 700)
                
                # Initialize variables
                self.is_processing = False
                self.processing_thread = None
                self.file_queue = []
                self.processed_count = 0
                self.total_count = 0
                
                # Create the UI
                self._create_ui()
                
                # Load the logo
                self._load_logo()
                
                # Initialize directories
                self._initialize_directories()
                
                logger.info("Application initialized")
                
            def _load_logo(self):
                """
                Load the application logo.
                
                # Tries to load a logo. If it fails, we'll just use a placeholder.
                # Because branding is important, even when it doesn't work.
                """
                try:
                    logo_path = os.path.join("assets", "logo.png")
                    if os.path.exists(logo_path):
                        # Open the image file
                        image = Image.open(logo_path)
                        # Resize the image to maintain the 5:1 aspect ratio (400x80)
                        image = image.resize((400, 80), Image.LANCZOS)
                        # Convert the image to a PhotoImage
                        self.logo_image = ImageTk.PhotoImage(image)
                        # Update the logo label
                        self.logo_label.configure(image=self.logo_image)
                        logger.info("Logo loaded successfully")
                    else:
                        logger.warning(f"Logo file not found: {logo_path}")
                except Exception as e:
                    logger.error(f"Error loading logo: {e}")
                    
            def _initialize_directories(self):
                """
                Initialize the import and export directories.
                
                # Creates directories if they don't exist.
                # Because apparently users can't be trusted to create their own folders.
                """
                # Create import directory if it doesn't exist
                import_dir = "./import/"
                if not os.path.exists(import_dir):
                    os.makedirs(import_dir)
                    logger.info(f"Created import directory: {import_dir}")
                    
                # Create export directory if it doesn't exist
                export_dir = config.get("export_directory", "./export/")
                if not os.path.exists(export_dir):
                    os.makedirs(export_dir)
                    logger.info(f"Created export directory: {export_dir}")
                    
            def _create_ui(self):
                """
                Create the user interface.
                
                # This function creates all the UI elements.
                # It's way too long and should be split up, but who has time for that?
                """
                # Create main frame
                self.main_frame = ctk.CTkFrame(self)
                self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Create header frame
                self.header_frame = ctk.CTkFrame(self.main_frame)
                self.header_frame.pack(fill=tk.X, padx=10, pady=10)
                
                # Logo placeholder - now centered and larger
                self.logo_label = ctk.CTkLabel(self.header_frame, text="")
                self.logo_label.pack(pady=10)
                
                self.version_label = ctk.CTkLabel(
                    self.header_frame, 
                    text="Version 0.1.3", 
                    font=ctk.CTkFont(size=12)
                )
                self.version_label.pack(pady=(0, 10))
                
                # Create content frame with two columns
                self.content_frame = ctk.CTkFrame(self.main_frame)
                self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Left column - Controls
                self.controls_frame = ctk.CTkFrame(self.content_frame)
                self.controls_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5), pady=0)
                
                # Options frame
                self.options_frame = ctk.CTkFrame(self.controls_frame)
                self.options_frame.pack(fill=tk.X, padx=10, pady=10)
                
                self.options_label = ctk.CTkLabel(
                    self.options_frame, 
                    text="Options", 
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                self.options_label.pack(anchor=tk.W, padx=10, pady=5)
                
                # Normal Map option
                self.normal_map_var = tk.BooleanVar(value=config.get("enable_normal_map", True))
                self.normal_map_checkbox = ctk.CTkCheckBox(
                    self.options_frame, 
                    text="Enable Normal Map", 
                    variable=self.normal_map_var,
                    command=self._on_normal_map_changed
                )
                self.normal_map_checkbox.pack(anchor=tk.W, padx=10, pady=5)
                
                # Bump Map option
                self.bump_map_var = tk.BooleanVar(value=config.get("enable_bump_map", True))
                self.bump_map_checkbox = ctk.CTkCheckBox(
                    self.options_frame, 
                    text="Enable Bump Map", 
                    variable=self.bump_map_var,
                    command=self._on_bump_map_changed
                )
                self.bump_map_checkbox.pack(anchor=tk.W, padx=10, pady=5)
                
                # AO/Roughness option
                self.ao_roughness_var = tk.BooleanVar(value=config.get("enable_ao_roughness", False))
                self.ao_roughness_checkbox = ctk.CTkCheckBox(
                    self.options_frame, 
                    text="Enable AO/Roughness", 
                    variable=self.ao_roughness_var,
                    command=self._on_ao_roughness_changed
                )
                self.ao_roughness_checkbox.pack(anchor=tk.W, padx=10, pady=5)
                
                # Kernel size option
                self.kernel_size_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
                self.kernel_size_frame.pack(fill=tk.X, padx=10, pady=5)
                
                self.kernel_size_label = ctk.CTkLabel(self.kernel_size_frame, text="Kernel Size:")
                self.kernel_size_label.pack(side=tk.LEFT, padx=(0, 10))
                
                self.kernel_size_var = tk.StringVar(value=str(config.get("sobel_kernel_size", 5)))
                self.kernel_size_options = ["3", "5", "7", "9"]
                self.kernel_size_dropdown = ctk.CTkOptionMenu(
                    self.kernel_size_frame, 
                    values=self.kernel_size_options,
                    variable=self.kernel_size_var,
                    command=self._on_kernel_size_changed
                )
                self.kernel_size_dropdown.pack(side=tk.LEFT)
                
                # Export directory option
                self.export_dir_frame = ctk.CTkFrame(self.options_frame)
                self.export_dir_frame.pack(fill=tk.X, padx=10, pady=10)
                
                self.export_dir_label = ctk.CTkLabel(self.export_dir_frame, text="Export Directory:")
                self.export_dir_label.pack(anchor=tk.W, padx=0, pady=5)
                
                self.export_dir_var = tk.StringVar(value=config.get("export_directory", "./export/"))
                self.export_dir_entry = ctk.CTkEntry(
                    self.export_dir_frame, 
                    textvariable=self.export_dir_var,
                    width=200
                )
                self.export_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), pady=0)
                
                self.export_dir_button = ctk.CTkButton(
                    self.export_dir_frame, 
                    text="Browse", 
                    width=80,
                    command=self._browse_export_dir
                )
                self.export_dir_button.pack(side=tk.RIGHT)
                
                # Theme option
                self.theme_frame = ctk.CTkFrame(self.options_frame, fg_color="transparent")
                self.theme_frame.pack(fill=tk.X, padx=10, pady=5)
                
                self.theme_label = ctk.CTkLabel(self.theme_frame, text="Theme:")
                self.theme_label.pack(side=tk.LEFT, padx=(0, 10))
                
                self.theme_var = tk.StringVar(value=config.get("theme", "dark").capitalize())
                self.theme_options = ["Dark", "Light", "System"]
                self.theme_dropdown = ctk.CTkOptionMenu(
                    self.theme_frame, 
                    values=self.theme_options,
                    variable=self.theme_var,
                    command=self._on_theme_changed
                )
                self.theme_dropdown.pack(side=tk.LEFT)
                
                # Action buttons
                self.actions_frame = ctk.CTkFrame(self.controls_frame)
                self.actions_frame.pack(fill=tk.X, padx=10, pady=10)
                
                self.actions_label = ctk.CTkLabel(
                    self.actions_frame, 
                    text="Actions", 
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                self.actions_label.pack(anchor=tk.W, padx=10, pady=5)
                
                self.select_files_button = ctk.CTkButton(
                    self.actions_frame, 
                    text="Select Files", 
                    command=self._select_files
                )
                self.select_files_button.pack(fill=tk.X, padx=10, pady=5)
                
                self.select_folder_button = ctk.CTkButton(
                    self.actions_frame, 
                    text="Select Folder", 
                    command=self._select_folder
                )
                self.select_folder_button.pack(fill=tk.X, padx=10, pady=5)
                
                self.process_button = ctk.CTkButton(
                    self.actions_frame, 
                    text="Process", 
                    command=self._start_processing
                )
                self.process_button.pack(fill=tk.X, padx=10, pady=5)
                
                self.stop_button = ctk.CTkButton(
                    self.actions_frame, 
                    text="Stop", 
                    command=self._stop_processing,
                    state="disabled"
                )
                self.stop_button.pack(fill=tk.X, padx=10, pady=5)
                
                self.open_export_button = ctk.CTkButton(
                    self.actions_frame, 
                    text="Open Export Folder", 
                    command=self._open_export_folder
                )
                self.open_export_button.pack(fill=tk.X, padx=10, pady=5)
                
                # Right column - Log and status
                self.log_frame = ctk.CTkFrame(self.content_frame)
                self.log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=0)
                
                # Status frame
                self.status_frame = ctk.CTkFrame(self.log_frame)
                self.status_frame.pack(fill=tk.X, padx=10, pady=10)
                
                self.status_label = ctk.CTkLabel(
                    self.status_frame, 
                    text="Status: Ready", 
                    font=ctk.CTkFont(size=14)
                )
                self.status_label.pack(side=tk.LEFT, padx=10)
                
                self.progress_frame = ctk.CTkFrame(self.log_frame)
                self.progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
                
                self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
                self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
                self.progress_bar.set(0)
                
                self.progress_label = ctk.CTkLabel(self.progress_frame, text="0/0 files processed")
                self.progress_label.pack(padx=10, pady=5)
                
                # Log area
                self.log_label = ctk.CTkLabel(
                    self.log_frame, 
                    text="Log", 
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                self.log_label.pack(anchor=tk.W, padx=10, pady=5)
                
                self.log_text = ctk.CTkTextbox(self.log_frame, wrap="word")
                self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
                
                # Footer
                self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
                self.footer_frame.pack(fill=tk.X, padx=10, pady=5)
                
                self.footer_label = ctk.CTkLabel(
                    self.footer_frame, 
                    text="© 2025 Kazlabs - Made with ♥️ by Liam Sorensen", 
                    font=ctk.CTkFont(size=10)
                )
                self.footer_label.pack(side=tk.RIGHT)
                
                # Set up log redirection
                self._setup_log_redirection()
                
            def _setup_log_redirection(self):
                """
                Set up log redirection to the UI.
                
                # Redirects logs to the UI text box.
                # Because users love to see logs they don't understand.
                """
                # Create a custom handler that writes to the UI
                class TextHandler(logging.Handler):
                    def __init__(self, text_widget):
                        logging.Handler.__init__(self)
                        self.text_widget = text_widget
                        
                    def emit(self, record):
                        msg = self.format(record)
                        
                        def append():
                            self.text_widget.configure(state="normal")
                            self.text_widget.insert("end", msg + "\n")
                            self.text_widget.see("end")
                            self.text_widget.configure(state="disabled")
                            
                        # Schedule the append to happen in the main thread
                        self.text_widget.after(0, append)
                        
                # Create and add the handler
                text_handler = TextHandler(self.log_text)
                text_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', 
                                                        datefmt='%H:%M:%S'))
                
                # Add the handler to the logger
                logger.logger.addHandler(text_handler)
                
                # Disable editing of the log text
                self.log_text.configure(state="disabled")
                
            def _on_normal_map_changed(self):
                """Handle normal map checkbox change."""
                value = self.normal_map_var.get()
                config.set("enable_normal_map", value)
                logger.info(f"Normal map generation {'enabled' if value else 'disabled'}")
                
            def _on_bump_map_changed(self):
                """Handle bump map checkbox change."""
                value = self.bump_map_var.get()
                config.set("enable_bump_map", value)
                logger.info(f"Bump map generation {'enabled' if value else 'disabled'}")
                
            def _on_ao_roughness_changed(self):
                """Handle AO/roughness checkbox change."""
                value = self.ao_roughness_var.get()
                config.set("enable_ao_roughness", value)
                logger.info(f"AO/roughness map generation {'enabled' if value else 'disabled'}")
                
            def _on_kernel_size_changed(self, value):
                """Handle kernel size dropdown change."""
                try:
                    size = int(value)
                    if processor.set_kernel_size(size):
                        logger.info(f"Kernel size set to {size}")
                except ValueError:
                    logger.error(f"Invalid kernel size: {value}")
                    
            def _on_theme_changed(self, value):
                """Handle theme dropdown change."""
                theme = value.lower()
                config.set("theme", theme)
                ctk.set_appearance_mode(theme)
                logger.info(f"Theme changed to {theme}")
                
            def _browse_export_dir(self):
                """Browse for export directory."""
                directory = filedialog.askdirectory(
                    initialdir=config.get("export_directory", "./export/"),
                    title="Select Export Directory"
                )
                
                if directory:
                    # Ensure the path ends with a slash
                    if not directory.endswith("/") and not directory.endswith("\\"):
                        directory += "/"
                        
                    self.export_dir_var.set(directory)
                    config.set("export_directory", directory)
                    logger.info(f"Export directory set to {directory}")
                    
            def _select_files(self):
                """Select files to process."""
                files = filedialog.askopenfilenames(
                    initialdir=config.get("last_import_directory", "./import/"),
                    title="Select Files",
                    filetypes=(
                        ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                        ("All files", "*.*")
                    )
                )
                
                if files:
                    # Save the directory for next time
                    last_dir = os.path.dirname(files[0])
                    config.set("last_import_directory", last_dir)
                    
                    # Add files to the queue
                    self.file_queue.extend(files)
                    self.total_count = len(self.file_queue)
                    
                    # Update UI
                    self._update_progress()
                    logger.info(f"Added {len(files)} files to the queue. Total: {self.total_count}")
                    
            def _select_folder(self):
                """Select folder to process."""
                directory = filedialog.askdirectory(
                    initialdir=config.get("last_import_directory", "./import/"),
                    title="Select Folder"
                )
                
                if directory:
                    # Save the directory for next time
                    config.set("last_import_directory", directory)
                    
                    # Count image files in the directory
                    count = 0
                    for filename in os.listdir(directory):
                        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                            self.file_queue.append(os.path.join(directory, filename))
                            count += 1
                            
                    self.total_count = len(self.file_queue)
                    
                    # Update UI
                    self._update_progress()
                    logger.info(f"Added {count} files from {directory} to the queue. Total: {self.total_count}")
                    
            def _start_processing(self):
                """Start processing the file queue."""
                if not self.file_queue:
                    messagebox.showinfo("No Files", "Please select files or a folder to process first.")
                    return
                    
                if self.is_processing:
                    return
                    
                # Update export directory from UI
                export_dir = self.export_dir_var.get()
                config.set("export_directory", export_dir)
                
                # Update UI
                self.is_processing = True
                self.status_label.configure(text="Status: Processing")
                self.process_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
                
                # Start processing thread
                import threading
                self.processing_thread = threading.Thread(target=self._process_files)
                self.processing_thread.daemon = True
                self.processing_thread.start()
                
                logger.info("Processing started")
                
            def _process_files(self):
                """Process files in the queue (run in a separate thread)."""
                while self.file_queue and self.is_processing:
                    try:
                        # Get the next file
                        file_path = self.file_queue.pop(0)
                        
                        # Process the file
                        result = processor.process_image(file_path)
                        
                        # Update progress
                        self.processed_count += 1
                        self.after(0, self._update_progress)
                        
                    except Exception as e:
                        logger.exception(f"Error processing file: {e}")
                        
                # Processing complete or stopped
                self.after(0, self._processing_complete)
                
            def _processing_complete(self):
                """Handle processing complete."""
                self.is_processing = False
                self.status_label.configure(text="Status: Ready")
                self.process_button.configure(state="normal")
                self.stop_button.configure(state="disabled")
                
                if not self.file_queue:
                    logger.info("Processing complete")
                    messagebox.showinfo("Complete", f"Processed {self.processed_count} files successfully.")
                    self.processed_count = 0
                    self.total_count = 0
                    self._update_progress()
                else:
                    logger.info("Processing stopped")
                    
            def _stop_processing(self):
                """Stop processing."""
                if self.is_processing:
                    self.is_processing = False
                    logger.info("Processing stopped by user")
                    
            def _update_progress(self):
                """Update the progress bar and label."""
                if self.total_count > 0:
                    progress = self.processed_count / self.total_count
                    self.progress_bar.set(progress)
                    self.progress_label.configure(text=f"{self.processed_count}/{self.total_count} files processed")
                else:
                    self.progress_bar.set(0)
                    self.progress_label.configure(text="0/0 files processed")
                    
            def _open_export_folder(self):
                """Open the export folder in the file explorer."""
                export_dir = config.get("export_directory", "./export/")
                
                if not os.path.exists(export_dir):
                    os.makedirs(export_dir)
                    
                # Open the folder in the file explorer
                if sys.platform == 'win32':
                    os.startfile(export_dir)
                elif sys.platform == 'darwin':  # macOS
                    import subprocess
                    subprocess.Popen(['open', export_dir])
                else:  # Linux
                    import subprocess
                    subprocess.Popen(['xdg-open', export_dir])
                    
                logger.info(f"Opened export folder: {export_dir}")
        
        # Create and run the app
        app = TextureNormaliserApp()
        app.mainloop()
        
    except Exception as e:
        logger.exception(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 