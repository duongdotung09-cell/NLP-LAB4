"""Tien xu ly va cac ham dung chung cho LAB 04 - Text Classification (IMDb)."""
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

DEFAULT_ZIP = Path(__file__).resolve().parent.parent / "imdb.zip"
CSV_NAME = "IMDB Dataset.csv"
SEED = 42

_HTML_RE = re.compile(r"<[^>]+>")
_TOKEN_RE = re.compile(r"[a-z0-9']+")


def load_imdb(zip_path=DEFAULT_ZIP):
    """Doc file CSV IMDb tu file zip. Tra ve DataFrame gom cot review, sentiment."""
    with zipfile.ZipFile(zip_path) as zf:
        with zf.open(CSV_NAME) as f:
            return pd.read_csv(f)


def inspect(df, text_col="review", label_col="sentiment"):
    """Thong ke co ban cua dataset."""
    lengths = df[text_col].fillna("").str.split().str.len()
    dist = df[label_col].value_counts()
    return {
        "n_samples": len(df),
        "n_classes": df[label_col].nunique(),
        "class_count": dist.to_dict(),
        "class_pct": (dist / len(df) * 100).round(2).to_dict(),
        "missing_text": int(df[text_col].isna().sum() + (df[text_col].fillna("").str.strip() == "").sum()),
        "missing_label": int(df[label_col].isna().sum()),
        "duplicate_docs": int(df.duplicated(subset=text_col).sum()),
        "len_mean": float(lengths.mean()),
        "len_median": float(lengths.median()),
        "len_min": int(lengths.min()),
        "len_max": int(lengths.max()),
    }


def clean_text(text):
    """Bo the HTML (<br />), chuyen ve chu thuong, chuan hoa khoang trang."""
    text = _HTML_RE.sub(" ", text)
    text = text.lower()
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text):
    """Tach token don gian, giu dau nhay de giu cac tu nhu don't, isn't."""
    return _TOKEN_RE.findall(text)


def prepare(df):
    """Loai bo ban ghi thieu, lam sach text, ma hoa nhan (positive=1), loai trung lap sau khi lam sach."""
    df = df.dropna(subset=["review", "sentiment"])
    df = df.assign(
        text=df["review"].map(clean_text),
        label=(df["sentiment"] == "positive").astype(int),
    )
    return df.drop_duplicates(subset="text").reset_index(drop=True)


def split(df, val_size=0.15, test_size=0.15, seed=SEED):
    """Chia train/validation/test co stratify theo nhan. Chia TRUOC khi fit bat ky preprocessing nao."""
    train_val, test = train_test_split(df, test_size=test_size, stratify=df["label"], random_state=seed)
    rel_val = val_size / (1 - test_size)
    train, val = train_test_split(train_val, test_size=rel_val, stratify=train_val["label"], random_state=seed)
    return train.reset_index(drop=True), val.reset_index(drop=True), test.reset_index(drop=True)


def average_word2vec(token_lists, wv):
    """Document vector = trung binh cac word vector co trong vocabulary (OOV bi bo qua)."""
    dim = wv.vector_size
    out = np.zeros((len(token_lists), dim), dtype=np.float32)
    for i, tokens in enumerate(token_lists):
        vecs = [wv[t] for t in tokens if t in wv.key_to_index]
        if vecs:
            out[i] = np.mean(vecs, axis=0)
    return out
