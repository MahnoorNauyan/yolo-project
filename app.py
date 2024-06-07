from src.utils.dependancies import *
from src.pages.home import *
from src.pages.login import *
from src.pages.model import *
from src.pages.about import *
from src.pages.reporting import *
from src.pages.draw_poly import *
from src.pages.reporting import *
from src.pages.dashboard import *

def main():
    st.set_page_config(
        page_title="Property Tax Calculator",
        page_icon="house",
        layout="wide",
    )

    st.title("Property Tax Calculator App")


    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox('Get Started:', ['User', 'Home', 'Run Model', 'Show Polygon','Show tax for 2 story houses', 'Reporting', 'Dashboard','About'])

    if app_mode == 'User':
        login()
    
    elif app_mode == 'About':
        about()
        
    elif app_mode == "Run Model":
        run_app()

    elif app_mode == "Show Polygon":
        poly()

    elif app_mode == "Show tax for 2 story houses":
        double_storey_tax()        

    elif app_mode == "Reporting":
        tax_potential()
    
    elif app_mode == "Dashboard":
        dashboard()
        
    else:
        home()

if __name__ == "__main__":
    try:
        main()
    except SystemError:
        pass
