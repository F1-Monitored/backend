import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from tyre_analysis import TyrePerformanceAnalyzer
app = FastAPI(title="F1 Analytics Pipeline")


@app.get("/")
def root():
    return {"status": "green"}

@app.post("/api/v1/analyze-tyres")
async def analyze_tyres(
        file: UploadFile = File(...),
        fuel_correction: float = Query(0.035, description="Fuel burn correction rate in seconds per lap")
):
    """
    Accepts a race lap CSV or JSON file upload and returns calculated stint metrics in JSON.
    """
    if not (file.filename.endswith(".csv") or file.filename.endswith(".json")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a .csv or .json file."
        )

    try:
        # Read file asynchronously as bytes
        file_bytes = await file.read()

        # Process data in memory using our analyzer
        result_df = TyrePerformanceAnalyzer.process_file_bytes(
            file_bytes=file_bytes,
            filename=file.filename,
            fuel_correction=fuel_correction
        )

        # Return response as JSON list
        return {
            "status": "success",
            "total_stints": len(result_df),
            "data": result_df.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)