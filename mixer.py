input_file_1 = "toys/cachedList.txt"  # Path to your first input file (channels)
input_file_2 = "toys/updated_channels.txt"  # Path to your second input file (updated AceStream IDs)
output_file = "toys/cachedList.txt"  # Path to save the final updated content


# Function to read a file and return a list of channels and AceStream IDs
def read_channel_file(file_path):

    with open(file_path, "r") as f:
        lines = f.readlines()
    return [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines), 2)]

def mix_listas():

    # Read both input files
    first_list = read_channel_file(input_file_1)
    second_list = read_channel_file(input_file_2)

    # Initialize updated_lines with all entries from second_list
    updated_lines = []
    updated_count = 0  # Counter for updated channels (channels kept from the second list)
    added_count = 0  # Counter for channels added from the first list

    # Add all entries from second_list to updated_lines
    for channel, id in second_list:
        updated_lines.append(channel + "\n")
        updated_lines.append(id + "\n")
        updated_count += 1

    # Create a set of channels from second_list for easy lookup
    second_list_channels = {channel for channel, id in second_list}

    # Add entries from first_list that are not in second_list
    for channel, id in first_list:
        if channel not in second_list_channels:
            updated_lines.append(channel + "\n")
            updated_lines.append(id + "\n")
            added_count += 1

    # Write the updated content to a new file
    with open(output_file, "w") as f:
        f.writelines(updated_lines)

    # Total channels in the first and second lists (each channel has a name and an ID)
    total_channels_first_list = len(first_list)
    total_channels_second_list = len(second_list)

    # Total channels in the final list (each channel has a name and an ID)
    total_channels_final_list = len(updated_lines) // 2  # Two lines per channel (name + ID)

    # Print the log summary
    print(f"\nMIXER:")
    #print(f"Total channels in the first list: {total_channels_first_list}")
    print(f"Channels in the new list: {total_channels_second_list}")
    #print(f"Channels kept from the second list: {updated_count}")
    #print(f"Channels added from the first list: {added_count}")
    print(f"Channels in the final list: {total_channels_final_list}")
    print(f"Updated file saved as {output_file}\n")


#mix_listas()
