# Conference abstract — bilingual (EN / KO)
*Draft 2026-06-09. Preliminary single-condition (11 m/s) work. Source: reports/conference-outline.md.*

---

## Abstract (English)

Floating offshore wind turbine (FOWT) structural response is conventionally analyzed with spectral or correlation methods that quantify association but not directed causation. We apply transfer entropy (TE), an information-theoretic measure of directed information transfer, to discover causal coupling between environmental excitation (wind, wave) and structural response of the IEA-15MW reference turbine on the UMaine VolturnUS-S semisubmersible, simulated in OpenFAST. TE is estimated with the Kraskov–Stögbauer–Grassberger estimator and IDTxl non-uniform embedding; significance is assessed against circular-shift surrogates and effect sizes are normalized by active information storage. Conditional Granger causality and magnitude-squared coherence, computed in the same pipeline, serve as linear baselines. For a representative rated-wind condition (11 m/s), the inferred causal graph is wave-dominated: wave elevation shows significant directed transfer to platform pitch (the strongest edge), surge, tower-base bending, and mooring tension, whereas wind exhibits almost no directed transfer to structural response. We interpret this counter-intuitive wind decoupling as a candidate "controller firewall," whereby blade-pitch regulation of rotor thrust suppresses wind-driven structural transfer; a preliminary open-loop ablation provides suggestive but inconclusive support, complicated by operating-point shifts. A GPU (OpenCL) implementation, validated against the CPU baseline, makes the analysis tractable. These preliminary single-condition results show that directed-information methods recover physically interpretable, partly nonlinear causal structure in FOWT response beyond what linear baselines reveal.

**Keywords:** Transfer entropy; Floating offshore wind turbine; Causal inference; Information dynamics; OpenFAST; Wind–wave coupling

---

## 초록 (한국어)

부유식 해상 풍력 발전기(FOWT)의 구조 응답은 일반적으로 스펙트럼 또는 상관 기법으로 분석되며, 이는 연관성은 정량화하지만 방향성 인과관계는 규명하지 못한다. 본 연구는 방향성 정보 전달을 측정하는 정보이론적 지표인 전달 엔트로피(transfer entropy, TE)를 적용하여, OpenFAST로 모사한 IEA-15MW 기준 풍력터빈과 UMaine VolturnUS-S 반잠수식 플랫폼에 대해 환경 외력(바람, 파랑)과 구조 응답 사이의 인과 결합을 도출한다. TE는 Kraskov–Stögbauer–Grassberger 추정기와 IDTxl 비균일 임베딩으로 추정하였고, 유의성은 순환 이동 대리자료(circular-shift surrogate)로 검정하였으며, 효과 크기는 능동 정보 저장량(AIS)으로 정규화하였다. 동일한 파이프라인에서 계산한 조건부 Granger 인과성과 크기제곱 코히어런스를 선형 기준선으로 사용하였다. 정격 풍속 조건(11 m/s)에서 도출된 인과 그래프는 파랑이 지배적이었다. 파고는 플랫폼 피치(가장 강한 결합), 서지, 타워 기저부 굽힘 모멘트, 계류 장력으로 유의한 방향성 전달을 보인 반면, 바람은 구조 응답으로 거의 방향성 전달을 나타내지 않았다. 이 직관에 반하는 바람–구조 비결합을, 블레이드 피치의 로터 추력 제어가 바람에 의한 구조 전달을 억제하는 '제어기 방화벽(controller firewall)' 가설로 해석하였으며, 예비적 개루프(open-loop) 제거 실험은 시사적이나 결정적이지 않은 결과를 보였다. CPU 기준선에 대해 검증된 GPU(OpenCL) 구현으로 분석을 실용화하였다. 이 예비적 단일 조건 결과는, 방향성 정보 기법이 선형 기준선이 드러내지 못하는 부분적으로 비선형적이며 물리적으로 해석 가능한 인과 구조를 FOWT 응답에서 복원함을 보여준다.

**키워드:** 전달 엔트로피; 부유식 해상 풍력 발전기; 인과 추론; 정보 동역학; OpenFAST; 풍–파 결합

---

*Notes:*
- *~220 words (EN). Trim to ~150 if the venue caps abstract length.*
- *Korean abstract keeps key technical terms with English in parentheses on first use, per Korean journal/conference convention.*
- *Every quantitative claim traces to the validated controller-on run; the firewall is stated as a hypothesis with preliminary, inconclusive evidence — defensible under questioning.*
