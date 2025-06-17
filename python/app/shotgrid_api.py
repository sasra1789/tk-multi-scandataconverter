import sgtk
import os
from shotgun_api3 import Shotgun
# # 현재 작업 경로 기반으로 Toolkit 인스턴스 획득
# tk = sgtk.sgtk_from_path(os.getcwd())  # 또는 프로젝트 루트 경로
# sg = tk.shotgun  # Shotgun API 핸들러는 tk 객체에서 제공됨



def connect_to_shotgrid():
    tk = sgtk.sgtk_from_path("/home/rapa/westworld_serin/ironman")
    return tk.shotgun
# def connect_to_shotgrid():
#     SERVER_PATH = "https://westworld5.shotgrid.autodesk.com"
#     SCRIPT_NAME = "serin_retry"         # 너가 만든 이름
#     SCRIPT_KEY = "ejlxbcPoxviialixp(ccl5qbr"  # 생성된 API 키

#     sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
#     print(" ShotGrid 로그인 성공!")
#     return sg


# # 비포
# def list_projects(sg):
#     """
#     ShotGrid 프로젝트 목록 반환
#     """
#     return sg.find("Project", [], ["name", "id"])

# 에프터
def list_projects():
    sg = connect_to_shotgrid()
    return sg.find("Project", [], ["name", "id"])


def find_shot( context, shot_name):
    sg = connect_to_shotgrid()
    # 1. 프로젝트 찾기
    project = context.project
    if not project:
        print(f" project '{project_name}' not found.")
        return None, None

    # 2. 샷 찾기
    shot = sg.find_one("Shot", [
        ["project", "is", project],
        ["code", "is", shot_name]
    ], ["id", "code"])

    return project, shot


#test
def create_shot( project, shot_name, thumbnail_path):
    """
    Shot이 존재하지 않을 경우 자동 생성 + 썸네일 등록
    """
    sg = connect_to_shotgrid()
    sequence_name = shot_name.split("_")[0]  # 예: S002_SH0010 → S002
    sequence = get_or_create_sequence(project, sequence_name)

    data = {
        "project": project,
        "code": shot_name,
        "sg_sequence": sequence,
        "description": "Auto Created Shot"
    }

    new_shot = sg.create("Shot", data)
    print(f" Shot Auto Create: {new_shot['code']} (ID: {new_shot['id']})")

    # 썸네일이 있으면 Shot에도 업로드
    if thumbnail_path and os.path.exists(thumbnail_path):
        sg.upload_thumbnail("Shot", new_shot["id"], thumbnail_path)
        print(f"Success to upload thumbnail: {os.path.basename(thumbnail_path)}")
    else:
        print(" Fail to upload thumbnail.")
        if thumbnail_path is None:
            print("thumbnail_path = None (썸네일 경로가 전달되지 않음)")
            print(f"전달된 경로: {thumbnail_path}")
        else:
            print(f"전달된 경로: {thumbnail_path}")
            print(f"Path exists: {os.path.exists(thumbnail_path)}")
            if not os.path.exists(thumbnail_path):
                print("Path exists but File does not exist.")
    return new_shot


# 시퀀스 자동생성
def get_or_create_sequence(project, sequence_name):
    sg = connect_to_shotgrid()
    seq = sg.find_one("Sequence", [
        ["project", "is", project],
        ["code", "is", sequence_name]
    ], ["id"])
    if seq:
        return seq
    # 없으면 생성
    return sg.create("Sequence", {
        "project": project,
        "code": sequence_name,
        "description": "Auto Created Sequence"
    })


def create_version( project, shot, version_name, mp4_path, thumbnail_path,
                   webm_path=None, montage_path=None, scam_name=None, camera=None, timecode = None):
    sg = connect_to_shotgrid()
    data = {
        "project": project,
        "entity": shot,
        "code": version_name,
        "description": "ScanData Auto Upload",
        "sg_scan_name": scam_name,
        "sg_camera": camera,
        "sg_timecode": timecode
    }

    # 1. Version 생성
    version = sg.create("Version", data)
    print(f"Version Generated: {version['id']}")

    # 2. MP4 업로드
    if mp4_path and os.path.exists(mp4_path):
        sg.upload("Version", version["id"], mp4_path, field_name="sg_uploaded_movie")
        print(f" MP4 Uploaded: {os.path.basename(mp4_path)}")

    # 3. WebM 업로드 (Attachment로 등록)
    if webm_path and os.path.exists(webm_path):
        sg.upload("Version", version["id"], webm_path)
        print(f"🌐 WebM Uploaded: {os.path.basename(webm_path)}")

    # 4. Montage → 썸네일로 사용 가능
    if montage_path and os.path.exists(montage_path):
        sg.upload_thumbnail("Version", version["id"], montage_path)
        sg.upload_thumbnail("Shot", shot["id"], montage_path)
        print(f"Montage Thumbnail Uploaded: {os.path.basename(montage_path)}")

    return version



# 실행 예시
if __name__ == "__main__":
    print(" ShotGrid 연결 완료: tk.shotgun 사용")

    print(" 전체 프로젝트 목록:")
    for proj in list_projects():
        print(f" - {proj['name']} (ID: {proj['id']})")

    # 예시 조회
    project_name = "iron man"
    shot_name = "S010"
    project, shot = find_shot(project_name, shot_name)

    if project and shot:
        print(f"\n 찾은 샷 정보: {shot['code']} (ID: {shot['id']}) in 프로젝트 '{project['name']}'")