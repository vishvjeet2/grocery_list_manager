import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog
import os

class GroceryListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Smart Grocery List Manager")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.grocery_file = "groceryList.txt"
        self.recipe_file = "recipes.txt"
        self.recipe_map = {}
        self.items = []

        self.load_recipes()

        # --- Grocery List Frame ---
        grocery_frame = ttk.Frame(root, padding=10)
        grocery_frame.pack(fill=BOTH, expand=True)

        self.listbox = tk.Listbox(grocery_frame, font=("Segoe UI", 12), height=10)
        self.listbox.pack(pady=10, fill=BOTH, expand=True, side=TOP)

        if os.path.exists(self.grocery_file):
            with open(self.grocery_file, "r") as f:
                for line in f:
                    self.listbox.insert(END, line.strip())

        # --- Entry Section ---
        entry_frame = ttk.Frame(grocery_frame)
        entry_frame.pack(fill=X, pady=5)

        self.entry = ttk.Entry(entry_frame, font=("Segoe UI", 12))
        self.entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))

        self.add_button = ttk.Button(entry_frame, text="➕ Add", bootstyle=SUCCESS, command=self.add_item)
        self.add_button.pack(side=RIGHT)

        # --- Control Buttons ---
        control_frame = ttk.Frame(grocery_frame)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="🗑 Remove", bootstyle=DANGER, command=self.remove_item).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="🧹 Clear All", bootstyle=WARNING, command=self.clear_list).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="🍽 Suggest Recipe", bootstyle=INFO, command=self.suggest_recipe).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="📂 Manage Recipes", bootstyle=PRIMARY, command=self.manage_recipes).grid(row=0, column=3, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_item(self):
        item = self.entry.get().strip()
        if item:
            self.listbox.insert(END, item)
            self.entry.delete(0, END)
        else:
            messagebox.showinfo("Info", "Please enter an item before adding.")

    def remove_item(self):
        selected = self.listbox.curselection()
        if selected:
            self.listbox.delete(selected)
        else:
            messagebox.showinfo("Info", "Please select an item to remove.")

    def clear_list(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the entire list?"):
            self.listbox.delete(0, END)

    def suggest_recipe(self):
        items = [self.listbox.get(i).lower() for i in range(self.listbox.size())]
        for name, ingredients in self.recipe_map.items():
            if all(ing.lower() in items for ing in ingredients):
                messagebox.showinfo("🍽 Suggested Recipe", f"Suggested recipe: {name}")
                return
        messagebox.showinfo("No Match", "😔 No matching recipes found with current items.")

    def on_close(self):
        with open(self.grocery_file, "w") as f:
            for i in range(self.listbox.size()):
                f.write(self.listbox.get(i) + "\n")
        self.save_recipes()
        self.root.destroy()

    def load_recipes(self):
        if os.path.exists(self.recipe_file):
            with open(self.recipe_file, "r") as f:
                for line in f:
                    if ':' in line:
                        name, ing_str = line.split(':', 1)
                        ingredients = [i.strip() for i in ing_str.split(',') if i.strip()]
                        self.recipe_map[name.strip()] = ingredients

    def save_recipes(self):
        with open(self.recipe_file, "w") as f:
            for name, ingredients in self.recipe_map.items():
                f.write(f"{name}: {', '.join(ingredients)}\n")

    def manage_recipes(self):
        top = ttk.Toplevel(self.root)
        top.title("📂 Recipe Manager")
        top.geometry("700x400")

        left_frame = ttk.Frame(top, padding=10)
        left_frame.pack(side=LEFT, fill=Y)

        recipe_listbox = tk.Listbox(left_frame, width=30)
        recipe_listbox.pack(fill=Y, expand=True)

        for name in self.recipe_map:
            recipe_listbox.insert(END, name)

        right_frame = ttk.Frame(top, padding=10)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True)

        ingredient_text = tk.Text(right_frame, height=10, font=("Segoe UI", 11))
        ingredient_text.pack(fill=BOTH, expand=True)

        button_frame = ttk.Frame(right_frame)
        button_frame.pack(pady=10)

        def show_ingredients(event):
            selected = recipe_listbox.curselection()
            if selected:
                name = recipe_listbox.get(selected[0])
                ingredients = self.recipe_map.get(name, [])
                ingredient_text.delete(1.0, END)
                ingredient_text.insert(END, ', '.join(ingredients))

        def update_recipe():
            selected = recipe_listbox.curselection()
            if selected:
                name = recipe_listbox.get(selected[0])
                updated = simpledialog.askstring("Update", f"Update ingredients for {name}:", initialvalue=ingredient_text.get(1.0, END).strip())
                if updated:
                    ingredients = [i.strip() for i in updated.split(',')]
                    self.recipe_map[name] = ingredients
                    self.save_recipes()
                    messagebox.showinfo("Updated", "Recipe updated.")

        def add_recipe():
            name = simpledialog.askstring("Add Recipe", "Enter recipe name:")
            if name:
                ingredients = simpledialog.askstring("Add Ingredients", "Enter ingredients separated by commas:")
                if ingredients:
                    ing_list = [i.strip() for i in ingredients.split(',')]
                    self.recipe_map[name.strip()] = ing_list
                    recipe_listbox.insert(END, name.strip())
                    self.save_recipes()
                    messagebox.showinfo("Added", "Recipe added.")

        def delete_recipe():
            selected = recipe_listbox.curselection()
            if selected:
                name = recipe_listbox.get(selected[0])
                del self.recipe_map[name]
                recipe_listbox.delete(selected[0])
                ingredient_text.delete(1.0, END)
                self.save_recipes()
                messagebox.showinfo("Deleted", "Recipe deleted.")

        ttk.Button(button_frame, text="✏️ Update", bootstyle=INFO, command=update_recipe).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="➕ Add", bootstyle=SUCCESS, command=add_recipe).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="🗑 Delete", bootstyle=DANGER, command=delete_recipe).pack(side=LEFT, padx=5)

        recipe_listbox.bind('<<ListboxSelect>>', show_ingredients)


if __name__ == "__main__":
    app = ttk.Window(themename="flatly")  # Options: flatly, vapor, cyborg, minty, morph, etc.
    GroceryListApp(app)
    app.mainloop()
