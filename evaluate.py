import os
import json
from typing import Dict, List, Set

VALID_DATASETS = set(['a_example', 'b_lovely_landscapes', 'c_memorable_moments', 'd_pet_pictures', 'e_shiny_selfies'])

def slide_valid(slide: List[str], line_number: int, slide_map: Dict[str, str], used_slides: Set[str]):
    """
    Check if a slide is valid based on certain conditions.

    Parameters:
    slide (List[str]): The list of pictures on the slide.
    line_number (int): The line number corresponding to the slide.
    slide_map (Dict[str, str]): A mapping of picture names to their attributes.
    used_slides (Set[str]): A set of picture names that have already been used.

    Returns:
    tuple: A tuple containing a boolean value indicating whether the slide is valid,
           and the updated set of used slide names.
    """
    if slide == ['']:
        # Check if there is no picture on the slide
        print(f'Line {line_number} is invalid, there is no picture on the slide.')
        return False, used_slides
    
    if len(slide) > 2:
        # Check if there are more than 2 pictures on the slide
        print(f'Line {line_number} is invalid, there is more than 2 pictures on the slide.')
        return False, used_slides

    for e in slide:
        try:
            p = slide_map[e]
        except KeyError:
            # Check if the picture doesn't exist in the original dataset
            print(f'Line {line_number} is invalid, picture {e} doesn\'t exist in the original dataset.')
            return False, used_slides
        
        if p['style'] == 'H':
            if len(slide) > 1:
                # Check if there is more than 1 horizontal picture on the slide
                print(f'Line {line_number} is invalid, there is more than 1 horizontal picture on the slide.')
                return False, used_slides
        
        if e in used_slides:
            # Check if the picture is used at least twice in the slideshow
            print(f'Line {line_number} is invalid, picture {e} is used at least twice in the slideshow.')
            return False, used_slides
        
        used_slides.add(e)
    
    # Return True if all conditions are satisfied, along with the updated set of used slide names
    return True, used_slides

def slide_to_picture(slide: List[str], slide_map: Dict[str, str]):
    """
    Convert a slide to a set of picture tags.

    Parameters:
    slide (List[str]): The list of pictures on the slide.
    slide_map (Dict[str, str]): A mapping of picture names to their attributes.

    Returns:
    set: A set of picture tags from the pictures on the slide.
    """
    picture = set()

    # Iterate through each picture on the slide
    for e in slide:
        # Access the picture tags from the slide_map dictionary and add them to the slide tag set
        picture = picture.union(set(slide_map[e]['tags']))

    # Return the set of picture tags
    return picture

def score(slide1: Set[str], slide2: Set[str]) -> int:
    """
    Calculate the score between two slides based on common and distinct elements.

    Parameters:
    slide1 (Set[str]): Set of picture tags in slide 1.
    slide2 (Set[str]): Set of picture tags in slide 2.

    Returns:
    int: The score between the two slides.
    """
    # Calculate the number of common elements between slide1 and slide2
    f1 = len(slide1.intersection(slide2))

    # Calculate the number of elements in slide1 that are not in slide2
    f2 = len(slide1 - slide2)

    # Calculate the number of elements in slide2 that are not in slide1
    f3 = len(slide2 - slide1)

    # Return the minimum value among f1, f2, and f3 as the score
    return min(f1, f2, f3)

def evaluate(file_path: str) -> int:
    """
    Evaluate a file containing slide data and calculate the total score.

    Parameters:
    file_path (str): The path to the file to be evaluated.

    Returns:
    int: The total score calculated from the slide data.
    """
    total_score = 0
    used_slides = set()
    previous_picture = None

    with open(file_path) as f:
        # Check that the first line contains a valid dataset name
        dataset = f.readline().strip()
        if dataset not in VALID_DATASETS:
            print("Invalid dataset name in the first line.")
            return 0

        with open(f'./datasets_map/{dataset}.json') as dmap:
            slide_map = json.load(dmap)

        # Check that the second line contains a valid number
        try:
            n_lines = int(f.readline().strip())
        except ValueError:
            print("Incorrect value in the second line, an integer is expected.")
            return 0
        
        for i in range(n_lines):
            current_slide = f.readline().strip().split(' ')

            # Check the validity of the current slide
            valid, used_slides = slide_valid(current_slide, i+3, slide_map, used_slides)
            if not valid:
                return 0

            # Convert the current slide to picture tags
            current_picture = slide_to_picture(current_slide, slide_map)

            if previous_picture:
                # Calculate the score between the current and previous slide
                total_score += score(previous_picture, current_picture)
            previous_picture = current_picture

    return total_score

    
if __name__ == "__main__":
    output_path = './outputs'

    for file_path in os.listdir(output_path):
        total_score = 0
        print(f'Evaluating file: {file_path}')
        dscore = evaluate(os.path.join(output_path, file_path))
        print(f"Score: {dscore}")
        total_score += dscore
    print(f"Cumulated score over all the result files is: {total_score}")