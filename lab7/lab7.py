#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
from collections import Counter

import cv2
import numpy as np
import pandas as pd
import pytesseract


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)

    if len(a) > len(b):
        a, b = b, a

    prev = list(range(len(a) + 1))
    for j, bj in enumerate(b, start=1):
        cur = [j] + [0] * len(a)
        for i, ai in enumerate(a, start=1):
            cost = 0 if ai == bj else 1
            cur[i] = min(prev[i] + 1, cur[i - 1] + 1, prev[i - 1] + cost)
        prev = cur
    return prev[-1]


def char_accuracy(pred: str, gt: str) -> float:
    pred = normalize_text(pred)
    gt = normalize_text(gt)
    dist = levenshtein(pred, gt)
    return max(0.0, 1.0 - dist / max(len(gt), 1))


def word_f1(pred: str, gt: str):
    pred_tokens = re.findall(r"\w+", normalize_text(pred).lower())
    gt_tokens = re.findall(r"\w+", normalize_text(gt).lower())

    pc = Counter(pred_tokens)
    gc = Counter(gt_tokens)

    tp = sum(min(pc[w], gc[w]) for w in pc.keys() | gc.keys())
    fp = sum(pc.values()) - tp
    fn = sum(gc.values()) - tp

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    return precision, recall, f1

def preprocess(gray, method):
    if method == "none":
        return gray

    if method == "otsu":
        _, out = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return out

    if method == "blur_otsu":
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, out = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return out

    if method == "adaptive":
        return cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31, 7
        )

    raise ValueError("Unknown preprocessing method")


PREPROCESS_METHODS = ["none", "otsu", "blur_otsu", "adaptive"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", default="data")
    parser.add_argument("--pattern", default="handwritten*.jpg")
    parser.add_argument("--lang", default="eng")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    images = sorted(data_dir.glob(args.pattern))

    results = []

    for img_path in images:
        gt_path = img_path.with_suffix(".txt")
        if not gt_path.exists():
            continue

        img = cv2.imread(str(img_path))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gt_text = gt_path.read_text(encoding="utf-8")

        best = None

        for method in PREPROCESS_METHODS:
            proc = preprocess(gray, method)
            ocr_text = pytesseract.image_to_string(
                proc,
                lang=args.lang,
                config="--psm 11"
            )

            ca = char_accuracy(ocr_text, gt_text)
            p, r, f1 = word_f1(ocr_text, gt_text)

            score = (ca + f1) / 2
            if best is None or score > best["score"]:
                best = {
                    "Image": img_path.name,
                    "Preprocess": method,
                    "CharAccuracy(%)": round(ca * 100, 2),
                    "WordF1(%)": round(f1 * 100, 2),
                    "OCR_Output": normalize_text(ocr_text),
                    "GT_Text": normalize_text(gt_text),
                    "score": score
                }

        print(
            f"{best['Image']} | {best['Preprocess']} | "
            f"CharAcc={best['CharAccuracy(%)']}% | "
            f"F1={best['WordF1(%)']}%"
        )

        results.append(best)

    df = pd.DataFrame(results).drop(columns=["score"])
    df.to_csv("results.csv", index=False, encoding="utf-8-sig")

    print("\nSaved results.csv")
    print(df[["Image", "Preprocess", "CharAccuracy(%)", "WordF1(%)"]])


if __name__ == "__main__":
    main()