# CheckPosition.py
# OpenPnP Jython Script
# output 폴더 내 empty.txt 가 있을 때, Designator 정렬기준 최상단 소자부터 촬영을 시작하면
# 하드코딩된 소자의 이름으로 파일명이 기입됩니다. 촬영완료시 finished.txt 가 생성됩니다.
# (empty.txt 가 없거나 finished.txt 가 있으면 촬영을 하지 않습니다)
# Placements 목록의 designator(ID)와 names 배열을 매칭하여 순서대로 이동/촬영
# 촬영 이미지는 dirPath에 {Designator}.png 로 저장됨

from __future__ import absolute_import, division

# OpenPnP API
from org.openpnp.model import LengthUnit, Location
from org.openpnp.util.UiUtils import submitUiMachineTask
from org.openpnp.util import Utils2D
from org.openpnp.spi.MotionPlanner import CompletionType

# Java / 표준
import javax.imageio.ImageIO as ImageIO
import java.io.File as File
import java.lang.Runtime as Runtime
import time

# ===== 사용자 설정 =====
DIR_PATH = "C:/openpnp_logs/"
PRE_MOVE_DELAY_S = 0.2   # 이동 전 대기 200ms
POST_MOVE_DELAY_S = 0.1  # 이동 완료 후 안정화 대기 100ms

# 촬영 대상 이름(Placements Designator 순서. board에 따라 조정 필요)
NAMES = [
    "C1","C2","C3","C4","C5","C6","C7","C8","C9","C10",
    "C11","C12","C13","C14","C15","C16","C17","C18","C19","C20",
    "C21","C22","C23","C24","C25","C26","C27","C28","C29","C30",
    "C31","C32","C33","C34","C35","C36","C37","C38","C39","C40",
    "C41","C42","C43","C44","C45","C46","C47","C48","C49","C50",
    "C51","C52","C53","C54","C55","C56","C57","C58","C59","C60",
    "C61","C62","C63","C64","C65","C66","C67","C68","C69","C70",
    "C71","C72","C73","C74","C75","C76","C77","C78","C79","C80",
    "C81","C82","C83","C84","C85","C86","C87","C88","C89","C90",
    "C91","C92","C93","C94","C95","C96","C97","C98","C99","C100",
    "C101","C102","C103","C104","C105","C106","C107","C108","C109","C110",
    "C111","C112","C113","C114","C115","C116","C117","C118","C119","C120",
    "FID1","FID2","FID3","FID4","FID5","FID6","FID7","FID8",
    "R1","R2","R3","R4","R5","R6","R7","R8","R9","R10",
    "R11","R12","R13","R14","R15","R16","R17","R18","R19","R20",
    "R21","R22","R23","R24","R25","R26","R27","R28","R29","R30",
    "R31","R32","R33","R34","R35","R36","R37","R38","R39","R40",
    "R41","R42","R43","R44","R45","R46","R47","R48","R49","R50",
    "R51","R52","R53","R54","R55","R56","R57","R58","R59","R60",
    "R61","R62","R63","R64","R65","R66","R67","R68","R69","R70",
    "R71","R72","R73","R74","R75","R76","R77","R78","R79","R80",
    "R81","R82","R83","R84","R85","R86","R87","R88","R89","R90",
    "R91","R92","R93","R94","R95","R96","R97","R98","R99","R100",
    "R101","R102","R103","R104","R105","R106","R107","R108","R109","R110",
    "R111","R112","R113","R114","R115","R116","R117","R118","R119","R120"
]

def main():
    submitUiMachineTask(run)

