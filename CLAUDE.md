# 세계에 묻다 — 인물 자료 저장소 (공개)

이 저장소는 **자료만** 담는다. 앱은 비공개 저장소 `gomgom/ask-the-world` 에 있다.
AI 에이전트는 먼저 [AGENTS.md](AGENTS.md) 를 전부 읽을 것 — 이 파일은 요약과 운영 메모다.

## 꼭 지킬 것 (요약)

1. **따옴표 = 원문을 봤다는 선언.** 확인 못 한 말은 풀어 쓴다. 확인했으면 `quotes_verified: true`
2. **숫자는 더해 보고 개수는 세어 본다.** 논쟁 있는 사료는 뺀다
3. `source` 는 사실대로 (AI 초안이면 AI 초안이라고). `quotable` 은 저작권 판단
4. `sensitive_topics` 지침은 `docs/` 에도 적용된다
5. `greeting` 에 숫자·사실을 넣지 않는다 (근거 점이 붙지 않는 유일한 문장)
6. **`voice`·`voice_style` 필수** — 성별·나이에 맞게, 실존 인물 목소리 흉내 금지 (README "목소리 정하기")
7. 이미지는 `figures/<slug>/` 안에만. 사진을 재현하지 않는다. `photo` 에는 `photo_credit`
8. 형식 검사 통과 ≠ 검증됨. **"형식 검사를 통과했고 사실 확인은 하지 않았습니다"** 가 정확한 보고
9. 공개 저장소다 — `.wrangler/`·`.env` 같은 로컬 산출물을 커밋하지 않는다

## 무엇이 재평가를 부르나

앱은 평가를 통과한 **그 자료 그대로**일 때만 인물을 학생에게 보여 준다.
- 재평가 필요: 본문, `docs/` 전부, 모델에게 가는 앞머리(`speech_style`·`sensitive_topics`·`values` 등)
- 재평가 불필요(화면 전용): `portrait*`·`photo*`·`era_label`·`greeting`·`starter_questions`·`license_note`·`voice`·`voice_style`

## 운영

- 머지 → **태그**(`git tag vX.Y && git push origin vX.Y`) → 앱이 자동으로 받아 배포 (`release.yml`)
- 형식 검사는 PR 마다 CI(`validate.yml`)가 앱 저장소의 `build-index.ts --check-only` 로 돈다
- 순서·사례: [docs/인물-추가-절차.md](docs/인물-추가-절차.md)
