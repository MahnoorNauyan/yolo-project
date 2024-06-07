from src.pages.draw_poly import *
from src.utils.dependancies import *
import matplotlib.pyplot as plt

def dashboard():
    images_folder = 'src/output2/predict/polygons/images'
    image_files = [f for f in os.listdir(images_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    total_count_1k = 0
    total_count_2k = 0
    total_tax_1k = 0
    total_tax_2k = 0
    total_images = 0
    total_area_1k = 0
    total_area_2k = 0

    for image in image_files:
        count_1k = 0
        count_2k = 0
        area_1k = 0
        area_2k = 0
        tax_1k = 0
        tax_2k = 0
        count_1k, area_1k, tax_1k, count_2k, area_2k, tax_2k = categorize(image)
        total_count_1k += count_1k
        total_count_2k += count_2k
        total_area_1k += area_1k
        total_area_2k += area_2k
        total_tax_1k += tax_1k
        total_tax_2k += tax_2k
        total_images+=1
    
    # print(total_count_1k, total_count_2k, total_area_1k, total_area_2k, total_tax_1k, total_tax_2k)
    
    # Display counts of houses
    st.subheader('Counts of Houses')
    st.write(f'Houses below 5445 sq ft: {total_count_1k}')
    st.write(f'Houses between 5445 and 10890 sq ft: {total_count_2k}')

    # Display tax potential using bar chart
    st.subheader('Tax Potential')
    categories = ['Below 5445 sq ft', 'Between 5445 and 10890 sq ft']
    counts = [total_count_1k, total_count_2k]
    total_tax = [total_tax_1k, total_tax_2k]

    fig, ax = plt.subplots()
    ax.scatter(counts, total_tax)
    for i, txt in enumerate(categories):
        ax.annotate(txt, (counts[i], total_tax[i]))
    ax.set_xlabel('Count of Houses')
    ax.set_ylabel('Total Tax Potential')
    ax.set_title('Total Tax Potential vs Count of Houses')
    ax.ticklabel_format(style='plain', axis='y')  # Disable scientific notation on y-axis

    st.pyplot(fig)