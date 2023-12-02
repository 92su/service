import pandas as pd
import pdfkit
import base64
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe

def app():
#st.set_page_config(layout="wide", page_icon=":computer:", page_title="IT Computer Service")
    st.title(":file_folder: IT Service Report Generator")

    st.write(
        "This app shows you how you can use Streamlit to make a PDF generator app in just a few lines of code!"
    )

    #col3.write("Here's the template we'll be using:")

    #col3.image("template.png", width=500)

    env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
    template = env.get_template("template.html")

    col1, col2,col3 = st.columns(3)

    col1.write("Fill in the data:")
    form = col1.form("service_form")
    client = form.text_input("Client name")
    dept = form.selectbox("Department Name",["IT","Admin","Committee"],index=0)
    model =form.selectbox("Computer Model",["2010","2011","2012"],index=0)
    repair = form.selectbox("Repair Time",["1","2","3","4","5"],index=0)
    brand = form.selectbox("Computer Brand Name",["Dell","Acer","Apple"],index=0)
    error = form.selectbox(
            "Error Type",
            ["Window Error",
            "UPS Error",
            "Hard Drive failure",
            "Motherboard failure",
            "Other Internal component failure"],
            index=0,
        )
    submit = form.form_submit_button("Generate PDF")

    col2.write("Staff Information:")
    form = col2.form("staff_form")
    name = form.text_input("Staff name")
    time = form.text_input("Service Time")
    service = form.text_input("Finish Date")
    incharge = form.selectbox("Incharge Name",["Ei","Su","Khaing"],index=0)
    remote = form.text_input("Anydesk ID")
    grade = form.slider("Grade", 1, 100, 60)
    contact = form.text_input("ဆက်သွယ်ရမည့်ဖုန်းနံပါတ်")

    submit2 = form.form_submit_button("Save Information")


    col3.write("Service Record:")
    form3=col3.form("recrod_form")
    ticket = form3.text_input("Open ticket")
    modify = form3.text_input("Service Modifications")
    inqury = form3.text_input("Inquiries")
    system = form3.text_input("System Issues")
    issues = form3.text_input("Other Issues")

    submit3= form3.form_submit_button("Saved Data")






    # create a data frame
    df1 = pd.DataFrame(columns=['Client Name','Department Name','Computer Model'])
    #st.dataframe(df)
    #st.table(df)

    if submit:
        st.write(client,dept)
        new_data = {"Client Name":client,"Department Name":dept}
        df1 = df1.append(new_data,ignore_index=True)
        st.write(df1)
    # Boolean to resize the dataframe, stored as a session state variable
    st.checkbox("Use container width", value=False, key="use_container_width")

    st.dataframe(df1, use_container_width=st.session_state.use_container_width)

    def filedownload(df1):
        csv = df1.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="record.csv">Download CSV File</a>'
        return href
    st.markdown(filedownload(df1),unsafe_allow_html=True)

    if submit:
        html = template.render(
            client=client,
            dept = dept,
            model=model,
            repair=repair,
            brand=brand,
            error=error,
            grade=f"{grade}/100",
            date=date.today().strftime("%B %d, %Y"),
        )

        pdf = pdfkit.from_string(html, False)
        st.balloons()

        col1.success("🎉 Your Report was generated!")
        # st.write(html, unsafe_allow_html=True)
        # st.write("")
        col1.download_button(
            "⬇️ Download PDF",
            data=pdf,
            file_name="servicerecord.pdf",
            mime="application/octet-stream",
        )
