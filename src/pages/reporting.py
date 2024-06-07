from src.pages.draw_poly import *

def tax_potential():
    images_folder = 'src/output2/predict/polygons/images'

    image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    total_houses = 0
    total_tax = 0
    total_images = 0
    total_area = 0

    for image in image_files:
        count = 0
        area = 0
        tax = 0
        count, area, tax = tax_pot_img(image)
        total_houses += count
        total_area += area
        total_tax += tax
        total_images+=1
    
    st.write(f"Total number of images: {total_images}")
    st.write(f"Total house size: {total_area} square feet")
    st.write(f"Total house count: {total_houses}")
    st.write(f"Total tax potential: Rs.{total_tax}")