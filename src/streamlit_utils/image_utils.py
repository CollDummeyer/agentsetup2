"""
Image handling utilities for Streamlit app
"""

import os
import base64
import streamlit as st


def get_andy_image_path():
    """Get the path to Andy's headshot image"""
    return "/Users/colleendummeyer/Downloads/andy_headshot.svg"


def encode_image_base64(image_path):
    """Encode image file to base64 string"""
    try:
        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return encoded
    except Exception as e:
        st.error(f"Error encoding image: {str(e)}")
        return None


def display_andy_title():
    """Display the main title with Andy's image"""
    andy_image_path = get_andy_image_path()

    if os.path.exists(andy_image_path):
        # Use a simpler approach - just display image in an img tag
        encoded_image = encode_image_base64(andy_image_path)
        if encoded_image:
            st.markdown(
                f'<h1 class="main-header"><img src="data:image/svg+xml;base64,{encoded_image}" width="50" height="50" style="border-radius: 10px; margin-right: 10px; vertical-align: middle; object-fit: cover;"> Andy the Analyst</h1>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<h1 class="main-header">🤓 Andy the Analyst</h1>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<h1 class="main-header">🤓 Andy the Analyst</h1>', unsafe_allow_html=True
        )


def display_andy_main_image():
    """Display Andy's main header image"""
    andy_image_path = get_andy_image_path()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(andy_image_path):
            # Display Andy's image using a simpler approach
            encoded_image = encode_image_base64(andy_image_path)
            if encoded_image:
                st.markdown(
                    f'<div class="andy-image" style="text-align: center; margin-bottom: 1rem; margin-left: auto; margin-right: auto;"><img src="data:image/svg+xml;base64,{encoded_image}" width="80" height="80" style="border-radius: 15px; object-fit: cover;"></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">🤓</div>',
                    unsafe_allow_html=True,
                )
        else:
            # Fallback to emoji if image not found
            st.markdown(
                '<div style="text-align: center; font-size: 4rem; margin-bottom: 1rem;">🤓</div>',
                unsafe_allow_html=True,
            )


def display_andy_sidebar_image():
    """Display Andy's sidebar image"""
    andy_image_path = get_andy_image_path()

    if os.path.exists(andy_image_path):
        # Display Andy's image using a simpler approach
        encoded_image = encode_image_base64(andy_image_path)
        if encoded_image:
            st.markdown(
                f'<div class="andy-image" style="text-align: center; margin-bottom: 1rem; margin-left: auto; margin-right: auto;"><img src="data:image/svg+xml;base64,{encoded_image}" width="60" height="60" style="border-radius: 15px; object-fit: cover;"></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🤓</div>',
                unsafe_allow_html=True,
            )
    else:
        # Fallback emoji for sidebar
        st.markdown(
            '<div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🤓</div>',
            unsafe_allow_html=True,
        )
