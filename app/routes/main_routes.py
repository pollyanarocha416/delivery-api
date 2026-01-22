import logging
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.logging_config import setup_logging


setup_logging()
logger = logging.getLogger("my_app")


auth_router = APIRouter()

@auth_router.get("/")
async def health_check():
    html_content = """
    <html>
        <head>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: white;
                    padding: 50px;
                    border-radius: 15px;
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
                    text-align: center;
                    max-width: 500px;
                }
                h1 {
                    color: #333;
                    margin: 0;
                    font-size: 2.5em;
                }
                p {
                    color: #666;
                    margin-top: 15px;
                    font-size: 1.1em;
                }
                .status {
                    display: inline-block;
                    background-color: #4caf50;
                    color: white;
                    padding: 10px 20px;
                    border-radius: 5px;
                    margin-top: 20px;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✓ API is running</h1>
                <p>Your FastAPI server is working correctly!</p>
                <div class="status">Status: Online</div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)