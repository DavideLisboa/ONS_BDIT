import re


def update_token(typescript_file_path, new_value):
    # Define the file path to your TypeScript file

    # Define the variable name and the new value

    # Read the TypeScript file
    with open(typescript_file_path, 'r') as file:
        file_contents = file.read()

    # Use regular expressions to find and replace the variable assignment
    pattern = re.compile(fr'token\s*=\s*\'[^\']*\'')
    replacement = f'token = \'{new_value}\''
    modified_contents = re.sub(pattern, replacement, file_contents)

    # Write the modified content back to the TypeScript file
    with open(typescript_file_path, 'w') as file:
        file.write(modified_contents)
