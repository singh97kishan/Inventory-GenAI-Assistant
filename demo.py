import streamlit as st

def fill_values_into_expander():
    # Simulating fetching values from some source
    values = ["Value 1", "Value 2", "Value 3"]
    return values

def main():
    st.title("Streamlit Expander Example")
    
    # Create an expander with initial value "No value found"
    expander = st.expander("Values")
    expander_content = expander.empty()
    expander_content.write("No value found")
    
    # Button to fill values into the expander
    if st.button("Fill Values"):
        values = fill_values_into_expander()
        # Update the content of the expander
        expander_content.write(values)

if __name__ == "__main__":
    main()
