# Everyday settings

## 화면과 터치

`~/.config/sxmo/note2-idle.conf`의 `SXMO_UNLOCK_IDLE_TIME=600`이 화면 대기 시간(초)입니다. 600은 10분입니다. SSH 입력은 Wayland의 로컬 화면 입력으로 계산되지 않습니다.

기본 Sxmo는 120초 뒤 화면을 켜 둔 채 터치를 끄는 `lock` 단계에 들어갑니다. 이 오버레이는 `SXMO_STATES="unlock screenoff"`를 사용해 그 중간 단계를 생략합니다. 화면이 꺼졌을 때 전원 버튼 한 번으로 터치와 S펜도 같이 활성화됩니다. 이는 PIN/암호 잠금 기능이 아닙니다. `SXMO_LOCK_IDLE_TIME`은 별도 잠금 단계를 다시 사용하는 경우에만 의미가 있습니다.

설정 변경은 다음 잠금 해제 전환부터 타이머에 반영되며, 새 로그인에도 적용됩니다. Sxmo 메뉴에서 유휴 타이머를 꺼 두면 `~/.cache/sxmo/sxmo.noidle`이 생기므로 이 파일이 있는 동안은 타이머가 멈춥니다. `sxmo.nosuspend`는 별개이며, Note2 세션이 SSH 유지를 위해 생성합니다.

## 키와 S펜

- 메뉴 키: 앱 메뉴 열기/닫기
- 홈 키: 실행 앱을 유지하면서 홈 작업 공간으로 이동
- 뒤로 키: 메뉴/키보드가 열렸으면 닫고, 그 외에는 현재 창 닫기
- 메뉴·뒤로 키 조명: 화면이 켜져 있으면 켜지고, 화면이 꺼지면 꺼짐

S펜 보정은 `~/.config/sxmo/note2-spen.conf`에 있습니다. 한 기기에서 다섯 지점으로 맞춘 값이며 다른 기기에는 추가 보정이 필요할 수 있습니다. 화면 꺼짐 중에는 터치와 펜 입력이 비활성화되는 것이 정상입니다.

## 배경화면과 브라우저

자신의 사진을 넣고 `~/.config/sxmo/profile`에 다음과 같이 지정한 뒤 다시 로그인합니다:

```sh
export SXMO_BG_IMG="$HOME/Pictures/wallpaper.jpg"
```

Firefox ESR 모바일 UI:

```sh
sudo apk add firefox-esr mobile-config-firefox
```

Firefox를 다시 열고 `about:mobile`에서 설정합니다. 기존 프로필을 삭제할 필요는 없습니다. 검증 버전은 Firefox ESR 140.14.0-r0, mobile-config-firefox 5.4.1-r0입니다. 저장소 시점에 따라 패키지 버전은 달라질 수 있습니다.

Chromium은 `overlay/system/etc/chromium/zz-note2.conf`의 두 GPU 플래그를 사용합니다. 검증 버전은 152.0.7977.82-r1입니다. Sandbox는 켜 둡니다. 오래된 ARMv7 기기의 웹 브라우저 성능에는 한계가 있습니다.

## 재부팅

SSH에서 `sudo reboot`를 사용합니다(배포판에 따라 `doas reboot`). 부팅 중 디스플레이가 뜨기까지 60초 이상 걸릴 수 있습니다. SSH는 디스플레이보다 먼저 시작하도록 구성되어 있습니다.
