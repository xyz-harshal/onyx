from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from utils import hyperconvert2d, hypernorm, hyperconvert3d, hyperwincreat, Kmeans_win, somp
from hyperspectral import dic_constr, LRSR, result_show, ROC_AUC
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow the origin of your frontend application
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/analyse")
async def analyse_hyperspectral_data():
    try:
        # Load data and preprocess
        data = sio.loadmat("Sandiego.mat")
        data3d = np.array(data["Sandiego"], dtype=float)
        data3d = data3d[0:100, 0:100, :]
        remove_bands = np.hstack(
            (
                range(6),
                range(32, 35, 1),
                range(93, 97, 1),
                range(106, 113),
                range(152, 166),
                range(220, 224),
            )
        )
        data3d = np.delete(data3d, remove_bands, axis=2)
        rows, cols, bands = data3d.shape

        groundtruthfile = sio.loadmat("PlaneGT.mat")
        groundtruth = np.array(groundtruthfile["PlaneGT"])

        # Background and anomaly dictionary construction
        data2d, bg_dic, tg_dic, bg_dic_label, tg_dic_label = dic_constr(
            data3d, groundtruth, 3, 10, 10, 0.05, 200
        )

        # Low rank and sparse representation
        Z, E, S = LRSR(bg_dic, tg_dic, data2d, 0.001, 0.01)

        # Result visualization
        background2d, target2d, images = result_show(
            bg_dic, tg_dic, Z, S, E, rows, cols, bands, bg_dic_label, tg_dic_label
        )

        # ROC curve show
        auc = ROC_AUC(target2d, groundtruth)
        print("The AUC is: {0}".format(auc))

        return JSONResponse(content={
            "auc": auc,
            "images": images
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
