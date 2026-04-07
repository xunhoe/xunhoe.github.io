import os
from bs4 import BeautifulSoup
from pathlib import Path

def clear_console():
    """Clear the console for better user experience."""
    os.system("cls" if os.name == "nt" else "clear")

def add_project_interactively(html_path):
    """Interactive function to add a project to the portfolio."""
    print("=== Add Project ===")
    project_title = input("Enter project title: ").strip()
    project_category = input("Enter project category: ").strip()
    project_link = input("Enter project link (URL): ").strip()
    project_image_path = input("Enter path to project image: ").strip()

    # Read and parse HTML
    html = Path(html_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    # Locate the portfolio section
    portfolio_section = soup.find("ul", class_="project-list")
    if not portfolio_section:
        print("Error: Portfolio section not found.")
        return

    # Create new project entry
    new_project = soup.new_tag("li", **{"class": "project-item active", "data-filter-item": "", "data-category": project_category.lower()})
    project_link_tag = soup.new_tag("a", href=project_link)
    figure_tag = soup.new_tag("figure", **{"class": "project-img"})
    icon_box = soup.new_tag("div", **{"class": "project-item-icon-box"})
    icon = soup.new_tag("ion-icon", attrs={"name": "eye-outline"})  # Fixed this line
    icon_box.append(icon)
    figure_tag.append(icon_box)
    image_tag = soup.new_tag("img", src=project_image_path, alt=project_title, loading="lazy")
    figure_tag.append(image_tag)
    project_link_tag.append(figure_tag)

    title_tag = soup.new_tag("h3", **{"class": "project-title"})
    title_tag.string = project_title
    project_link_tag.append(title_tag)

    category_tag = soup.new_tag("p", **{"class": "project-category"})
    category_tag.string = project_category
    project_link_tag.append(category_tag)

    new_project.append(project_link_tag)
    portfolio_section.append(new_project)

    # Write updated HTML
    Path(html_path).write_text(str(soup), encoding="utf-8")
    print("Project successfully added!")


def add_resume_interactively(html_path):
    """Interactive function to add an entry to a specific section of the resume."""
    print("=== Add Resume Entry ===")
    
    # Read and parse HTML
    html = Path(html_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    # Locate the sections
    sections = soup.find_all("section", class_="timeline")
    if not sections:
        print("Error: Resume sections not found.")
        return

    # Display available sections
    print("Available sections:")
    section_titles = []
    for i, section in enumerate(sections):
        title = section.find("h3").text.strip() if section.find("h3") else f"Section {i + 1}"
        section_titles.append(title)
        print(f"{i + 1}. {title}")

    # Ask the user which section to update
    while True:
        try:
            choice = int(input("Select the section to update (enter the number): ").strip())
            if 1 <= choice <= len(section_titles):
                selected_section = sections[choice - 1]
                break
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(section_titles)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Gather details for the new entry
    title = input("Enter title of the entry: ").strip()
    start_date = input("Enter start date (e.g., 2022): ").strip()
    end_date = input("Enter end date (or 'Present'): ").strip()
    description = input("Enter description (optional): ").strip()

    # Locate the timeline list in the chosen section
    timeline_list = selected_section.find("ol", class_="timeline-list")
    if not timeline_list:
        print("Error: Timeline list not found in the selected section.")
        return

    # Create new resume entry
    new_item = soup.new_tag("li", **{"class": "timeline-item"})
    title_tag = soup.new_tag("h4", **{"class": "h4 timeline-item-title"})
    title_tag.string = title
    new_item.append(title_tag)

    date_span = soup.new_tag("span")
    date_span.string = f"{start_date} - {end_date}"
    new_item.append(date_span)

    if description:
        description_tag = soup.new_tag("p", **{"class": "timeline-text"})
        description_tag.string = description
        new_item.append(description_tag)

    timeline_list.append(new_item)

    # Write updated HTML
    Path(html_path).write_text(str(soup), encoding="utf-8")
    print(f"Entry successfully added to the '{section_titles[choice - 1]}' section!")


def main():
    """Main CLI menu for managing the portfolio and resume."""
    html_path = input("Enter the path to your HTML file (e.g., index.html): ").strip()
    if not Path(html_path).exists():
        print("Error: The specified file does not exist.")
        return

    while True:
        clear_console()
        print("=== Portfolio & Resume Manager ===")
        print("1. Add Project to Portfolio")
        print("2. Add Entry to Resume")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            add_project_interactively(html_path)
        elif choice == "2":
            add_resume_interactively(html_path)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("Press Enter to return to the menu...")

if __name__ == "__main__":
    main()
