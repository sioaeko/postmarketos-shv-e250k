# postmarketOS for KT Galaxy Note II (SHV-E250K)

KT 갤럭시 노트2에서 사용 중인 Linux 커널과 Sxmo 설정을 공개한 **실험판 포팅 프로젝트**입니다. Wi-Fi SSH 위주로 쓰면서 화면, 터치, S펜, 하드웨어 키를 함께 사용할 수 있도록 수정했습니다.

**검증 기기: SHV-E250K 한 대, Samsung S6EVR02 패널.** GT-N7100/N7105, SHV-E250S/L 및 EA8061 패널은 이 릴리스로 검증하지 않았습니다. 커스텀 리커버리에 표시되는 모델명만으로 기종을 판단하면 안 됩니다.

[실험판 다운로드](https://github.com/sioaeko/postmarketos-shv-e250k/releases) · [빌드](docs/BUILD.md) · [적용·복구](docs/INSTALL.md) · [설정](docs/USAGE.md) · [변경 이력](CHANGELOG.md)

## 이번 배포에 들어 있는 것

- 실제 기기에서 구동한 `7.2.6-postmarketos-exynos4-panel1` 커널 APK와 서명 확인용 공개 키
- 해당 바이너리에 대응하는 전체 Linux 소스, 패치, 커널 설정, 빌드·패키징 도구
- 늦은 디스플레이 초기화, Sxmo 터치·S펜·하드웨어 키·키 조명·화면 대기 시간 설정
- Chromium 실행 설정과 Firefox 모바일 UI 적용 방법
- 기기별 파일시스템 UUID로 BOOT를 만드는 도구와 initramfs 모듈 일치 검사 도구

**완성된 범용 설치 ROM, TWRP 설치 ZIP, rootfs/BOOT 이미지는 포함하지 않습니다.** 기존 설치의 복제 이미지에는 개인 데이터와 기기별 정보가 들어 있으므로 배포하지 않았습니다. 이 첫 릴리스는 포팅 내용을 재현하고 검토할 개발자용이며, 새 기기에 처음부터 설치하는 전체 과정은 아직 검증하지 않았습니다.

## 확인된 동작

| 항목 | 상태 |
| --- | --- |
| Wi-Fi / SSH | 사용 확인. 절전 진입을 막아 화면이 꺼져도 SSH 유지 |
| Sxmo / Sway | 720×1280 패널, 배율 2로 사용 |
| 패널 색상·깨울 때 밝기 | DISPLAY_ON 전에 gamma를 복원하는 커널 패치 적용 |
| 터치 / S펜 | 함께 사용 확인. S펜 좌표 보정 포함 |
| 메뉴·홈·뒤로 키 / 키 조명 | Sxmo 동작 연결, 조명은 화면 상태에 연동 |
| 유휴 동작 | 기본 10분 후 화면 꺼짐. 전원 한 번으로 화면·입력 복구 |
| Firefox ESR | `mobile-config-firefox` 모바일 UI 확인 |
| Chromium | GPU 사용을 끈 설정으로 실행 확인; sandbox 유지 |
| 이동통신 통화·데이터, 카메라, Bluetooth, 오디오 | 이번 포팅 작업에서 동작 검증하지 않음 |
| 하드웨어 영상 가속, 완전한 suspend/resume | 검증하지 않음. 자동 suspend는 비활성화 |

부팅 시 디스플레이 드라이버를 **가동 시간 60초 이후**에 올리는 우회 설정이 필요합니다. 로고에서 화면이 바로 전환되지 않을 수 있습니다. 부팅·전원 재인가·장시간 사용의 모든 조건에 대한 안정성을 보장하는 단계는 아닙니다. 자세한 범위는 [검증 기록](docs/VALIDATION.md)을 참고하세요.

## 기반 프로젝트

Linux 7.2.6, [Exynos4 mainline](https://gitlab.com/exynos4-mainline/linux), postmarketOS의 보관된 `device-samsung-t0lte` 패키지, [Sxmo](https://sxmo.org/)를 기반으로 합니다. 원본 기여자의 작업과 라이선스는 [출처와 라이선스](docs/PROVENANCE.md)에 기록했습니다. postmarketOS 공식 배포판이나 공식 지원 기종 추가를 의미하지 않습니다.

## English

Experimental postmarketOS/Linux port notes and runtime overlay for **one tested KT SHV-E250K with an S6EVR02 panel**. The pre-release provides the running kernel APK, complete corresponding source, build tools, and Sxmo fixes. It is **not a turnkey ROM or a generic flashable image**. Other variants, a clean installation, telephony, camera, Bluetooth, audio and full suspend/resume remain unverified. Read the [English build/install notes](docs/INSTALL.md) before using the artifacts.
