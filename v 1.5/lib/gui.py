import tkinter as tk

class GUI:
    """GUI for finding reciprocal modulo determinants for
    Hills cipher encryption/decryption"""

    def __init__(self, title='tk', dev_prints=False, dev_lbl_output=False):

        self.description = """Small script for calculating inverse Modulo numbers.
Enter your Modulo-n and your integer, then hit run."""

        self.dev_prints = dev_prints
        self.dev_lbl_output = dev_lbl_output

        self.root = tk.Tk()
        self.root.title(title)

        self._setupWidgets()
        self._drawWidgets()

    def devOutput(self, *args):
        if self.dev_prints or self.dev_lbl_output:
            str_output = ""
            for arg in args:
                str_output += str(arg)

            if self.dev_prints:
                print(args)

    def devTextOutput(self, *args):
        
        if self.dev_lbl_output:
            output_text = ""
            for arg in args:
                if type(arg) == tuple: #fix for passed nested tuples
                    for element in arg:
                        output_text += str(element) + " "
                else:
                    output_text += str(arg) + " "

            self.dev_output_text_lbl.config(state=tk.NORMAL) #open editing to update/write to
            self.dev_output_text_lbl.insert(tk.END, output_text+"\n")
            self.dev_output_text_lbl.yview_moveto('1.0') #scroll down
            self.dev_output_text_lbl.config(state=tk.DISABLED) #disable editing
            self.root.update() #make changes visible

    def _setupWidgets(self):
        """"""
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)
        ##Widgets
        #Frames
        self.header_frm = tk.Frame(master=self.root)
        self.body_frm = tk.Frame(master=self.root)
        self.dev_output_frm = tk.Frame(master=self.root)

         #header
        self.title_lbl = tk.Label(master=self.header_frm,
                                  text=self.root.title(), font=("bold"))
        self.description_lbl = tk.Label(master=self.header_frm,
                                        text=self.description)

        #Modulo Input
        self.mod_input_lbl = tk.Label(master=self.body_frm, text="Modulo-n")
        self.mod_input_entry = tk.Entry(master=self.body_frm)
        
        #Integer Input
        self.int_input_lbl = tk.Label(master=self.body_frm, text="Integer")
        self.int_input_entry = tk.Entry(master=self.body_frm)

        #Answer Output
        self.output_lbl = tk.Label(master=self.body_frm, text="", fg="red")
        #self.answer_output_value_lbl = tk.Label(master=self.body_frm, text="my goodness!")

        #run button
        self.run_btn = tk.Button(master=self.body_frm, text="Run", width=10)

        #text output & scroll bar
        self.dev_output_text_lbl = tk.Text(master=self.dev_output_frm,
                                       height=10,
                                       bg="white")
        self.scroll_bar_wid = tk.Scrollbar(master=self.dev_output_frm,
                                           command=self.dev_output_text_lbl.yview)
        self.dev_output_text_lbl["yscrollcommand"] = self.scroll_bar_wid.set      

        
    def _drawWidgets(self):
        """Method that 'draws' widgets, eg. widget.grid()"""
        ##pack/grid/place of widgets
        #header
        self.title_lbl.grid(row=0)
        self.description_lbl.grid(row=1)

        #Modulo Input
        self.mod_input_lbl.grid(column=1, row=0)
        self.mod_input_entry.grid(column=2, row=0)
        #self.mod_input_btn.grid(column=3, row=0)

        #Integer Input
        self.int_input_lbl.grid(column=1, row=1)
        self.int_input_entry.grid(column=2, row=1)
        #self.int_input_btn.grid(column=3, row=1)

        #Answer Output
        self.output_lbl.grid(columnspan=5, row=2)

        #run button
        self.run_btn.grid(columnspan=5, row=3, padx=5)

        #text output & scroll bar
        self.dev_output_text_lbl.grid(row=5, pady=5)
        self.scroll_bar_wid.grid(row=5, column=1, sticky='ns')
        if not self.dev_lbl_output: #hide dev widgets
            self.dev_output_text_lbl.grid_remove()
            self.scroll_bar_wid.grid_remove()
        

        #frames
        self.header_frm.grid(column=2, pady=5, padx=5)
        self.body_frm.grid(column=2, pady=5, padx=5)
        self.dev_output_frm.grid(column=2, pady=5, sticky="s")

    def getIntInput(self, entryWidget):
        """Returns True and integer if successful.
        Returns False and "InvalidInteger" if unsuccessful"""
        try:
            value = int(entryWidget.get())
            entryWidget.delete(0, tk.END)
            return True, value
        except ValueError:
            self.output_lbl['text'] = "Please Enter a Valid Integer"
            self.devOutput("Please Enter a Valid Integer")
            self.devTextOutput("Please Enter a Valid Integer")
            return False, "InvalidInteger"


if __name__ == "__main__":
    GUI = GUI("Mod-n Inverse Finder", True, True)
