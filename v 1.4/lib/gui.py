import tkinter as tk

class GUI:
    """GUI for finding reciprocal modulo determinants for
    Hills cipher encryption/decryption"""

    def __init__(self, title='tk'):

        self.description = """Small script for calculating inverse Modulo numbers.
Enter your Modulo-n and your integer, then hit run."""

        self.root = tk.Tk()
        self.root.title(title)

        self._setupWidgets()
        self._drawWidgets()

    def _setupWidgets(self):
        """"""
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)
        ##Widgets
        #Frames
        self.header_frm = tk.Frame(master=self.root)
        self.body_frm = tk.Frame(master=self.root)

         #header
        self.title_lbl = tk.Label(master=self.header_frm,
                                  text=self.root.title(), font=("bold"))
        self.description_lbl = tk.Label(master=self.header_frm,
                                        text=self.description)

        #Modulo Input
        self.mod_input_lbl = tk.Label(master=self.body_frm, text="Modulo-n")
        self.mod_input_entry = tk.Entry(master=self.body_frm)
        #self.mod_input_btn = tk.Button(master=self.body_frm, text="Submit")
        #self.mod_input_btn['command'] = lambda: self.getIntInput(self.mod_input_entry)

        #Integer Input
        self.int_input_lbl = tk.Label(master=self.body_frm, text="Integer")
        self.int_input_entry = tk.Entry(master=self.body_frm)
        #self.int_input_btn = tk.Button(master=self.body_frm, text="Submit")

        #Answer Output
        self.output_lbl = tk.Label(master=self.body_frm, text="", fg="red")
        #self.answer_output_value_lbl = tk.Label(master=self.body_frm, text="my goodness!")

        #run button
        self.run_btn = tk.Button(master=self.body_frm, text="Run", width=10)
        

        
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
        

        #frames
        self.header_frm.grid(column=2, pady=5, padx=5)
        self.body_frm.grid(column=2, pady=5, padx=5)

    def getIntInput(self, entryWidget):
        """Returns integer"""
        try:
            value = int(entryWidget.get())
            entryWidget.delete(0, tk.END)
            return value
        except ValueError:
            self.output_lbl['text'] = "Please Enter a Valid Integer"
            print("Please Enter a Valid Integer")
            return False


if __name__ == "__main__":
    GUI = GUI("Mod-n Inverse Finder")
