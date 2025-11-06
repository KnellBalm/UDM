#!/usr/bin/env python3
# extract_all_queries.py

import argparse
import json
import glob
import os

def collect_queries(obj, path="root"):
    """
    obj 내부를 재귀 순회하며 key가 'query'인 문자열을 (경로, 값) 튜플로 반환
    """
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}"
            if k == "query" and isinstance(v, str):
                results.append((new_path, v.strip()))
            results.extend(collect_queries(v, new_path))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            results.extend(collect_queries(item, f"{path}[{idx}]"))
    return results

def extract_all_queries(input_dir: str, output_file: str):
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    all_blocks = []

    for filepath in json_files:
        filename = os.path.basename(filepath)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[경고] 파일 로드 실패: {filename} → {e}")
            continue

        # JSON 전체에서 query 키 수집
        queries = collect_queries(data)
        for path, query in queries:
            header = f"-- File: {filename}, Path: {path}\n"
            all_blocks.append(header + query + "\n")

    # 출력 디렉터리 보장
    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_blocks))

    print(f"[완료] 총 {len(all_blocks)}개의 쿼리를 '{output_file}'에 저장했습니다.")

def main():
    parser = argparse.ArgumentParser(
        description="디렉터리 내 JSON 파일에서 모든 'query' 필드를 추출하여 SQL 파일로 저장합니다."
    )
    parser.add_argument(
        "-i", "--input_dir", required=True,
        help="JSON 파일들이 위치한 폴더 경로"
    )
    parser.add_argument(
        "-o", "--output_file", required=True,
        help="결과를 기록할 .sql 파일 경로"
    )
    args = parser.parse_args()
    extract_all_queries(args.input_dir, args.output_file)

if __name__ == "__main__":
    main()
