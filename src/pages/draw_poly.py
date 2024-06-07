from src.utils.dependancies import *
from src.utils.convert_box_to_poly import convert

def polygon_area(vertices):
    x = [vertex[0] for vertex in vertices]
    y = [vertex[1] for vertex in vertices]
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
    return area

def propery_tax_for_double_storey(area_in_square_feet):
    per_square_feet_tax = 15
    covered_area = area_in_square_feet *2
    total_area_of_house = covered_area + area_in_square_feet
    return covered_area* per_square_feet_tax


def propery_tax(area_in_square_feet):
    per_square_feet_tax = 4000
    return per_square_feet_tax * area_in_square_feet

def square_meters_to_square_yards(area_in_square_meters):
    # Conversion factor: 1 square meter = 1.19599 square yards
    conversion_factor = 1.19599
    area_in_square_yards = area_in_square_meters * conversion_factor
    return area_in_square_yards

def calculate_house_size_in_meters(polygon_vertices):
    pixel_area = polygon_area(polygon_vertices)
    pixel_area_in_meters = 0.597 ** 2
    house_size_in_meters = pixel_area * pixel_area_in_meters
    house_size_in_square_feet = square_meters_to_square_yards(house_size_in_meters)
    return house_size_in_square_feet

def extract_lat_lng(file_name):
    # Split the file name based on underscores
    parts = file_name.split('_')
    
    # Initialize latitude and longitude variables
    latitude = None
    longitude = None
    
    # Iterate through the parts to find latitude and longitude
    for i in range(len(parts)):
        if parts[i].startswith('lat'):
            latitude = float(parts[i+1])
        elif parts[i].startswith('lng'):
            longitude = float(parts[i+1])
    
    return latitude, longitude

