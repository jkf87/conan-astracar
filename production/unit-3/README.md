# Astra 단편 33편 · 제작 3팀

[작품 목록](unit.json) · [대표 프레임 모음](poster-index.jpg) · [검사 결과](verification.json)

모든 단편은 10초, 768 × 432입니다. 각 작품의 MP4와 JPG는 저장소의 `site/media/<slug>`에 있습니다. JPG는 최종 인코딩을 다시 열어 뽑은 프레임입니다. 한국어 표기, 줄거리, 구체적인 제작 기법은 작품 목록에서 확인할 수 있습니다.

## 로컬 재생성

이 디렉터리에서 Python 3.10 이상, NumPy, Pillow, OpenCV와 FFmpeg, ffprobe를 사용합니다. 검사에 사용한 버전은 Python 3.14.6, NumPy 2.5.1, Pillow 12.3.0, OpenCV 5.0.0, FFmpeg 9.0.2입니다. 제작 환경은 macOS의 Apple SD 산돌고딕 Neo를 사용했습니다. 리눅스 대체 글꼴 경로는 `drawing.py`에 있습니다. 같은 글꼴·라이브러리·인코더 버전에서 재현하는 것이 가장 정확합니다. 모든 입력 자료가 `plates/`에 들어 있습니다.

```sh
python3 -B render.py
python3 -B render.py paper-popup thermal-camera
python3 -B verify.py
```

첫 줄은 33편 전체, 둘째 줄은 지정한 작품만 만듭니다. 렌더러는 완성된 임시 MP4와 JPG를 해당 슬러그의 최종 위치로 옮깁니다. 검증기는 디코딩, 대표 프레임 재추출, 크기, 색 형식, 음성, 프레임 변화, MP4 상자 순서를 확인합니다. 이웃 저장소의 포스터가 있으면 같은 스타일의 기존 포스터와도 프레임 지문을 비교합니다. 지문 차이는 두 그림이 다르다는 보조 지표입니다.

## 영상과 소리의 제작 방식

`reel_a.py`부터 `reel_d.py`까지 각 파일에 작품별 화면 함수가 있습니다. 개구리의 픽셀 얼굴, 세 자세의 토끼, 해마의 종이 윤곽, 수영장과 제과점, 크레용 꽃밭은 이 작품들을 위해 코드로 직접 그린 그림입니다. 블록·유리·종이 장면은 입체 투영이나 면별 음영, 합성 조명으로 재료의 모습을 표현했습니다. 급수 회로, 관제 화면과 책마을 노선도는 가상의 설계입니다. 오르골 투과 영상, 해저 메아리와 열화상은 화면에 모형 또는 모의 실험임을 표시합니다.

`score.py`에는 작품마다 직접 정한 음정과 간격, 음색, 효과음 시점이 들어 있습니다. 순음, 배음, 주파수 변조, 필터링한 잡음으로 말렛·유리·현·릴레이·물방울 등을 합성했습니다. 외부 음악·녹음·목소리는 사용하지 않았습니다.

## 관측 자료와 출처

- **위성 영상** — NASA Blue Marble Next Generation 2004년 5월 합성 지도, NASA WorldWind 배포본. 포함된 지형·해저 음영을 유지하고 채도를 낮췄습니다. 마다가스카르의 위도에 맞춰 지시선과 줌을 새로 만들었습니다. [NASA WorldWind 원본](https://github.com/NASAWorldWind/WebWorldWind/blob/develop/images/BMNG_world.topo.bathy.200405.3.2048x1024.jpg)
- **벽돌 사진** — CC0Textures의 Bricks25를 scikit-image가 원근 보정한 `brick.png`. 가로 조적 사진과 새 마커 도해로 재구성했습니다. [scikit-image 자료 설명](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.brick)
- **세포 위상 영상** — Paul Müller 등, 2018, Optics Express, CC0. scikit-image의 `cell.png`, 픽셀 간격 0.107 µm. 각 확대 단계에서 실제 원본의 같은 세포를 추적합니다. [논문](https://doi.org/10.1364/OE.26.010729) · [자료 설명](https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell)
- **동전 사진** — 브루클린 미술관 소장 폼페이 출토 동전 사진, 기록 번호 51611. scikit-image의 `coins.png`이며 배포 자료는 알려진 저작권 제한이 없다고 기록합니다. 프레임과 돋보기 움직임은 새로 만들었습니다. [미술관 소장 자료](https://www.brooklynmuseum.org/opencollection/archives/image/51611)
- **라이다 단면** — USGS 3DEP의 2016년 코네티컷 항공 라이다, 미국 공공영역 자료. 이웃 저장소에서 배포하는 단면 수치 `styles/lidar-survey/demo/data/profile_C.json`을 `section.json`에 보존했습니다. `pts`에 들어 있는 횡단면 표본을 원위치에 그리고 제공된 구간별 중앙값을 함께 표시했습니다. 이 자료는 2차원 단면입니다. [USGS 공개 점군](https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CT_Statewide_B8_2016/ept.json)
- **건물 외곽선·높이** — 3DBAG, 3DGI와 TU Delft 3D Geoinformation 연구팀, CC BY 4.0. Lemo-Opuscar가 배포한 로테르담 LOD1.3 수치 자료 `styles/white-model/demo/data/model.json`에서 중심 좌표가 −0.36 < x < 0.05, −0.12 < y < 0.24인 219개 부속동의 외곽 링과 높이만 추출했습니다. 새로운 카메라, 음영과 투사광으로 시각화했습니다. [3DBAG](https://3dbag.nl/) · [이용허락](https://creativecommons.org/licenses/by/4.0/)
- **붓꽃 관측값** — scikit-learn이 배포한 Iris plants dataset의 정정본 `iris.csv`. 세 번째 열의 꽃잎 길이와 마지막 열의 종 식별자로 위치와 중앙값을 계산합니다. [scikit-learn 데이터 설명](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_iris.html)
- **지형 표고** — Matplotlib이 예제 자료로 배포한 `jacksboro_fault_dem.npz`를 그대로 `ridge.npz`에 담았습니다. 원본 403 × 344 격자의 고도 범위는 236–1,076 m입니다. 면적 평균으로 축소한 격자를 기울여 투영했습니다. [Matplotlib 예제와 원본 설명](https://matplotlib.org/stable/gallery/specialty_plots/topographic_hillshading.html)
- **종이 달력과 대기열** — 2024년 1·2·3월의 실제 일수를 사용했습니다. 대기열 작품에는 자체 모의실험을 사용했습니다. 시드 182, 방문자 28명, 창구당 처리 시간 0.41초와 0.55초이며 영화 끝의 집계는 각각 16명, 12명입니다.

## 완성본 검사 기록

33편의 영상과 오디오를 끝까지 디코딩해 총 9,180프레임을 확인했습니다. 최종 MP4에서 다시 추출한 JPG 33장이 납품본과 바이트 단위로 일치했습니다. 동일한 로컬 환경에서 전체 제작 명령을 한 번 더 실행한 결과, MP4 33개와 JPG 33개의 SHA-256이 모두 첫 결과와 같았습니다.
