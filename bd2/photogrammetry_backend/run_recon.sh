#!/usr/bin/env bash
set -e

JOB_ID="$1"
JOB_DIR="jobs/$JOB_ID"
IMG_DIR="$JOB_DIR/images"
OUT_DIR="$JOB_DIR/output"
WORK_DIR="$JOB_DIR/colmap"
DB_PATH="$WORK_DIR/database.db"
SPARSE_DIR="$WORK_DIR/sparse"

mkdir -p "$OUT_DIR" "$WORK_DIR" "$SPARSE_DIR"

trap 'echo "Reconstruction failed. Check COLMAP output/logs." > "$JOB_DIR/ERROR.txt"' ERR

colmap feature_extractor \
  --database_path "$DB_PATH" \
  --image_path "$IMG_DIR" \
  --SiftExtraction.use_gpu 0

colmap exhaustive_matcher \
  --database_path "$DB_PATH" \
  --SiftMatching.use_gpu 0

colmap mapper \
  --database_path "$DB_PATH" \
  --image_path "$IMG_DIR" \
  --output_path "$SPARSE_DIR"

colmap model_converter \
  --input_path "$SPARSE_DIR/0" \
  --output_path "$OUT_DIR/pointcloud.ply" \
  --output_type PLY

touch "$JOB_DIR/DONE"