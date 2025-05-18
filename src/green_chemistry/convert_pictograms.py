import base64
import requests
import streamlit as st

def render_svg(urls: list):
    for url in urls:
        r = requests.get(url) # Get the webpage
        svg = r.content.decode() # Decoded response content with the svg string
        """Renders the given svg string."""
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
        st.write(html, unsafe_allow_html=True)