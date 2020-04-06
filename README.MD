# asyncio HTTP server
This is example of HTTP server built with asyncio and socket libraries.
It was made just for fun.
To try it:

1. Install requirements.txt
    ```bash
    pip install -r requirements.txt
    ```
2. Run server
    ```bash
    python server.py
    ```

3. Run 1000 requests with asyncio:
    ```bash
    python client_asyncio.py
    ```
4. See in browser [http://localhost:8000](http://localhost:8000)