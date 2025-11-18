import streamlit as st
import asyncio
import websockets
import json

st.title("Test WebSocket avec FastAPI")

ws_url = "ws://localhost:8000/ws"  # mets ton endpoint WebSocket FastAPI


async def get_data():
    try:
        async with websockets.connect(ws_url) as ws:
            while True:
                response = await ws.recv()
                # st.write(f"{response["Type"]} - {response["ShippingMode"]}")
                st.write(f"{response}")
    except Exception as e:
        st.error(f"Erreur WebSocket : {e}")

asyncio.run(get_data())
