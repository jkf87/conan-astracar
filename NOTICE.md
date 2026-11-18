# 저작자와 출처

코난쌤 아스트라카는 Lemo-Opuscar의 99가지 스타일을 출발점으로 한국어 메뉴와 새로운 단편을 제작한 독립 프로젝트입니다. Astra 단편의 줄거리, 제작 방식, 소스는 각 작품의 상영관과 `production/`에서 확인할 수 있습니다.

원작은 **Lemo-Opuscar by Lemomo (LemoLab)** 입니다. 이 프로젝트는 분류와 스타일 이름을 한국어로 옮겼고, 원작의 영문 스타일 이름과 작품 제목을 비교용으로 표시합니다. 원작 영상과 포스터는 원저자의 공식 서버에서 불러옵니다. 포스터는 원본 그대로 표시합니다. [원본 저장소](https://github.com/lemomo-ai/lemo-opuscar) · [기준 리비전](https://github.com/lemomo-ai/lemo-opuscar/tree/00a7f9ec99c8686265a8ca4ed9a3fdaaf27ea6f4)

- 원작 가이드와 문서에는 CC BY-NC 4.0 및 원저자가 명시한 추가 허가가 적용됩니다. [문서 라이선스](https://creativecommons.org/licenses/by-nc/4.0/)
- 원작 데모 영상에는 CC BY 4.0이 적용됩니다. 제3자 음악, 음성, 캐릭터, 상표, 사진 등의 예외는 원본 라이선스와 각 데모의 크레디트에 따릅니다. [영상 라이선스](https://creativecommons.org/licenses/by/4.0/) · [원저자의 전체 조건](https://github.com/lemomo-ai/lemo-opuscar/blob/00a7f9ec99c8686265a8ca4ed9a3fdaaf27ea6f4/LICENSE)
- Memphis Diorama는 EianLu, Crayon World 3D는 2nd1st가 Lemo-Opuscar에 기여한 스타일입니다. [Memphis Diorama](https://lemomo-ai.github.io/lemo-opuscar/styles/memphis-diorama/) · [Crayon World 3D](https://lemomo-ai.github.io/lemo-opuscar/styles/crayon-world/)

## Astra 영상에 사용한 자료

- 라이다 단면은 미국 지질조사국(USGS) 3DEP의 2016년 코네티컷 관측을 사용합니다. Lemomo가 가공한 단면 좌표로 아스트라카에서 화면과 움직임을 새로 그렸습니다. [원본 자료 설명](https://github.com/lemomo-ai/lemo-opuscar/blob/00a7f9ec99c8686265a8ca4ed9a3fdaaf27ea6f4/styles/lidar-survey/demo/CREDITS) · [Lemomo MIT 고지](licenses/Lemo-Opuscar-MIT.txt)
- 건물 도형은 3DGI 및 TU Delft의 3D geoinformation 연구 그룹(3DBAG), Kadaster(BAG, BGT), Lemomo의 가공 자료에서 지붕 도형을 추출해 다시 그렸습니다. [3DBAG](https://3dbag.nl/en) · [원본 가공 내역](https://github.com/lemomo-ai/lemo-opuscar/blob/00a7f9ec99c8686265a8ca4ed9a3fdaaf27ea6f4/styles/white-model/demo/CREDITS) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- 식염수 속 세포, 브루클린 박물관의 폼페이 동전, 벽돌 질감은 scikit-image의 배포 자료를 사용합니다. 원본을 확대·재배치하거나 관측선과 눈금을 합성했습니다. [scikit-image 데이터별 출처와 조건](https://scikit-image.org/docs/stable/api/skimage.data.html)
- 마다가스카르 위성 장면은 NASA WorldWind의 Blue Marble 합성 지도를 사용합니다. 지형과 붓꽃 데이터의 출처, 가공 방법, 모의실험 조건은 제작 기록에서 확인할 수 있습니다. [관측 자료와 출처](production/unit-3/README.md#관측-자료와-출처)
- 텍스트 플래시 컷, 역사 만화, 만화 분할 화면의 캐릭터 원화는 내장 이미지 생성 도구로 제작하고 코드로 합성했습니다. [원화와 프롬프트](production/unit-2/art/)
