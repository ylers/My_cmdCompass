import customtkinter as ctk

class UtilityBox(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Frame for variable input fields
        self.variable_input_frame = ctk.CTkFrame(self, height=50)
        self.variable_input_frame.pack(padx=10, pady=(10, 10), fill="both", expand=True)

        # Generate button
        self.generate_button = ctk.CTkButton(
            self,
            text="Templating & Copy",
            command=self.generate_command
        )
        self.generate_button.pack(pady=(0, 10))
        self.generate_button.pack_forget()

    def set_command(self, command):
        # Clear previous input fields
        for child in self.variable_input_frame.winfo_children():
            child.destroy()

        if command:
            self.command = command
            variables = command.get_template_variables()
            if variables:
                self.generate_button.pack(pady=(0, 10))
                for i, var in enumerate(variables):
                    entry = ctk.CTkEntry(self.variable_input_frame, placeholder_text=var)
                    entry.grid(row=0, column=i, padx=5, pady=5)

                # Make entry fields expandable and distribute space evenly
                self.variable_input_frame.grid_columnconfigure(tuple(range(len(variables))), weight=1)
            else:
                self.generate_button.pack_forget()

    def generate_command(self):
        # Get the currently selected command
        selected_command = self.command

        if selected_command:
            # Collect variable values from input fields
            replacements = {}
            for child in self.variable_input_frame.winfo_children():
                if isinstance(child, ctk.CTkEntry):
                    var_name = child.cget("placeholder_text")
                    var_value = child.get()
                    replacements[var_name] = var_value

            try:
                # Generate the command using parse_command
                generated_command = selected_command.parse_template(replacements)

                # Copy the generated command to clipboard
                self.master.master.clipboard_clear()
                self.master.master.clipboard_append(generated_command)
                # TODO: Use floting window popup for the messaging
                print("Command Generated", "The command has been copied to your clipboard!")
            except ValueError as e:
                print("Error" + str(e))