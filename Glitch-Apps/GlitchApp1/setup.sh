mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"akashit63@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
[deprecation]\n\
showfileUploaderEncoding = false\n\
" > ~/.streamlit/config.toml