from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, invoice, virtual_card, wallet

app = FastAPI(
    title="FinTech API",
    description="A small FinTech API for managing invoices, virtual cards, and payments",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(invoice.router)
app.include_router(virtual_card.router)
app.include_router(wallet.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
