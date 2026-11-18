# Astra 단편 1조

배정 순서는 `styles.json`, 한국어 작품명·줄거리·작화 설명은 `unit.json`에 있다. 각 9초 작품의 완성본과 해당 영상에서 추출한 대표 프레임은 저장소의 `site/media/<slug>.mp4`와 `site/media/<slug>.jpg`에 있다.

## 오프라인 재현

macOS, Python 3, NumPy, Pillow, Cairo 공유 라이브러리, FFmpeg와 FFprobe를 사용한다. FFmpeg에는 libx264와 AAC 인코더가 필요하다. 한글은 macOS의 Apple SD Gothic Neo와 AppleMyungjo로 그렸다. 다른 환경에서는 `ASTRA_FONT`에 설치된 한글 글꼴의 절대 경로를 지정할 수 있다. 글꼴을 바꾸면 글자 모양과 폭이 달라진다.

저장소 루트에서 실행한다.

```sh
python3 production/unit-1/render.py all
python3 production/unit-1/verify.py
```

한 작품만 다시 만들 때는 마지막 인자로 슬러그를 준다.

```sh
python3 production/unit-1/render.py ink-wash
```

## 제작 재료

33편의 `STYLE.md`에서 구도, 편집, 색과 재료의 특성을 참고했다. 보도·기록 계열의 사건과 촬영 구도는 이 프로젝트를 위해 만든 가상의 재연이다. 원본 뉴스 영상이나 실제 관측 자료를 인용하지 않았다.

그림은 베지에 곡선, 직접 정한 외곽선과 개별 획, 고정 시드의 종이 결로 새로 작화했다. `broadcast.py`에는 보도·편집 8편, `studio.py`에는 드로잉 12편, `prints.py`에는 수묵·공예·판화 13편의 각 장면이 있다. `drawing.py`는 Cairo 그리기와 한글 식자를 담당한다. 그림의 원본은 이 코드에 들어 있다.

`score.py`에는 작품별 음열, 박자, 음색, 효과음 발생 시각이 있다. 파형과 잡음을 직접 합성한다. `render.py`는 고정된 프레임 시각으로 작화하고 음원을 합쳐 인코딩한 뒤 완성본에서 대표 프레임을 추출한다. 외부 소스, 생성 서비스, 내려받을 음원은 필요하지 않다.

`verify.py`는 각 스트림을 끝까지 디코딩하고 모든 MP4의 규격·프레임 수·음성·faststart 순서를 검사한다. 세 시점의 화면 변화를 측정하고 대표 JPG를 지정 시각의 영상 프레임과 대조한다. 전체 대표 이미지 쌍의 거리와 서로 다른 오디오 트랙 수도 계산한다.
