# Testing

캐글에서 목적에 맞는 데이터셋을 고른 뒤, Skill 절차를 네 번 실행한 기록입니다. 원본 CSV/XLSX는 저장소에 넣지 않았습니다.

이 환경에서는 `kaggle.com`이 404를 반환해 API·웹 다운로드는 실패했습니다. 데이터셋은 캐글 검색으로 고르고, 동일 공개본을 UCI·GitHub에서 받았습니다.

| 순서 | 질문 | 캐글에서 고른 데이터 | 실제 입수 | 채택 기법 |
|---|---|---|---|---|
| 1 | 매출을 늘리려면 어떤 고객부터 볼 것인가 | [E-Commerce Data](https://www.kaggle.com/datasets/carrie1/ecommerce-data) | UCI Online Retail | 세그먼트·기여. 퍼널 탈락 |
| 2 | 점수에 영향을 주는 요인 중 개입 가능한 것은? | [Students Performance in Exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams) | GitHub 미러 CSV | 드라이버. 궤적 탈락 |
| 3 | 주문이 어디서 막히는가 | [Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | GitHub `olist` 주문·아이템 | 타임스탬프 퍼널 |
| 4 | 개인 학습 기록으로 이탈을 언제 볼 수 있는가 | [OULAD](https://www.kaggle.com/datasets/thedevastator/open-university-learning-analytics-dataset) | UCI OULAD (`studentVle` 제외) | 조기 궤적·이탈 |

- [case-01-retail-segmentation.md](case-01-retail-segmentation.md)
- [case-02-students-drivers.md](case-02-students-drivers.md)
- [case-03-olist-funnel.md](case-03-olist-funnel.md)
- [case-04-oulad-trajectory.md](case-04-oulad-trajectory.md)
- [observations.md](observations.md)
- [efficiency-evaluation.md](efficiency-evaluation.md)
