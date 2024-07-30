import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
import html

def save_pdf():
    # Get the text from the text widget
    text = text_widget.get("1.0", tk.END).strip()
    
    if not text:
        messagebox.showwarning("Warning", "Text is empty. Nothing to save.")
        return

    # Ask the user to select a file location and name
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        title="Save PDF"
    )
    
    if not file_path:
        return

    try:
        # Create a PDF file
        doc = SimpleDocTemplate(file_path, pagesize=letter)

        # Set up styles
        styles = getSampleStyleSheet()
        
        # Create a custom style based on user selections
        custom_style = ParagraphStyle(
            name='CustomStyle',
            fontName=font_type.get(),
            fontSize=font_size.get(),
            leading=font_size.get() * 1.5,
        )
        
        # Escape HTML characters and preserve whitespace
        escaped_text = html.escape(text).replace('\n', '<br/>').replace(' ', '&nbsp;')

        # Add the text as a Paragraph element
        para = Paragraph(escaped_text, style=custom_style)
        story = [para]
        
        # Build the PDF
        doc.build(story)

        messagebox.showinfo("Success", f"PDF saved successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Text to PDF Converter")

# Create a frame for the text widget
frame = tk.Frame(root, padx=10, pady=10)
frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Create a text widget for input
text_widget = tk.Text(frame, wrap='word', height=20, width=60)
text_widget.pack(side='left', fill='both', expand=True)

# Add a vertical scrollbar
scrollbar = tk.Scrollbar(frame, orient='vertical', command=text_widget.yview)
scrollbar.pack(side='right', fill='y')

# Attach the scrollbar to the text widget
text_widget.config(yscrollcommand=scrollbar.set)

# Create a frame for font selection
font_frame = tk.Frame(root, padx=10, pady=10)
font_frame.grid(row=1, column=0, pady=10)

# Create a label and dropdown for font type
tk.Label(font_frame, text="Font Type:").grid(row=0, column=0, padx=5)
font_type = tk.StringVar(value='Helvetica')
font_types = ['Helvetica', 'Times-Roman', 'Courier']
font_menu = ttk.Combobox(font_frame, textvariable=font_type, values=font_types, state='readonly')
font_menu.grid(row=0, column=1, padx=5)

# Create a label and dropdown for font size
tk.Label(font_frame, text="Font Size:").grid(row=0, column=2, padx=5)
font_size = tk.IntVar(value=12)
font_sizes = [8, 10, 12, 14, 18, 24, 36]
size_menu = ttk.Combobox(font_frame, textvariable=font_size, values=font_sizes, state='readonly')
size_menu.grid(row=0, column=3, padx=5)

# Create a frame for the button
button_frame = tk.Frame(root, padx=10, pady=10)
button_frame.grid(row=2, column=0, pady=10)

# Create a button to save the text as PDF
save_button = tk.Button(button_frame, text="Save as PDF", command=save_pdf)
save_button.pack()

# Configure grid row and column weights
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=1)

# Run the application
root.mainloop()
