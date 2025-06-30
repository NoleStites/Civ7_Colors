from controller.Controller import Controller
from tkinter import *
from tkinter.colorchooser import askcolor
import os

class View():

    def __init__(self, controller: Controller):
        self.controller = controller

        # Main root window configuration
        self.root = Tk()
        self.root.title("Civilization VII Coloring")
        self.root.configure(background="black")

        # BORROWED CODE (start)
        # Used to center the window so that it doesn't spawn in a random location every time.
        w = 1200
        h = 600

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y-100))
        # BORROWED CODE (end)

        # Chosen colors
        self.primary = (0, 102, 102)
        self.prev_primary = None
        self.secondary = (238, 238, 238)
        self.prev_secondary = None

        # Left frame
        left_frame = Frame(self.root, width=20, height=h+20, background="black")
        left_frame.pack(side=LEFT)

        leader_label = Label(left_frame, text="Select a Leader", bg="black", fg="white", height=2, width=20, font=("Arial", 15))
        leader_label.pack(side=TOP, expand=True)
        
        left_bottom_frame = Frame(left_frame, width=w/4, height=30, background="#a6a6a6")
        left_bottom_frame.pack(side=TOP, expand=True)
        
        # Leader list box
        self.leader_box = Listbox(left_bottom_frame, font=("Arial", 12), height=30, width=29, bg="#a6a6a6", fg="black", relief="raised", selectmode="single", selectbackground="#262626")
       
        # Acquire list of leader strings
        leader_list, self.leader_dict = self.acquire_leaders()
		
        for i in range(len(leader_list)):
            self.leader_box.insert(i+1,leader_list[i])

        self.leader_box.pack(side=TOP)

        # Top frame
        top_frame = Frame(self.root, width=w, height=2*h/3, background="#202020")
        top_frame.pack(side=TOP, fill=BOTH)

        # Button traits
        ht = 2          # height
        wd = 25         # width
        bg_color = "#202020"    # background color
        fg_color = "#ffffff"    # foreground color
        highlight = "#404040"   # background when hovering
        fore = "white"          # foreground when hovering

        # Buttons
        primary_button = Button(top_frame, bg=bg_color, activeforeground=fore, font=("Arial", 15), activebackground=highlight, fg=fg_color, text="Choose Primary Color", height=ht, width=wd, command=self.display_primary_chooser)
        primary_button.pack(side=LEFT, fill=BOTH)

        secondary_button = Button(top_frame, bg=bg_color, fg=fg_color, font=("Arial", 15), activeforeground=fore, activebackground=highlight, text="Choose Secondary Color", height=ht, width=wd, command=self.display_secondary_chooser)
        secondary_button.pack(side=LEFT, fill=BOTH)

        reset_button = Button(top_frame, bg=bg_color, fg=fg_color, font=("Arial", 15), text="Reset Files", height=ht, activeforeground=fore, activebackground=highlight, width=10, command=self.reset_files)
        reset_button.pack(side=LEFT, fill=BOTH)

        submit_button = Button(top_frame, bg=bg_color, fg=fg_color, font=("Arial", 15), text="Submit!", height=ht, activeforeground=fore, activebackground=highlight, width=wd, command=self.submit)
        submit_button.pack(side=LEFT, fill=BOTH)

        # Bottom frame
        bottom_frame = Frame(self.root, width=w, height=h/3, background="#bfbfbf")
        bottom_frame.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.error_box = Label(bottom_frame, width=40, height=1, bg="#bfbfbf", fg="red", font=("Arial", 20))
        self.error_box.pack()

        self.city_bar = Label(bottom_frame, width=25, height=2, text="Washington", bg="#006666", fg="#eeeeee", font=("Times New Roman", 30))
        self.city_bar.pack(ipadx=10, ipady=1)
        self.city_bar.pack(expand=True)

        self.root.mainloop()
   

    def reset_files(self):
        self.controller.reset_files(self.leader_dict)
        self.error_box.config(fg="blue", text="Files have been reset!")

    def acquire_leaders(self):
        """
        Searches the Civ 6 files for all leaders
        and returns a list of strings.
        """
        leader_list, leader_dict = self.controller.acquire_leaders()
        leader_list.sort()
        return leader_list, leader_dict

    
    def submit(self):
        result = self.leader_box.curselection()
        try:
            chosen_leader = self.leader_box.get(result[0])
        except:
            self.error_box.config(fg="red", text="Error: select a leader!")
        else:
            # Add chosen colors to the global list
            if self.primary == None:
                self.primary = self.prev_primary
            if self.secondary == None:
                self.secondary = self.prev_secondary
            primary_title, secondary_title = self.controller.add_colors(self.primary, self.secondary)
            self.error_box.config(fg="green", text="Colors added!")

            # Change Alt3 color of chosen leader
            leader_path = self.leader_dict[chosen_leader]
            self.controller.assign_alt3(chosen_leader, leader_path, primary_title, secondary_title)


    def display_primary_chooser(self):
        result=askcolor(color=self.city_bar["bg"], title="Choose Your Primary Color")
        self.city_bar.config(bg=result[1])
        self.prev_primary = self.primary
        self.primary = result[0]
        self.error_box.config(text="")
    

    def display_secondary_chooser(self):
        result=askcolor(color=self.city_bar["fg"], title="Choose Your Secondary Color")
        self.city_bar.config(fg=result[1])
        self.prev_secondary = self.secondary
        self.secondary = result[0]
        self.error_box.config(text="")

