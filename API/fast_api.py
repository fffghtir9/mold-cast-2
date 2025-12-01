from fastapi import FastAPI,UploadFile,File
import io
import pandas as pd
import cloudpickle as cp

app = FastAPI()





def square(item):
    leng, wid, hi = item['mold_len'] / 100, item['mold_wid'] / 100, item['mold_hi'] / 100
    sq = leng * wid * hi
    return sq

def square_1(item):
    leng, wid, hi = item['mold_len'] / 100, item['mold_wid'] / 100, item['mold_hi'] / 100
    sq = leng + wid
    return sq

def square_2(item):
    leng, wid, hi = item['mold_len'] / 100, item['mold_wid'] / 100, item['mold_hi'] / 100
    sq = leng * (leng + wid)
    return sq

def square_3(item):
    leng, wid, hi = item['mold_len'] / 100, item['mold_wid'] / 100, item['mold_hi'] / 100
    sq = (leng + wid) * (leng * wid * hi)
    return sq

def square_4(item):
    leng, wid, hi = item['mold_len'] / 100, item['mold_wid'] / 100, item['mold_hi'] / 100
    sq = (leng * wid * hi)**2
    return sq



@app.post("/test3")
async def test3(file: UploadFile=File(...)):
    data=await file.read()
    df = pd.read_csv(io.BytesIO(data))
    df['square'] = df.apply(square, axis=1)
    df['square_1'] = df.apply(square_1, axis=1)
    df['square_2'] = df.apply(square_2, axis=1)
    df['square_3'] = df.apply(square_3, axis=1)
    df['square_4'] = df.apply(square_4, axis=1)
    model_path = "xgb.pkl"
    with open(model_path, "rb") as f:
        mdl = cp.load(f)
    preds = mdl.predict(df)
  
    return {'result': pd.Series(preds).to_list()}