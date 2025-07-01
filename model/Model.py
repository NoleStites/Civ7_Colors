from os import remove

class Model():
    def __init__(self, path, sub_path):
        self.color_path = path
        self.sub_path = sub_path

    def set_color_path(self, path):
        self.color_path = path

    def reset_files(self, leader_dict):
        """
        This method will remove all colors created by this application
        and assign a new default value to all affected Alt3s.
        """
        # Reset the global colors
        original = open(self.color_path + self.sub_path + "playerstandardcolors.xml", "r")
        new_copy = open(self.color_path + self.sub_path + "copy_playerstandardcolors.xml", "w")

        # Figure out how many colors need to be removed during copy process
        counter = 1
        entry_count = 0
        for line in original:
            if counter != 5:
                new_copy.write(line)
                counter += 1
                continue
            
            temp_line = line
            temp_line.lstrip()
            temp_line = temp_line.split("_")[-1]
            temp_line = temp_line.replace("</Type>\n", "")
            try:
                entry_count = int(temp_line)
            except:
                new_copy.write(line)
                entry_count = 0
                counter += 1
                continue
            new_copy.write(line)
            counter += 1

        original.close()
        new_copy.close()

        # Move copy file contents into original, skipping entry_count*5 lines
        original = open(self.color_path + "playerstandardcolors.xml", "w")
        new_copy = open(self.color_path + "copy_playerstandardcolors.xml", "r")
        
        entry_count *= 5
        counter = 1
        for line in new_copy:
            if counter == 4:
                if entry_count != 0:
                    entry_count -= 1
                    continue

            original.write(line)
            counter += 1

        original.close()
        new_copy.close()
        remove(self.color_path + "copy_playerstandardcolors.xml")

        # Remove colors from playercolors.xml
        original = open(self.color_path + self.sub_path + "playercolors.xml", "r")
        new_copy = open(self.color_path + self.sub_path + "copy_playercolors.xml", "w")

        # Copy contents of original file to temporary file
        for line in original:
            new_copy.write(line)

        original.close()
        new_copy.close()

        # Rewrite the original by using the copy, uncommenting changes along the way 
        original = open(self.color_path + self.sub_path + "playercolors.xml", "w")
        new_copy = open(self.color_path + self.sub_path + "copy_playercolors.xml", "r")

        counter = 0 # 1 -> on second comment; 2 -> first line to remove; 3 -> second line to remove
        for line in new_copy:
            if (line.find("<!--") != -1) or (counter == 1): # Uncomment found comment
                new_line = line.strip().split("<!-- ")[1].split(" -->")[0]
                new_line = '\t\t\t' + new_line +'\n'
                original.write(new_line)
                counter += 1
                continue
    
            if (counter == 2) or (counter == 3): # Dont write custom colors back to file
                counter += 1
                continue

            if counter == 4: # Made it past the comments and custom colors, so reset vars
                counter = 0

            original.write(line)

        original.close()
        new_copy.close()
        remove(self.color_path + self.sub_path + "copy_playercolors.xml")

        # === OLD CODE FOR DLC LEADERS ===
        # Reset red and white to all Alt3s as default
        #default_primary = "COLOR_STANDARD_RED_MD"
        #default_secondary = "COLOR_STANDARD_WHITE_LT"
        #tuple_list = leader_dict.items()
        #for leader_path in tuple_list:
        #    self.assign_alt3(leader_path[0], leader_path[1], default_primary, default_secondary)


    def assign_alt3(self, leader, path, p_title, s_title):
        """
        Will search for 'leader' in the file at the end of the
        'path'. Once located, this method will assign new primary
        and secondary values to the Alt3 color of that leader.
        """
        # Reformat the leader string to fit the contents of the file
        caps_leader = leader.upper().replace(" ", "_")
        caps_leader = "LEADER_" + caps_leader

        # Open and prepare the file at the end of the given path
        new_path = path + "temp.xml"
        original = open(path + "playercolors.xml", "r")
        new_copy = open(new_path, "w")

        # As we copy original to copy, keep track of where leader is
        leader_location = None
        counter = 1
        for line in original:
            new_copy.write(line)
            if line.find(caps_leader) != -1:
                leader_location = counter
            counter += 1

        original.close()
        new_copy.close()

        # Move copy into original and write over Alt3 at leader_location
        original = open(path + "playercolors.xml", "w")
        new_copy = open(new_path, "r")
        
        finished = False
        counter = 1
        first_time_assignment = True # Whether or not a custom color has been assigned to the leader yet (and whether the original color needs to be commented out)
        original_primary = None # The original primary color
        for line in new_copy:
            # Skim over lines until desire leader is found or finished
            if counter <= leader_location or finished == True:
                original.write(line)
                counter += 1
                continue

            # Skip over <Usage>
            if line.find("<Usage>") != -1:
                original.write(line)
                continue

            # Skip over original (commented out) colors
            if line.find("<!--") != -1:
                original.write(line)
                first_time_assignment = False
                continue
            
            # If first time, record and comment out original colors
            # Then add new colors
            if first_time_assignment:
                if original_primary == None: # <PrimaryColor>
                    original_primary = line
                    continue
                else: # <SecondaryColor>
                    original.write("\t\t\t<!-- " + original_primary.strip().strip('\n') + " -->\n")
                    original.write("\t\t\t<!-- " + line.strip().strip('\n') + " -->\n") # Comment out original color
                 
                # Add new <PrimaryColor> and <SecondaryColor>            
                new_primary = "\t\t\t<PrimaryColor>" + p_title + "</PrimaryColor>\n"
                new_secondary = "\t\t\t<SecondaryColor>" + s_title + "</SecondaryColor>\n"
                original.write(new_primary)
                original.write(new_secondary)
                finished = True
                continue
             
            # Not first time, so write new colors instead of previous custom
            if line.find("<PrimaryColor>") != -1: 
                new_primary = "\t\t\t<PrimaryColor>" + p_title + "</PrimaryColor>\n" 
                original.write(new_primary)
                continue
            
            if line.find("<SecondaryColor>") != -1: 
                new_secondary = "\t\t\t<SecondaryColor>" + s_title + "</SecondaryColor>\n"
                original.write(new_secondary)
                finished = True                
                continue

        original.close()
        new_copy.close()
        remove(new_path) 


    def add_colors(self, primary_rgb, secondary_rgb):
        """
        Will add the given primary and secondary rgb values
        to the global list of colors for use by the leaders.
        """
        
        # Create a copy of the original file
        original = open(self.color_path + self.sub_path + "playerstandardcolors.xml", "r")
        new_copy = open(self.color_path + self.sub_path + "copy_playerstandardcolors.xml", "w")

        counter = 1
        max_color = 0
        for line in original:
            new_copy.write(line)
            temp_line = ""
            for ch in line:
                temp_line += ch
            if counter == 5:
                if temp_line.find("NEW_COLOR_") != -1:
                    y = temp_line.split("_")[2]
                    max_color = int(y.split("<")[0])
            counter += 1

        original.close()
        new_copy.close()

        # Write to the original by using the copy and editing what needs to be editted
        original = open(self.color_path + self.sub_path + "playerstandardcolors.xml", "w")
        new_copy = open(self.color_path + self.sub_path + "copy_playerstandardcolors.xml", "r")

        counter = 1
        for line in new_copy:
            if counter != 4:
                original.write(line)
            else:
                pri_sec = (primary_rgb, secondary_rgb)
                for i in range(2, 0, -1): # One for primary, one for secondary
                    if i == 1:
                        primary_num = max_color + i
                    elif i == 2:
                        secondary_num = max_color + i
                    temp1 = f"\t\t\t<Type>NEW_COLOR_{max_color + i}</Type>\n"
                    temp2 = f"\t\t\t<Color>{pri_sec[i-1][0]},{pri_sec[i-1][1]},{pri_sec[i-1][2]},255</Color>\n"
                    temp3 = f"\t\t\t<Color3D>{pri_sec[i-1][0]},{pri_sec[i-1][1]},{pri_sec[i-1][2]},255</Color3D>\n"
                    color_template = [
                    "\t\t<Row>\n",
                    temp1,
                    temp2,
                    temp3,
                    "\t\t</Row>\n"
                    ]
                    for new_line in color_template:
                        original.write(new_line)
                original.write(line)

            counter += 1

        original.close()
        new_copy.close()
        remove(self.color_path + self.sub_path + "copy_playerstandardcolors.xml")

        primary_title = f"NEW_COLOR_{primary_num}"
        secondary_title = f"NEW_COLOR_{secondary_num}"
        return primary_title, secondary_title



    def acquire_leaders(self):
        """
        Responsible for going directly into the
        Civ 6 files and extracting the leader
        names as strings.
        """
        all_leaders = []

        # Get list of Base Leaders
        base_leaders, base_dict = self.get_base_leaders()
                
        # Get DLC Leaders
        #dlc_leaders, dlc_dict = self.get_dlc_leaders()

        # Sort the results
        #base_leaders.extend(dlc_leaders)
        for leader in base_leaders:
            all_leaders.append(leader)

        # Combine the dictionaries
        #dlc_list = dlc_dict.items()
        #for tup in dlc_list:
        #    base_dict[tup[0]] = tup[1]

        return all_leaders, base_dict


    def get_dlc_leaders(self):
        # Create file paths to search for
        civs = [
            "Australia",
            "Aztec_Montezuma",
            "Byzantium_Gaul",
            "CatherineDeMedici",
            "Ethiopia",
            "GranColombia_Maya",
            "GreatBuilders",
            "GreatNegotiators",
            "GreatWarlords",
            "Indonesia_Khmer",
            "JuliusCaesar",
            "KublaiKhan_Vietnam",
            "Macedonia_Persia",
            "Nubia_Amanitore",
            "Poland_Jadwiga",
            "Portugal",
            "RulersOfChina",
            "RulersOfEngland",
            "RulersOfTheSahara",
            "TeddyRoosevelt",
            "Expansion1",
            "Expansion2",
            "Babylon"
        ]
        
        files_to_search = []
        for civ in civs:
            if civ == "Nubia_Amanitore":
                end = civ.replace("_Amanitore", "")
                files_to_search.append(f"{civ}\\Data\\{end}_PlayerColors.xml")
            elif civ == "Macedonia_Persia":
                files_to_search.append(f"{civ}\\Data\\{civ}_PlayerColors.xml")
            elif civ == "Expansion1":
                files_to_search.append(f"{civ}\\Data\\{civ}_PlayerColors.xml")
            elif civ == "Expansion2":
                files_to_search.append(f"{civ}\\Data\\{civ}_PlayerColors.xml")
            elif civ == "Babylon":
                files_to_search.append(f"{civ}\\Data\\{civ}_Colors_Config.xml")
            else:
                files_to_search.append(f"{civ}\\Data\\{civ}_Colors.xml")

        # Add the leaders that the user owns to a list to be returned
        dlc_leaders = []
        dlc_leaders_dict = {}

        for filepath in files_to_search:
            try:
                f = open(f"C:\\Program Files (x86)\\Steam\steamapps\\common\\Sid Meier's Civilization VI\\DLC\\{filepath}", "r")
            except:
                temp = filepath.split("\\")
                print(f"You don't have {temp[0]}.")
                continue
            
            for line in f:
                if line.find("LEADER") != -1:
                    line = line.lstrip().replace("<Type>LEADER_", "").replace("</Type>", "").replace("\n", "").replace("_", " ")
                    line = line.lower().title()
                    if line == "Joao Iii":
                        line = line.replace("Iii", "III")
                    dlc_leaders.append(line)
                    dlc_leaders_dict[line] = f"C:\\Program Files (x86)\\Steam\steamapps\\common\\Sid Meier's Civilization VI\\DLC\\{filepath}"
            f.close()
        
        return dlc_leaders, dlc_leaders_dict

    
    def get_base_leaders(self):
        try:
            f = open(self.color_path + self.sub_path + "playercolors.xml", "r")
        except:
            raise Exception("playercolors.xml doesn't exist!")

        leader_list = []
        leader_path_dict = {}

        for line in f:
            if line.find("LEADER") != -1:
                line = line.lstrip().replace("<Type>LEADER_", "").replace("</Type>", "").replace("\n", "").replace("_", " ")
                line = line.lower().title()
                leader_list.append(line)
                leader_path_dict[line] = self.color_path + self.sub_path
        f.close()
        return leader_list, leader_path_dict
    

    def create_global_color(self, rgb_values):
        """
        Given a tuple of rgb values, this method will
        create a new global color in playerstandardcolors.xml.
        """
        r = rgb_values[0]
        g = rgb_values[1]
        b = rgb_values[2]
        template_string = f"<Row>\n    <Type>NEW_COLOR_A</Type>\n    <Color>{r},{g},{b},255</Color>\n</Row>\n"
        print(template_string)

