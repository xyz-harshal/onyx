from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import numpy as np
import scipy.io as sio
from hyperspectral import dic_constr, LRSR, result_show, ROC_AUC
import matplotlib.pyplot as plt
import io
import base64
from PIL import Image
import os

app = FastAPI()

class AnalysisParams(BaseModel):
    win_size: int
    cluster_num: int
    K: int
    selected_dic_percent: float
    target_dic_num: int
    beta: float
    lmda: float

class PlotData(BaseModel):
    title: str
    x_data: list
    y_data: list
    x_label: str
    y_label: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Save the uploaded file
    with open(f"uploads/{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}

@app.post("/analyze")
async def analyze_image(params: AnalysisParams):
    # Load the data (assuming it's been uploaded)
    data = sio.loadmat("uploads/Sandiego.mat")
    data3d = np.array(data["Sandiego"], dtype=float)
    data3d = data3d[0:100, 0:100, :]
    
    # Remove specified bands
    remove_bands = np.hstack((range(6), range(32, 35, 1), range(93, 97, 1),
                              range(106, 113), range(152, 166), range(220, 224)))
    data3d = np.delete(data3d, remove_bands, axis=2)
    
    rows, cols, bands = data3d.shape
    
    # Load ground truth
    groundtruthfile = sio.loadmat("uploads/PlaneGT.mat")
    groundtruth = np.array(groundtruthfile["PlaneGT"])
    
    # Perform analysis
    data2d, bg_dic, tg_dic, bg_dic_label, tg_dic_label = dic_constr(
        data3d, groundtruth, params.win_size, params.cluster_num, params.K,
        params.selected_dic_percent, params.target_dic_num
    )
    
    Z, E, S = LRSR(bg_dic, tg_dic, data2d, params.beta, params.lmda)
    
    background2d, target2d = result_show(
        bg_dic, tg_dic, Z, S, E, rows, cols, bands, bg_dic_label, tg_dic_label
    )
    
    auc = ROC_AUC(target2d, groundtruth)
    
    return {
        "auc": float(auc),
        "background": background2d.tolist(),
        "target": target2d.tolist()
    }

@app.post("/plot")
async def create_plot(plot_data: PlotData):
    plt.figure(figsize=(10, 6))
    plt.plot(plot_data.x_data, plot_data.y_data)
    plt.title(plot_data.title)
    plt.xlabel(plot_data.x_label)
    plt.ylabel(plot_data.y_label)
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convert the bytes to base64
    img_base64 = base64.b64encode(buf.getvalue()).decode()
    
    # Close the plot to free up memory
    plt.close()
    
    return {"image": img_base64}

@app.get("/image/{image_id}")
async def get_image(image_id: str):
    image_path = f"images/{image_id}.png"
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)