def draw_polygons_on_image(image_path, label_path):
    image = cv2.imread(image_path)
    height_img, width_img, _ = image.shape

    polygons = []

    with open(label_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        data = line.split()
        class_id, *coordinates = map(float, data)
        vertices = [(int(coordinates[i] * width_img), int(coordinates[i + 1] * height_img)) for i in range(0, len(coordinates), 2)]
        polygons.append(vertices)

    for i, vertices in enumerate(polygons):
        cv2.polylines(image, [np.array(vertices)], True, (255, 0, 0), thickness=2)
        # Add annotation
        cv2.putText(image, f"House {i+1}", (vertices[0][0], vertices[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    return image, polygons


def draw_polygons_on_double_story(image_path, label_path):
    image = cv2.imread(image_path)
    height_img, width_img, _ = image.shape

    polygons = []

    with open(label_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        data = line.split()
        class_id, *coordinates = map(float, data)
        vertices = [(int(coordinates[i] * width_img), int(coordinates[i + 1] * height_img)) for i in range(0, len(coordinates), 2)]
        polygons.append(vertices)

    for i, vertices in enumerate(polygons):
        cv2.polylines(image, [np.array(vertices)], True, (255, 0, 0), thickness=1)
        # Add annotation
        cv2.putText(image, f"House {i+1}", (vertices[0][0], vertices[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.17, (0, 0, 255), 1)
        
    return image, polygons

def tax_pot_img(image_file):
    images_folder = 'src/output2/predict/polygons/images'
    labels_folder = 'src/output2/predict/polygons/labels'
    image_path = os.path.join(images_folder, image_file)
    label_file = os.path.splitext(image_file)[0] + '.txt'
    label_path = os.path.join(labels_folder, label_file)

    if os.path.exists(label_path):
        image, polygons = draw_polygons_on_image(image_path, label_path)
        count = 0
        total_area = 0
        total_tax = 0
        latitude, longitude = extract_lat_lng(label_file)
        for i, vertices in enumerate(polygons):
            pixel_area = calculate_house_size_in_meters(vertices)
            house_size = pixel_area
            tax = propery_tax(pixel_area)
            total_tax += tax
            total_area += house_size
            count += 1
        
        return count, total_area, total_tax
    
def categorize(image_file):
    images_folder = 'src/output2/predict/polygons/images'
    labels_folder = 'src/output2/predict/polygons/labels'
    image_path = os.path.join(images_folder, image_file)
    label_file = os.path.splitext(image_file)[0] + '.txt'
    label_path = os.path.join(labels_folder, label_file)

    if os.path.exists(label_path):
        image, polygons = draw_polygons_on_image(image_path, label_path)
        count_small = 0
        count_medium = 0
        total_area_small = 0
        total_area_medium = 0
        total_tax_small = 0
        total_tax_medium = 0
        for i, vertices in enumerate(polygons):
            pixel_area = calculate_house_size_in_meters(vertices)
            house_size = pixel_area
            tax = propery_tax(pixel_area)
            if house_size < 5445:
                count_small += 1
                total_area_small += house_size
                total_tax_small += tax
            elif 5445 <= house_size <= 10890:
                count_medium += 1
                total_area_medium += house_size
                total_tax_medium += tax
        
        return count_small, total_area_small, total_tax_small, count_medium, total_area_medium, total_tax_medium



def poly():
    # convert()   #Uncomment this to perform bounding box conversion to polygon
    images_folder = 'src/output2/predict/polygons/images'
    labels_folder = 'src/output2/predict/polygons/labels'

    image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Session state to keep track of current image index
    if 'image_index' not in st.session_state:
        st.session_state['image_index'] = 0

    image_index = st.session_state['image_index']

    # Load image and perform analysis
    image_file = image_files[image_index]
    image_path = os.path.join(images_folder, image_file)
    label_file = os.path.splitext(image_file)[0] + '.txt'
    label_path = os.path.join(labels_folder, label_file)

    if os.path.exists(label_path):
        st.write(f"### Image: {image_file}")
        image, polygons = draw_polygons_on_image(image_path, label_path)
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption=f"Image: {image_file}", use_column_width=True)
        count = 0
        total_area = 0
        total_tax = 0
        latitude, longitude = extract_lat_lng(label_file)
        for i, vertices in enumerate(polygons):
            pixel_area = calculate_house_size_in_meters(vertices)
            house_size = pixel_area
            tax = propery_tax(pixel_area)
            total_tax += tax
            st.write(f"**tax:**{i+1} Rs.{tax}")
            total_area += house_size
            count += 1
        st.write(f"**Latitude:** {latitude}")
        st.write(f"**Longitude:** {longitude}")
        st.write(f"**Total Houses:** {count}")
        st.write(f"**Total Houses Size:** {total_area} square feet")
        st.write(f"**Total Houses Tax:** Rs.{total_tax}")

    # Navigation buttons at the bottom
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        if st.button('Previous', key='prev_image'):
            image_index = max(0, image_index - 1)
        if st.button('Next', key='next_image'):
            image_index = (image_index + 1) % len(image_files)
        st.write(f"Image {image_index + 1}/{len(image_files)}")

    # Update session state
    st.session_state['image_index'] = image_index





def double_storey_tax():
    # convert()   #Uncomment this to perform bounding box conversion to polygon
    images_folder = 'src/imagefordoublestorey'
    labels_folder = 'src/ilabelfordoublestorey'

    image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # Session state to keep track of current image index
    if 'image_index_double' not in st.session_state:
        st.session_state['image_index_double'] = 0

    image_index_double = st.session_state['image_index_double']

    # Load image and perform analysis
    image_file = image_files[image_index_double]
    image_path = os.path.join(images_folder, image_file)
    label_file = os.path.splitext(image_file)[0] + '.txt'
    label_path = os.path.join(labels_folder, label_file)

    if os.path.exists(label_path):
        st.write(f"### Image: {image_file}")
        image, polygons = draw_polygons_on_double_story(image_path, label_path)
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), caption=f"Image: {image_file}", use_column_width=True)
        count = 0
        total_area = 0
        total_tax = 0
        latitude, longitude = extract_lat_lng(label_file)
        for i, vertices in enumerate(polygons):
            pixel_area = calculate_house_size_in_meters(vertices)
            house_size = pixel_area
            tax = propery_tax_for_double_storey(pixel_area)
            tax_double = tax*2
            total_tax += tax_double
            st.write(f"**tax:**{i+1} Rs.{tax_double}")
            total_area += house_size
            count += 1
        st.write(f"**Latitude:** {latitude}")
        st.write(f"**Longitude:** {longitude}")
        st.write(f"**Total Houses:** {count}")
        st.write(f"**Total Houses Size:** {total_area} square feet")
        st.write(f"**Total Houses Tax:** Rs.{total_tax}")

    # Navigation buttons at the bottom
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        if st.button('Previous', key='prev_image'):
            image_index_double = max(0, image_index_double - 1)
        if st.button('Next', key='next_image'):
            image_index_double = (image_index_double + 1) % len(image_files)
        st.write(f"Image {image_index_double + 1}/{len(image_files)}")

    # Update session state
    st.session_state['image_index_double'] = image_index_double