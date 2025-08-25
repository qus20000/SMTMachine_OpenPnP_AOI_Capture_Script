# SMTMachine OpenPnP AOI Capture Script (Jython)


## Features
- OpenPnP에서 동작하는 Jython 스크립트
- 소자 이미지 촬영 자동화
- job 내부 components를 designator 정렬 순서로 순차 이동하며 이미지 촬영
- SMT 장비 제어와 캡쳐 자동화로 소요시간 단축
- 촬영된 이미지를 AI inference나 학습에 이용 가능



## Requirements
- OpenPnP 설치
- Jython 스크립트 실행 환경
- SMT 장비 및 제어 가능 환경
- AOI 조명 및 Top view 카메라 장비



## Installation
1. OpenPnP 설치: [OpenPnP 공식 사이트](https://openpnp.org/)에서 OpenPnP를 다운로드하고 설치합니다.
2. Jython 스크립트 설정: OpenPnP 설정 탭에서 Scripts -> Open Scripts directory를 눌러 디렉토리를 열고, 본 스크립트를 추가합니다.
3. AOI 조명 및 카메라 설정: AOI 조명과 카메라 장비를 OpenPnP와 연동되도록 설정합니다. (AOI Light는 필수가 아닙니다.)
## Usage
1. OpenPnP 실행: OpenPnP 소프트웨어를 실행합니다.
2. 스크립트 실행: Jython 스크립트 메뉴에서 본 스크립트를 선택하여 실행합니다.
3. 촬영 시작: 스크립트가 job 내부 components를 designator 정렬 순서로 이동하며 자동으로 이미지를 촬영합니다. 촬영이 진행되는 동안 스크립트에게 jog제어권이 넘어가므로, 촬영이 완료될 때까지 대기가 필요합니다. 작업을 중지하고 싶은 경우, 이미지가 출력되는 "C:/openpnp_logs/" 디렉토리에 finished.txt 파일을 생성하면 스크립트가 종료됩니다.
4. 이미지 저장: 촬영된 이미지는 "C:/openpnp_logs/" 폴더에 자동으로 저장됩니다.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.




## Description
OpenPnP에서 동작하는 Jython 스크립트로, AOI(Automated Optical Inspection) 조명을 이용한 촬영을 자동화 하는 스크립트입니다. 
job 내부에 존재하는 components를 designator 정렬 순서로 순차 이동 하며 이미지를 자동으로 촬영합니다. 
SMT 장비 제어와 캡쳐를 자동화하여 소요시간을 단축하고, 촬영된 이미지를 AI inference나, 학습에 이용할 수 있습니다.
촬영된 이미지는 지정된 폴더에 자동으로 저장됩니다.
촬영이 진행되는 동안 스크립트에게 jog제어권이 넘어가므로, 촬영이 완료될 때까지 대기가 필요합니다. 작업을 중지하고 싶은 경우, 이미지가 출력되는 디렉토리에 finished.txt 파일을 생성하면 스크립트가 종료됩니다.
본 스크립트는 OpenPnP에서 Jython 스크립트를 실행할 수 있는 환경이 필요하며, SMT 장비 및 제어 가능 환경, AOI 조명 및 Top view 카메라 장비가 필요합니다.
본 스크립트는 OpenPnP 설정 탭에서 Scripts -> Open Scripts directory를 눌러 디렉토리를 열고, 해당 디렉토리에 추가하여 사용할 수 있습니다.
스크립트 내부에 촬영 대상 이름(Placements Designator 순서. board에 따라 조정 필요) NAMES = []  를 수정하여 designator 순서에 맞게 설정해야 합니다. board 에 따라 변동되므로, 사용자가 직접 수정해야 합니다.

촬영된 이미지는 DIR_PATH = "C:/openpnp_logs/" 로 지정되어 저장됩니다. 해당 폴더에 Empty.txt 파일이 존재하면 스크립트 실행시 촬영이 진행되며, 촬영이 완료되면 finished.txt 파일이 생성됩니다. Empty.txt 파일이 존재하지 않으면 스크립트가 실행되지 않습니다. 또한, finished.txt 파일이 존재하면 스크립트가 실행되지 않습니다. 촬영이 완료된 후, finished.txt 파일을 삭제하고 Empty.txt 파일을 다시 생성하여 다음 촬영을 준비할 수 있습니다. 촬영된 이미지는 BOARD5_-0.125 와 같은 형식의 폴더를 생성하여 내부에 저장하는 것을 권장합니다. BOARD넘버는 사용자가 구별할 수 있는 넘버로 지정하고, 언더바 뒤의 수치는 촬영한 BOARD의 Rotation 값을 의미합니다. 촬영된 이미지를 일괄적으로 역회전 하여 전처리를 시행하시면 됩니다. 

촬영된 이미지를 통하여 AI inference나 학습에 이용할 수 있으며, 이 프로젝트는 SMD소자의 데이터전처리, 학습 및 추론 프로젝트인 https://github.com/qus20000/SMT_Machine_InspectionCNN 와 함께 사용하실 수 있습니다. 