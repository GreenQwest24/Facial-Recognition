import tkinter as tk  # Tkinter for GUI
from tkinter import filedialog, messagebox  # File selection and popups
from deepface import DeepFace  # DeepFace for face analysis
from PIL import Image, ImageTk  # For displaying images in the GUI

def analyze_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if not file_path:
        return
    
    try:
        # Analyze the image with DeepFace
        analysis = DeepFace.analyze(img_path=file_path, actions=["age", "gender", "emotion", "race"], enforce_detection=True)
        
        # Ensure analysis is valid and not empty
        if not isinstance(analysis, list) or len(analysis) == 0:
            messagebox.showerror("Error", "No face detected in the image.")
            return
        
        # Extract results safely using .get()
        result_text.set(f"Age: {analysis[0].get('age', 'N/A')}\n"
                        f"Gender: {analysis[0].get('dominant_gender', 'N/A')}\n"
                        f"Emotion: {analysis[0].get('dominant_emotion', 'N/A')}\n"
                        f"Race: {analysis[0].get('dominant_race', 'N/A')}")
        
        # Load and display the image
        img = Image.open(file_path)
        img = img.resize((250, 250))  # Resize for better display
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img  # Store reference to avoid garbage collection
        
    except ValueError as ve:
        messagebox.showerror("Error", f"No face detected: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"Analysis failed: {e}")

# Create GUI window
root = tk.Tk()
root.title("Face Analysis App")
root.geometry("500x600")  # Adjusted size

# Button to select an image
select_button = tk.Button(root, text="Select Image", command=analyze_image)
select_button.pack(pady=10)

# Label to display the image
image_label = tk.Label(root)
image_label.pack()

# Text label for analysis results
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=10)

# Run the GUI loop
root.mainloop()
