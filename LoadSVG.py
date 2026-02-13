def load_svg(file_path, primary_color="#ff8ae8", secondary_color="#6edbff", background_color="#222"):
    print(f"colors are: {primary_color} | {secondary_color} | {background_color}")
    with open(file_path, 'r') as file:
        svg_content = file.read()
    # Replace colors in SVG content
    svg_content = svg_content.replace("#ff8ae8", primary_color)
    svg_content = svg_content.replace("#6edbff", secondary_color)
    svg_content = svg_content.replace("#222", background_color)
    return svg_content


if __name__ == "__main__":
    print(load_svg("SVG/Discord.svg", background_color="#test"))