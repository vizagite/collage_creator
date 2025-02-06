#!/usr/bin/env python3
import sys
import os
import subprocess
import platform
from pathlib import Path

def install_package(package):
    """Install a Python package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("pip is not installed. Please install pip first:")
        if platform.system() == "Windows":
            print("Download get-pip.py from https://bootstrap.pypa.io/get-pip.py and run:")
            print("python get-pip.py")
        else:
            print("Run: sudo apt-get install python3-pip  # For Ubuntu/Debian")
            print("Run: sudo yum install python3-pip      # For CentOS/RHEL")
        sys.exit(1)

    print(f"Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. Please try manually:")
        print(f"pip install {package}")
        sys.exit(1)

def check_dependencies():
    """Check and install required dependencies."""
    try:
        import PIL
    except ImportError:
        print("Pillow (PIL) is not installed.")
        user_input = input("Would you like to install Pillow now for handling images? (y/n): ").lower()
        if user_input in ['y', 'yes']:
            install_package('Pillow')
            try:
                import PIL
            except ImportError:
                print("Failed to import Pillow even after installation.")
                print("Please try restarting the script.")
                sys.exit(1)
        else:
            print("Pillow is required to run this script.")
            print("Please install it manually using: pip install Pillow")
            sys.exit(1)

    global Image
    from PIL import Image

def validate_directory(dir_path):
    """Validate and create directory if it doesn't exist."""
    path = Path(dir_path)
    if not path.exists():
        try:
            path.mkdir(parents=True)
            print(f"Created directory: {path}")
        except Exception as e:
            print(f"Error creating directory {path}: {e}")
            sys.exit(1)
    return path

def get_supported_images(directory):
    """Get all supported image files in the directory."""
    extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
    image_files = []
    
    for ext in extensions:
        image_files.extend(list(directory.glob(f'*{ext}')))
        image_files.extend(list(directory.glob(f'*{ext.upper()}')))
    
    return sorted(image_files)

def create_collage(input_dir='.', output_file='books_collage.jpg', cols=5, 
                  target_width=350, target_height=600, padding=10, bg_color='white'):
    """
    Create a collage from images in the specified directory.
    
    Args:
        input_dir (str): Directory containing input images
        output_file (str): Output filename for the collage
        cols (int): Number of columns in the collage
        target_width (int): Target width for each image
        target_height (int): Target height for each image
        padding (int): Padding between images
        bg_color (str): Background color of the collage
    """
    input_path = validate_directory(input_dir)
    
    image_files = get_supported_images(input_path)
    
    if not image_files:
        print(f"No supported image files found in {input_dir}")
        print("Supported formats: JPG, JPEG, PNG, BMP, GIF, WEBP")
        return
    
    num_images = len(image_files)
    rows = (num_images + cols - 1) // cols
    
    canvas_width = cols * (target_width + padding) - padding
    canvas_height = rows * (target_height + padding) - padding
    
    try:
        canvas = Image.new('RGB', (canvas_width, canvas_height), bg_color)
    except ValueError:
        print(f"Invalid background color: {bg_color}")
        print("Please use common color names (e.g., 'white', 'black', 'red')")
        print("or RGB hex values (e.g., '#FFFFFF')")
        return
    
    print(f"\nCreating collage with {num_images} images...")
    print(f"Canvas size: {canvas_width}x{canvas_height} pixels")
    
    for i, image_path in enumerate(image_files, 1):
        try:
            print(f"Processing image {i}/{num_images}: {image_path.name}")
            
            with Image.open(image_path) as img:
                if img.mode in ['RGBA', 'P']:
                    img = img.convert('RGB')
                
                img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
                
                if img.size != (target_width, target_height):
                    left = (img.width - target_width) // 2 if img.width > target_width else 0
                    top = (img.height - target_height) // 2 if img.height > target_height else 0
                    right = left + target_width
                    bottom = top + target_height
                    img = img.crop((left, top, right, bottom))
                                    
                col = (i - 1) % cols
                row = (i - 1) // cols
                x_offset = col * (target_width + padding)
                y_offset = row * (target_height + padding)
                
                canvas.paste(img, (x_offset, y_offset))
                
        except Exception as e:
            print(f"Error processing {image_path.name}: {e}")
            print("Skipping this image and continuing...")
            continue
    
    output_path = Path(output_file)
    if output_path.parent != Path('.'):
        validate_directory(output_path.parent)
    
    try:
        canvas.save(output_file, 'JPEG', quality=95)
        print(f"\nCollage successfully saved as: {output_file}")
        
        if platform.system() == "Windows":
            os.startfile(os.path.dirname(os.path.abspath(output_file)))
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", "-R", output_file])
        
    except Exception as e:
        print(f"Error saving collage: {e}")
        print("Please make sure you have write permissions in the output directory.")
        return

def main():
    """Main function to handle command line arguments and run the collage creation."""
    check_dependencies()
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Create an image collage from your images.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
            Example usage:
            --------------
            Basic usage (uses current directory and default settings):
                python collage.py
            
            Specify number of columns:
                python collage.py --columns 3
            
            Full customization:
                python collage.py --columns 3 --input-dir "my_images" --output "collages/my_collage.jpg" --width 400 --height 600 --padding 15 --background "black"
            
            Supported image formats: JPG, JPEG, PNG, BMP, GIF, WEBP
            '''))
    
    parser.add_argument('-c', '--columns', type=int, default=5,
                        help='Number of columns in the collage (default: 5)')
    parser.add_argument('-i', '--input-dir', type=str, default='.',
                        help='Input directory containing images (default: current directory)')
    parser.add_argument('-o', '--output', type=str, default='collage_output.jpg',
                        help='Output filename (default: collage_output.jpg)')
    parser.add_argument('-w', '--width', type=int, default=350,
                        help='Target width for each image (default: 350)')
    parser.add_argument('-t', '--height', type=int, default=600,
                        help='Target height for each image (default: 600)')
    parser.add_argument('-p', '--padding', type=int, default=10,
                        help='Padding between images (default: 10)')
    parser.add_argument('-b', '--background', type=str, default='white',
                        help='Background color (default: white)')

    args = parser.parse_args()

    if args.columns < 1:
        print("Error: Number of columns must be at least 1")
        sys.exit(1)
    if args.width < 1 or args.height < 1:
        print("Error: Width and height must be positive numbers")
        sys.exit(1)
    if args.padding < 0:
        print("Error: Padding cannot be negative")
        sys.exit(1)

    create_collage(
        input_dir=args.input_dir,
        output_file=args.output,
        cols=args.columns,
        target_width=args.width,
        target_height=args.height,
        padding=args.padding,
        bg_color=args.background
    )

if __name__ == '__main__':
    import textwrap
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("\nIf this issue persists, please report it with the error message above.")
        sys.exit(1)
