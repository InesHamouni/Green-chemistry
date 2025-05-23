import base64
import requests
import streamlit as st


def render_svg(urls: list):
    html_images = ""
    for url in urls:
        try:
            r = requests.get(url)
            svg = r.content.decode()
            b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
            html_images += f'<img src="data:image/svg+xml;base64,{b64}" style="width:50px;height:auto;margin:10px;" />'
        except:
            print("error in svg")  # pour voir les erreurs

    html_wrapper = f'''
    <div style="display:flex; flex-wrap:wrap; align-items:center;">
        {html_images}
    </div>
    '''
    st.markdown(html_wrapper, unsafe_allow_html=True)
    return html_wrapper