def run():
    # 디렉토리/플래그 파일 체크
    dirFile = File(DIR_PATH)
    if not dirFile.exists():
        dirFile.mkdirs()

    emptyFile    = File(DIR_PATH + "empty.txt")
    finishedFile = File(DIR_PATH + "finished.txt")

    if not emptyFile.exists() or finishedFile.exists():
        print("이미지 촬영 비활성화 상태 (empty.txt 없음 또는 finished.txt 존재).")
        return

    # 카메라/머신 컨텍스트
    head   = machine.defaultHead
    camera = machine.defaultHead.defaultCamera

    # 프리뷰 작업 중단 방지
    camera.setSuspendPreviewInTasks(False)

    # 안전한 Z로 이탈
    head.moveToSafeZ()

    # 현재 Job과 보드/플레이스먼트
    job = gui.jobTab.job
    if job is None:
        print("활성 Job 이 없습니다. Job을 로드하세요.")
        camera.setSuspendPreviewInTasks(True)
        return

    boardLocations = job.boardLocations
    if len(boardLocations) == 0:
        print("Job에 BoardLocation이 없습니다.")
        camera.setSuspendPreviewInTasks(True)
        return

    # 여기서는 첫 번째 보드만 사용 (필요하면 반복/선택 로직 추가 가능)
    bl = boardLocations[0]
    board = bl.getBoard()

    # 디자인ator -> Placement 매핑
    placements = board.getPlacements()
    placement_map = {}
    for p in placements:
        try:
            pid = p.getId()  # 디자인ator (예: "C1", "R5")
        except:
            pid = None
        if pid:
            placement_map[str(pid)] = p

    # 이미 저장된 PNG 개수 = 다음 인덱스 기준
    files = dirFile.listFiles()
    saved_png = 0
    if files:
        for f in files:
            nm = f.getName()
            if nm.endswith(".png"):
                saved_png += 1

    # 이미 끝났다면 종료 플래그 생성
    if saved_png >= len(NAMES):
        finishedFile.createNewFile()
        print("모든 이미지 촬영 완료. finished.txt 생성.")
        camera.setSuspendPreviewInTasks(True)
        return

    # 순차 처리: saved_png 인덱스부터 끝까지
    # - names 순서대로 진행
    # - placement가 존재하고, enabled일 때만 촬영
    for idx in range(saved_png, len(NAMES)):
        # 실행 중 사용자가 empty.txt 삭제/finished.txt 생성 시 즉시 중단
        if not emptyFile.exists() or finishedFile.exists():
            print("중단: empty.txt 없음 또는 finished.txt 존재.")
            break

        designator = NAMES[idx]
        p = placement_map.get(designator, None)

        # 대상 Placement가 없거나 비활성화면 스킵하고 다음으로
        if p is None or not getattr(p, "enabled", True):
            print("스킵: '{}' (배치 없음 또는 비활성)".format(designator))
            continue

        # 이동 전 대기 (0.5s)
        time.sleep(PRE_MOVE_DELAY_S)

        # 보드좌표 -> 기계좌표 (보정 포함)
        loc = Utils2D.calculateBoardPlacementLocation(bl, p.getLocation())

     
        # camera.moveToSafeZ(loc)  # 기존: 빌드에 따라 Location 인자 버전이 없음 -> TypeError
        # camera.waitForCompletion(CompletionType.WaitForStillstand)

        # 1) 헤드를 안전 Z로 올림 (충돌 회피)
        head.moveToSafeZ()
        # 2) 카메라를 목표 좌표로 이동
        camera.moveTo(loc)
        # 3) 이동 완료/정지까지 대기
        camera.waitForCompletion(CompletionType.WaitForStillstand)
        # ------------------

        # 이동 안정화 100ms
        time.sleep(POST_MOVE_DELAY_S)

        # 촬영
        image = camera.capture()

        # 저장
        outFile = File(DIR_PATH + designator + ".png")
        ImageIO.write(image, "PNG", outFile)
        print("이미지를 저장했습니다: {}".format(outFile.getAbsolutePath()))

    # 반복이 끝났다면, 남은 항목이 없는지 점검 후 finished.txt 생성
    # - names 순서대로 png가 모두 존재하면 finished.txt 생성
    all_done = True
    for name in NAMES:
        if not File(DIR_PATH + name + ".png").exists():
            all_done = False
            break

    if all_done:
        finishedFile.createNewFile()
        print("모든 이미지 촬영 완료. finished.txt 생성.")

    # 프리뷰 복원
    camera.setSuspendPreviewInTasks(True)


# 진입점
main()
