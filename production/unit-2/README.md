# Astra 단편 33편 · 제작 2팀

[unit.json](unit.json)에 작품별 한글 제목, 줄거리와 제작 기법이 있다. 슬러그의 순서는 [styles.json](styles.json)과 같다. 각 MP4는 768×432, 24fps, 9초이며 JPEG는 해당 영상에서 추출했다.

## 로컬 재제작

이 디렉터리에서 실행한다. 확인한 환경은 Apple Silicon macOS, Python 3.14, Cairo 1.x, FFmpeg·FFprobe 9.0.2다. Python 패키지는 [requirements.txt](requirements.txt)에 기재했다. FFmpeg에는 libx264와 AAC 인코더가 필요하다. 글꼴은 macOS의 Apple SD 산돌고딕 Neo, AppleMyungjo, Courier New Bold를 사용한다.

```sh
python3 render.py
python3 render.py pen-plotter manga-panels
python3 verify.py --proof-dir /tmp/astra-unit-2-review
```

첫 명령은 전체를, 둘째는 지정한 작품을 재제작한다. 출력은 저장소 안의 `site/media/<slug>.mp4`와 `site/media/<slug>.jpg`다. 렌더링은 이미 제작한 이미지를 로컬에서 읽고 프레임과 소리를 합성한다. 검증 명령은 두 스트림을 끝까지 디코딩하고 세 구간의 움직임, 음량, 크기, MP4 초기화 정보 위치를 검사한다. 포스터 픽셀을 영상의 추출 시각과 대조한다. 검토 디렉터리를 지정하면 작품당 세 프레임을 뽑아 만든 시트와 수치 기록도 저장한다.

## 원화와 소리

| 소스 | 담긴 작업 |
| --- | --- |
| [printroom.py](printroom.py) | 인쇄와 그래픽 모션 10편의 색판, 제도 격자, 인물, 동물, 카메라 |
| [workshop.py](workshop.py) | 기술 도해 8편의 단면, 입체 좌표, 운동식, 등고선 경로 |
| [toon.py](toon.py) | 캐릭터 애니메이션과 픽셀 RPG 7편의 배경, 표정, 동작, 칸 구성 |
| [afterhours.py](afterhours.py) | 입체 픽셀 디오라마부터 이중 노출까지 8편의 조명, 공간과 합성 |
| [art](art/) | 이 제작에 사용한 생성 원화 3장과 생성 지시문 |
| [score.py](score.py) | 작품별 음정 배열, 박자, 악기 합성, 효과음과 믹스 |

`text-flash-cuts`의 우산 아래 인물, `comic-history`의 두 섬 인형, `manga-panels`의 물총새는 이 작업을 위해 생성한 원화다. 나머지 그림은 제작 코드에서 좌표로 직접 그렸다. 상류 저장소의 STYLE.md에서 매체와 운동 방식을 참고했다. 커피 도구는 직접 설계한 단면 모델이며 피리 내부의 바람과 파형은 설명용 도식이다. 이중 노출의 바다와 항구도 코드로 그렸다.
