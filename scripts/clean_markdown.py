import os
import re


def clean_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split content into lines
    lines = content.split("\n")
    cleaned_lines = []
    in_code_block = False
    in_front_matter = False

    for i, line in enumerate(lines):
        # Handle front matter
        if line.strip() == "---":
            if not in_front_matter:
                in_front_matter = True
            else:
                in_front_matter = False
            cleaned_lines.append(line)
            continue

        # Preserve front matter formatting
        if in_front_matter:
            cleaned_lines.append(line)
            continue

        # Handle code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            cleaned_lines.append(line)
            continue

        if in_code_block:
            cleaned_lines.append(line)
            continue

        # Handle HTML blocks
        if line.strip().startswith("<"):
            cleaned_lines.append(line)
            continue

        # Handle image blocks
        if line.strip().startswith("![") or line.strip().startswith("<figcaption>"):
            cleaned_lines.append(line)
            continue

        # Remove empty lines between paragraphs
        if not line.strip():
            if cleaned_lines and cleaned_lines[-1].strip():
                cleaned_lines.append("")
            continue

        # Remove trailing spaces
        line = line.rstrip()

        # Add non-empty lines
        if line:
            cleaned_lines.append(line)

    # Join lines and ensure proper spacing between sections
    cleaned_content = "\n".join(cleaned_lines)

    # Remove multiple consecutive empty lines
    cleaned_content = re.sub(r"\n{3,}", "\n\n", cleaned_content)

    # Write back to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)


def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            print(f"Cleaning {filename}...")
            clean_markdown_file(file_path)
            print(f"Finished cleaning {filename}")


if __name__ == "__main__":
    posts_directory = "_posts"
    process_directory(posts_directory)
