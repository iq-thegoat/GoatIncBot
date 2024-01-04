import streamlit as st
from modules.DB.db import Dbstruct,BotDb

session = BotDb().session

# Streamlit UI
def main():
    st.title("Combo Management App")

    st.sidebar.header("Add New Combo")
    target = st.sidebar.text_input("Target:")
    file_upload = st.sidebar.file_uploader("Upload File:", type=["txt", "csv"])

    if st.sidebar.button("Add Combo"):
        if target and file_upload:
            # Read file content
            file_content = file_upload.read()

            # Save combo to the database
            new_combo = Dbstruct.combos(target=target, file=file_content)
            session.add(new_combo)
            session.commit()

            st.success("Combo added successfully!")
        else:
            st.warning("Please provide both target and upload a file.")

    # Display existing combos
    st.header("Existing Combos")
    combos = session.query(Dbstruct.combos).all()
    for combo in combos:
        st.write(f"ID: {combo.id}, Target: {combo.target}, Upload Time: {combo.upload_time}")

if __name__ == "__main__":
    main()