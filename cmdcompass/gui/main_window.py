import customtkinter as ctk
from cmdcompass.datamanager import DataManager
from cmdcompass.gui.commandbox import CommandBox
from cmdcompass.gui.commentbox import CommentBox
from cmdcompass.gui.commandbodybox import CommandBodyBox
from cmdcompass.gui.utilitybox import UtilityBox
from cmdcompass.gui.command_tag_operation import TagOperation
from cmdcompass.gui.global_tag import GlobalTagWindow
from cmdcompass.models.collection import Collection
from cmdcompass.models.command import Command
from cmdcompass.gui.manpagebox import ManPageBox
from cmdcompass.utils.utils import load_ctk_image
from CTkToolTip import CTkToolTip

from CTkMessagebox import CTkMessagebox
DEFAULT_BUTTON_COLOR = "blue"


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("cmdCompass")
        self.geometry("900x670")

        # Load data
        self.data_manager = DataManager()
        self.data_manager.load_data()
        self.collections = self.data_manager.get_collections()

        # Create main frames
        self.left_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        self.placeholder_frame = ctk.CTkFrame(self)
        self.placeholder_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)
        self.placeholder_label = ctk.CTkLabel(self.placeholder_frame, text="Please choose a command.")
        self.placeholder_label.pack(pady=20, padx=20)

        # Layout frames
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        #self.right_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)
        self.grid_rowconfigure(0, weight=1)
        # Adjust layout weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=30)

        # Collection operations frame
        self.collection_operation_frame = ctk.CTkFrame(self.left_frame)
        self.collection_operation_frame.grid(row=2, column=0, padx=10, pady=(10,0), sticky="ew")

        # Collection dropdown (within collection_operation_frame)
        self.collection_dropdown = ctk.CTkOptionMenu(
            self.collection_operation_frame,
            values=[collection.name for collection in self.collections],
            command=self.on_collection_select
        )
        self.collection_dropdown.pack(side=ctk.LEFT, padx=(10, 0), pady=10)
        self.collection_dropdown.set("Choose a collection")

        # Remove collection button
        self.remove_collection_button = ctk.CTkButton(
            self.collection_operation_frame,
            text="",
            image=load_ctk_image("delete.png"),
            fg_color="red",
            hover_color="#c77c78",
            width=30,
            height=30,
            command=self.on_remove_collection_click,
            font=("TkDefaultFont ", 14)
        )
        self.remove_collection_button.pack(side=ctk.LEFT, padx=(5, 5), pady=10)
        CTkToolTip(self.remove_collection_button, message="Remove Selected Collection")

        # Add new collection button
        self.add_collection_button = ctk.CTkButton(
            self.collection_operation_frame,
            text="",
            image=load_ctk_image("add.png"),
            width=30,
            height=30,
            command=self.on_add_collection_click
        )
        self.add_collection_button.pack(side=ctk.LEFT, padx=(0, 5), pady=10)
        CTkToolTip(self.add_collection_button, message="Add New Collection")

        # Tag Operations Frame
        tag_operations_frame = ctk.CTkFrame(self.left_frame)
        tag_operations_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Tag Operations Button
        tag_operations_button = ctk.CTkButton(
            tag_operations_frame,
            text="Define/Remove Tag",
            command=self.open_tag_creation_window
        )
        tag_operations_button.pack(pady=5, padx=10)
        CTkToolTip(tag_operations_button, message="Define/Remove Tags here to be later assigned to commands")

        # Create scrollable frame for the command list
        self.command_list_frame = ctk.CTkScrollableFrame(self.left_frame, height=450, width=230)
        self.command_list_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        # Configure scrolling behavior
        self.command_list_frame.configure(corner_radius=5)

        self.theme_toggle_button = ctk.CTkSwitch(
            self.left_frame,
            text="Light Mode",
            command=self.toggle_theme
        )
        self.theme_toggle_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Right Pane Boxes
        self.command_body_box = CommandBodyBox(self.right_frame, self)
        self.command_body_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.utility_box = UtilityBox(self.right_frame)
        self.utility_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Tab Control Frame
        self.tab_control_frame = ctk.CTkFrame(self.right_frame)
        self.tab_control_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=0, sticky="ew")

        # Tab Buttons
        self.comment_tab_button = ctk.CTkButton(self.tab_control_frame, text="Comment",
                                                command=lambda: self.switch_tab("comment"), height=20)
        self.man_page_tab_button = ctk.CTkButton(self.tab_control_frame, text="Man Page",
                                                 command=lambda: self.switch_tab("man_page"), height=20)
        self.comment_tab_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.man_page_tab_button.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")
        CTkToolTip(self.comment_tab_button, message="Switch to the Comment Tab")
        CTkToolTip(self.man_page_tab_button, message="Switch to the Man Page Tab")
        global DEFAULT_BUTTON_COLOR
        DEFAULT_BUTTON_COLOR = self.man_page_tab_button._fg_color[0]
        print(DEFAULT_BUTTON_COLOR)

        # Comment Box
        self.comment_box = CommentBox(self.tab_control_frame, self)
        self.comment_box.grid(row=1, column=0, columnspan=2, padx=10, pady=3, sticky="nsew")

        # Create ManPageBox
        self.man_page_box = ManPageBox(self.tab_control_frame)

        self.tab_control_frame.columnconfigure(0, weight=1)
        self.tab_control_frame.columnconfigure(1, weight=1)

        # Adjust layout weights for the two pane
        self.right_frame.grid_rowconfigure(0, weight=0)
        self.right_frame.grid_rowconfigure(1, weight=0)
        self.right_frame.grid_rowconfigure(2, weight=1)  # Tab control frame should shrink
        self.right_frame.grid_columnconfigure(0, weight=4)

        self.left_frame.grid_rowconfigure(1, weight=0) # TagOperation button
        self.left_frame.grid_rowconfigure(2, weight=0) # collection operations frame
        self.left_frame.grid_rowconfigure(3, weight=1)  # command_list_frame
        self.left_frame.grid_rowconfigure(4, weight=0)  # Theme toggle

        self.active_tab = "comment"  # Set the initial active tab
        self.switch_tab("comment")

        # Create TagOperation instance
        self.tag_operation = TagOperation(self, self.data_manager)

    def switch_tab(self, tab_name):
        if tab_name == "comment":
            self.comment_box.grid(row=1, column=0, columnspan=2, padx=10, pady=3, sticky="nsew")
            self.man_page_box.grid_forget()
        elif tab_name == "man_page":
            self.man_page_box.grid(row=1, column=0, columnspan=2, padx=10, pady=3, sticky="nsew")
            self.comment_box.grid_forget()
            # Load and display man page (passing progress_window)
            self.man_page_box.set_man_page(
                self.selected_command
            )
        self.active_tab = tab_name
        self.update_tab_button_states()

    def update_command_view(self):
        if self.selected_command:
            # Show the right frame and hide the placeholder
            self.right_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)
            self.placeholder_frame.grid_forget()

            self.command_body_box.set_command(self.selected_command)
            self.comment_box.set_comment(self.selected_command.comment)
            self.utility_box.set_command(self.selected_command)
        else:
            # Hide the right frame and show the placeholder
            self.right_frame.grid_forget()
            self.placeholder_frame.grid(row=0, column=1, sticky="nsew", padx=3, pady=3)

            self.command_body_box.set_command(None)
            self.comment_box.set_comment(None)
            self.utility_box.set_command(None)
        self.switch_tab("comment")
    def update_tab_button_states(self):
        if self.active_tab == "comment":
            self.comment_tab_button.configure(state="disabled", fg_color="gray")
            self.man_page_tab_button.configure(state="normal", fg_color=DEFAULT_BUTTON_COLOR)
        elif self.active_tab == "man_page":
            self.man_page_tab_button.configure(state="disabled", fg_color="gray")
            self.comment_tab_button.configure(state="normal", fg_color=DEFAULT_BUTTON_COLOR)

    def open_tag_creation_window(self):
        tag_creation_window = GlobalTagWindow(self, self.data_manager)
        tag_creation_window.grab_set()

    def open_add_tag_window(self, command):
        self.tag_operation.open_add_tag_window(command)

    def on_collection_select(self, choice):
        selected_collection = self.data_manager.get_collection(choice)
        if selected_collection:
            self.update_command_list(selected_collection.commands)
            self.selected_command = None
            self.update_command_view()

    def on_add_collection_click(self):
        # Create a dialog to get collection name 
        dialog = ctk.CTkInputDialog(
            text="Enter your new collection name",
            title="Add New Collection",
        )
        collection_name = dialog.get_input()
        if collection_name:
            # Check for duplicate collection name
            if collection_name in [c.name for c in self.collections]:
                CTkMessagebox(title="Error", message="The collection name already exist", icon="cancel")
            else:
                # Create a new Collection object
                new_collection = Collection(name=collection_name, commands=[])
                # Add the collection using the DataManager
                self.data_manager.add_collection(new_collection)
                # Update the collection dropdown
                self.collection_dropdown.configure(values=[c.name for c in self.data_manager.get_collections()])
                self.collection_dropdown.set(collection_name)
                self.on_collection_select(collection_name)

    def on_remove_collection_click(self):
        selected_collection_name = self.collection_dropdown.get()

        if selected_collection_name:
            msg = CTkMessagebox(title="Confirm Deletion",
                                message=f"Are you sure you want to remove the '{selected_collection_name}' collection?",
                                icon="warning", option_1="Cancel", option_2="Yes")
            if msg.get() == "Yes":
                # Remove the collection using the DataManager
                self.data_manager.delete_collection(selected_collection_name)
                # Update the collection dropdown
                self.collections = self.data_manager.get_collections()
                self.collection_dropdown.configure(values=[c.name for c in self.collections])
                # Clear command list and command view
                self.update_command_list([])
                self.selected_command = None
                self.update_command_view()
                self.collection_dropdown.set("Choose a collection")

    def update_command_list(self, commands):
        for child in self.command_list_frame.winfo_children():
            child.destroy()  # Clear previous command boxes
        if self.collection_dropdown.get() != "Choose a collection":
            # Add Command button
            self.add_command_button = ctk.CTkButton(
                self.command_list_frame,
                text="",
                image=load_ctk_image("create.png"),
                command=self.add_new_command,
                width=200
            )
            self.add_command_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")
            CTkToolTip(self.add_command_button, message="Add a new command to this Collection")

            for i, command in enumerate(commands):
                tags = [self.data_manager.tags[tag_id] for tag_id in command.tag_ids]
                command_box = CommandBox(self.command_list_frame, command, tags, i, self)
                command_box.grid(row=i+1, column=0, pady=5, padx=0, sticky="ew")

    def add_new_command(self):
        # Get the currently selected collection
        selected_collection_name = self.collection_dropdown.get()
        selected_collection = self.data_manager.get_collection(selected_collection_name)

        if selected_collection:
            # Create a new Command object
            new_command = Command(command_str="Please Enter Your Command Here",
                                  comment="Please Enter Your Comment for the Command Here",
                                  tag_ids=[])

            # Add the new command to the collection
            selected_collection.commands.append(new_command)

            # Update the data manager
            self.data_manager.save_data()

            # Refresh the command list UI
            self.refresh_command_list()

            # Select the newly created command
            self.selected_command = new_command
            self.update_command_view()
        else:
            raise ValueError("Error: No collection selected.")

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_toggle_button.configure(text="Light Mode")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_toggle_button.configure(text="Dark Mode")
        self.man_page_box.change_theme()

    def on_command_select(self, command_index):
        selected_collection_name = self.collection_dropdown.get()
        for i, collection in enumerate(self.collections):
            if collection.name == selected_collection_name:
                self.selected_command = self.collections[i].commands[command_index]
                self.update_command_view()
                self.switch_tab("comment")
                return  # Exit the loop once the collection is found
        raise ValueError(f"Collection '{selected_collection_name}' not found.")

    def delete_command(self, command_index):
        # Get the currently selected collection
        selected_collection_name = self.collection_dropdown.get()
        selected_collection = self.data_manager.get_collection(selected_collection_name)

        if selected_collection:
            to_be_delete = selected_collection.commands[command_index]
            # Remove the command from the collection's commands list
            del selected_collection.commands[command_index]

            # Update the data manager
            self.data_manager.save_data()

            # Refresh the command list UI
            self.refresh_command_list()

            # Clear the command view if the deleted command was selected
            if self.selected_command == to_be_delete:
                if len(selected_collection.commands) >= 1:
                    self.selected_command = selected_collection.commands[0]
                else:
                    self.selected_command = None
                self.update_command_view()
        else:
            # Handle case where no collection is selected
            print("Error: No collection selected.")

    def refresh_command_list(self):
        selected_collection_name = self.collection_dropdown.get()
        selected_collection = self.data_manager.get_collection(selected_collection_name)
        if selected_collection:
            self.update_command_list(selected_collection.commands)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
