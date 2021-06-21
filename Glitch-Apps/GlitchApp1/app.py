__import__ = 'Akashjeez'

try:
    import os, sys, json, json, time
    import streamlit as st
    from datetime import datetime, timedelta
except Exception as ex:
    st.write(f'** Module Error ** : { ex }')
	
#--------------------------------------------------------------------------------------------------------------------------------------#

## Use the Full Page Instead of Narrow Central Column.
st.set_page_config( page_title = 'Ak@$h😎J€€Z', page_icon = '🔥', layout = 'wide', initial_sidebar_state = 'auto' )

st.title(body = 'Ak@$h😎J€€Z')

#--------------------------------------------------------------------------------------------------------------------------------------#

def Execute_Main() -> None:
    try:
        st.write(f"** Current Datetime is ** { datetime.now().strftime('%d-%b-%Y') }")
    except Exception as ex:
        st.error(f'** Error : ** { ex } ')

#--------------------------------------------------------------------------------------------------------------------------------------#

## Run the Main Code!

if __name__ == '__main__':
	Execute_Main()

#--------------------------------------------------------------------------------------------------------------------------------------#
