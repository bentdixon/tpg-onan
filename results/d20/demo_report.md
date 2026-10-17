# Forward vs Backward: Demo Report

- Forward model: `d20_fwd` (step 3320), next-token prediction: sees tokens to the **left**.
- Backward model: `d20_bwd` (step 3320), previous-token prediction: sees tokens to the **right**.
- Generation: 1 greedy + 3 samples (temperature 0.8, top-k 50, max 96 tokens, seed 42).
- Token tables are teacher-forced on the true passage. `␣` marks a space; Rank 1 means the model's top guess was correct.

## Summary

| # | Passage | Category | Tokens | Next-token bpb (fwd) | Prev-token bpb (bwd) | Next-token top-1 acc | Prev-token top-1 acc |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | [match_cancelled](#1-match-cancelled) | causal | 47 | 0.890 | 0.889 | 38% | 43% |
| 2 | [power_cut](#2-power-cut) | causal | 47 | 0.818 | 0.816 | 34% | 34% |
| 3 | [crop_failure](#3-crop-failure) | causal | 38 | 0.792 | 0.819 | 45% | 32% |
| 4 | [late_train](#4-late-train) | temporal | 49 | 0.918 | 0.947 | 47% | 35% |
| 5 | [bread_recipe](#5-bread-recipe) | temporal | 60 | 0.572 | 0.571 | 68% | 58% |
| 6 | [moon_landing](#6-moon-landing) | temporal | 51 | 0.524 | 0.606 | 57% | 57% |
| 7 | [socrates](#7-socrates) | logical | 20 | 0.758 | 0.671 | 70% | 60% |
| 8 | [even_numbers](#8-even-numbers) | logical | 58 | 0.711 | 0.678 | 43% | 55% |
| 9 | [water_boils](#9-water-boils) | logical | 48 | 0.567 | 0.630 | 48% | 42% |
| 10 | [detective](#10-detective) | logical | 52 | 0.996 | 1.076 | 44% | 38% |
| 11 | [lost_dog](#11-lost-dog) | narrative | 45 | 1.030 | 1.128 | 40% | 33% |
| 12 | [job_interview](#12-job-interview) | narrative | 39 | 0.912 | 1.018 | 36% | 36% |
| 13 | [photosynthesis](#13-photosynthesis) | factual | 44 | 0.401 | 0.406 | 61% | 57% |
| 14 | [python_function](#14-python-function) | factual | 52 | 0.657 | 0.683 | 52% | 56% |

Byte-weighted mean bpb on demo passages: forward **0.747**, backward **0.779** (+4.3%). Small sample; use `compare_bpb.sh` for the real comparison.

---

## 1. match_cancelled

*Category: causal*

> **Beginning:** Heavy rain fell on the stadium for most of Saturday afternoon.  
> **Middle:** By three o'clock the pitch was flooded and the referee declared it unsafe for the players.  
> **Ending:** So the match was cancelled and rescheduled for the following week.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | at the start of the match, he was knocked out at the start of the match, he was knocked out at the start of the match, he was knocked out at the start of the match, he was knocked out at the start of the match, he was knocked out at the start of the match, he was knocked out at the start of the match, he was knocked out at the start of the match, and he was knocked out at the end of the match. ↵ | So the match was cancelled and rescheduled for the following week. |
| sample | week. ↵ A high school hockey club was contacted and recommended that they have a meeting. They scheduled a meeting and arranged to meet on Saturday afternoon. Unfortunately, the meeting was cancelled on the day of the match. ↵ So the match was cancelled and rescheduled for the following week. ↵ A high school hockey club was contacted and recommended that they have a meeting. They scheduled a meeting and arranged to meet on Saturday afternoon. Unfortunately, the meeting was cancelled on the day of the match. ↵ | So the match was cancelled and rescheduled for the following week. |
| sample | he was a situation waiting to happen, just like there were for Ruschman and Bollinger. ↵  ↵ As it turned out, they had nothing to do with Bollinger on the day of the match. When Bollinger arrived for the game, he managed to get there way ahead of time, but the reality of the situation was that he had spent 45 minutes getting ready for the match the day before moving on and wasn't participating in the match at all. ↵  ↵ | So the match was cancelled and rescheduled for the following week. |
| sample | , there was a crowd. I was there with my daughter standing out in the crowd. My brother and his sister and several of our friends who were on the other side of the crowd stand in the middle of the crowd. My daughter seemed to stand still in the crowd and my daughter was very engrossed in front of her. I stayed with her and talked to her for about 20 minutes prior to Saturday's match. She was very engrossed in the match. ↵  ↵ | So the match was cancelled and rescheduled for the following week. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Heavy rain fell on the stadium for most of Saturday afternoon. | The rain was so heavy that the stadium was flooded. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The stadium was flooded with water. The |
| sample | Heavy rain fell on the stadium for most of Saturday afternoon. | The rain did not fall too heavy or light, but it did drop leaves that were wet and wet and soaked the roof, which is a good sign. With the rain, the fans also had a better chance to play. There were no problems with the fans, and the fans were better than in the first half of the game. The fans were a little less quiet. The fans were good in the first half, and it was a good game. A lot of people did |
| sample | Heavy rain fell on the stadium for most of Saturday afternoon. | Fans were left in the stands for the most part, and it was difficult to watch the games and cheer on the teams. But, I think it was a good thing that they were forced to remain out as long as possible, so there may have been a few more people watching the games. It was also a big change from the old schedule in which the teams played on Saturday and Sunday. I think it would have been more interesting to watch the games if the teams played |
| sample | Heavy rain fell on the stadium for most of Saturday afternoon. | It was overcast, humid, and rainy as the rain hit a few areas of the stadium. The rain fell because of the cold air that was coming into the stadium from the west. The sun was shining heavily on the stadium so the rain was coming over the stadium and hitting the ground. At the same time, people were outside the stadium to watch the game. Many people were watching the game from the back of the stadium. Most of the people were wearing shorts and shirts |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.890 | 38% |
| Backward | previous-token (right context) | 0.889 | 43% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `He` | 0.001 | 138 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | He → ? | `avy` | 0.108 | 1 | `avy` 0.11, `ating` 0.06, `aling` 0.06, `␣was` 0.04, `␣is` 0.04 |
| 3 | Heavy → ? | `␣rain` | 0.030 | 6 | `␣metals` 0.07, `␣metal` 0.06, `␣Metals` 0.06, `␣D` 0.05, `␣Metal` 0.05 |
| 4 | Heavy rain → ? | `␣fell` | 0.003 | 42 | `␣can` 0.12, `␣and` 0.10, `,` 0.10, `␣is` 0.09, `␣in` 0.03 |
| 5 | Heavy rain fell → ? | `␣on` | 0.195 | 2 | `␣in` 0.21, `␣on` 0.19, `␣across` 0.08, `␣over` 0.06, `␣for` 0.03 |
| 6 | …avy rain fell on → ? | `␣the` | 0.379 | 1 | `␣the` 0.38, `␣a` 0.05, `␣this` 0.01, `␣` 0.01, `␣parts` 0.01 |
| 7 | …rain fell on the → ? | `␣stadium` | 0.000 | 1334 | `␣island` 0.03, `␣city` 0.03, `␣town` 0.01, `␣streets` 0.01, `␣` 0.01 |
| 8 | …fell on the stadium → ? | `␣for` | 0.014 | 13 | `,` 0.13, `␣on` 0.09, `␣in` 0.09, `␣as` 0.07, `␣and` 0.05 |
| 9 | …on the stadium for → ? | `␣most` | 0.019 | 13 | `␣the` 0.24, `␣a` 0.14, `␣` 0.08, `␣more` 0.05, `␣several` 0.04 |
| 10 | …the stadium for most → ? | `␣of` | 0.966 | 1 | `␣of` 0.97, `␣part` 0.01, `␣parts` 0.00, `,` 0.00, `␣days` 0.00 |
| 11 | …stadium for most of → ? | `␣Saturday` | 0.017 | 3 | `␣the` 0.77, `␣last` 0.03, `␣Saturday` 0.02, `␣this` 0.02, `␣Sunday` 0.01 |
| 12 | …for most of Saturday → ? | `␣afternoon` | 0.033 | 6 | `,` 0.34, `.` 0.15, `␣and` 0.11, `␣night` 0.10, `␣morning` 0.08 |
| 13 | …most of Saturday afternoon → ? | `.` | 0.257 | 2 | `,` 0.41, `.` 0.26, `␣and` 0.11, `␣as` 0.05, `␣with` 0.02 |
| 14 | …of Saturday afternoon. → ? | `␣By` | 0.006 | 23 | `␣The` 0.18, `␣It` 0.05, `␣But` 0.04, `␣A` 0.04, `␣As` 0.02 |
| 15 | …Saturday afternoon. By → ? | `␣three` | 0.000 | 71 | `␣the` 0.21, `␣` 0.17, `␣Sunday` 0.15, `␣noon` 0.06, `␣mid` 0.05 |
| 16 | …afternoon. By three → ? | `␣o` | 0.279 | 1 | `␣o` 0.28, `␣in` 0.19, `␣p` 0.14, `,` 0.09, `:` 0.04 |
| 17 | …. By three o → ? | `'` | 0.962 | 1 | `'` 0.96, `’` 0.02, `␣clock` 0.01, `clock` 0.00, `'` 0.00 |
| 18 | …By three o' → ? | `clock` | 0.989 | 1 | `clock` 0.99, `␣clock` 0.01, `Cl` 0.00, `cl` 0.00, `␣clocks` 0.00 |
| 19 | …three o'clock → ? | `␣the` | 0.097 | 3 | `,` 0.42, `␣in` 0.14, `␣the` 0.10, `␣on` 0.06, `␣Sunday` 0.03 |
| 20 | …o'clock the → ? | `␣pitch` | 0.001 | 113 | `␣rain` 0.23, `␣sun` 0.06, `␣weather` 0.03, `␣sky` 0.02, `␣heavy` 0.02 |
| 21 | …'clock the pitch → ? | `␣was` | 0.389 | 1 | `␣was` 0.39, `␣had` 0.35, `ing` 0.04, `␣began` 0.01, `␣deck` 0.01 |
| 22 | …clock the pitch was → ? | `␣flooded` | 0.036 | 4 | `␣covered` 0.08, `␣dry` 0.08, `␣wet` 0.07, `␣flooded` 0.04, `␣still` 0.03 |
| 23 | …the pitch was flooded → ? | `␣and` | 0.153 | 3 | `␣with` 0.32, `,` 0.17, `␣and` 0.15, `.` 0.13, `␣by` 0.04 |
| 24 | …pitch was flooded and → ? | `␣the` | 0.285 | 1 | `␣the` 0.29, `␣a` 0.04, `␣it` 0.03, `␣there` 0.02, `,` 0.02 |
| 25 | …was flooded and the → ? | `␣refere` | 0.002 | 67 | `␣stadium` 0.13, `␣fans` 0.05, `␣crowd` 0.04, `␣game` 0.03, `␣field` 0.03 |
| 26 | …flooded and the refere → ? | `e` | 0.569 | 1 | `e` 0.57, `es` 0.41, `nd` 0.01, `ed` 0.01, `ns` 0.00 |
| 27 | …and the referee → ? | `␣declared` | 0.008 | 14 | `'s` 0.14, `␣was` 0.08, `␣had` 0.06, `␣called` 0.05, `,` 0.04 |
| 28 | …the referee declared → ? | `␣it` | 0.042 | 4 | `␣a` 0.48, `␣the` 0.21, `␣that` 0.05, `␣it` 0.04, `␣an` 0.03 |
| 29 | …referee declared it → ? | `␣unsafe` | 0.014 | 14 | `␣a` 0.28, `␣over` 0.08, `␣to` 0.07, `␣"` 0.04, `␣was` 0.03 |
| 30 | …e declared it unsafe → ? | `␣for` | 0.267 | 2 | `␣to` 0.48, `␣for` 0.27, `.` 0.15, `.\n` 0.01, `,` 0.01 |
| 31 | …declared it unsafe for → ? | `␣the` | 0.284 | 1 | `␣the` 0.28, `␣play` 0.27, `␣games` 0.05, `␣a` 0.03, `␣playing` 0.03 |
| 32 | …it unsafe for the → ? | `␣players` | 0.026 | 4 | `␣game` 0.41, `␣match` 0.10, `␣games` 0.06, `␣players` 0.03, `␣play` 0.03 |
| 33 | …unsafe for the players → ? | `.` | 0.317 | 2 | `␣to` 0.42, `.` 0.32, `␣and` 0.08, `,` 0.04, `.\n` 0.04 |
| 34 | …for the players. → ? | `␣So` | 0.002 | 56 | `␣The` 0.23, `␣A` 0.04, `␣He` 0.03, `␣It` 0.03, `␣At` 0.02 |
| 35 | …the players. So → ? | `␣the` | 0.178 | 1 | `␣the` 0.18, `,` 0.17, `␣he` 0.06, `on` 0.03, `␣it` 0.03 |
| 36 | …players. So the → ? | `␣match` | 0.025 | 8 | `␣players` 0.09, `␣game` 0.08, `␣fans` 0.04, `␣refere` 0.03, `␣team` 0.03 |
| 37 | …. So the match → ? | `␣was` | 0.509 | 1 | `␣was` 0.51, `␣went` 0.11, `␣ended` 0.06, `␣continued` 0.03, `␣res` 0.02 |
| 38 | …So the match was → ? | `␣cancelled` | 0.106 | 1 | `␣cancelled` 0.11, `␣res` 0.10, `␣postp` 0.10, `␣abandoned` 0.05, `␣played` 0.04 |
| 39 | …the match was cancelled → ? | `␣and` | 0.145 | 2 | `.` 0.34, `.\n` 0.15, `␣and` 0.15, `,` 0.09, `.\n\n` 0.09 |
| 40 | …match was cancelled and → ? | `␣res` | 0.003 | 31 | `␣the` 0.46, `␣a` 0.09, `␣it` 0.02, `␣another` 0.01, `␣no` 0.01 |
| 41 | …was cancelled and res → ? | `ched` | 0.888 | 1 | `ched` 0.89, `umed` 0.10, `che` 0.00, `usc` 0.00, `igned` 0.00 |
| 42 | …cancelled and resched → ? | `uled` | 1.000 | 1 | `uled` 1.00, `uling` 0.00, `ored` 0.00, `aled` 0.00, `iated` 0.00 |
| 43 | …and rescheduled → ? | `␣for` | 0.358 | 1 | `␣for` 0.36, `␣to` 0.14, `.` 0.13, `.\n` 0.06, `␣on` 0.04 |
| 44 | …rescheduled for → ? | `␣the` | 0.272 | 1 | `␣the` 0.27, `␣Sunday` 0.23, `␣a` 0.08, `␣Saturday` 0.07, `␣another` 0.06 |
| 45 | …cheduled for the → ? | `␣following` | 0.267 | 2 | `␣next` 0.55, `␣following` 0.27, `␣evening` 0.03, `␣morning` 0.02, `␣second` 0.01 |
| 46 | …uled for the following → ? | `␣week` | 0.030 | 9 | `␣day` 0.37, `␣morning` 0.16, `␣Saturday` 0.10, `␣Sunday` 0.08, `␣evening` 0.04 |
| 47 | …for the following week → ? | `.` | 0.416 | 1 | `.` 0.42, `.\n` 0.23, `.\n\n` 0.14, `,` 0.06, `␣on` 0.01 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣week` | 0.001 | 89 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← week. | `␣following` | 0.009 | 11 | `␣a` 0.43, `␣per` 0.13, `␣the` 0.08, `␣each` 0.05, `␣this` 0.05 |
| 4 | ? ← following week. | `␣the` | 0.968 | 1 | `␣the` 0.97, `␣The` 0.01, `␣every` 0.00, `␣each` 0.00, `␣or` 0.00 |
| 5 | ? ← the following week. | `␣for` | 0.143 | 1 | `␣for` 0.14, `␣of` 0.06, `␣until` 0.05, `␣in` 0.05, `␣again` 0.03 |
| 6 | ? ← for the following week… | `uled` | 0.000 | 354 | `␣day` 0.02, `␣plan` 0.01, `␣it` 0.01, `␣meals` 0.01, `␣planned` 0.01 |
| 7 | ? ← uled for the following… | `ched` | 0.839 | 1 | `ched` 0.84, `hed` 0.12, `␣overha` 0.02, `␣ha` 0.01, `r` 0.00 |
| 8 | ? ← cheduled for the… | `␣res` | 0.884 | 1 | `␣res` 0.88, `-s` 0.09, `res` 0.01, `␣Res` 0.01, `␣pres` 0.00 |
| 9 | ? ← rescheduled for… | `␣and` | 0.028 | 7 | `␣be` 0.54, `␣is` 0.12, `␣was` 0.09, `␣are` 0.04, `␣or` 0.04 |
| 10 | ? ← and rescheduled… | `␣cancelled` | 0.114 | 1 | `␣cancelled` 0.11, `,` 0.09, `uled` 0.04, `oned` 0.04, `led` 0.03 |
| 11 | ? ← cancelled and resched… | `␣was` | 0.247 | 2 | `␣be` 0.41, `␣was` 0.25, `␣is` 0.15, `␣are` 0.05, `␣were` 0.05 |
| 12 | ? ← was cancelled and res… | `␣match` | 0.002 | 51 | `␣It` 0.14, `␣it` 0.13, `␣event` 0.10, `␣class` 0.07, `␣meeting` 0.06 |
| 13 | ? ← match was cancelled and… | `␣the` | 0.296 | 2 | `␣The` 0.59, `␣the` 0.30, `'s` 0.01, `␣entire` 0.00, `␣football` 0.00 |
| 14 | ? ← the match was cancelled… | `␣So` | 0.001 | 28 | `,` 0.66, `␣and` 0.14, `␣but` 0.04, `␣so` 0.03, `␣that` 0.02 |
| 15 | ? ← So the match was… | `.` | 0.894 | 1 | `.` 0.89, `:` 0.03, `).` 0.02, `!` 0.01, `".` 0.01 |
| 16 | ? ← . So the match… | `␣players` | 0.004 | 24 | `␣match` 0.04, `␣game` 0.02, `␣time` 0.01, `␣day` 0.01, `␣it` 0.01 |
| 17 | ? ← players. So the… | `␣the` | 0.243 | 1 | `␣the` 0.24, `␣other` 0.05, `␣of` 0.04, `␣two` 0.03, `␣both` 0.02 |
| 18 | ? ← the players. So… | `␣for` | 0.105 | 2 | `␣of` 0.32, `␣for` 0.10, `␣all` 0.08, `␣to` 0.07, `␣between` 0.05 |
| 19 | ? ← for the players.… | `␣unsafe` | 0.005 | 23 | `␣bad` 0.04, `␣match` 0.02, `␣dangerous` 0.02, `␣good` 0.02, `␣problems` 0.02 |
| 20 | ? ← unsafe for the players… | `␣it` | 0.096 | 2 | `␣was` 0.25, `␣it` 0.10, `␣and` 0.08, `␣be` 0.07, `␣very` 0.06 |
| 21 | ? ← it unsafe for the… | `␣declared` | 0.001 | 14 | `␣made` 0.44, `␣making` 0.38, `␣make` 0.10, `␣found` 0.01, `␣deemed` 0.01 |
| 22 | ? ← declared it unsafe for… | `e` | 0.007 | 16 | `␣and` 0.34, `␣officials` 0.06, `␣they` 0.05, `␣coach` 0.03, `,` 0.02 |
| 23 | ? ← e declared it unsafe… | `␣refere` | 0.960 | 1 | `␣refere` 0.96, `ere` 0.01, `␣by` 0.00, `ore` 0.00, `we` 0.00 |
| 24 | ? ← referee declared it… | `␣the` | 0.789 | 1 | `␣the` 0.79, `␣The` 0.10, `␣match` 0.01, `The` 0.01, `␣and` 0.01 |
| 25 | ? ← the referee declared… | `␣and` | 0.218 | 2 | `,` 0.38, `␣and` 0.22, `␣but` 0.09, `␣when` 0.02, `␣as` 0.02 |
| 26 | ? ← and the referee… | `␣flooded` | 0.000 | 359 | `,` 0.19, `␣match` 0.05, `␣game` 0.03, `␣out` 0.01, `␣rain` 0.01 |
| 27 | ? ← flooded and the refere… | `␣was` | 0.407 | 1 | `␣was` 0.41, `␣were` 0.12, `␣stadium` 0.08, `␣got` 0.06, `␣became` 0.03 |
| 28 | ? ← was flooded and the… | `␣pitch` | 0.098 | 3 | `␣field` 0.23, `␣stadium` 0.19, `␣pitch` 0.10, `adium` 0.05, `␣court` 0.05 |
| 29 | ? ← pitch was flooded and… | `␣the` | 0.645 | 1 | `␣the` 0.65, `␣The` 0.22, `The` 0.03, `␣cricket` 0.01, `␣football` 0.01 |
| 30 | ? ← the pitch was flooded… | `clock` | 0.000 | 255 | `,` 0.43, `␣that` 0.07, `␣as` 0.07, `␣but` 0.04, `␣and` 0.04 |
| 31 | ? ← clock the pitch was… | `'` | 0.946 | 1 | `'` 0.95, `␣o` 0.03, `’` 0.01, `00` 0.00, `´` 0.00 |
| 32 | ? ← 'clock the pitch… | `␣o` | 0.980 | 1 | `␣o` 0.98, `␣O` 0.01, `o` 0.01, `00` 0.00, `\` 0.00 |
| 33 | ? ← o'clock the… | `␣three` | 0.022 | 16 | `11` 0.10, `10` 0.09, `9` 0.07, `12` 0.06, `00` 0.05 |
| 34 | ? ← three o'clock… | `␣By` | 0.048 | 5 | `␣at` 0.25, `␣At` 0.17, `␣after` 0.12, `␣around` 0.08, `␣By` 0.05 |
| 35 | ? ← By three o'… | `.` | 0.953 | 1 | `.` 0.95, `).` 0.01, `:` 0.01, `!` 0.01, `'.` 0.00 |
| 36 | ? ← . By three o… | `␣afternoon` | 0.006 | 15 | `␣pitch` 0.04, `␣match` 0.04, `␣rain` 0.03, `␣game` 0.02, `clock` 0.01 |
| 37 | ? ← afternoon. By three… | `␣Saturday` | 0.047 | 4 | `␣the` 0.40, `␣that` 0.11, `␣Sunday` 0.06, `␣Saturday` 0.05, `␣Friday` 0.05 |
| 38 | ? ← Saturday afternoon. By… | `␣of` | 0.017 | 3 | `␣on` 0.61, `␣a` 0.12, `␣of` 0.02, `␣rainy` 0.01, `␣for` 0.01 |
| 39 | ? ← of Saturday afternoon.… | `␣most` | 0.015 | 12 | `␣middle` 0.14, `␣end` 0.10, `␣afternoon` 0.08, `␣hours` 0.07, `␣morning` 0.07 |
| 40 | ? ← most of Saturday afternoon… | `␣for` | 0.657 | 1 | `␣for` 0.66, `␣lasted` 0.04, `␣on` 0.03, `␣throughout` 0.02, `␣through` 0.02 |
| 41 | ? ← for most of Saturday… | `␣stadium` | 0.001 | 123 | `␣rain` 0.11, `␣pitch` 0.04, `␣lasted` 0.04, `␣on` 0.03, `␣continued` 0.02 |
| 42 | ? ← stadium for most of… | `␣the` | 0.796 | 1 | `␣the` 0.80, `␣football` 0.01, `␣main` 0.01, `'s` 0.01, `␣home` 0.00 |
| 43 | ? ← the stadium for most… | `␣on` | 0.021 | 11 | `␣in` 0.34, `␣at` 0.10, `␣of` 0.05, `␣over` 0.05, `␣flooded` 0.04 |
| 44 | ? ← on the stadium for… | `␣fell` | 0.225 | 1 | `␣fell` 0.22, `␣rain` 0.18, `␣down` 0.07, `␣heavily` 0.05, `ined` 0.05 |
| 45 | ? ← fell on the stadium… | `␣rain` | 0.630 | 1 | `␣rain` 0.63, `␣snow` 0.10, `␣Rain` 0.07, `␣rains` 0.06, `Rain` 0.02 |
| 46 | ? ← rain fell on the… | `avy` | 0.017 | 9 | `␣and` 0.22, `␣heavy` 0.18, `␣of` 0.12, `,` 0.07, `␣Heavy` 0.06 |
| 47 | ? ← avy rain fell on… | `He` | 0.986 | 1 | `He` 0.99, `he` 0.01, `␣He` 0.00, `-he` 0.00, `␣he` 0.00 |

---

## 2. power_cut

*Category: causal*

> **Beginning:** A storm brought down several power lines on the edge of town last night.  
> **Middle:** Thousands of homes lost electricity, and traffic lights across the city stopped working.  
> **Ending:** As a result, schools stayed closed the next morning while engineers repaired the damage.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it, nothing is going to come out of it," he said. ↵  ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |
| sample | time to see what happened," he said. ↵  ↵ We really wanted to be able to go to school that night and the next morning to try to assess the damage, Chakrabarty said. ↵  ↵ "We know that all of the power lines were knocked out, but we did not know exactly what it was because all the towers were down," he said. ↵  ↵ "We really wanted to be able to go to school that night and the next morning to try to assess the damage," he said. ↵  ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |
| sample | rear of the turbine facing into the wind, he said. ↵ City officials are working to ensure they don’t run out of wind power. ↵ “There’s a road in front of the turbine, so we can’t get too close to it,” he said. “When we’re hit with high winds, turbines can be blown over or blown away.” ↵ City officials said that, because of its proximity to the power plant, the turbines were damaged and the water had to be shut off. ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |
| sample | went off to be cleaned up and were returned the next day, Bunnell said. ↵ The fire department learned Monday that the school had been involved in the incident and has ordered a survey of the damage, he said. ↵ Nurses at the schools were part of the problem, as there was no way to keep track of which building was hit, or how many people were injured, Bunnell said. ↵ "They really weren't sure what to do," Bunnell said. ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | A storm brought down several power lines on the edge of town last night. | The power lines were down for a few hours, but the storm was over. The power lines were down for a few hours, but the storm was over. The power lines were down for a few hours, but the storm was over. The power lines were down for a few hours, but the storm was over. The power lines were down for a few hours, but the storm was over. The power lines were down for a few hours, but the storm was over. |
| sample | A storm brought down several power lines on the edge of town last night. | The power is back on after it was dropped the next day, but in spite of it being "safe" (for the time being) it looks like it might be a bad idea to stay there. ↵ Is it safe to stay for a couple of days? It's not safe to stay out of the storm, but it's not safe to stay in the basement, either. It's just too bad it was raining at the time. ↵ I had a similar experience several |
| sample | A storm brought down several power lines on the edge of town last night. | What exactly happened? The power lines will be down sometime Thursday. Is this an isolated occurrence? What was the cause of the power outage? ↵ My wife wanted to know if it was safe to keep her daughter and her family home, and if you keep a child in a room that has power, what happens if it gets caught on fire? We want to know if the power lines are safe. Anyone have any knowledge about this? ↵ Thanks in advance. ↵ Daniel, ↵ I'm with |
| sample | A storm brought down several power lines on the edge of town last night. | I was very concerned about the power lines, they were very far from the house. The power lines were not down, but the power lines were down, they were in a very high wind, a very high, very, high voltage, and the power lines were not down. I went to try to put them back into service again, but they were not down, even though they were down. I know a lot of people in my city have heard of the power lines, |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.818 | 34% |
| Backward | previous-token (right context) | 0.816 | 34% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `A` | 0.021 | 4 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | A → ? | `␣storm` | 0.000 | 791 | `␣new` 0.03, `:` 0.02, `␣few` 0.02, `␣Guide` 0.01, `␣` 0.01 |
| 3 | A storm → ? | `␣brought` | 0.001 | 86 | `␣is` 0.12, `␣surge` 0.08, `␣of` 0.05, `␣in` 0.04, `␣that` 0.04 |
| 4 | A storm brought → ? | `␣down` | 0.049 | 3 | `␣a` 0.11, `␣heavy` 0.08, `␣down` 0.05, `␣the` 0.05, `␣in` 0.03 |
| 5 | A storm brought down → ? | `␣several` | 0.020 | 9 | `␣a` 0.19, `␣the` 0.14, `␣` 0.08, `␣trees` 0.06, `␣power` 0.03 |
| 6 | …storm brought down several → ? | `␣power` | 0.026 | 5 | `␣trees` 0.10, `␣of` 0.07, `␣hundred` 0.03, `␣buildings` 0.03, `␣power` 0.03 |
| 7 | …brought down several power → ? | `␣lines` | 0.696 | 1 | `␣lines` 0.70, `lines` 0.14, `␣poles` 0.06, `␣plants` 0.04, `␣stations` 0.01 |
| 8 | …down several power lines → ? | `␣on` | 0.060 | 4 | `␣in` 0.22, `␣and` 0.14, `,` 0.12, `␣on` 0.06, `␣at` 0.05 |
| 9 | …several power lines on → ? | `␣the` | 0.277 | 1 | `␣the` 0.28, `␣Friday` 0.05, `␣Saturday` 0.05, `␣a` 0.05, `␣Tuesday` 0.04 |
| 10 | …power lines on the → ? | `␣edge` | 0.003 | 76 | `␣island` 0.04, `␣east` 0.03, `␣way` 0.03, `␣East` 0.02, `␣coast` 0.02 |
| 11 | …lines on the edge → ? | `␣of` | 0.987 | 1 | `␣of` 0.99, `,` 0.00, `\n` 0.00, `␣and` 0.00, `.` 0.00 |
| 12 | …on the edge of → ? | `␣town` | 0.070 | 3 | `␣the` 0.40, `␣a` 0.11, `␣town` 0.07, `␣downtown` 0.03, `␣Lake` 0.02 |
| 13 | …the edge of town → ? | `␣last` | 0.038 | 6 | `,` 0.30, `.` 0.11, `␣in` 0.09, `␣and` 0.08, `␣on` 0.04 |
| 14 | …edge of town last → ? | `␣night` | 0.282 | 2 | `␣week` 0.38, `␣night` 0.28, `␣weekend` 0.09, `␣Friday` 0.04, `␣month` 0.04 |
| 15 | …of town last night → ? | `.` | 0.353 | 2 | `,` 0.40, `.` 0.35, `␣and` 0.07, `␣as` 0.02, `.\n` 0.02 |
| 16 | …town last night. → ? | `␣Th` | 0.001 | 86 | `␣The` 0.17, `␣I` 0.06, `␣It` 0.05, `␣A` 0.03, `␣One` 0.03 |
| 17 | …last night. Th → ? | `ousands` | 0.705 | 1 | `ousands` 0.70, `underst` 0.09, `irty` 0.06, `ick` 0.04, `row` 0.01 |
| 18 | …night. Thousands → ? | `␣of` | 0.792 | 1 | `␣of` 0.79, `␣were` 0.06, `␣have` 0.02, `␣are` 0.01, `␣had` 0.01 |
| 19 | …. Thousands of → ? | `␣homes` | 0.030 | 4 | `␣people` 0.45, `␣residents` 0.05, `␣dollars` 0.04, `␣homes` 0.03, `␣customers` 0.03 |
| 20 | …Thousands of homes → ? | `␣lost` | 0.065 | 4 | `␣were` 0.34, `␣and` 0.22, `,` 0.08, `␣lost` 0.07, `␣without` 0.04 |
| 21 | …ousands of homes lost → ? | `␣electricity` | 0.074 | 2 | `␣power` 0.83, `␣electricity` 0.07, `␣their` 0.04, `␣electric` 0.01, `␣service` 0.01 |
| 22 | …of homes lost electricity → ? | `,` | 0.240 | 1 | `,` 0.24, `.` 0.20, `␣and` 0.19, `␣in` 0.06, `␣as` 0.02 |
| 23 | …homes lost electricity, → ? | `␣and` | 0.413 | 1 | `␣and` 0.41, `␣businesses` 0.04, `␣but` 0.03, `␣some` 0.02, `␣many` 0.02 |
| 24 | …lost electricity, and → ? | `␣traffic` | 0.001 | 78 | `␣the` 0.11, `␣many` 0.06, `␣a` 0.06, `␣thousands` 0.05, `␣hundreds` 0.04 |
| 25 | …electricity, and traffic → ? | `␣lights` | 0.031 | 4 | `␣was` 0.31, `␣and` 0.05, `␣jams` 0.04, `␣lights` 0.03, `␣slowed` 0.02 |
| 26 | …, and traffic lights → ? | `␣across` | 0.006 | 19 | `␣were` 0.36, `␣and` 0.11, `␣went` 0.07, `,` 0.04, `␣turned` 0.03 |
| 27 | …and traffic lights across → ? | `␣the` | 0.624 | 1 | `␣the` 0.62, `␣town` 0.15, `␣a` 0.01, `␣towns` 0.01, `␣downtown` 0.01 |
| 28 | …traffic lights across the → ? | `␣city` | 0.100 | 3 | `␣country` 0.26, `␣state` 0.12, `␣city` 0.10, `␣street` 0.07, `␣area` 0.07 |
| 29 | …lights across the city → ? | `␣stopped` | 0.009 | 10 | `␣were` 0.49, `␣went` 0.07, `␣turned` 0.03, `␣are` 0.02, `␣had` 0.02 |
| 30 | …across the city stopped → ? | `␣working` | 0.653 | 1 | `␣working` 0.65, `.` 0.06, `␣functioning` 0.05, `␣for` 0.04, `␣at` 0.02 |
| 31 | …the city stopped working → ? | `.` | 0.558 | 1 | `.` 0.56, `.\n` 0.07, `.\n\n` 0.05, `␣for` 0.05, `,` 0.04 |
| 32 | …city stopped working. → ? | `␣As` | 0.014 | 12 | `␣The` 0.15, `␣But` 0.05, `␣It` 0.04, `␣Many` 0.03, `␣A` 0.03 |
| 33 | …stopped working. As → ? | `␣a` | 0.141 | 2 | `␣the` 0.25, `␣a` 0.14, `␣I` 0.05, `␣of` 0.04, `␣we` 0.03 |
| 34 | …working. As a → ? | `␣result` | 0.773 | 1 | `␣result` 0.77, `␣matter` 0.01, `␣precaution` 0.01, `␣city` 0.01, `␣consequence` 0.01 |
| 35 | …. As a result → ? | `,` | 0.861 | 1 | `,` 0.86, `␣of` 0.10, `␣the` 0.01, `␣many` 0.01, `␣a` 0.00 |
| 36 | …As a result, → ? | `␣schools` | 0.002 | 53 | `␣the` 0.21, `␣many` 0.07, `␣a` 0.05, `␣some` 0.03, `␣thousands` 0.03 |
| 37 | …a result, schools → ? | `␣stayed` | 0.001 | 62 | `␣and` 0.31, `,` 0.17, `␣were` 0.12, `␣closed` 0.10, `␣shut` 0.04 |
| 38 | …result, schools stayed → ? | `␣closed` | 0.486 | 1 | `␣closed` 0.49, `␣open` 0.41, `␣shut` 0.03, `␣on` 0.01, `␣online` 0.01 |
| 39 | …, schools stayed closed → ? | `␣the` | 0.002 | 29 | `␣and` 0.23, `,` 0.21, `␣for` 0.18, `.` 0.11, `␣until` 0.06 |
| 40 | …schools stayed closed the → ? | `␣next` | 0.032 | 7 | `␣entire` 0.37, `␣whole` 0.21, `␣night` 0.08, `␣rest` 0.08, `␣last` 0.04 |
| 41 | …stayed closed the next → ? | `␣morning` | 0.131 | 2 | `␣day` 0.83, `␣morning` 0.13, `␣few` 0.01, `␣school` 0.01, `␣night` 0.00 |
| 42 | …closed the next morning → ? | `␣while` | 0.015 | 10 | `.` 0.28, `,` 0.26, `␣and` 0.12, `.\n` 0.10, `.\n\n` 0.07 |
| 43 | …the next morning while → ? | `␣engineers` | 0.001 | 123 | `␣the` 0.21, `␣police` 0.05, `␣people` 0.04, `␣power` 0.04, `␣residents` 0.03 |
| 44 | …next morning while engineers → ? | `␣repaired` | 0.017 | 5 | `␣worked` 0.20, `␣and` 0.09, `␣were` 0.06, `␣tried` 0.04, `,` 0.02 |
| 45 | …morning while engineers repaired → ? | `␣the` | 0.441 | 1 | `␣the` 0.44, `␣power` 0.08, `␣damage` 0.05, `␣damaged` 0.04, `␣and` 0.04 |
| 46 | …while engineers repaired the → ? | `␣damage` | 0.300 | 1 | `␣damage` 0.30, `␣power` 0.14, `␣lines` 0.07, `␣damaged` 0.05, `␣lights` 0.04 |
| 47 | …engineers repaired the damage → ? | `.` | 0.392 | 1 | `.` 0.39, `.\n` 0.20, `.\n\n` 0.12, `␣to` 0.10, `,` 0.06 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣damage` | 0.001 | 82 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← damage. | `␣the` | 0.027 | 8 | `␣further` 0.06, `␣or` 0.05, `␣water` 0.04, `␣of` 0.04, `␣cause` 0.04 |
| 4 | ? ← the damage. | `␣repaired` | 0.001 | 98 | `␣of` 0.27, `␣repair` 0.09, `␣assess` 0.04, `␣minimize` 0.03, `␣repairing` 0.03 |
| 5 | ? ← repaired the damage. | `␣engineers` | 0.001 | 83 | `␣and` 0.25, `␣have` 0.12, `␣has` 0.07, `␣or` 0.03, `'ve` 0.03 |
| 6 | ? ← engineers repaired the damage… | `␣while` | 0.066 | 5 | `␣after` 0.12, `␣the` 0.11, `␣and` 0.08, `,` 0.07, `␣while` 0.07 |
| 7 | ? ← while engineers repaired the… | `␣morning` | 0.000 | 289 | `,` 0.06, `␣months` 0.04, `␣days` 0.04, `␣weeks` 0.04, `␣hours` 0.04 |
| 8 | ? ← morning while engineers repaired… | `␣next` | 0.151 | 2 | `␣the` 0.35, `␣next` 0.15, `␣until` 0.05, `␣following` 0.04, `␣this` 0.04 |
| 9 | ? ← next morning while engineers… | `␣the` | 0.957 | 1 | `␣the` 0.96, `␣until` 0.01, `␣early` 0.01, `␣The` 0.00, `␣very` 0.00 |
| 10 | ? ← the next morning while… | `␣closed` | 0.006 | 21 | `␣until` 0.17, `␣for` 0.03, `␣early` 0.03, `␣back` 0.02, `␣work` 0.02 |
| 11 | ? ← closed the next morning… | `␣stayed` | 0.001 | 72 | `␣was` 0.31, `␣be` 0.08, `␣were` 0.08, `␣and` 0.06, `␣it` 0.03 |
| 12 | ? ← stayed closed the next… | `␣schools` | 0.010 | 15 | `␣and` 0.10, `␣airport` 0.05, `␣it` 0.04, `␣It` 0.03, `␣but` 0.03 |
| 13 | ? ← schools stayed closed the… | `,` | 0.044 | 4 | `␣The` 0.20, `␣the` 0.13, `␣and` 0.13, `,` 0.04, `␣many` 0.03 |
| 14 | ? ← , schools stayed closed… | `␣result` | 0.010 | 7 | `␣No` 0.13, `␣Yes` 0.05, `␣cases` 0.02, `␣damage` 0.02, `␣However` 0.02 |
| 15 | ? ← result, schools stayed… | `␣a` | 0.980 | 1 | `␣a` 0.98, `␣the` 0.01, `␣direct` 0.00, `␣The` 0.00, `␣this` 0.00 |
| 16 | ? ← a result, schools… | `␣As` | 0.857 | 1 | `␣As` 0.86, `As` 0.07, `␣as` 0.07, `as` 0.00, `␣was` 0.00 |
| 17 | ? ← As a result,… | `.` | 0.958 | 1 | `.` 0.96, `."` 0.01, `).` 0.01, `:` 0.00, `.”` 0.00 |
| 18 | ? ← . As a result… | `␣working` | 0.000 | 536 | `␣damage` 0.03, `␣schools` 0.02, `␣school` 0.02, `␣buildings` 0.01, `␣water` 0.01 |
| 19 | ? ← working. As a… | `␣stopped` | 0.192 | 1 | `␣stopped` 0.19, `␣stop` 0.12, `␣not` 0.11, `␣were` 0.08, `␣from` 0.06 |
| 20 | ? ← stopped working. As… | `␣city` | 0.001 | 181 | `␣system` 0.05, `␣pumps` 0.05, `␣had` 0.05, `␣systems` 0.04, `␣and` 0.03 |
| 21 | ? ← city stopped working.… | `␣the` | 0.864 | 1 | `␣the` 0.86, `␣entire` 0.05, `␣whole` 0.02, `␣a` 0.01, `␣their` 0.00 |
| 22 | ? ← the city stopped working… | `␣across` | 0.022 | 10 | `␣in` 0.33, `␣of` 0.12, `␣throughout` 0.08, `␣to` 0.07, `,` 0.04 |
| 23 | ? ← across the city stopped… | `␣lights` | 0.030 | 6 | `␣lines` 0.15, `␣systems` 0.10, `␣schools` 0.06, `␣electricity` 0.04, `␣stations` 0.03 |
| 24 | ? ← lights across the city… | `␣traffic` | 0.203 | 1 | `␣traffic` 0.20, `␣street` 0.18, `␣the` 0.16, `␣and` 0.07, `␣electric` 0.03 |
| 25 | ? ← traffic lights across the… | `␣and` | 0.160 | 1 | `␣and` 0.16, `␣the` 0.15, `,` 0.13, `␣all` 0.08, `␣many` 0.05 |
| 26 | ? ← and traffic lights across… | `,` | 0.496 | 1 | `,` 0.50, `␣lines` 0.02, `␣power` 0.02, `␣schools` 0.02, `␣damaged` 0.01 |
| 27 | ? ← , and traffic lights… | `␣electricity` | 0.010 | 15 | `␣power` 0.03, `␣damaged` 0.03, `␣lines` 0.02, `␣out` 0.02, `␣off` 0.02 |
| 28 | ? ← electricity, and traffic… | `␣lost` | 0.127 | 2 | `␣without` 0.25, `␣lost` 0.13, `␣no` 0.12, `␣of` 0.10, `␣out` 0.04 |
| 29 | ? ← lost electricity, and… | `␣homes` | 0.048 | 3 | `␣city` 0.07, `␣schools` 0.05, `␣homes` 0.05, `␣people` 0.05, `,` 0.04 |
| 30 | ? ← homes lost electricity,… | `␣of` | 0.164 | 3 | `,` 0.32, `0` 0.19, `␣of` 0.16, `␣many` 0.05, `␣Many` 0.03 |
| 31 | ? ← of homes lost electricity… | `ousands` | 0.248 | 2 | `␣thousands` 0.33, `ousands` 0.25, `undreds` 0.12, `␣hundreds` 0.11, `␣dozens` 0.04 |
| 32 | ? ← ousands of homes lost… | `␣Th` | 0.935 | 1 | `␣Th` 0.93, `Th` 0.06, `th` 0.00, `-th` 0.00, `h` 0.00 |
| 33 | ? ← Thousands of homes… | `.` | 0.945 | 1 | `.` 0.95, `:` 0.04, `."` 0.00, `).` 0.00, `?` 0.00 |
| 34 | ? ← . Thousands of… | `␣night` | 0.015 | 5 | `␣city` 0.03, `␣storm` 0.02, `␣power` 0.02, `␣outages` 0.02, `␣night` 0.02 |
| 35 | ? ← night. Thousands… | `␣last` | 0.026 | 12 | `␣the` 0.18, `␣at` 0.17, `␣that` 0.08, `␣Tuesday` 0.07, `␣Friday` 0.07 |
| 36 | ? ← last night. Th… | `␣town` | 0.007 | 22 | `␣city` 0.05, `␣storm` 0.03, `␣City` 0.02, `␣late` 0.02, `␣area` 0.02 |
| 37 | ? ← town last night.… | `␣of` | 0.082 | 4 | `␣the` 0.11, `␣in` 0.11, `␣through` 0.09, `␣of` 0.08, `␣Texas` 0.03 |
| 38 | ? ← of town last night… | `␣edge` | 0.027 | 7 | `␣parts` 0.22, `␣part` 0.20, `␣out` 0.12, `␣much` 0.05, `␣section` 0.04 |
| 39 | ? ← edge of town last… | `␣the` | 0.803 | 1 | `␣the` 0.80, `␣eastern` 0.04, `␣northern` 0.02, `␣southern` 0.02, `␣western` 0.02 |
| 40 | ? ← the edge of town… | `␣on` | 0.431 | 1 | `␣on` 0.43, `␣at` 0.17, `␣to` 0.08, `␣along` 0.07, `␣near` 0.04 |
| 41 | ? ← on the edge of… | `␣lines` | 0.007 | 20 | `␣fell` 0.09, `␣down` 0.05, `␣struck` 0.03, `␣right` 0.03, `␣plant` 0.02 |
| 42 | ? ← lines on the edge… | `␣power` | 0.878 | 1 | `␣power` 0.88, `␣electric` 0.02, `␣electrical` 0.01, `␣gas` 0.01, `␣transmission` 0.01 |
| 43 | ? ← power lines on the… | `␣several` | 0.007 | 21 | `ed` 0.31, `␣damaged` 0.08, `␣and` 0.06, `␣down` 0.05, `␣hit` 0.04 |
| 44 | ? ← several power lines on… | `␣down` | 0.077 | 3 | `␣damaged` 0.15, `ed` 0.15, `␣down` 0.08, `␣hit` 0.07, `␣into` 0.05 |
| 45 | ? ← down several power lines… | `␣brought` | 0.228 | 2 | `␣knocked` 0.39, `␣brought` 0.23, `␣shut` 0.14, `re` 0.08, `␣took` 0.04 |
| 46 | ? ← brought down several power… | `␣storm` | 0.291 | 1 | `␣storm` 0.29, `␣winds` 0.07, `␣tornado` 0.05, `␣storms` 0.04, `storm` 0.03 |
| 47 | ? ← storm brought down several… | `A` | 0.061 | 5 | `␣winter` 0.19, `␣ice` 0.14, `␣electrical` 0.07, `␣severe` 0.07, `A` 0.06 |

---

## 3. crop_failure

*Category: causal*

> **Beginning:** The region received almost no rain between March and August.  
> **Middle:** Wells dried up and farmers could not irrigate their fields.  
> **Ending:** Because of the drought, the wheat harvest was the smallest in forty years.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | because of the drought, he said he is pretty confident that we’re going to have a good harvest this year. ↵ “I’m pretty confident that we’re going to have a good harvest this year,” he said. “I’m pretty confident that we’re going to have a good harvest this year. I’m pretty confident that we’re going to have a good harvest this year. ↵ “I’m pretty confident that we’re going to have a good harvest this year,” he said. ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |
| sample | greater losses in wheat production because of the drought, the losses from insects and pests, and the lack of irrigation water, he said. ↵ “Each of these crops can produce like a normal crop over 15 to 20 years,” he said, explaining that wheat, sorghum, corn and fruit trees can reach full yields in only four to five years. ↵ “You can still be producing a crop under normal conditions for 10, 20, 30 years,” he said. ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |
| sample | 9.7 inches of rain fell in the western half of the state. ↵  ↵ Meat production in Missouri has been lower than normal. ↵  ↵ Spring plant growth has been slower than normal this year in the Central and Northern Great Plains. ↵  ↵ In the Central Great Plains, demand for water has been at record levels this year. ↵  ↵ Drought in the Great Plains ↵  ↵ The Great Plains are in a decades-long drought. ↵  ↵ Last year, the wheat harvest declined 300 percent due to the lack of water. ↵  ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |
| sample | Wheat yields, soybean yields, corn yields and wheat yields were all above normal during the drought and we had rains in the early part of the summer. But he thinks the soils should be below normal heading into the winter months. ↵  ↵ "I think the soils will be wetter than normal for winter. If they are above average, I think they should be drier than normal and if they are below average, I think they should be more dry than normal going into summer," Smith said. ↵  ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | The region received almost no rain between March and August. | The average annual rainfall was 1.5 inches, which is about 3.5 inches less than the 1981-2010 average. The region received 1.5 inches of rain, which is about 3.5 inches less than the 1981-2010 average. The region received 1.5 inches of rain, which is about 3.5 inches less than the 1981-2010 average. The region received 1. |
| sample | The region received almost no rain between March and August. | The average number of rainy days for the region was 19.3 days (range of 11.8 to 35.4 days) per year (National Climate Assessment, 2009). ↵  ↵ The mean yearly precipitation for the region during the study period was 5.9 mm (range of 0.7 to 13.7 mm) (National Climate Assessment, 2009). The annual average temperature was 24.0 °C (range of 26 |
| sample | The region received almost no rain between March and August. | April temperatures were 10 to 14 degrees cooler than normal. There was 0.8 to 1.3 inches of snow in central Ohio, while the rest of the state received 0.8 to 2.4 inches. On May 23, the National Weather Service declared a severe weather emergency in Columbus County, Ohio and designated three days of extreme weather as the "rainiest day" in 2023. In the northwestern portion of the state, |
| sample | The region received almost no rain between March and August. | In the period of intense growth, the region lost 1 million cubic meters of water, the equivalent of 10,000 cubic meters of water a day. The water was stored in the underground aquifers with a water capacity of 1,500 cubic meters. The water level in storage was 4.9 meters lower than in the previous year. The year was also very dry in the summer due to the strong winds that brought the monsoon rains to the region. ↵ |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.792 | 45% |
| Backward | previous-token (right context) | 0.819 | 32% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `The` | 0.066 | 1 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | The → ? | `␣region` | 0.000 | 784 | `␣` 0.01, `␣first` 0.01, `␣most` 0.01, `␣Importance` 0.01, `␣best` 0.01 |
| 3 | The region → ? | `␣received` | 0.001 | 56 | `␣of` 0.20, `␣is` 0.15, `'s` 0.10, `␣has` 0.07, `␣was` 0.04 |
| 4 | The region received → ? | `␣almost` | 0.006 | 24 | `␣a` 0.16, `␣` 0.08, `␣its` 0.06, `␣the` 0.06, `␣an` 0.05 |
| 5 | The region received almost → ? | `␣no` | 0.089 | 2 | `␣` 0.39, `␣no` 0.09, `␣a` 0.07, `␣$` 0.05, `␣the` 0.03 |
| 6 | …region received almost no → ? | `␣rain` | 0.236 | 2 | `␣rainfall` 0.28, `␣rain` 0.24, `␣precipitation` 0.15, `␣snow` 0.05, `␣snowfall` 0.04 |
| 7 | …received almost no rain → ? | `␣between` | 0.022 | 11 | `␣in` 0.21, `,` 0.12, `␣during` 0.11, `␣this` 0.05, `␣last` 0.05 |
| 8 | …almost no rain between → ? | `␣March` | 0.045 | 10 | `␣` 0.19, `␣the` 0.10, `␣April` 0.07, `␣July` 0.06, `␣May` 0.06 |
| 9 | …no rain between March → ? | `␣and` | 0.621 | 1 | `␣and` 0.62, `␣` 0.34, `,` 0.01, `␣to` 0.01, `-A` 0.00 |
| 10 | …rain between March and → ? | `␣August` | 0.057 | 7 | `␣May` 0.31, `␣June` 0.21, `␣October` 0.09, `␣July` 0.08, `␣September` 0.07 |
| 11 | …between March and August → ? | `.` | 0.135 | 3 | `,` 0.40, `␣` 0.24, `.` 0.13, `␣of` 0.04, `␣and` 0.03 |
| 12 | …March and August. → ? | `␣Wells` | 0.000 | 960 | `␣The` 0.19, `␣In` 0.06, `␣This` 0.05, `␣However` 0.05, `␣It` 0.03 |
| 13 | …and August. Wells → ? | `␣dried` | 0.004 | 23 | `␣were` 0.24, `␣and` 0.09, `,` 0.09, `␣are` 0.05, `␣had` 0.03 |
| 14 | …August. Wells dried → ? | `␣up` | 0.706 | 1 | `␣up` 0.71, `␣out` 0.10, `␣in` 0.02, `␣quickly` 0.02, `,` 0.02 |
| 15 | …. Wells dried up → ? | `␣and` | 0.127 | 3 | `␣in` 0.15, `,` 0.14, `␣and` 0.13, `␣during` 0.04, `␣quickly` 0.03 |
| 16 | …Wells dried up and → ? | `␣farmers` | 0.012 | 9 | `␣the` 0.14, `␣were` 0.03, `␣water` 0.03, `␣many` 0.03, `␣some` 0.02 |
| 17 | …dried up and farmers → ? | `␣could` | 0.015 | 7 | `␣were` 0.17, `␣had` 0.15, `␣lost` 0.06, `␣began` 0.03, `␣and` 0.02 |
| 18 | …up and farmers could → ? | `␣not` | 0.592 | 1 | `␣not` 0.59, `␣no` 0.18, `␣see` 0.03, `␣only` 0.03, `␣barely` 0.03 |
| 19 | …and farmers could not → ? | `␣irrig` | 0.100 | 1 | `␣irrig` 0.10, `␣get` 0.09, `␣harvest` 0.06, `␣access` 0.05, `␣use` 0.05 |
| 20 | …farmers could not irrig → ? | `ate` | 1.000 | 1 | `ate` 1.00, `ated` 0.00, `at` 0.00, `age` 0.00, `ating` 0.00 |
| 21 | …could not irrigate → ? | `␣their` | 0.377 | 1 | `␣their` 0.38, `␣the` 0.11, `.` 0.10, `␣fields` 0.04, `␣crops` 0.04 |
| 22 | …not irrigate their → ? | `␣fields` | 0.521 | 1 | `␣fields` 0.52, `␣crops` 0.19, `␣land` 0.08, `␣lands` 0.05, `␣farms` 0.03 |
| 23 | …irrigate their fields → ? | `.` | 0.422 | 1 | `.` 0.42, `,` 0.13, `.\n` 0.05, `␣because` 0.04, `␣due` 0.04 |
| 24 | …ate their fields. → ? | `␣Because` | 0.004 | 31 | `␣The` 0.20, `␣In` 0.06, `␣This` 0.03, `␣Farmers` 0.02, `␣As` 0.02 |
| 25 | …their fields. Because → ? | `␣of` | 0.667 | 1 | `␣of` 0.67, `␣the` 0.14, `␣there` 0.02, `␣it` 0.01, `␣they` 0.01 |
| 26 | …fields. Because of → ? | `␣the` | 0.443 | 1 | `␣the` 0.44, `␣this` 0.25, `␣these` 0.05, `␣a` 0.02, `␣drought` 0.02 |
| 27 | …. Because of the → ? | `␣drought` | 0.119 | 2 | `␣lack` 0.12, `␣drought` 0.12, `␣dry` 0.08, `␣low` 0.05, `␣high` 0.04 |
| 28 | …Because of the drought → ? | `,` | 0.804 | 1 | `,` 0.80, `␣and` 0.04, `␣conditions` 0.03, `␣the` 0.03, `␣in` 0.02 |
| 29 | …of the drought, → ? | `␣the` | 0.283 | 1 | `␣the` 0.28, `␣farmers` 0.05, `␣many` 0.05, `␣there` 0.03, `␣a` 0.02 |
| 30 | …the drought, the → ? | `␣wheat` | 0.003 | 48 | `␣region` 0.04, `␣government` 0.04, `␣farmers` 0.04, `␣water` 0.02, `␣state` 0.02 |
| 31 | …drought, the wheat → ? | `␣harvest` | 0.130 | 2 | `␣crop` 0.29, `␣harvest` 0.13, `␣was` 0.07, `␣and` 0.05, `␣crops` 0.04 |
| 32 | …, the wheat harvest → ? | `␣was` | 0.475 | 1 | `␣was` 0.48, `␣in` 0.07, `␣is` 0.05, `␣dropped` 0.04, `␣had` 0.02 |
| 33 | …the wheat harvest was → ? | `␣the` | 0.004 | 37 | `␣low` 0.09, `␣reduced` 0.07, `␣very` 0.06, `␣delayed` 0.05, `␣small` 0.04 |
| 34 | …wheat harvest was the → ? | `␣smallest` | 0.077 | 3 | `␣lowest` 0.30, `␣second` 0.14, `␣smallest` 0.08, `␣worst` 0.07, `␣third` 0.05 |
| 35 | …harvest was the smallest → ? | `␣in` | 0.522 | 1 | `␣in` 0.52, `␣since` 0.15, `␣on` 0.07, `␣ever` 0.05, `␣it` 0.04 |
| 36 | …was the smallest in → ? | `␣forty` | 0.001 | 53 | `␣the` 0.28, `␣` 0.17, `␣history` 0.05, `␣a` 0.03, `␣more` 0.03 |
| 37 | …the smallest in forty → ? | `␣years` | 0.797 | 1 | `␣years` 0.80, `-five` 0.07, `-e` 0.02, `␣five` 0.02, `-t` 0.01 |
| 38 | …smallest in forty years → ? | `.` | 0.450 | 1 | `.` 0.45, `,` 0.16, `.\n` 0.15, `␣and` 0.07, `.\n\n` 0.06 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣years` | 0.004 | 7 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← years. | `␣forty` | 0.002 | 84 | `␣of` 0.05, `0` 0.05, `␣two` 0.05, `10` 0.04, `20` 0.04 |
| 4 | ? ← forty years. | `␣in` | 0.019 | 13 | `␣over` 0.14, `␣than` 0.11, `␣to` 0.11, `␣for` 0.11, `␣Over` 0.06 |
| 5 | ? ← in forty years. | `␣smallest` | 0.001 | 248 | `␣time` 0.15, `␣seen` 0.03, `␣changed` 0.01, `␣once` 0.01, `␣been` 0.01 |
| 6 | ? ← smallest in forty years… | `␣the` | 0.715 | 1 | `␣the` 0.71, `␣its` 0.08, `␣The` 0.06, `␣their` 0.04, `␣second` 0.02 |
| 7 | ? ← the smallest in forty… | `␣was` | 0.231 | 1 | `␣was` 0.23, `␣be` 0.19, `␣is` 0.13, `,` 0.09, `␣of` 0.05 |
| 8 | ? ← was the smallest in… | `␣harvest` | 0.003 | 22 | `␣It` 0.17, `␣it` 0.16, `␣population` 0.05, `␣which` 0.03, `␣size` 0.02 |
| 9 | ? ← harvest was the smallest… | `␣wheat` | 0.016 | 6 | `␣the` 0.15, `'s` 0.14, `␣The` 0.09, `’s` 0.02, `␣corn` 0.02 |
| 10 | ? ← wheat harvest was the… | `␣the` | 0.109 | 3 | `'s` 0.24, `␣The` 0.11, `␣the` 0.11, `␣winter` 0.07, `␣spring` 0.04 |
| 11 | ? ← the wheat harvest was… | `,` | 0.418 | 1 | `,` 0.42, `␣and` 0.20, `␣that` 0.09, `␣as` 0.04, `␣when` 0.03 |
| 12 | ? ← , the wheat harvest… | `␣drought` | 0.006 | 6 | `␣No` 0.33, `␣Yes` 0.15, `␣year` 0.04, `␣years` 0.01, `␣areas` 0.01 |
| 13 | ? ← drought, the wheat… | `␣the` | 0.293 | 1 | `␣the` 0.29, `␣severe` 0.09, `␣and` 0.06, `␣a` 0.05, `␣to` 0.04 |
| 14 | ? ← the drought, the… | `␣of` | 0.237 | 2 | `␣to` 0.41, `␣of` 0.24, `␣Despite` 0.11, `␣despite` 0.05, `␣during` 0.02 |
| 15 | ? ← of the drought,… | `␣Because` | 0.307 | 1 | `␣Because` 0.31, `␣because` 0.22, `␣result` 0.17, `␣severity` 0.03, `␣spite` 0.03 |
| 16 | ? ← Because of the drought… | `.` | 0.435 | 2 | `:` 0.54, `.` 0.44, `."` 0.00, `).` 0.00, `-` 0.00 |
| 17 | ? ← . Because of the… | `␣fields` | 0.005 | 21 | `␣drought` 0.04, `␣year` 0.03, `␣years` 0.02, `␣wheat` 0.02, `␣harvest` 0.02 |
| 18 | ? ← fields. Because of… | `␣their` | 0.111 | 3 | `␣the` 0.23, `␣wheat` 0.15, `␣their` 0.11, `␣his` 0.05, `␣some` 0.02 |
| 19 | ? ← their fields. Because… | `ate` | 0.034 | 6 | `␣in` 0.28, `␣of` 0.09, `␣to` 0.06, `␣on` 0.05, `␣water` 0.05 |
| 20 | ? ← ate their fields.… | `␣irrig` | 0.958 | 1 | `␣irrig` 0.96, `rig` 0.03, `␣renov` 0.00, `␣rehabilit` 0.00, `␣rejuven` 0.00 |
| 21 | ? ← irrigate their fields… | `␣not` | 0.039 | 2 | `␣to` 0.78, `␣not` 0.04, `␣and` 0.04, `␣farmers` 0.02, `␣properly` 0.02 |
| 22 | ? ← not irrigate their… | `␣could` | 0.462 | 1 | `␣could` 0.46, `␣did` 0.38, `␣do` 0.08, `␣to` 0.02, `␣would` 0.02 |
| 23 | ? ← could not irrigate… | `␣farmers` | 0.394 | 1 | `␣farmers` 0.39, `␣they` 0.24, `␣who` 0.06, `␣and` 0.05, `␣growers` 0.02 |
| 24 | ? ← farmers could not irrig… | `␣and` | 0.145 | 2 | `␣many` 0.20, `␣and` 0.15, `,` 0.12, `␣some` 0.06, `␣that` 0.06 |
| 25 | ? ← and farmers could not… | `␣up` | 0.004 | 18 | `,` 0.44, `␣drought` 0.04, `␣dry` 0.04, `␣water` 0.01, `␣out` 0.01 |
| 26 | ? ← up and farmers could… | `␣dried` | 0.441 | 1 | `␣dried` 0.44, `␣dry` 0.25, `␣drying` 0.15, `␣dries` 0.02, `␣went` 0.02 |
| 27 | ? ← dried up and farmers… | `␣Wells` | 0.001 | 107 | `␣rivers` 0.11, `␣reservoirs` 0.09, `␣fields` 0.06, `␣had` 0.05, `␣wells` 0.04 |
| 28 | ? ← Wells dried up and… | `.` | 0.893 | 1 | `.` 0.89, `:` 0.07, `."` 0.00, `).` 0.00, `".` 0.00 |
| 29 | ? ← . Wells dried up… | `␣August` | 0.002 | 84 | `␣drought` 0.07, `␣water` 0.02, `␣crops` 0.02, `␣years` 0.02, `␣wheat` 0.02 |
| 30 | ? ← August. Wells dried… | `␣and` | 0.147 | 2 | `␣in` 0.35, `␣and` 0.15, `␣of` 0.15, `␣early` 0.10, `␣late` 0.08 |
| 31 | ? ← and August. Wells… | `␣March` | 0.002 | 7 | `␣July` 0.91, `,` 0.04, `␣June` 0.02, `␣May` 0.01, `July` 0.01 |
| 32 | ? ← March and August.… | `␣between` | 0.778 | 1 | `␣between` 0.78, `␣in` 0.10, `␣of` 0.04, `␣during` 0.02, `,` 0.02 |
| 33 | ? ← between March and August… | `␣rain` | 0.040 | 4 | `␣fell` 0.08, `␣drought` 0.05, `␣rainfall` 0.04, `␣rain` 0.04, `␣occurred` 0.03 |
| 34 | ? ← rain between March and… | `␣no` | 0.206 | 2 | `␣of` 0.42, `␣no` 0.21, `␣little` 0.14, `␣without` 0.03, `␣any` 0.03 |
| 35 | ? ← no rain between March… | `␣almost` | 0.188 | 2 | `␣was` 0.22, `␣almost` 0.19, `␣had` 0.10, `␣to` 0.10, `␣with` 0.07 |
| 36 | ? ← almost no rain between… | `␣received` | 0.075 | 4 | `␣was` 0.40, `␣had` 0.18, `␣with` 0.13, `␣received` 0.07, `␣and` 0.03 |
| 37 | ? ← received almost no rain… | `␣region` | 0.041 | 3 | `␣California` 0.07, `␣state` 0.06, `␣region` 0.04, `␣country` 0.04, `␣area` 0.03 |
| 38 | ? ← region received almost no… | `The` | 0.024 | 5 | `␣the` 0.45, `␣The` 0.18, `␣Plains` 0.04, `␣this` 0.03, `The` 0.02 |

---

## 4. late_train

*Category: temporal*

> **Beginning:** Sarah woke up late because her alarm did not go off.  
> **Middle:** She skipped breakfast and ran to the station, but the doors closed just as she reached the platform.  
> **Ending:** She finally arrived at the office an hour after the meeting had started.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, and I don't want to talk about it," she said. ↵  ↵ | She finally arrived at the office an hour after the meeting had started. |
| sample | azkiewicz said. ↵  ↵ Technology is an integral part of our daily lives and impacts millions of people each day. ↵  ↵ Last semester, she had to give a lecture in a class. During the meeting, she needed to explain something to the class. After the meeting, her professor refused to help her with her work. Finally, she asked the professor what to do next time. At this time, the professor ignored her. ↵  ↵ "This has nothing to do with me," she said. ↵  ↵ | She finally arrived at the office an hour after the meeting had started. |
| sample | to reach out to them at the beginning of the meeting. ↵ She wanted to reach out to them, so she decided to talk about them in the meeting. ↵ After the start of the meeting, she asked the person to come to her within an hour at a time. ↵ She also made an agenda at the beginning of the meeting, and she also asked for a meeting that took no more than ten minutes. Some meetings require more and more time, and this was not one of them. ↵ | She finally arrived at the office an hour after the meeting had started. |
| sample | the people I'm talking about, what's your name, what's your name, your name, the age that it is, and stuff like that," she said. ↵ She is often happy when she thinks about where she is going, she said. ↵ "I thought I would go to all the places I thought I would go to. I thought I would go to all the places I thought I would go to the school and all the places I thought I would go," she said. ↵ | She finally arrived at the office an hour after the meeting had started. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Sarah woke up late because her alarm did not go off. | She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she couldn't sleep. She was so tired that she |
| sample | Sarah woke up late because her alarm did not go off. | She was exhausted and she knew there was no way she could do more than one thing. She thought of her husband who was in a wheelchair, but there was no way she could stand up. When she went to the bathroom, she thought of how she could go down the stairs. She thought to herself, "I can't do that because I can't stand up," and she was not going to be able to get out of bed. She thought she could get out of |
| sample | Sarah woke up late because her alarm did not go off. | She took a nap, but then it was a total 15 minutes until lunchtime and she had to wait for the bus to pick up. The one time she was late was at a bakery in the parking lot, so she went and asked where they were. They were in a hotel room, and she went to their manager and asked, "Would you like me to go a few more minutes early?" She told them that she would not, because she did not want to |
| sample | Sarah woke up late because her alarm did not go off. | The alarm company called the first technician she called the next day with no response. She was told to call the company first. The technician did not respond to her call. Sarah was very upset because a technician called the first technician. "I am not going to call the company because I do not have a service technician. Why does she call the first technician?" Sarah was frustrated because the company did not respond to her call. Sarah was also very upset because the company did not respond |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.918 | 47% |
| Backward | previous-token (right context) | 0.947 | 35% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Sar` | 0.000 | 1486 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Sar → ? | `ah` | 0.785 | 1 | `ah` 0.79, `co` 0.03, `aw` 0.02, `gent` 0.02, `ang` 0.01 |
| 3 | Sarah → ? | `␣w` | 0.000 | 833 | `:` 0.07, `'s` 0.05, `,` 0.03, `␣had` 0.02, `␣is` 0.02 |
| 4 | Sarah w → ? | `oke` | 0.501 | 1 | `oke` 0.50, `akes` 0.18, `aved` 0.06, `ink` 0.02, `aded` 0.01 |
| 5 | Sarah woke → ? | `␣up` | 0.928 | 1 | `␣up` 0.93, `␣from` 0.01, `␣to` 0.01, `␣with` 0.01, `␣early` 0.01 |
| 6 | …ah woke up → ? | `␣late` | 0.005 | 23 | `␣one` 0.26, `␣the` 0.06, `␣with` 0.06, `␣in` 0.06, `␣early` 0.05 |
| 7 | …woke up late → ? | `␣because` | 0.019 | 15 | `,` 0.15, `␣one` 0.14, `␣and` 0.12, `␣to` 0.06, `␣on` 0.05 |
| 8 | …oke up late because → ? | `␣her` | 0.128 | 3 | `␣she` 0.47, `␣of` 0.23, `␣her` 0.13, `␣the` 0.04, `␣I` 0.03 |
| 9 | …up late because her → ? | `␣alarm` | 0.020 | 8 | `␣husband` 0.09, `␣parents` 0.04, `␣mother` 0.03, `␣mom` 0.02, `␣boyfriend` 0.02 |
| 10 | …late because her alarm → ? | `␣did` | 0.001 | 34 | `␣clock` 0.63, `␣went` 0.10, `␣was` 0.06, `␣sounded` 0.06, `␣had` 0.03 |
| 11 | …because her alarm did → ? | `␣not` | 0.969 | 1 | `␣not` 0.97, `␣the` 0.01, `␣a` 0.00, `␣nothing` 0.00, `␣NOT` 0.00 |
| 12 | …her alarm did not → ? | `␣go` | 0.484 | 1 | `␣go` 0.48, `␣wake` 0.09, `␣sound` 0.09, `␣ring` 0.06, `␣work` 0.04 |
| 13 | …alarm did not go → ? | `␣off` | 0.995 | 1 | `␣off` 1.00, `␣to` 0.00, `␣on` 0.00, `␣out` 0.00, `.` 0.00 |
| 14 | …did not go off → ? | `.` | 0.469 | 1 | `.` 0.47, `,` 0.11, `␣at` 0.07, `␣and` 0.04, `␣when` 0.03 |
| 15 | …not go off. → ? | `␣She` | 0.428 | 1 | `␣She` 0.43, `␣The` 0.05, `␣Her` 0.04, `␣I` 0.04, `␣It` 0.03 |
| 16 | …go off. She → ? | `␣sk` | 0.000 | 244 | `␣was` 0.13, `␣had` 0.09, `␣went` 0.06, `␣w` 0.04, `␣didn` 0.03 |
| 17 | …off. She sk → ? | `ipped` | 0.985 | 1 | `ipped` 0.99, `idd` 0.00, `ips` 0.00, `ir` 0.00, `ated` 0.00 |
| 18 | …. She skipped → ? | `␣breakfast` | 0.314 | 1 | `␣breakfast` 0.31, `␣a` 0.10, `␣the` 0.09, `␣her` 0.08, `␣to` 0.08 |
| 19 | …She skipped breakfast → ? | `␣and` | 0.410 | 1 | `␣and` 0.41, `,` 0.23, `␣because` 0.09, `.` 0.06, `␣to` 0.03 |
| 20 | …skipped breakfast and → ? | `␣ran` | 0.005 | 28 | `␣went` 0.12, `␣ate` 0.11, `␣had` 0.10, `␣was` 0.07, `␣then` 0.03 |
| 21 | …ipped breakfast and ran → ? | `␣to` | 0.559 | 1 | `␣to` 0.56, `␣out` 0.10, `␣home` 0.04, `␣into` 0.03, `␣around` 0.03 |
| 22 | …breakfast and ran to → ? | `␣the` | 0.613 | 1 | `␣the` 0.61, `␣her` 0.16, `␣school` 0.04, `␣work` 0.03, `␣class` 0.03 |
| 23 | …and ran to the → ? | `␣station` | 0.000 | 125 | `␣kitchen` 0.22, `␣bathroom` 0.19, `␣store` 0.06, `␣gym` 0.03, `␣car` 0.03 |
| 24 | …ran to the station → ? | `,` | 0.072 | 3 | `␣to` 0.28, `.` 0.13, `,` 0.07, `␣at` 0.04, `␣before` 0.03 |
| 25 | …to the station, → ? | `␣but` | 0.088 | 2 | `␣where` 0.23, `␣but` 0.09, `␣which` 0.08, `␣only` 0.05, `␣and` 0.03 |
| 26 | …the station, but → ? | `␣the` | 0.099 | 2 | `␣she` 0.11, `␣the` 0.10, `␣it` 0.07, `␣when` 0.06, `␣her` 0.05 |
| 27 | …station, but the → ? | `␣doors` | 0.002 | 73 | `␣alarm` 0.19, `␣station` 0.07, `␣bus` 0.03, `␣clock` 0.03, `␣radio` 0.02 |
| 28 | …, but the doors → ? | `␣closed` | 0.033 | 8 | `␣were` 0.33, `␣did` 0.08, `␣opened` 0.06, `␣didn` 0.05, `␣to` 0.05 |
| 29 | …but the doors closed → ? | `␣just` | 0.011 | 15 | `.` 0.20, `␣and` 0.16, `,` 0.10, `␣behind` 0.08, `␣before` 0.06 |
| 30 | …the doors closed just → ? | `␣as` | 0.253 | 2 | `␣before` 0.35, `␣as` 0.25, `␣in` 0.10, `␣after` 0.05, `␣when` 0.05 |
| 31 | …doors closed just as → ? | `␣she` | 0.682 | 1 | `␣she` 0.68, `␣Sarah` 0.14, `␣her` 0.06, `␣the` 0.04, `␣they` 0.01 |
| 32 | …closed just as she → ? | `␣reached` | 0.033 | 6 | `␣was` 0.22, `␣got` 0.14, `␣entered` 0.11, `␣left` 0.10, `␣arrived` 0.05 |
| 33 | …just as she reached → ? | `␣the` | 0.633 | 1 | `␣the` 0.63, `␣her` 0.13, `␣home` 0.04, `␣it` 0.04, `␣for` 0.04 |
| 34 | …as she reached the → ? | `␣platform` | 0.001 | 167 | `␣station` 0.21, `␣door` 0.06, `␣exit` 0.03, `␣entrance` 0.03, `␣counter` 0.02 |
| 35 | …she reached the platform → ? | `.` | 0.553 | 1 | `.` 0.55, `,` 0.07, `␣to` 0.07, `␣and` 0.05, `␣for` 0.04 |
| 36 | …reached the platform. → ? | `␣She` | 0.302 | 1 | `␣She` 0.30, `␣The` 0.10, `␣Sarah` 0.09, `␣When` 0.03, `␣Her` 0.03 |
| 37 | …the platform. She → ? | `␣finally` | 0.002 | 81 | `␣was` 0.13, `␣had` 0.06, `␣ran` 0.02, `␣could` 0.02, `␣couldn` 0.02 |
| 38 | …platform. She finally → ? | `␣arrived` | 0.021 | 11 | `␣got` 0.20, `␣reached` 0.05, `␣opened` 0.05, `␣found` 0.05, `␣went` 0.04 |
| 39 | …. She finally arrived → ? | `␣at` | 0.619 | 1 | `␣at` 0.62, `,` 0.05, `␣and` 0.04, `␣in` 0.04, `␣to` 0.03 |
| 40 | …She finally arrived at → ? | `␣the` | 0.816 | 1 | `␣the` 0.82, `␣a` 0.04, `␣her` 0.04, `␣` 0.01, `␣school` 0.01 |
| 41 | …finally arrived at the → ? | `␣office` | 0.003 | 25 | `␣station` 0.37, `␣platform` 0.05, `␣train` 0.02, `␣door` 0.02, `␣entrance` 0.01 |
| 42 | …arrived at the office → ? | `␣an` | 0.001 | 54 | `,` 0.28, `␣and` 0.19, `.` 0.09, `␣where` 0.08, `␣to` 0.05 |
| 43 | …at the office an → ? | `␣hour` | 0.860 | 1 | `␣hour` 0.86, `x` 0.02, `␣exhausted` 0.01, `␣early` 0.01, `␣empty` 0.01 |
| 44 | …the office an hour → ? | `␣after` | 0.034 | 5 | `␣later` 0.66, `␣and` 0.09, `␣before` 0.07, `␣late` 0.06, `␣after` 0.03 |
| 45 | …office an hour after → ? | `␣the` | 0.208 | 1 | `␣the` 0.21, `␣she` 0.20, `␣her` 0.18, `␣waking` 0.03, `␣it` 0.03 |
| 46 | …an hour after the → ? | `␣meeting` | 0.003 | 31 | `␣alarm` 0.50, `␣bell` 0.06, `␣station` 0.04, `␣door` 0.04, `␣doors` 0.03 |
| 47 | …hour after the meeting → ? | `␣had` | 0.072 | 4 | `.` 0.27, `,` 0.18, `␣and` 0.10, `␣had` 0.07, `.\n` 0.05 |
| 48 | …after the meeting had → ? | `␣started` | 0.266 | 1 | `␣started` 0.27, `␣begun` 0.21, `␣ended` 0.19, `␣finished` 0.08, `␣been` 0.07 |
| 49 | …the meeting had started → ? | `.` | 0.515 | 1 | `.` 0.51, `,` 0.21, `.\n` 0.08, `␣and` 0.08, `.\n\n` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣started` | 0.000 | 753 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← started. | `␣had` | 0.001 | 40 | `␣get` 0.54, `␣you` 0.11, `␣getting` 0.06, `␣it` 0.02, `␣be` 0.01 |
| 4 | ? ← had started. | `␣meeting` | 0.001 | 109 | `␣they` 0.10, `␣it` 0.09, `␣he` 0.04, `␣I` 0.03, `␣you` 0.02 |
| 5 | ? ← meeting had started. | `␣the` | 0.594 | 1 | `␣the` 0.59, `␣a` 0.07, `␣The` 0.02, `␣first` 0.02, `␣this` 0.01 |
| 6 | ? ← the meeting had started… | `␣after` | 0.403 | 1 | `␣after` 0.40, `␣before` 0.16, `␣once` 0.09, `␣that` 0.06, `,` 0.03 |
| 7 | ? ← after the meeting had… | `␣hour` | 0.031 | 8 | `␣minutes` 0.11, `␣hours` 0.08, `␣days` 0.06, `␣long` 0.06, `␣until` 0.04 |
| 8 | ? ← hour after the meeting… | `␣an` | 0.728 | 1 | `␣an` 0.73, `␣one` 0.14, `␣half` 0.04, `1` 0.03, `␣An` 0.02 |
| 9 | ? ← an hour after the… | `␣office` | 0.001 | 56 | `␣half` 0.19, `␣than` 0.13, `␣about` 0.13, `␣over` 0.05, `␣About` 0.03 |
| 10 | ? ← office an hour after… | `␣the` | 0.210 | 2 | `'s` 0.22, `␣the` 0.21, `␣his` 0.10, `␣my` 0.06, `␣her` 0.05 |
| 11 | ? ← the office an hour… | `␣at` | 0.124 | 3 | `␣to` 0.31, `␣in` 0.17, `␣at` 0.12, `␣into` 0.11, `␣left` 0.10 |
| 12 | ? ← at the office an… | `␣arrived` | 0.305 | 1 | `␣arrived` 0.30, `␣back` 0.16, `␣arrive` 0.06, `␣up` 0.04, `␣was` 0.04 |
| 13 | ? ← arrived at the office… | `␣finally` | 0.006 | 19 | `␣They` 0.08, `␣He` 0.07, `␣and` 0.06, `␣She` 0.06, `␣who` 0.05 |
| 14 | ? ← finally arrived at the… | `␣She` | 0.036 | 8 | `␣and` 0.21, `␣he` 0.07, `␣they` 0.06, `␣He` 0.05, `␣They` 0.05 |
| 15 | ? ← She finally arrived at… | `.` | 0.439 | 2 | `:` 0.53, `.` 0.44, `."` 0.01, `!` 0.00, `).` 0.00 |
| 16 | ? ← . She finally arrived… | `␣platform` | 0.000 | 2851 | `␣meeting` 0.03, `␣her` 0.02, `␣time` 0.02, `␣hours` 0.01, `␣minutes` 0.01 |
| 17 | ? ← platform. She finally… | `␣the` | 0.207 | 1 | `␣the` 0.21, `␣meeting` 0.04, `␣a` 0.04, `␣her` 0.03, `␣media` 0.03 |
| 18 | ? ← the platform. She… | `␣reached` | 0.001 | 45 | `␣on` 0.37, `␣to` 0.10, `␣of` 0.09, `␣from` 0.04, `␣off` 0.03 |
| 19 | ? ← reached the platform.… | `␣she` | 0.168 | 2 | `␣had` 0.18, `␣she` 0.17, `␣finally` 0.05, `␣they` 0.05, `␣never` 0.04 |
| 20 | ? ← she reached the platform… | `␣as` | 0.121 | 4 | `␣before` 0.21, `␣when` 0.17, `␣time` 0.13, `␣until` 0.12, `␣as` 0.12 |
| 21 | ? ← as she reached the… | `␣just` | 0.019 | 3 | `␣soon` 0.48, `␣her` 0.03, `␣just` 0.02, `␣quickly` 0.01, `␣up` 0.01 |
| 22 | ? ← just as she reached… | `␣closed` | 0.002 | 58 | `,` 0.05, `␣her` 0.05, `␣meeting` 0.02, `␣up` 0.02, `␣office` 0.02 |
| 23 | ? ← closed just as she… | `␣doors` | 0.028 | 6 | `␣door` 0.14, `␣was` 0.13, `␣eyes` 0.06, `␣were` 0.04, `␣office` 0.03 |
| 24 | ? ← doors closed just as… | `␣the` | 0.391 | 1 | `␣the` 0.39, `␣The` 0.14, `␣office` 0.13, `␣and` 0.04, `'s` 0.02 |
| 25 | ? ← the doors closed just… | `␣but` | 0.038 | 6 | `␣and` 0.28, `,` 0.13, `␣as` 0.06, `␣all` 0.06, `␣that` 0.05 |
| 26 | ? ← but the doors closed… | `,` | 0.772 | 1 | `,` 0.77, `␣meeting` 0.01, `␣office` 0.01, `␣room` 0.01, `␣door` 0.01 |
| 27 | ? ← , but the doors… | `␣station` | 0.002 | 73 | `␣meeting` 0.05, `␣office` 0.05, `␣room` 0.03, `␣door` 0.03, `␣in` 0.02 |
| 28 | ? ← station, but the… | `␣the` | 0.290 | 1 | `␣the` 0.29, `␣train` 0.12, `␣her` 0.05, `␣police` 0.02, `␣bus` 0.02 |
| 29 | ? ← the station, but… | `␣to` | 0.194 | 2 | `␣at` 0.21, `␣to` 0.19, `␣of` 0.05, `␣into` 0.04, `␣from` 0.04 |
| 30 | ? ← to the station,… | `␣ran` | 0.004 | 46 | `␣back` 0.11, `␣get` 0.06, `␣way` 0.06, `␣her` 0.06, `␣up` 0.03 |
| 31 | ? ← ran to the station… | `␣and` | 0.208 | 2 | `␣She` 0.23, `␣and` 0.21, `␣she` 0.07, `She` 0.03, `,` 0.03 |
| 32 | ? ← and ran to the… | `␣breakfast` | 0.002 | 80 | `␣up` 0.08, `␣car` 0.05, `,` 0.04, `␣door` 0.03, `␣phone` 0.02 |
| 33 | ? ← breakfast and ran to… | `ipped` | 0.070 | 4 | `␣her` 0.27, `␣ate` 0.10, `␣for` 0.10, `ipped` 0.07, `␣had` 0.05 |
| 34 | ? ← ipped breakfast and ran… | `␣sk` | 0.995 | 1 | `␣sk` 0.99, `␣Sk` 0.00, `sk` 0.00, `␣s` 0.00, `k` 0.00 |
| 35 | ? ← skipped breakfast and… | `␣She` | 0.398 | 1 | `␣She` 0.40, `␣she` 0.08, `,` 0.06, `She` 0.05, `␣had` 0.01 |
| 36 | ? ← She skipped breakfast… | `.` | 0.935 | 1 | `.` 0.93, `."` 0.02, `:` 0.02, `?` 0.00, `!` 0.00 |
| 37 | ? ← . She skipped… | `␣off` | 0.003 | 42 | `␣morning` 0.03, `␣meeting` 0.03, `␣office` 0.02, `␣her` 0.02, `␣breakfast` 0.02 |
| 38 | ? ← off. She sk… | `␣go` | 0.025 | 9 | `␣went` 0.12, `␣it` 0.06, `␣took` 0.06, `␣her` 0.04, `␣take` 0.03 |
| 39 | ? ← go off. She… | `␣not` | 0.056 | 4 | `␣to` 0.55, `␣would` 0.12, `␣alarm` 0.07, `␣not` 0.06, `'t` 0.05 |
| 40 | ? ← not go off.… | `␣did` | 0.791 | 1 | `␣did` 0.79, `␣would` 0.18, `␣could` 0.01, `␣does` 0.01, `␣do` 0.00 |
| 41 | ? ← did not go off… | `␣alarm` | 0.333 | 1 | `␣alarm` 0.33, `␣clock` 0.14, `␣phone` 0.05, `␣bell` 0.04, `␣bells` 0.04 |
| 42 | ? ← alarm did not go… | `␣her` | 0.166 | 2 | `␣the` 0.32, `␣her` 0.17, `␣The` 0.14, `␣Her` 0.11, `'s` 0.05 |
| 43 | ? ← her alarm did not… | `␣because` | 0.012 | 7 | `␣but` 0.39, `,` 0.24, `␣and` 0.16, `␣that` 0.04, `␣But` 0.03 |
| 44 | ? ← because her alarm did… | `␣late` | 0.038 | 3 | `,` 0.15, `␣morning` 0.06, `␣late` 0.04, `␣up` 0.04, `␣early` 0.03 |
| 45 | ? ← late because her alarm… | `␣up` | 0.125 | 2 | `␣was` 0.20, `␣up` 0.13, `␣minutes` 0.10, `␣running` 0.07, `␣arrived` 0.06 |
| 46 | ? ← up late because her… | `oke` | 0.275 | 1 | `oke` 0.27, `␣stayed` 0.22, `␣got` 0.09, `␣was` 0.07, `␣stay` 0.06 |
| 47 | ? ← oke up late because… | `␣w` | 0.995 | 1 | `␣w` 1.00, `␣W` 0.00, `W` 0.00, `w` 0.00, `␣aw` 0.00 |
| 48 | ? ← woke up late… | `ah` | 0.003 | 23 | `␣She` 0.17, `␣she` 0.17, `,` 0.05, `␣and` 0.04, `␣woman` 0.02 |
| 49 | ? ← ah woke up… | `Sar` | 0.514 | 1 | `Sar` 0.51, `␣Le` 0.05, `Le` 0.03, `j` 0.03, `bor` 0.02 |

---

## 5. bread_recipe

*Category: temporal*

> **Beginning:** First, mix the flour, yeast, salt and warm water in a large bowl.  
> **Middle:** Knead the dough for ten minutes, then leave it to rise for an hour until it has doubled in size.  
> **Ending:** Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | butter all over it, and let it sit for thirty minutes. ↵  ↵ When the dough is ready, pour it into a loaf pan, pour the melted butter all over it, and let it sit for thirty minutes. ↵  ↵ When the dough is ready, pour it into a loaf pan, pour the melted butter all over it, and let it sit for thirty minutes. ↵  ↵ Next, sift the flour, mix it with the brown sugar, and sprinkle it all over the top of the loaf. ↵  ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |
| sample | ball. Once the dough has risen, form it into a loaf shape and place it on a baking sheet. ↵  ↵ Once ready, cover the loaf with a kitchen towel and allow it to prove for two hours, or until doubled in size. ↵  ↵ Next, the dough should be moved to a lightly floured surface and place on a baking sheet. It should then be brushed lightly with sugar and again dusted with flour, making sure that it is evenly distributed across the surface of the loaf. ↵  ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |
| sample | a springform pan. It is easy; just take it one step at a time. ↵ Next, bake the dough in a large springform pan. Use only enough flour to coat the bottom of the pan. ↵ After that, you should add a beaten egg mixed with two tablespoons of milk, a generous amount of flour, a dash of cinnamon, brown sugar, and a sprinkling of cinnamon. Now all you need to do is coat the surface of the loaf with the mixture. ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |
| sample | whisk a mixture of honey, melted butter, brown sugar, and water to make the glaze. Brush the top of the loaf with the glaze, and bake the loaf at 220 degrees for thirty minutes until it is golden brown. ↵ While the loaf is baking, whisk a mixture of egg, honey, melted butter, and brown sugar to make the glaze. Lightly brush the top of the loaf with the crumb mixture, and sprinkle the glaze over the top of the loaf. ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | First, mix the flour, yeast, salt and warm water in a large bowl. | Add the sugar, oil, and milk and mix until the dough is smooth. Cover the dough with plastic wrap and let it rise in a warm place for about 1 hour. ↵ Preheat the oven to 350 degrees Fahrenheit. Line a baking sheet with parchment paper and set aside. ↵ In a large bowl, mix the flour, yeast, salt, and warm water. Add the sugar, oil, and milk and mix until the dough is smooth. Cover the dough with plastic |
| sample | First, mix the flour, yeast, salt and warm water in a large bowl. | Add the softened butter, then gradually add the sour cream and milk until the dough is the consistency of soft butter. Turn the dough out onto a floured work surface and knead it for about five minutes. This will help develop the structure of the dough and make it easier to work with. ↵ Shape the dough into a ball and place it in a greased bowl. Cover the bowl with a damp cloth and let the dough rise for about an hour or until it has doubled |
| sample | First, mix the flour, yeast, salt and warm water in a large bowl. | Combine the milk, eggs, and melted butter and start your breading by making a hole in the center of the flour mixture. Place a sheet of wax paper in the center of the flour mixture and set it aside to rise. Once the dough has risen, punch it down to remove the air bubbles and begin kneading and forming the dough. ↵  ↵ Rounding out the dough, divide the dough into 12 equal pieces and roll them out into a rope. Then, wrap the rope |
| sample | First, mix the flour, yeast, salt and warm water in a large bowl. | Then, add the sugar, eggs, milk, and oil or olive oil. Mix well until the dough is smooth. Cover the dough with plastic wrap and let it rise for 2 hours. Next, preheat the oven to 350 degrees F. Bake the pizza for 15-20 minutes, or until the crust is golden brown and the cheese is bubbling. ↵ What do you put on a thin crust pizza? ↵ There are a few things you can put on a |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.572 | 68% |
| Backward | previous-token (right context) | 0.571 | 58% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `First` | 0.001 | 128 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | First → ? | `,` | 0.307 | 1 | `,` 0.31, `␣of` 0.11, `␣off` 0.03, `␣and` 0.03, `␣Aid` 0.03 |
| 3 | First, → ? | `␣mix` | 0.000 | 243 | `␣the` 0.10, `␣let` 0.08, `␣you` 0.07, `␣we` 0.06, `␣I` 0.06 |
| 4 | First, mix → ? | `␣the` | 0.421 | 1 | `␣the` 0.42, `␣together` 0.14, `␣a` 0.05, `␣` 0.05, `␣up` 0.05 |
| 5 | First, mix the → ? | `␣flour` | 0.049 | 1 | `␣flour` 0.05, `␣ingredients` 0.04, `␣dry` 0.02, `␣water` 0.02, `␣oil` 0.02 |
| 6 | …, mix the flour → ? | `,` | 0.462 | 1 | `,` 0.46, `␣and` 0.32, `␣with` 0.17, `␣into` 0.01, `␣in` 0.01 |
| 7 | …mix the flour, → ? | `␣yeast` | 0.026 | 4 | `␣baking` 0.39, `␣salt` 0.22, `␣sugar` 0.14, `␣yeast` 0.03, `␣water` 0.02 |
| 8 | …the flour, yeast → ? | `,` | 0.829 | 1 | `,` 0.83, `␣and` 0.15, `␣powder` 0.01, `␣extract` 0.00, `␣(` 0.00 |
| 9 | …flour, yeast, → ? | `␣salt` | 0.219 | 3 | `␣and` 0.40, `␣sugar` 0.24, `␣salt` 0.22, `␣water` 0.02, `␣baking` 0.02 |
| 10 | …, yeast, salt → ? | `␣and` | 0.129 | 2 | `,` 0.86, `␣and` 0.13, `␣&` 0.00, `␣(` 0.00, `␣water` 0.00 |
| 11 | …yeast, salt and → ? | `␣warm` | 0.022 | 7 | `␣sugar` 0.51, `␣water` 0.10, `␣oil` 0.08, `␣olive` 0.04, `␣pepper` 0.03 |
| 12 | …, salt and warm → ? | `␣water` | 0.912 | 1 | `␣water` 0.91, `␣milk` 0.06, `,` 0.01, `␣(` 0.01, `␣but` 0.00 |
| 13 | …salt and warm water → ? | `␣in` | 0.437 | 1 | `␣in` 0.44, `␣together` 0.23, `.` 0.12, `␣to` 0.04, `␣until` 0.03 |
| 14 | …and warm water in → ? | `␣a` | 0.920 | 1 | `␣a` 0.92, `␣the` 0.05, `␣your` 0.00, `␣large` 0.00, `␣an` 0.00 |
| 15 | …warm water in a → ? | `␣large` | 0.485 | 1 | `␣large` 0.49, `␣bowl` 0.27, `␣small` 0.07, `␣mixing` 0.05, `␣medium` 0.02 |
| 16 | …water in a large → ? | `␣bowl` | 0.630 | 1 | `␣bowl` 0.63, `␣mixing` 0.25, `,` 0.02, `␣pot` 0.01, `␣bucket` 0.01 |
| 17 | …in a large bowl → ? | `.` | 0.675 | 1 | `.` 0.67, `␣and` 0.07, `.\n` 0.06, `␣until` 0.05, `,` 0.05 |
| 18 | …a large bowl. → ? | `␣K` | 0.030 | 9 | `␣Add` 0.23, `␣Then` 0.08, `␣Let` 0.07, `␣Make` 0.05, `␣Stir` 0.04 |
| 19 | …large bowl. K → ? | `ne` | 0.996 | 1 | `ne` 1.00, `not` 0.00, `osher` 0.00, `need` 0.00, `ibble` 0.00 |
| 20 | …bowl. Kne → ? | `ad` | 0.999 | 1 | `ad` 1.00, `ading` 0.00, `aded` 0.00, `ader` 0.00, `el` 0.00 |
| 21 | …. Knead → ? | `␣the` | 0.751 | 1 | `␣the` 0.75, `␣until` 0.07, `␣for` 0.02, `␣in` 0.02, `␣it` 0.02 |
| 22 | …Knead the → ? | `␣dough` | 0.771 | 1 | `␣dough` 0.77, `␣mixture` 0.13, `␣dry` 0.02, `␣flour` 0.02, `␣ingredients` 0.02 |
| 23 | …nead the dough → ? | `␣for` | 0.322 | 1 | `␣for` 0.32, `␣until` 0.27, `␣on` 0.10, `␣with` 0.04, `␣together` 0.03 |
| 24 | …ad the dough for → ? | `␣ten` | 0.006 | 12 | `␣` 0.41, `␣about` 0.28, `␣a` 0.15, `␣at` 0.03, `␣five` 0.02 |
| 25 | …the dough for ten → ? | `␣minutes` | 0.903 | 1 | `␣minutes` 0.90, `␣to` 0.08, `␣or` 0.01, `␣seconds` 0.00, `-` 0.00 |
| 26 | …dough for ten minutes → ? | `,` | 0.307 | 1 | `,` 0.31, `␣until` 0.21, `.` 0.15, `␣or` 0.11, `␣and` 0.05 |
| 27 | …for ten minutes, → ? | `␣then` | 0.227 | 1 | `␣then` 0.23, `␣until` 0.22, `␣or` 0.11, `␣adding` 0.10, `␣turning` 0.04 |
| 28 | …ten minutes, then → ? | `␣leave` | 0.015 | 10 | `␣cover` 0.37, `␣let` 0.20, `␣turn` 0.05, `␣add` 0.04, `␣kne` 0.04 |
| 29 | …minutes, then leave → ? | `␣it` | 0.684 | 1 | `␣it` 0.68, `␣to` 0.20, `␣the` 0.05, `␣for` 0.02, `␣aside` 0.01 |
| 30 | …, then leave it → ? | `␣to` | 0.832 | 1 | `␣to` 0.83, `␣in` 0.04, `␣for` 0.04, `␣aside` 0.03, `␣on` 0.01 |
| 31 | …then leave it to → ? | `␣rise` | 0.563 | 1 | `␣rise` 0.56, `␣rest` 0.38, `␣proof` 0.02, `␣prove` 0.01, `␣stand` 0.01 |
| 32 | …leave it to rise → ? | `␣for` | 0.388 | 1 | `␣for` 0.39, `␣until` 0.18, `␣in` 0.17, `.` 0.07, `␣again` 0.05 |
| 33 | …it to rise for → ? | `␣an` | 0.439 | 1 | `␣an` 0.44, `␣another` 0.16, `␣` 0.09, `␣one` 0.08, `␣about` 0.05 |
| 34 | …to rise for an → ? | `␣hour` | 0.909 | 1 | `␣hour` 0.91, `␣additional` 0.08, `␣extra` 0.01, `␣further` 0.00, `␣an` 0.00 |
| 35 | …rise for an hour → ? | `␣until` | 0.054 | 5 | `.` 0.33, `.\n` 0.19, `␣or` 0.14, `,` 0.08, `␣until` 0.05 |
| 36 | …for an hour until → ? | `␣it` | 0.615 | 1 | `␣it` 0.61, `␣doubled` 0.25, `␣the` 0.04, `␣double` 0.03, `␣a` 0.01 |
| 37 | …an hour until it → ? | `␣has` | 0.458 | 1 | `␣has` 0.46, `␣is` 0.16, `␣doubles` 0.13, `'s` 0.13, `␣becomes` 0.03 |
| 38 | …hour until it has → ? | `␣doubled` | 0.835 | 1 | `␣doubled` 0.83, `␣increased` 0.04, `␣risen` 0.02, `␣double` 0.02, `␣become` 0.01 |
| 39 | …until it has doubled → ? | `␣in` | 0.801 | 1 | `␣in` 0.80, `.` 0.10, `.\n` 0.04, `,` 0.01, `␣its` 0.01 |
| 40 | …it has doubled in → ? | `␣size` | 0.833 | 1 | `␣size` 0.83, `␣volume` 0.13, `␣bulk` 0.03, `␣height` 0.00, `␣length` 0.00 |
| 41 | …has doubled in size → ? | `.` | 0.445 | 1 | `.` 0.44, `.\n` 0.39, `.\n\n` 0.09, `,` 0.03, `␣and` 0.02 |
| 42 | …doubled in size. → ? | `␣Finally` | 0.003 | 51 | `␣Pre` 0.13, `␣Then` 0.06, `␣Divide` 0.05, `␣P` 0.05, `␣Shape` 0.04 |
| 43 | …in size. Finally → ? | `,` | 0.958 | 1 | `,` 0.96, `␣kne` 0.01, `␣divide` 0.01, `␣shape` 0.01, `␣punch` 0.00 |
| 44 | …size. Finally, → ? | `␣bake` | 0.005 | 28 | `␣divide` 0.19, `␣punch` 0.13, `␣kne` 0.12, `␣shape` 0.09, `␣roll` 0.04 |
| 45 | …. Finally, bake → ? | `␣the` | 0.626 | 1 | `␣the` 0.63, `␣it` 0.18, `␣in` 0.08, `␣at` 0.06, `␣for` 0.02 |
| 46 | …Finally, bake the → ? | `␣loaf` | 0.010 | 10 | `␣dough` 0.29, `␣bread` 0.25, `␣pizza` 0.06, `␣cookies` 0.03, `␣b` 0.02 |
| 47 | …, bake the loaf → ? | `␣at` | 0.263 | 2 | `␣in` 0.45, `␣at` 0.26, `␣for` 0.20, `␣on` 0.02, `␣according` 0.02 |
| 48 | …bake the loaf at → ? | `␣` | 0.913 | 1 | `␣` 0.91, `␣a` 0.06, `␣the` 0.01, `␣around` 0.00, `␣an` 0.00 |
| 49 | …the loaf at → ? | `22` | 0.012 | 12 | `35` 0.39, `18` 0.16, `37` 0.09, `20` 0.06, `40` 0.06 |
| 50 | …loaf at 22 → ? | `0` | 0.704 | 1 | `0` 0.70, `5` 0.29, `7` 0.00, `2` 0.00, `6` 0.00 |
| 51 | …at 220 → ? | `␣degrees` | 0.456 | 1 | `␣degrees` 0.46, `°C` 0.16, `°F` 0.12, `C` 0.06, `º` 0.05 |
| 52 | …220 degrees → ? | `␣for` | 0.181 | 2 | `␣Fahrenheit` 0.49, `␣for` 0.18, `␣F` 0.17, `␣Celsius` 0.11, `␣C` 0.01 |
| 53 | …220 degrees for → ? | `␣thirty` | 0.020 | 7 | `␣` 0.50, `␣about` 0.17, `␣an` 0.12, `␣approximately` 0.06, `␣one` 0.03 |
| 54 | …0 degrees for thirty → ? | `␣minutes` | 0.826 | 1 | `␣minutes` 0.83, `␣to` 0.11, `-five` 0.04, `␣five` 0.01, `-` 0.00 |
| 55 | …degrees for thirty minutes → ? | `␣until` | 0.034 | 6 | `.\n` 0.29, `,` 0.22, `.` 0.18, `␣or` 0.12, `.\n\n` 0.05 |
| 56 | …for thirty minutes until → ? | `␣it` | 0.374 | 1 | `␣it` 0.37, `␣golden` 0.35, `␣the` 0.13, `␣a` 0.06, `␣cooked` 0.02 |
| 57 | …thirty minutes until it → ? | `␣is` | 0.455 | 1 | `␣is` 0.46, `␣has` 0.33, `'s` 0.15, `␣reaches` 0.02, `␣becomes` 0.01 |
| 58 | …minutes until it is → ? | `␣golden` | 0.607 | 1 | `␣golden` 0.61, `␣done` 0.07, `␣cooked` 0.05, `␣lightly` 0.04, `␣light` 0.04 |
| 59 | …until it is golden → ? | `␣brown` | 0.889 | 1 | `␣brown` 0.89, `␣and` 0.05, `.\n` 0.02, `-brown` 0.01, `.` 0.01 |
| 60 | …it is golden brown → ? | `.` | 0.182 | 3 | `.\n` 0.38, `␣and` 0.26, `.` 0.18, `␣on` 0.07, `.\n\n` 0.06 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣brown` | 0.000 | 1515 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← brown. | `␣golden` | 0.218 | 1 | `␣golden` 0.22, `␣or` 0.09, `␣and` 0.08, `␣turn` 0.07, `␣to` 0.06 |
| 4 | ? ← golden brown. | `␣is` | 0.144 | 2 | `␣until` 0.47, `␣is` 0.14, `␣and` 0.11, `␣are` 0.07, `␣turn` 0.04 |
| 5 | ? ← is golden brown. | `␣it` | 0.113 | 3 | `␣crust` 0.15, `␣top` 0.13, `␣it` 0.11, `␣bread` 0.09, `␣pastry` 0.05 |
| 6 | ? ← it is golden brown… | `␣until` | 0.880 | 1 | `␣until` 0.88, `␣when` 0.03, `␣Until` 0.02, `␣till` 0.01, `␣When` 0.01 |
| 7 | ? ← until it is golden… | `␣minutes` | 0.083 | 3 | `␣or` 0.21, `,` 0.09, `␣minutes` 0.08, `␣it` 0.07, `␣side` 0.06 |
| 8 | ? ← minutes until it is… | `␣thirty` | 0.001 | 43 | `20` 0.12, `10` 0.10, `15` 0.10, `30` 0.09, `␣few` 0.09 |
| 9 | ? ← thirty minutes until it… | `␣for` | 0.265 | 1 | `␣for` 0.27, `␣to` 0.27, `␣about` 0.12, `␣every` 0.08, `␣About` 0.07 |
| 10 | ? ← for thirty minutes until… | `␣degrees` | 0.070 | 4 | `␣oven` 0.19, `␣bake` 0.10, `␣Bake` 0.07, `␣degrees` 0.07, `␣Fahrenheit` 0.05 |
| 11 | ? ← degrees for thirty minutes… | `0` | 0.788 | 1 | `0` 0.79, `5` 0.13, `␣hundred` 0.02, `␣thousand` 0.01, `00` 0.01 |
| 12 | ? ← 0 degrees for thirty… | `22` | 0.009 | 10 | `35` 0.42, `40` 0.17, `18` 0.11, `30` 0.09, `20` 0.07 |
| 13 | ? ← 220 degrees for… | `␣` | 0.990 | 1 | `␣` 0.99, `-` 0.01, `/` 0.00, `,` 0.00, `␣-` 0.00 |
| 14 | ? ← 220 degrees… | `␣at` | 0.925 | 1 | `␣at` 0.93, `␣to` 0.01, `␣on` 0.01, `␣of` 0.01, `:` 0.01 |
| 15 | ? ← at 220… | `␣loaf` | 0.001 | 77 | `␣oven` 0.28, `␣bake` 0.16, `␣Bake` 0.14, `␣it` 0.07, `ake` 0.04 |
| 16 | ? ← loaf at 22… | `␣the` | 0.815 | 1 | `␣the` 0.82, `␣your` 0.02, `␣a` 0.01, `␣bread` 0.01, `␣whole` 0.01 |
| 17 | ? ← the loaf at… | `␣bake` | 0.254 | 2 | `␣Bake` 0.53, `␣bake` 0.25, `ake` 0.11, `␣baking` 0.02, `␣Baking` 0.02 |
| 18 | ? ← bake the loaf at… | `,` | 0.150 | 2 | `␣and` 0.51, `,` 0.15, `␣then` 0.09, `␣to` 0.07, `␣Then` 0.03 |
| 19 | ? ← , bake the loaf… | `␣Finally` | 0.193 | 1 | `␣Finally` 0.19, `␣Then` 0.06, `␣oven` 0.06, `␣baking` 0.03, `␣done` 0.03 |
| 20 | ? ← Finally, bake the… | `.` | 0.967 | 1 | `.` 0.97, `).` 0.01, `:` 0.01, `-` 0.00, `!` 0.00 |
| 21 | ? ← . Finally, bake… | `␣size` | 0.003 | 54 | `␣loaf` 0.09, `␣it` 0.05, `␣pan` 0.04, `␣top` 0.03, `␣shape` 0.03 |
| 22 | ? ← size. Finally,… | `␣in` | 0.481 | 1 | `␣in` 0.48, `␣desired` 0.17, `␣its` 0.06, `␣loaf` 0.05, `␣same` 0.04 |
| 23 | ? ← in size. Finally… | `␣doubled` | 0.584 | 1 | `␣doubled` 0.58, `␣doubles` 0.11, `␣double` 0.10, `␣inches` 0.04, `␣inch` 0.02 |
| 24 | ? ← doubled in size.… | `␣has` | 0.368 | 2 | `␣until` 0.38, `␣has` 0.37, `␣is` 0.10, `␣have` 0.04, `␣almost` 0.02 |
| 25 | ? ← has doubled in size… | `␣it` | 0.915 | 1 | `␣it` 0.91, `␣dough` 0.06, `␣loaf` 0.01, `␣bread` 0.00, `␣mixture` 0.00 |
| 26 | ? ← it has doubled in… | `␣until` | 0.932 | 1 | `␣until` 0.93, `␣when` 0.02, `␣once` 0.02, `␣after` 0.01, `␣that` 0.01 |
| 27 | ? ← until it has doubled… | `␣hour` | 0.101 | 5 | `␣or` 0.27, `␣rise` 0.16, `␣hours` 0.14, `␣minutes` 0.13, `␣hour` 0.10 |
| 28 | ? ← hour until it has… | `␣an` | 0.646 | 1 | `␣an` 0.65, `␣one` 0.28, `␣another` 0.03, `␣half` 0.01, `1` 0.01 |
| 29 | ? ← an hour until it… | `␣for` | 0.619 | 1 | `␣for` 0.62, `␣about` 0.23, `␣half` 0.07, `␣least` 0.04, `␣to` 0.02 |
| 30 | ? ← for an hour until… | `␣rise` | 0.449 | 1 | `␣rise` 0.45, `␣place` 0.13, `␣rest` 0.06, `␣proof` 0.06, `␣it` 0.04 |
| 31 | ? ← rise for an hour… | `␣to` | 0.178 | 2 | `␣it` 0.61, `␣to` 0.18, `␣dough` 0.12, `␣loaf` 0.05, `␣bread` 0.01 |
| 32 | ? ← to rise for an… | `␣it` | 0.590 | 1 | `␣it` 0.59, `␣dough` 0.22, `␣loaf` 0.04, `␣bread` 0.02, `␣leave` 0.02 |
| 33 | ? ← it to rise for… | `␣leave` | 0.203 | 2 | `␣allow` 0.69, `␣leave` 0.20, `␣Allow` 0.08, `␣let` 0.01, `␣Leave` 0.01 |
| 34 | ? ← leave it to rise… | `␣then` | 0.053 | 3 | `␣and` 0.83, `,` 0.09, `␣then` 0.05, `␣Then` 0.01, `␣to` 0.00 |
| 35 | ? ← then leave it to… | `,` | 0.584 | 1 | `,` 0.58, `␣and` 0.36, `;` 0.01, `),` 0.00, `␣towel` 0.00 |
| 36 | ? ← , then leave it… | `␣minutes` | 0.075 | 2 | `␣towel` 0.11, `␣minutes` 0.08, `␣dough` 0.05, `␣pan` 0.05, `␣wrap` 0.05 |
| 37 | ? ← minutes, then leave… | `␣ten` | 0.161 | 1 | `␣ten` 0.16, `␣thirty` 0.16, `␣five` 0.11, `␣fifteen` 0.11, `30` 0.11 |
| 38 | ? ← ten minutes, then… | `␣for` | 0.824 | 1 | `␣for` 0.82, `␣about` 0.10, `␣another` 0.01, `␣to` 0.01, `␣approximately` 0.01 |
| 39 | ? ← for ten minutes,… | `␣dough` | 0.085 | 3 | `ad` 0.14, `␣rest` 0.12, `␣dough` 0.09, `␣it` 0.07, `␣degrees` 0.06 |
| 40 | ? ← dough for ten minutes… | `␣the` | 0.966 | 1 | `␣the` 0.97, `␣your` 0.01, `␣of` 0.00, `␣bread` 0.00, `aded` 0.00 |
| 41 | ? ← the dough for ten… | `ad` | 0.846 | 1 | `ad` 0.85, `␣rest` 0.03, `ading` 0.02, `␣Rest` 0.02, `␣proof` 0.01 |
| 42 | ? ← ad the dough for… | `ne` | 0.785 | 1 | `ne` 0.79, `␣kne` 0.21, `-ne` 0.00, `ere` 0.00, `n` 0.00 |
| 43 | ? ← nead the dough… | `␣K` | 0.984 | 1 | `␣K` 0.98, `K` 0.01, `.K` 0.00, `k` 0.00, `-k` 0.00 |
| 44 | ? ← Knead the… | `.` | 0.990 | 1 | `.` 0.99, `).` 0.01, `:` 0.00, `!` 0.00, `.)` 0.00 |
| 45 | ? ← . Knead… | `␣bowl` | 0.056 | 2 | `␣dough` 0.06, `␣bowl` 0.06, `␣pan` 0.06, `␣it` 0.04, `␣loaf` 0.04 |
| 46 | ? ← bowl. Kne… | `␣large` | 0.141 | 2 | `␣the` 0.28, `␣large` 0.14, `␣a` 0.14, `ed` 0.12, `ased` 0.09 |
| 47 | ? ← large bowl. K… | `␣a` | 0.945 | 1 | `␣a` 0.95, `␣the` 0.03, `␣another` 0.01, `␣or` 0.00, `␣one` 0.00 |
| 48 | ? ← a large bowl.… | `␣in` | 0.710 | 1 | `␣in` 0.71, `␣into` 0.21, `␣to` 0.05, `␣of` 0.00, `␣and` 0.00 |
| 49 | ? ← in a large bowl… | `␣water` | 0.032 | 7 | `␣it` 0.24, `␣together` 0.17, `␣salt` 0.16, `␣ingredients` 0.09, `␣dough` 0.03 |
| 50 | ? ← water in a large… | `␣warm` | 0.165 | 2 | `␣and` 0.51, `␣warm` 0.17, `␣of` 0.11, `␣cold` 0.07, `␣with` 0.03 |
| 51 | ? ← warm water in a… | `␣and` | 0.573 | 1 | `␣and` 0.57, `␣of` 0.18, `␣with` 0.10, `␣in` 0.04, `␣the` 0.03 |
| 52 | ? ← and warm water in… | `␣salt` | 0.057 | 4 | `,` 0.53, `␣flour` 0.16, `␣yeast` 0.08, `␣salt` 0.06, `␣sugar` 0.04 |
| 53 | ? ← salt and warm water… | `,` | 0.742 | 1 | `,` 0.74, `␣of` 0.09, `␣with` 0.06, `␣the` 0.04, `␣sea` 0.02 |
| 54 | ? ← , salt and warm… | `␣yeast` | 0.314 | 1 | `␣flour` 0.31, `␣yeast` 0.31, `␣sugar` 0.11, `␣soda` 0.08, `␣powder` 0.05 |
| 55 | ? ← yeast, salt and… | `,` | 0.904 | 1 | `,` 0.90, `␣the` 0.03, `␣dry` 0.02, `␣with` 0.01, `␣instant` 0.00 |
| 56 | ? ← , yeast, salt… | `␣flour` | 0.545 | 1 | `␣flour` 0.55, `␣sugar` 0.32, `␣honey` 0.02, `␣soda` 0.02, `␣oil` 0.02 |
| 57 | ? ← flour, yeast,… | `␣the` | 0.438 | 1 | `␣the` 0.44, `,` 0.08, `␣mix` 0.07, `␣combine` 0.07, `␣together` 0.04 |
| 58 | ? ← the flour, yeast… | `␣mix` | 0.230 | 2 | `␣combine` 0.24, `␣mix` 0.23, `␣together` 0.22, `␣Combine` 0.09, `␣Mix` 0.06 |
| 59 | ? ← mix the flour,… | `,` | 0.832 | 1 | `,` 0.83, `␣to` 0.06, `␣simply` 0.02, `␣first` 0.02, `␣Simply` 0.01 |
| 60 | ? ← , mix the flour… | `First` | 0.012 | 10 | `␣Next` 0.35, `␣First` 0.13, `␣Then` 0.13, `Next` 0.05, `␣loaf` 0.05 |

---

## 6. moon_landing

*Category: temporal*

> **Beginning:** Apollo 11 launched from Kennedy Space Center on July 16, 1969.  
> **Middle:** Four days later, the lunar module Eagle separated from the command module and descended to the surface.  
> **Ending:** Neil Armstrong then became the first person to walk on the Moon.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | first person to walk on the Moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the Moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the Moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the Moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the Moon. ↵ | Neil Armstrong then became the first person to walk on the Moon. |
| sample | 10: Who Becomes The First Man To Walk On The Moon? ↵ Neil Armstrong was the only man walking on the moon. ↵ Neil Armstrong was the first man set foot on the moon by Neil Armstrong and Edwin Aldrin. ↵ Neil Armstrong is the only man walking on the moon. ↵ Neil Armstrong and Edwin Aldrin walked on the moon. ↵ Neil Armstrong and Edwin Aldrin became the first humans to land on the Moon. ↵ | Neil Armstrong then became the first person to walk on the Moon. |
| sample | the moon was also important in determining the success of the moon landing. ↵  ↵ After 26 hours, Neil Armstrong was able to see the results of the moon landing and returned to Earth. ↵  ↵ First moon landing ↵  ↵ Neil Armstrong successfully landed his rocket and became the first man to land on the moon. ↵  ↵ The crew regarded the landing as a failure and managed to make a soft landing on the surface of the moon. ↵  ↵ One of the crew died two months before the completion of the mission. ↵  ↵ | Neil Armstrong then became the first person to walk on the Moon. |
| sample | American astronaut Neil Armstrong, walking on the Moon. (NASA)NASA ↵  ↵ American astronaut Neil Armstrong, walking on the Moon. (NASA) ↵  ↵ NASA ↵  ↵ Neil Armstrong is walking on the Moon's surface. ↵  ↵ NASA ↵  ↵ Neil Armstrong was the first man to walk on the Moon ↵  ↵ On July 20, 1969, Neil Armstrong first walked on the surface of the Moon, but got lost in the process of walking on the surface of the Moon. ↵  ↵ | Neil Armstrong then became the first person to walk on the Moon. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | The mission was to land on the moon and return to Earth. The mission was a success, and the Apollo 11 spacecraft was launched on July 20, 1969. The mission was a success, and the Apollo 11 spacecraft was launched on July 20, 1969. The mission was a success, and the Apollo 11 spacecraft was launched on July 20, 1969. The mission was a success, and the Apollo 11 spacecraft was launched |
| sample | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | The mission was to test the capabilities of the launch vehicle, the Saturn V rocket, in the space station's launch window. The launch window is a predetermined point in space where the launch vehicle is to be lifted. The launch window's goal is to launch the vehicle at a point in space where, at that point, the vehicle will be the closest to the planet with the greatest chance of avoiding Earth's gravity, which is 9.8 m/s (26 ft/s). ↵ |
| sample | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | It was the first manned space flight, but because of a mechanical failure of the spacecraft, the United States refused to send astronauts into orbit by July 1970. The space agency was soon unable to provide enough spacecraft for the manned mission so that the Apollo 11 program ended in 1972. Apollo 11 left the Kennedy Space Center on July 17, 1969. ↵ U.S. astronauts John Glenn and Alan Shepard, as well as their |
| sample | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | It was the 11th manned mission launched by the Space Shuttle program. It was the first manned space flight by a commercial spaceflight operation. The flight was a joint effort between the United States and the United Kingdom. The mission was scheduled to take off from Kennedy Space Center in Florida and reach the White Sands Missile Range in New Mexico, on July 24, 1969 (this was the last flight of the program). It was designed to |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.524 | 57% |
| Backward | previous-token (right context) | 0.606 | 57% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Ap` | 0.000 | 799 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Ap → ? | `ollo` | 0.067 | 5 | `pearance` 0.10, `ache` 0.10, `ologies` 0.09, `pe` 0.09, `ollo` 0.07 |
| 3 | Apollo → ? | `␣` | 0.635 | 1 | `␣` 0.64, `'s` 0.01, `␣was` 0.01, `␣X` 0.01, `,` 0.01 |
| 4 | Apollo → ? | `11` | 0.217 | 1 | `11` 0.22, `13` 0.17, `12` 0.09, `17` 0.06, `10` 0.05 |
| 5 | Apollo 11 → ? | `␣launched` | 0.001 | 84 | `:` 0.09, `␣was` 0.06, `\n\n` 0.06, `\n` 0.04, `,` 0.03 |
| 6 | …ollo 11 launched → ? | `␣from` | 0.134 | 3 | `␣on` 0.21, `␣in` 0.15, `␣from` 0.13, `␣the` 0.07, `␣` 0.05 |
| 7 | …11 launched from → ? | `␣Kennedy` | 0.184 | 3 | `␣the` 0.28, `␣Cape` 0.22, `␣Kennedy` 0.18, `␣Florida` 0.07, `␣Launch` 0.02 |
| 8 | …11 launched from Kennedy → ? | `␣Space` | 0.963 | 1 | `␣Space` 0.96, `'s` 0.00, `␣space` 0.00, `\n` 0.00, `,` 0.00 |
| 9 | …launched from Kennedy Space → ? | `␣Center` | 0.975 | 1 | `␣Center` 0.97, `␣Centre` 0.02, `␣center` 0.00, `\n` 0.00, `␣and` 0.00 |
| 10 | …from Kennedy Space Center → ? | `␣on` | 0.330 | 2 | `␣in` 0.34, `␣on` 0.33, `,` 0.14, `␣(` 0.03, `␣at` 0.02 |
| 11 | …Kennedy Space Center on → ? | `␣July` | 0.075 | 4 | `␣` 0.21, `␣November` 0.10, `␣the` 0.09, `␣July` 0.07, `␣May` 0.06 |
| 12 | …Space Center on July → ? | `␣` | 0.998 | 1 | `␣` 1.00, `,` 0.00, `␣the` 0.00, `\n` 0.00, `.` 0.00 |
| 13 | …Center on July → ? | `16` | 0.208 | 1 | `16` 0.21, `20` 0.19, `17` 0.12, `24` 0.07, `14` 0.06 |
| 14 | …on July 16 → ? | `,` | 0.905 | 1 | `,` 0.90, `th` 0.02, `.` 0.02, `␣and` 0.01, `␣` 0.01 |
| 15 | …July 16, → ? | `␣` | 0.967 | 1 | `␣` 0.97, `␣and` 0.01, `␣the` 0.00, `␣marking` 0.00, `19` 0.00 |
| 16 | …16, → ? | `19` | 0.999 | 1 | `19` 1.00, `20` 0.00, `11` 0.00, `17` 0.00, `50` 0.00 |
| 17 | …16, 19 → ? | `69` | 0.888 | 1 | `69` 0.89, `71` 0.08, `70` 0.01, `68` 0.01, `97` 0.00 |
| 18 | …, 1969 → ? | `.` | 0.348 | 2 | `,` 0.47, `.` 0.35, `␣and` 0.03, `␣with` 0.03, `␣as` 0.02 |
| 19 | …1969. → ? | `␣Four` | 0.004 | 25 | `␣The` 0.27, `␣It` 0.25, `␣On` 0.04, `␣Its` 0.03, `␣This` 0.02 |
| 20 | …1969. Four → ? | `␣days` | 0.390 | 1 | `␣days` 0.39, `␣years` 0.16, `␣months` 0.11, `teen` 0.08, `␣weeks` 0.05 |
| 21 | …69. Four days → ? | `␣later` | 0.539 | 1 | `␣later` 0.54, `␣after` 0.24, `␣and` 0.07, `␣before` 0.04, `␣into` 0.04 |
| 22 | …. Four days later → ? | `,` | 0.762 | 1 | `,` 0.76, `␣the` 0.07, `␣it` 0.06, `␣Apollo` 0.02, `␣on` 0.01 |
| 23 | …Four days later, → ? | `␣the` | 0.290 | 1 | `␣the` 0.29, `␣it` 0.16, `␣on` 0.14, `␣Apollo` 0.05, `␣Neil` 0.03 |
| 24 | …days later, the → ? | `␣lunar` | 0.007 | 22 | `␣spacecraft` 0.12, `␣crew` 0.10, `␣first` 0.07, `␣Apollo` 0.07, `␣astronauts` 0.05 |
| 25 | …later, the lunar → ? | `␣module` | 0.572 | 1 | `␣module` 0.57, `␣land` 0.17, `␣probe` 0.07, `␣landing` 0.04, `␣orbit` 0.02 |
| 26 | …, the lunar module → ? | `␣Eagle` | 0.092 | 2 | `␣landed` 0.09, `␣Eagle` 0.09, `␣touched` 0.09, `␣was` 0.06, `,` 0.05 |
| 27 | …the lunar module Eagle → ? | `␣separated` | 0.006 | 26 | `␣landed` 0.35, `␣was` 0.09, `,` 0.04, `␣touched` 0.04, `␣returned` 0.03 |
| 28 | …lunar module Eagle separated → ? | `␣from` | 0.942 | 1 | `␣from` 0.94, `␣and` 0.01, `␣the` 0.01, `␣into` 0.00, `,` 0.00 |
| 29 | …module Eagle separated from → ? | `␣the` | 0.887 | 1 | `␣the` 0.89, `␣its` 0.05, `␣Apollo` 0.01, `␣Columbia` 0.01, `␣it` 0.01 |
| 30 | …Eagle separated from the → ? | `␣command` | 0.017 | 14 | `␣launch` 0.07, `␣rocket` 0.07, `␣booster` 0.06, `␣Apollo` 0.06, `␣module` 0.06 |
| 31 | …separated from the command → ? | `␣module` | 0.952 | 1 | `␣module` 0.95, `␣Module` 0.01, `␣and` 0.01, `␣capsule` 0.00, `␣center` 0.00 |
| 32 | …from the command module → ? | `␣and` | 0.109 | 2 | `␣Columbia` 0.30, `␣and` 0.11, `,` 0.10, `␣Atl` 0.03, `␣R` 0.03 |
| 33 | …the command module and → ? | `␣descended` | 0.047 | 2 | `␣landed` 0.17, `␣descended` 0.05, `␣touched` 0.04, `␣parach` 0.03, `␣re` 0.03 |
| 34 | …command module and descended → ? | `␣to` | 0.344 | 1 | `␣to` 0.34, `␣into` 0.21, `␣toward` 0.11, `␣towards` 0.05, `␣through` 0.03 |
| 35 | …module and descended to → ? | `␣the` | 0.696 | 1 | `␣the` 0.70, `␣a` 0.09, `␣Earth` 0.09, `␣` 0.02, `␣earth` 0.01 |
| 36 | …and descended to the → ? | `␣surface` | 0.235 | 2 | `␣Moon` 0.28, `␣surface` 0.24, `␣lunar` 0.21, `␣moon` 0.10, `␣south` 0.03 |
| 37 | …descended to the surface → ? | `.` | 0.244 | 2 | `␣of` 0.53, `.` 0.24, `,` 0.08, `.\n` 0.02, `␣at` 0.01 |
| 38 | …to the surface. → ? | `␣Neil` | 0.002 | 64 | `␣The` 0.26, `␣It` 0.07, `␣On` 0.05, `␣After` 0.04, `␣At` 0.03 |
| 39 | …the surface. Neil → ? | `␣Arm` | 0.976 | 1 | `␣Arm` 0.98, `␣A` 0.01, `␣de` 0.00, `␣H` 0.00, `␣and` 0.00 |
| 40 | …surface. Neil Arm → ? | `strong` | 1.000 | 1 | `strong` 1.00, `br` 0.00, `st` 0.00, `ist` 0.00, `field` 0.00 |
| 41 | …. Neil Armstrong → ? | `␣then` | 0.003 | 19 | `␣and` 0.33, `,` 0.23, `␣became` 0.10, `␣stepped` 0.04, `␣was` 0.03 |
| 42 | …Neil Armstrong then → ? | `␣became` | 0.162 | 2 | `␣stepped` 0.26, `␣became` 0.16, `␣walked` 0.09, `␣took` 0.06, `␣landed` 0.06 |
| 43 | …Armstrong then became → ? | `␣the` | 0.976 | 1 | `␣the` 0.98, `␣commander` 0.00, `␣one` 0.00, `␣a` 0.00, `␣first` 0.00 |
| 44 | …strong then became the → ? | `␣first` | 0.954 | 1 | `␣first` 0.95, `␣second` 0.01, `␣commander` 0.01, `␣` 0.00, `␣fourth` 0.00 |
| 45 | …then became the first → ? | `␣person` | 0.222 | 3 | `␣man` 0.41, `␣human` 0.30, `␣person` 0.22, `␣to` 0.02, `␣American` 0.02 |
| 46 | …became the first person → ? | `␣to` | 0.887 | 1 | `␣to` 0.89, `␣on` 0.05, `␣ever` 0.03, `␣in` 0.01, `,` 0.01 |
| 47 | …the first person to → ? | `␣walk` | 0.569 | 1 | `␣walk` 0.57, `␣step` 0.19, `␣set` 0.17, `␣land` 0.01, `␣stand` 0.01 |
| 48 | …first person to walk → ? | `␣on` | 0.984 | 1 | `␣on` 0.98, `␣the` 0.01, `,` 0.00, `␣onto` 0.00, `␣and` 0.00 |
| 49 | …person to walk on → ? | `␣the` | 0.970 | 1 | `␣the` 0.97, `␣another` 0.01, `␣a` 0.00, `␣an` 0.00, `␣to` 0.00 |
| 50 | …to walk on the → ? | `␣Moon` | 0.306 | 2 | `␣moon` 0.50, `␣Moon` 0.31, `␣surface` 0.14, `␣lunar` 0.05, `␣smooth` 0.00 |
| 51 | …walk on the Moon → ? | `.` | 0.365 | 1 | `.` 0.36, `,` 0.19, `.\n` 0.09, `␣and` 0.08, `'s` 0.07 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣Moon` | 0.000 | 5194 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← Moon. | `␣the` | 0.663 | 1 | `␣the` 0.66, `␣The` 0.04, `␣and` 0.03, `␣Full` 0.02, `␣full` 0.01 |
| 4 | ? ← the Moon. | `␣on` | 0.240 | 1 | `␣on` 0.24, `␣of` 0.22, `␣to` 0.15, `␣and` 0.10, `␣from` 0.05 |
| 5 | ? ← on the Moon. | `␣walk` | 0.023 | 3 | `␣landing` 0.04, `␣land` 0.03, `␣walk` 0.02, `␣man` 0.02, `␣life` 0.02 |
| 6 | ? ← walk on the Moon… | `␣to` | 0.635 | 1 | `␣to` 0.63, `␣and` 0.03, `␣will` 0.03, `␣first` 0.03, `␣can` 0.03 |
| 7 | ? ← to walk on the… | `␣person` | 0.074 | 3 | `␣man` 0.19, `␣humans` 0.12, `␣person` 0.07, `␣human` 0.07, `␣first` 0.06 |
| 8 | ? ← person to walk on… | `␣first` | 0.867 | 1 | `␣first` 0.87, `␣second` 0.02, `␣First` 0.02, `␣third` 0.01, `␣last` 0.01 |
| 9 | ? ← first person to walk… | `␣the` | 0.947 | 1 | `␣the` 0.95, `␣The` 0.04, `␣and` 0.00, `␣was` 0.00, `,` 0.00 |
| 10 | ? ← the first person to… | `␣became` | 0.229 | 2 | `␣was` 0.37, `␣became` 0.23, `,` 0.09, `␣and` 0.04, `␣become` 0.03 |
| 11 | ? ← became the first person… | `␣then` | 0.001 | 60 | `strong` 0.59, `rin` 0.09, `␣he` 0.05, `␣who` 0.04, `␣and` 0.03 |
| 12 | ? ← then became the first… | `strong` | 0.023 | 6 | `␣and` 0.51, `␣who` 0.10, `␣He` 0.10, `,` 0.07, `␣he` 0.04 |
| 13 | ? ← strong then became the… | `␣Arm` | 0.996 | 1 | `␣Arm` 1.00, `m` 0.00, `␣Head` 0.00, `\n` 0.00, `␣arm` 0.00 |
| 14 | ? ← Armstrong then became… | `␣Neil` | 0.479 | 1 | `␣Neil` 0.48, `.` 0.32, `,` 0.06, `␣and` 0.03, `).` 0.01 |
| 15 | ? ← Neil Armstrong then… | `.` | 0.610 | 1 | `.` 0.61, `,` 0.10, `␣and` 0.06, `␣astronaut` 0.03, `:` 0.02 |
| 16 | ? ← . Neil Armstrong… | `␣surface` | 0.067 | 1 | `␣surface` 0.07, `␣moon` 0.06, `␣Moon` 0.06, `␣Earth` 0.05, `␣landing` 0.04 |
| 17 | ? ← surface. Neil Arm… | `␣the` | 0.097 | 3 | `␣lunar` 0.53, `'s` 0.24, `␣the` 0.10, `␣its` 0.04, `’s` 0.02 |
| 18 | ? ← the surface. Neil… | `␣to` | 0.195 | 2 | `␣on` 0.42, `␣to` 0.19, `␣from` 0.08, `␣above` 0.04, `␣onto` 0.03 |
| 19 | ? ← to the surface.… | `␣descended` | 0.023 | 10 | `␣back` 0.25, `␣returned` 0.09, `␣return` 0.09, `␣it` 0.04, `␣him` 0.03 |
| 20 | ? ← descended to the surface… | `␣and` | 0.267 | 1 | `␣and` 0.27, `␣he` 0.13, `␣then` 0.06, `strong` 0.05, `␣they` 0.04 |
| 21 | ? ← and descended to the… | `␣module` | 0.018 | 7 | `,` 0.14, `␣descent` 0.02, `␣capsule` 0.02, `␣Earth` 0.02, `␣surface` 0.02 |
| 22 | ? ← module and descended to… | `␣command` | 0.255 | 2 | `␣lunar` 0.47, `␣command` 0.26, `␣service` 0.09, `␣the` 0.05, `␣crew` 0.03 |
| 23 | ? ← command module and descended… | `␣the` | 0.520 | 1 | `␣the` 0.52, `'s` 0.11, `␣lunar` 0.08, `␣his` 0.04, `␣its` 0.03 |
| 24 | ? ← the command module and… | `␣from` | 0.402 | 1 | `␣from` 0.40, `␣of` 0.09, `␣in` 0.07, `␣to` 0.05, `␣on` 0.03 |
| 25 | ? ← from the command module… | `␣separated` | 0.266 | 1 | `␣separated` 0.27, `␣away` 0.08, `ed` 0.06, `␣launched` 0.05, `␣released` 0.05 |
| 26 | ? ← separated from the command… | `␣Eagle` | 0.002 | 37 | `␣crew` 0.12, `␣he` 0.10, `␣successfully` 0.08, `strong` 0.05, `␣then` 0.05 |
| 27 | ? ← Eagle separated from the… | `␣module` | 0.346 | 1 | `␣module` 0.35, `,` 0.15, `␣the` 0.15, `␣Module` 0.12, `␣The` 0.02 |
| 28 | ? ← module Eagle separated from… | `␣lunar` | 0.202 | 2 | `␣command` 0.62, `␣lunar` 0.20, `␣service` 0.03, `␣the` 0.02, `␣landing` 0.02 |
| 29 | ? ← lunar module Eagle separated… | `␣the` | 0.827 | 1 | `␣the` 0.83, `␣The` 0.03, `11` 0.01, `'s` 0.01, `␣their` 0.01 |
| 30 | ? ← the lunar module Eagle… | `,` | 0.423 | 1 | `,` 0.42, `␣of` 0.13, `␣on` 0.05, `␣and` 0.05, `␣when` 0.04 |
| 31 | ? ← , the lunar module… | `␣later` | 0.079 | 1 | `␣later` 0.08, `␣landing` 0.07, `11` 0.06, `␣moon` 0.05, `␣Moon` 0.05 |
| 32 | ? ← later, the lunar… | `␣days` | 0.098 | 3 | `␣minutes` 0.37, `␣seconds` 0.13, `␣days` 0.10, `␣hours` 0.10, `␣hour` 0.06 |
| 33 | ? ← days later, the… | `␣Four` | 0.062 | 3 | `␣Two` 0.13, `␣Three` 0.13, `␣Four` 0.06, `␣few` 0.05, `␣Five` 0.05 |
| 34 | ? ← Four days later,… | `.` | 0.945 | 1 | `.` 0.95, `).` 0.01, `."` 0.01, `:` 0.00, `␣…` 0.00 |
| 35 | ? ← . Four days later… | `69` | 0.012 | 11 | `␣Moon` 0.11, `␣surface` 0.10, `␣moon` 0.06, `␣module` 0.05, `␣Earth` 0.04 |
| 36 | ? ← 69. Four days… | `19` | 0.994 | 1 | `19` 0.99, `␣` 0.00, `-` 0.00, `␣'` 0.00, `.` 0.00 |
| 37 | ? ← 1969. Four… | `␣` | 0.983 | 1 | `␣` 0.98, `,` 0.01, `␣July` 0.00, `-` 0.00, `.` 0.00 |
| 38 | ? ← 1969.… | `,` | 0.748 | 1 | `,` 0.75, `␣July` 0.10, `␣in` 0.05, `20` 0.01, `␣June` 0.01 |
| 39 | ? ← , 1969… | `16` | 0.084 | 2 | `20` 0.47, `16` 0.08, `21` 0.08, `19` 0.05, `14` 0.04 |
| 40 | ? ← 16, 19… | `␣` | 0.997 | 1 | `␣` 1.00, `20` 0.00, `-` 0.00, `–` 0.00, `.` 0.00 |
| 41 | ? ← 16,… | `␣July` | 0.937 | 1 | `␣July` 0.94, `.` 0.02, `July` 0.01, `␣November` 0.00, `␣August` 0.00 |
| 42 | ? ← July 16,… | `␣on` | 0.859 | 1 | `␣on` 0.86, `,` 0.06, `␣of` 0.02, `␣Moon` 0.01, `␣was` 0.01 |
| 43 | ? ← on July 16… | `␣Center` | 0.000 | 137 | `␣Moon` 0.26, `␣surface` 0.16, `␣moon` 0.12, `␣landing` 0.06, `,` 0.05 |
| 44 | ? ← Center on July… | `␣Space` | 0.776 | 1 | `␣Space` 0.78, `␣Research` 0.06, `␣Control` 0.04, `␣Trade` 0.03, `ar` 0.02 |
| 45 | ? ← Space Center on July… | `␣Kennedy` | 0.791 | 1 | `␣Kennedy` 0.79, `␣Johnson` 0.17, `nedy` 0.01, `ennis` 0.01, `ard` 0.00 |
| 46 | ? ← Kennedy Space Center on… | `␣from` | 0.098 | 5 | `␣the` 0.30, `'s` 0.23, `␣at` 0.17, `’s` 0.14, `␣from` 0.10 |
| 47 | ? ← from Kennedy Space Center… | `␣launched` | 0.206 | 2 | `␣off` 0.41, `␣launched` 0.21, `␣rocket` 0.03, `␣launch` 0.03, `ed` 0.03 |
| 48 | ? ← launched from Kennedy Space… | `11` | 0.020 | 5 | `␣was` 0.54, `␣successfully` 0.10, `␣Eagle` 0.06, `,` 0.05, `11` 0.02 |
| 49 | ? ← 11 launched from Kennedy… | `␣` | 0.988 | 1 | `␣` 0.99, `-` 0.01, `10` 0.00, `11` 0.00, `.` 0.00 |
| 50 | ? ← 11 launched from… | `ollo` | 0.152 | 2 | `␣Apollo` 0.78, `ollo` 0.15, `anger` 0.02, `is` 0.01, `er` 0.01 |
| 51 | ? ← ollo 11 launched… | `Ap` | 0.986 | 1 | `Ap` 0.99, `p` 0.01, `R` 0.00, `App` 0.00, `ri` 0.00 |

---

## 7. socrates

*Category: logical*

> **Beginning:** All men are mortal.  
> **Middle:** Socrates is a man.  
> **Ending:** Therefore, Socrates is mortal.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ | Therefore, Socrates is mortal. |
| sample | Socrates is mortal. ↵ Socrates is a man. ↵ Every man is mortal. ↵ Socrates is a man. ↵ Socrates is mortal. ↵ Every man is mortal. ↵ Therefore, Socrates is a man. ↵ Consider an example of the sentence: ↵ Every man is mortal. ↵ Socrates is a man. ↵ Socrates is mortal. ↵ Socrates is a man. ↵ Therefore, Socrates is mortal. ↵ Every man is mortal. ↵ | Therefore, Socrates is mortal. |
| sample | If Socrates is mortal but another person is not, then Socrates is mortal but another person, like Socrates, is not. ↵ Therefore, given that Socrates is mortal, we can say that a person(s) is mortal of Socrates. ↵ The rule for determining what is mortal of Socrates is: ↵ and the rule for determining whether or not Socrates is mortal is: ↵ If Socrates is mortal, then Socrates is mortal ↵ | Therefore, Socrates is mortal. |
| sample | mortals. ↵ It is possible for Socrates to be a mortal person. Therefore, Socrates is mortal ↵ Socrates is a mortal person. Therefore, Socrates is mortal ↵ Therefore, it is possible for Socrates to be a mortal person. Therefore, Socrates is mortal ↵ Socrates is a mortal person. Therefore, it is possible for Socrates to be a mortal person. Therefore, Socrates is mortal ↵ | Therefore, Socrates is mortal. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | All men are mortal. | All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. All men are mortal. |
| sample | All men are mortal. | All men are mortified. This is the rule of the world. Man and man alone are mortal. Man alone is mortal. All mortal men are mortified. This is the rule of God. Man and man alone are mortified. Man alone is mortified. Man alone is mortified. Man alone is mortified. Man alone is mortified. Man alone is mortified. Man alone is mortified. Man alone is mortified. Man alone is |
| sample | All men are mortal. | We live in a mortal world, and the idea of death is terrifying for all. In fact, we are not mortal. Death may seem intimidating, but it is the ultimate end of life. In the human body, there is never, ever a "dead zone" the size of the world. The cells, the tissues that hold organs together, the brain, and the cells that make up the blood, the lymph and the flesh, all live in a very |
| sample | All men are mortal. | The only good thing about humans is that they make good men ↵ and women. (A good man is a good man, and a good woman is a good woman. There is ↵ no universal morality, but that is not the main point.) ↵ In other words, a man is a human being capable of producing and using things like his ↵ own. A woman is a human being capable of producing and using things as she sees fit. ↵ We do not do this. We cannot do |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.758 | 70% |
| Backward | previous-token (right context) | 0.671 | 60% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `All` | 0.002 | 74 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | All → ? | `␣men` | 0.001 | 85 | `␣About` 0.10, `␣of` 0.08, `␣the` 0.07, `␣about` 0.05, `␣posts` 0.02 |
| 3 | All men → ? | `␣are` | 0.191 | 1 | `␣are` 0.19, `,` 0.08, `␣have` 0.07, `␣and` 0.07, `␣of` 0.05 |
| 4 | All men are → ? | `␣mort` | 0.031 | 4 | `␣born` 0.31, `␣created` 0.10, `␣equal` 0.04, `␣mort` 0.03, `␣descended` 0.03 |
| 5 | All men are mort → ? | `al` | 0.962 | 1 | `al` 0.96, `ally` 0.01, `als` 0.01, `ified` 0.01, `g` 0.00 |
| 6 | …men are mortal → ? | `.` | 0.174 | 2 | `,` 0.39, `.` 0.17, `␣and` 0.05, `;` 0.04, `␣men` 0.03 |
| 7 | …are mortal. → ? | `␣Soc` | 0.011 | 19 | `␣All` 0.14, `␣But` 0.05, `␣The` 0.05, `␣Men` 0.04, `␣They` 0.04 |
| 8 | …mortal. Soc → ? | `rates` | 0.929 | 1 | `rates` 0.93, `io` 0.03, `cer` 0.01, `.` 0.01, `rate` 0.00 |
| 9 | …al. Socrates → ? | `␣is` | 0.173 | 1 | `␣is` 0.17, `,` 0.15, `␣was` 0.11, `\n` 0.06, `␣said` 0.05 |
| 10 | …. Socrates is → ? | `␣a` | 0.346 | 1 | `␣a` 0.35, `␣mort` 0.16, `␣not` 0.08, `␣dead` 0.05, `␣the` 0.04 |
| 11 | …Socrates is a → ? | `␣man` | 0.649 | 1 | `␣man` 0.65, `␣mort` 0.10, `␣human` 0.02, `␣philosopher` 0.01, `␣dead` 0.01 |
| 12 | …rates is a man → ? | `.` | 0.405 | 1 | `.` 0.41, `,` 0.18, `␣of` 0.10, `␣who` 0.05, `␣and` 0.04 |
| 13 | …is a man. → ? | `␣Therefore` | 0.024 | 6 | `␣Soc` 0.12, `␣All` 0.05, `␣The` 0.05, `␣He` 0.04, `␣Men` 0.04 |
| 14 | …a man. Therefore → ? | `,` | 0.576 | 1 | `,` 0.58, `␣Soc` 0.13, `␣all` 0.04, `␣he` 0.04, `␣men` 0.04 |
| 15 | …man. Therefore, → ? | `␣Soc` | 0.252 | 1 | `␣Soc` 0.25, `␣all` 0.13, `␣he` 0.10, `␣men` 0.08, `␣the` 0.04 |
| 16 | …. Therefore, Soc → ? | `rates` | 0.998 | 1 | `rates` 1.00, `rate` 0.00, `.` 0.00, `ates` 0.00, `rat` 0.00 |
| 17 | …Therefore, Socrates → ? | `␣is` | 0.631 | 1 | `␣is` 0.63, `␣must` 0.07, `␣has` 0.03, `␣was` 0.02, `␣cannot` 0.02 |
| 18 | …, Socrates is → ? | `␣mort` | 0.438 | 1 | `␣mort` 0.44, `␣a` 0.24, `␣also` 0.05, `␣not` 0.03, `␣Soc` 0.02 |
| 19 | …Socrates is mort → ? | `al` | 0.998 | 1 | `al` 1.00, `ified` 0.00, `ally` 0.00, `.` 0.00, `alan` 0.00 |
| 20 | …rates is mortal → ? | `.` | 0.532 | 1 | `.` 0.53, `.\n` 0.19, `.\n\n` 0.08, `,` 0.06, `␣as` 0.02 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `al` | 0.000 | 683 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← al. | `␣mort` | 0.004 | 58 | `␣Port` 0.05, `␣arous` 0.03, `and` 0.03, `␣immort` 0.02, `␣pedest` 0.02 |
| 4 | ? ← mortal. | `␣is` | 0.158 | 1 | `␣is` 0.16, `␣are` 0.09, `␣a` 0.09, `␣mere` 0.08, `␣be` 0.06 |
| 5 | ? ← is mortal. | `rates` | 0.128 | 1 | `rates` 0.13, `␣he` 0.11, `␣man` 0.04, `␣it` 0.04, `␣X` 0.03 |
| 6 | ? ← rates is mortal… | `␣Soc` | 0.930 | 1 | `␣Soc` 0.93, `oc` 0.06, `␣soc` 0.00, `c` 0.00, `␣C` 0.00 |
| 7 | ? ← Socrates is mort… | `,` | 0.226 | 2 | `:` 0.24, `␣that` 0.23, `,` 0.23, `.` 0.04, `␣and` 0.03 |
| 8 | ? ← , Socrates is… | `␣Therefore` | 0.096 | 3 | `␣Yes` 0.41, `␣No` 0.16, `␣Therefore` 0.10, `al` 0.02, `␣therefore` 0.02 |
| 9 | ? ← Therefore, Socrates… | `.` | 0.722 | 1 | `.` 0.72, `:` 0.15, `).` 0.03, `)` 0.02, `al` 0.02 |
| 10 | ? ← . Therefore, Soc… | `␣man` | 0.125 | 2 | `al` 0.48, `␣man` 0.12, `␣human` 0.06, `rates` 0.03, `␣men` 0.02 |
| 11 | ? ← man. Therefore,… | `␣a` | 0.654 | 1 | `␣a` 0.65, `al` 0.22, `␣of` 0.01, `␣dead` 0.01, `␣is` 0.01 |
| 12 | ? ← a man. Therefore… | `␣is` | 0.615 | 1 | `␣is` 0.61, `␣not` 0.12, `␣be` 0.03, `␣am` 0.03, `␣also` 0.02 |
| 13 | ? ← is a man.… | `rates` | 0.537 | 1 | `rates` 0.54, `␣he` 0.10, `al` 0.05, `␣He` 0.04, `␣man` 0.04 |
| 14 | ? ← rates is a man… | `␣Soc` | 0.980 | 1 | `␣Soc` 0.98, `oc` 0.02, `␣C` 0.00, `␣soc` 0.00, `c` 0.00 |
| 15 | ? ← Socrates is a… | `.` | 0.200 | 2 | `,` 0.25, `.` 0.20, `␣that` 0.12, `␣and` 0.09, `:` 0.06 |
| 16 | ? ← . Socrates is… | `al` | 0.335 | 1 | `al` 0.34, `␣man` 0.24, `rates` 0.05, `␣human` 0.03, `␣men` 0.03 |
| 17 | ? ← al. Socrates… | `␣mort` | 0.937 | 1 | `␣mort` 0.94, `␣immort` 0.06, `␣Mort` 0.00, `ort` 0.00, `␣corpor` 0.00 |
| 18 | ? ← mortal. Soc… | `␣are` | 0.338 | 2 | `␣is` 0.45, `␣are` 0.34, `␣not` 0.07, `␣be` 0.04, `␣also` 0.01 |
| 19 | ? ← are mortal.… | `␣men` | 0.605 | 1 | `␣men` 0.60, `rates` 0.08, `␣humans` 0.07, `␣Men` 0.04, `␣people` 0.02 |
| 20 | ? ← men are mortal… | `All` | 0.204 | 3 | `␣All` 0.48, `␣all` 0.22, `All` 0.20, `␣and` 0.01, `,` 0.01 |

---

## 8. even_numbers

*Category: logical*

> **Beginning:** An even number is any integer that can be divided by two without a remainder.  
> **Middle:** If we add two even numbers, each can be written as two times some integer, so their sum is two times the sum of those integers.  
> **Ending:** This proves that the sum of two even numbers is always even.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | the sum of two even numbers, the sum is even. ↵ So, when an odd number is added to the sum of two even numbers, the sum is even. ↵ So, when an odd number is added to the sum of two even numbers, the sum is even. ↵ So, when an odd number is added to the sum of two even numbers, the sum is even. ↵ So, when an odd number is added to the sum of two even numbers, the sum is even. ↵ | This proves that the sum of two even numbers is always even. |
| sample | Given the sum of three even numbers 2, 3, 9 and 11, their sum is 11. Thus, their sum is even. ↵ Given the sum of three even numbers 2, 4, 6 and 8, their sum is 8. Thus, their sum is even. ↵ Given the sum of three odd numbers 1, 4, 5 and 11, their sum is 10. Thus, their sum is even. ↵ | This proves that the sum of two even numbers is always even. |
| sample | Below is the formula of the sum of a product ↵ If the first term of the product is even, then the sum is an odd number. ↵ If the first term of the product is even, then the sum is even. ↵ It is only when the second term of the product is even, the sum is even. ↵ For example: ↵ 1 is an even number ↵ 2 is an even number ↵ 3 is an odd number whose only term is 1 ↵ 2 is an even number ↵ | This proves that the sum of two even numbers is always even. |
| sample | , so the number 7 is not even. ↵ The square of the '2 × 2 × 2' tells us that an odd number is greater than an even number. The square of '2 × 2 × 2' tells us that an odd number is greater than an even number. ↵ For example, '2 × 2 × 2' is used to find the sum of two even numbers. 2 × 2 × 2 × 2 ↵ | This proves that the sum of two even numbers is always even. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | An even number is any integer that can be divided by two without a remainder. | For example, 2 is an even number because it can be divided by two without a remainder. An odd number is any integer that can be divided by three without a remainder. For example, 3 is an odd number because it can be divided by three without a remainder. An even number is any integer that can be divided by two without a remainder. An odd number is any integer that can be divided by three without a remainder. An even number is any integer that can |
| sample | An even number is any integer that can be divided by two without a remainder. | For example, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13. It is also a pair with a remainder. The remainder of a division by an even number is a remainder of the division by the even number. For example, 1 divided by 5 is 5 remainder. A remainder of 1 is still a remainder of |
| sample | An even number is any integer that can be divided by two without a remainder. | The natural number 1 is even; 4 is odd, 2 is even and 5 is odd. The quotient of 1 and 2 is 2, which is even. The sum of 2 and 5 is 15, which is even. ↵ The reason that 2 is odd is that 2 is not divisible by 3. This means that it is not possible to make a number smaller than 2 divisible by 3. |
| sample | An even number is any integer that can be divided by two without a remainder. | The remainder of the division is the quotient which is the fractional part of the division. The remainder of division by an even number is 2, 4, 6 and 8 or 2, 4, 6, 8, 8 and 8 respectively. (4, 6, 8, 8, 8, 8, 8, 8 etc.) ↵ As per the algorithm below, we will use the integer |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.711 | 43% |
| Backward | previous-token (right context) | 0.678 | 55% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `An` | 0.004 | 33 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | An → ? | `␣even` | 0.001 | 189 | `alysis` 0.05, `atomy` 0.03, `␣Introduction` 0.03, `xiety` 0.02, `␣analysis` 0.02 |
| 3 | An even → ? | `␣number` | 0.008 | 14 | `␣more` 0.30, `␣better` 0.12, `␣bigger` 0.08, `␣greater` 0.05, `␣larger` 0.03 |
| 4 | An even number → ? | `␣is` | 0.086 | 2 | `␣of` 0.74, `␣is` 0.09, `,` 0.01, `␣has` 0.01, `␣(` 0.01 |
| 5 | An even number is → ? | `␣any` | 0.017 | 9 | `␣a` 0.30, `␣the` 0.07, `␣an` 0.06, `␣called` 0.06, `␣one` 0.06 |
| 6 | …even number is any → ? | `␣integer` | 0.042 | 3 | `␣number` 0.66, `␣positive` 0.07, `␣integer` 0.04, `␣whole` 0.03, `␣even` 0.02 |
| 7 | …number is any integer → ? | `␣that` | 0.271 | 1 | `␣that` 0.27, `␣greater` 0.19, `␣less` 0.07, `␣between` 0.06, `␣which` 0.05 |
| 8 | …is any integer that → ? | `␣can` | 0.124 | 2 | `␣is` 0.49, `␣can` 0.12, `␣has` 0.11, `␣divides` 0.04, `␣does` 0.02 |
| 9 | …any integer that can → ? | `␣be` | 0.924 | 1 | `␣be` 0.92, `␣take` 0.01, `␣appear` 0.01, `␣not` 0.01, `␣have` 0.01 |
| 10 | …integer that can be → ? | `␣divided` | 0.163 | 2 | `␣written` 0.32, `␣divided` 0.16, `␣expressed` 0.15, `␣represented` 0.11, `␣div` 0.02 |
| 11 | …that can be divided → ? | `␣by` | 0.587 | 1 | `␣by` 0.59, `␣into` 0.21, `␣evenly` 0.11, `␣equally` 0.01, `␣up` 0.01 |
| 12 | …can be divided by → ? | `␣two` | 0.184 | 3 | `␣itself` 0.33, `␣` 0.30, `␣two` 0.18, `␣a` 0.03, `␣the` 0.03 |
| 13 | …be divided by two → ? | `␣without` | 0.141 | 2 | `.` 0.22, `␣without` 0.14, `,` 0.11, `␣(` 0.06, `␣or` 0.06 |
| 14 | …divided by two without → ? | `␣a` | 0.111 | 2 | `␣leaving` 0.14, `␣a` 0.11, `␣remainder` 0.10, `␣the` 0.08, `␣giving` 0.06 |
| 15 | …by two without a → ? | `␣remainder` | 0.739 | 1 | `␣remainder` 0.74, `␣factor` 0.03, `␣div` 0.03, `␣loss` 0.02, `␣fraction` 0.02 |
| 16 | …two without a remainder → ? | `.` | 0.457 | 1 | `.` 0.46, `␣of` 0.17, `,` 0.12, `.\n` 0.05, `␣when` 0.03 |
| 17 | …without a remainder. → ? | `␣If` | 0.031 | 8 | `␣For` 0.14, `␣The` 0.12, `␣An` 0.07, `␣This` 0.05, `␣In` 0.05 |
| 18 | …a remainder. If → ? | `␣we` | 0.081 | 4 | `␣you` 0.25, `␣the` 0.16, `␣a` 0.14, `␣we` 0.08, `␣there` 0.05 |
| 19 | …remainder. If we → ? | `␣add` | 0.012 | 14 | `␣divide` 0.29, `␣have` 0.13, `␣want` 0.05, `␣take` 0.04, `␣divided` 0.03 |
| 20 | …. If we add → ? | `␣two` | 0.250 | 1 | `␣two` 0.25, `␣` 0.24, `␣a` 0.08, `␣up` 0.08, `␣the` 0.08 |
| 21 | …If we add two → ? | `␣even` | 0.118 | 3 | `␣integers` 0.25, `␣numbers` 0.15, `␣even` 0.12, `␣` 0.10, `␣odd` 0.06 |
| 22 | …we add two even → ? | `␣numbers` | 0.622 | 1 | `␣numbers` 0.62, `␣integers` 0.35, `␣integer` 0.01, `␣whole` 0.00, `␣` 0.00 |
| 23 | …add two even numbers → ? | `,` | 0.411 | 1 | `,` 0.41, `␣together` 0.38, `␣and` 0.03, `␣to` 0.03, `␣(` 0.03 |
| 24 | …two even numbers, → ? | `␣each` | 0.015 | 8 | `␣we` 0.45, `␣the` 0.18, `␣then` 0.10, `␣they` 0.04, `␣it` 0.02 |
| 25 | …even numbers, each → ? | `␣can` | 0.018 | 10 | `␣of` 0.16, `␣is` 0.10, `␣with` 0.09, `␣number` 0.07, `␣will` 0.07 |
| 26 | …numbers, each can → ? | `␣be` | 0.909 | 1 | `␣be` 0.91, `␣divide` 0.01, `␣have` 0.01, `␣remain` 0.01, `␣only` 0.01 |
| 27 | …, each can be → ? | `␣written` | 0.150 | 2 | `␣divided` 0.66, `␣written` 0.15, `␣represented` 0.03, `␣expressed` 0.02, `␣added` 0.01 |
| 28 | …each can be written → ? | `␣as` | 0.851 | 1 | `␣as` 0.85, `␣in` 0.06, `␣with` 0.02, `␣using` 0.01, `␣out` 0.01 |
| 29 | …can be written as → ? | `␣two` | 0.081 | 4 | `␣a` 0.32, `␣` 0.19, `␣an` 0.13, `␣two` 0.08, `␣the` 0.06 |
| 30 | …be written as two → ? | `␣times` | 0.016 | 15 | `␣even` 0.20, `␣numbers` 0.06, `␣odd` 0.05, `␣divided` 0.05, `␣` 0.03 |
| 31 | …written as two times → ? | `␣some` | 0.000 | 85 | `␣the` 0.47, `␣two` 0.21, `␣a` 0.08, `␣` 0.03, `␣as` 0.03 |
| 32 | …as two times some → ? | `␣integer` | 0.112 | 3 | `␣number` 0.24, `␣other` 0.14, `␣integer` 0.11, `␣even` 0.08, `␣odd` 0.04 |
| 33 | …two times some integer → ? | `,` | 0.231 | 2 | `.` 0.30, `,` 0.23, `␣greater` 0.04, `␣(` 0.03, `␣that` 0.03 |
| 34 | …times some integer, → ? | `␣so` | 0.047 | 5 | `␣and` 0.15, `␣such` 0.07, `␣which` 0.07, `␣e` 0.05, `␣or` 0.05 |
| 35 | …some integer, so → ? | `␣their` | 0.001 | 61 | `␣the` 0.18, `␣that` 0.14, `␣we` 0.14, `␣` 0.06, `␣an` 0.05 |
| 36 | …integer, so their → ? | `␣sum` | 0.406 | 1 | `␣sum` 0.41, `␣remainder` 0.11, `␣product` 0.09, `␣quot` 0.09, `␣remain` 0.02 |
| 37 | …, so their sum → ? | `␣is` | 0.534 | 1 | `␣is` 0.53, `␣can` 0.12, `␣will` 0.10, `␣equals` 0.06, `␣becomes` 0.03 |
| 38 | …so their sum is → ? | `␣two` | 0.133 | 1 | `␣two` 0.13, `␣` 0.12, `␣an` 0.11, `␣the` 0.10, `␣equal` 0.08 |
| 39 | …their sum is two → ? | `␣times` | 0.304 | 2 | `.` 0.37, `␣times` 0.30, `,` 0.06, `.\n` 0.03, `␣divided` 0.03 |
| 40 | …sum is two times → ? | `␣the` | 0.360 | 1 | `␣the` 0.36, `␣two` 0.14, `␣` 0.14, `␣some` 0.06, `␣(` 0.04 |
| 41 | …is two times the → ? | `␣sum` | 0.144 | 2 | `␣integer` 0.25, `␣sum` 0.14, `␣number` 0.12, `␣remainder` 0.05, `␣original` 0.05 |
| 42 | …two times the sum → ? | `␣of` | 0.982 | 1 | `␣of` 0.98, `.` 0.00, `,` 0.00, `␣(` 0.00, `.\n` 0.00 |
| 43 | …times the sum of → ? | `␣those` | 0.015 | 6 | `␣the` 0.68, `␣their` 0.11, `␣each` 0.06, `␣two` 0.04, `␣all` 0.03 |
| 44 | …the sum of those → ? | `␣integers` | 0.046 | 3 | `␣two` 0.79, `␣numbers` 0.08, `␣integers` 0.05, `␣even` 0.01, `␣of` 0.01 |
| 45 | …sum of those integers → ? | `.` | 0.597 | 1 | `.` 0.60, `.\n` 0.10, `,` 0.07, `.\n\n` 0.05, `␣divided` 0.02 |
| 46 | …of those integers. → ? | `␣This` | 0.056 | 4 | `␣The` 0.14, `␣For` 0.13, `␣If` 0.09, `␣This` 0.06, `␣In` 0.04 |
| 47 | …those integers. This → ? | `␣proves` | 0.000 | 226 | `␣is` 0.38, `␣means` 0.09, `␣can` 0.03, `␣number` 0.03, `␣sum` 0.03 |
| 48 | …integers. This proves → ? | `␣that` | 0.733 | 1 | `␣that` 0.73, `␣the` 0.13, `,` 0.01, `␣to` 0.01, `␣our` 0.01 |
| 49 | …. This proves that → ? | `␣the` | 0.233 | 1 | `␣the` 0.23, `␣even` 0.10, `␣two` 0.07, `␣there` 0.06, `␣each` 0.04 |
| 50 | …This proves that the → ? | `␣sum` | 0.393 | 1 | `␣sum` 0.39, `␣number` 0.10, `␣even` 0.06, `␣two` 0.04, `␣integers` 0.03 |
| 51 | …proves that the sum → ? | `␣of` | 0.887 | 1 | `␣of` 0.89, `␣is` 0.07, `␣must` 0.01, `␣and` 0.01, `␣(` 0.00 |
| 52 | …that the sum of → ? | `␣two` | 0.394 | 1 | `␣two` 0.39, `␣the` 0.22, `␣any` 0.08, `␣even` 0.06, `␣all` 0.06 |
| 53 | …the sum of two → ? | `␣even` | 0.673 | 1 | `␣even` 0.67, `␣odd` 0.11, `␣integers` 0.05, `␣numbers` 0.04, `␣positive` 0.01 |
| 54 | …sum of two even → ? | `␣numbers` | 0.783 | 1 | `␣numbers` 0.78, `␣integers` 0.19, `␣prim` 0.00, `␣is` 0.00, `␣integer` 0.00 |
| 55 | …of two even numbers → ? | `␣is` | 0.740 | 1 | `␣is` 0.74, `␣can` 0.06, `␣equals` 0.04, `␣must` 0.03, `,` 0.02 |
| 56 | …two even numbers is → ? | `␣always` | 0.133 | 2 | `␣two` 0.17, `␣always` 0.13, `␣equal` 0.13, `␣` 0.10, `␣the` 0.08 |
| 57 | …even numbers is always → ? | `␣even` | 0.154 | 2 | `␣two` 0.19, `␣even` 0.15, `␣an` 0.12, `␣odd` 0.11, `␣a` 0.10 |
| 58 | …numbers is always even → ? | `.` | 0.348 | 1 | `.` 0.35, `,` 0.20, `.\n` 0.18, `.\n\n` 0.11, `␣(` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣even` | 0.000 | 4385 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← even. | `␣always` | 0.001 | 56 | `␣and` 0.08, `,` 0.08, `␣is` 0.05, `␣break` 0.05, `␣or` 0.03 |
| 4 | ? ← always even. | `␣is` | 0.346 | 1 | `␣is` 0.35, `␣not` 0.32, `␣are` 0.13, `'t` 0.05, `␣be` 0.03 |
| 5 | ? ← is always even. | `␣numbers` | 0.008 | 13 | `␣it` 0.07, `␣which` 0.03, `␣It` 0.03, `␣number` 0.03, `␣that` 0.02 |
| 6 | ? ← numbers is always even… | `␣even` | 0.186 | 1 | `␣even` 0.19, `␣two` 0.12, `␣odd` 0.09, `␣of` 0.07, `␣natural` 0.06 |
| 7 | ? ← even numbers is always… | `␣two` | 0.226 | 2 | `␣of` 0.42, `␣two` 0.23, `␣and` 0.07, `␣consecutive` 0.04, `␣all` 0.04 |
| 8 | ? ← two even numbers is… | `␣of` | 0.831 | 1 | `␣of` 0.83, `␣adding` 0.04, `␣multiplying` 0.03, `␣between` 0.03, `␣any` 0.02 |
| 9 | ? ← of two even numbers… | `␣sum` | 0.355 | 2 | `␣product` 0.38, `␣sum` 0.35, `␣modulus` 0.03, `CM` 0.03, `␣squares` 0.02 |
| 10 | ? ← sum of two even… | `␣the` | 0.629 | 1 | `␣the` 0.63, `␣The` 0.29, `The` 0.01, `␣a` 0.01, `␣that` 0.01 |
| 11 | ? ← the sum of two… | `␣that` | 0.352 | 1 | `␣that` 0.35, `,` 0.19, `␣and` 0.09, `␣of` 0.06, `␣if` 0.03 |
| 12 | ? ← that the sum of… | `␣proves` | 0.003 | 40 | `␣states` 0.19, `␣prove` 0.08, `␣fact` 0.06, `␣such` 0.05, `␣show` 0.04 |
| 13 | ? ← proves that the sum… | `␣This` | 0.055 | 4 | `␣It` 0.12, `␣which` 0.11, `␣that` 0.07, `␣This` 0.05, `␣theorem` 0.05 |
| 14 | ? ← This proves that the… | `.` | 0.779 | 1 | `.` 0.78, `:` 0.05, `).` 0.04, `␣.` 0.02, `!` 0.01 |
| 15 | ? ← . This proves that… | `␣integers` | 0.008 | 18 | `␣even` 0.11, `0` 0.06, `␣numbers` 0.05, `2` 0.05, `␣odd` 0.05 |
| 16 | ? ← integers. This proves… | `␣those` | 0.001 | 35 | `␣even` 0.23, `␣positive` 0.16, `␣are` 0.12, `␣two` 0.09, `␣odd` 0.07 |
| 17 | ? ← those integers. This… | `␣of` | 0.652 | 1 | `␣of` 0.65, `␣all` 0.04, `␣for` 0.03, `␣to` 0.03, `␣on` 0.02 |
| 18 | ? ← of those integers.… | `␣sum` | 0.482 | 1 | `␣sum` 0.48, `␣product` 0.10, `␣one` 0.02, `␣products` 0.02, `␣squares` 0.02 |
| 19 | ? ← sum of those integers… | `␣the` | 0.916 | 1 | `␣the` 0.92, `␣a` 0.02, `␣total` 0.01, `␣positive` 0.00, `␣infinite` 0.00 |
| 20 | ? ← the sum of those… | `␣times` | 0.016 | 12 | `␣is` 0.20, `␣to` 0.12, `␣than` 0.10, `␣as` 0.07, `␣of` 0.05 |
| 21 | ? ← times the sum of… | `␣two` | 0.097 | 1 | `␣two` 0.10, `␣integers` 0.07, `␣integer` 0.06, `2` 0.06, `␣three` 0.05 |
| 22 | ? ← two times the sum… | `␣is` | 0.265 | 1 | `␣is` 0.27, `␣to` 0.21, `␣than` 0.06, `␣exactly` 0.06, `␣be` 0.06 |
| 23 | ? ← is two times the… | `␣sum` | 0.014 | 6 | `␣integers` 0.45, `␣numbers` 0.19, `␣integer` 0.09, `␣number` 0.04, `␣that` 0.02 |
| 24 | ? ← sum is two times… | `␣their` | 0.315 | 1 | `␣their` 0.31, `␣the` 0.29, `␣whose` 0.15, `␣Their` 0.05, `␣its` 0.03 |
| 25 | ? ← their sum is two… | `␣so` | 0.037 | 5 | `,` 0.38, `␣that` 0.16, `␣then` 0.12, `␣and` 0.12, `␣so` 0.04 |
| 26 | ? ← so their sum is… | `,` | 0.717 | 1 | `,` 0.72, `␣and` 0.10, `␣integers` 0.05, `␣even` 0.02, `␣numbers` 0.02 |
| 27 | ? ← , so their sum… | `␣integer` | 0.058 | 4 | `␣integers` 0.27, `␣numbers` 0.11, `␣even` 0.08, `␣integer` 0.06, `␣number` 0.04 |
| 28 | ? ← integer, so their… | `␣some` | 0.004 | 22 | `␣an` 0.34, `␣even` 0.14, `␣positive` 0.12, `␣odd` 0.06, `␣one` 0.04 |
| 29 | ? ← some integer, so… | `␣times` | 0.027 | 7 | `␣to` 0.19, `␣for` 0.14, `␣is` 0.13, `␣by` 0.11, `␣of` 0.09 |
| 30 | ? ← times some integer,… | `␣two` | 0.234 | 1 | `␣two` 0.23, `2` 0.08, `␣integers` 0.06, `␣integer` 0.05, `␣numbers` 0.04 |
| 31 | ? ← two times some integer… | `␣as` | 0.022 | 6 | `␣is` 0.37, `␣are` 0.12, `␣of` 0.11, `␣to` 0.06, `␣always` 0.05 |
| 32 | ? ← as two times some… | `␣written` | 0.357 | 1 | `␣written` 0.36, `␣expressed` 0.10, `␣same` 0.09, `␣represented` 0.06, `␣defined` 0.05 |
| 33 | ? ← written as two times… | `␣be` | 0.785 | 1 | `␣be` 0.78, `␣is` 0.13, `␣are` 0.02, `␣usually` 0.01, `␣also` 0.01 |
| 34 | ? ← be written as two… | `␣can` | 0.810 | 1 | `␣can` 0.81, `␣also` 0.08, `␣always` 0.03, `␣cannot` 0.02, `␣may` 0.01 |
| 35 | ? ← can be written as… | `␣each` | 0.008 | 20 | `␣numbers` 0.15, `␣integers` 0.11, `␣number` 0.10, `␣integer` 0.07, `␣sum` 0.04 |
| 36 | ? ← each can be written… | `,` | 0.320 | 1 | `,` 0.32, `␣and` 0.16, `␣that` 0.10, `␣because` 0.05, `␣numbers` 0.03 |
| 37 | ? ← , each can be… | `␣numbers` | 0.117 | 2 | `␣integers` 0.14, `␣numbers` 0.12, `␣However` 0.04, `␣example` 0.03, `␣addition` 0.02 |
| 38 | ? ← numbers, each can… | `␣even` | 0.541 | 1 | `␣even` 0.54, `␣odd` 0.16, `␣two` 0.08, `␣natural` 0.03, `␣prime` 0.02 |
| 39 | ? ← even numbers, each… | `␣two` | 0.558 | 1 | `␣two` 0.56, `␣are` 0.19, `␣of` 0.04, `␣For` 0.02, `␣consecutive` 0.01 |
| 40 | ? ← two even numbers,… | `␣add` | 0.027 | 7 | `␣any` 0.31, `␣have` 0.18, `␣are` 0.10, `␣of` 0.09, `␣given` 0.03 |
| 41 | ? ← add two even numbers… | `␣we` | 0.506 | 1 | `␣we` 0.51, `␣you` 0.39, `␣to` 0.05, `␣I` 0.02, `To` 0.00 |
| 42 | ? ← we add two even… | `␣If` | 0.199 | 2 | `␣if` 0.25, `␣If` 0.20, `␣when` 0.17, `␣When` 0.14, `When` 0.09 |
| 43 | ? ← If we add two… | `.` | 0.699 | 1 | `.` 0.70, `:` 0.17, `).` 0.02, `␣.` 0.01, `,` 0.01 |
| 44 | ? ← . If we add… | `␣remainder` | 0.001 | 60 | `␣integers` 0.15, `␣even` 0.14, `␣numbers` 0.13, `␣integer` 0.06, `␣odd` 0.05 |
| 45 | ? ← remainder. If we… | `␣a` | 0.124 | 4 | `␣the` 0.28, `␣no` 0.16, `␣any` 0.14, `␣a` 0.12, `␣same` 0.04 |
| 46 | ? ← a remainder. If… | `␣without` | 0.260 | 1 | `␣without` 0.26, `␣as` 0.13, `␣leaving` 0.09, `␣with` 0.05, `␣and` 0.05 |
| 47 | ? ← without a remainder.… | `␣two` | 0.023 | 10 | `␣numbers` 0.12, `␣integers` 0.10, `␣even` 0.09, `␣integer` 0.07, `␣number` 0.07 |
| 48 | ? ← two without a remainder… | `␣by` | 0.546 | 1 | `␣by` 0.55, `␣of` 0.12, `␣into` 0.05, `␣times` 0.04, `␣the` 0.02 |
| 49 | ? ← by two without a… | `␣divided` | 0.443 | 1 | `␣divided` 0.44, `␣divide` 0.16, `isible` 0.11, `␣divides` 0.09, `␣number` 0.04 |
| 50 | ? ← divided by two without… | `␣be` | 0.757 | 1 | `␣be` 0.76, `␣number` 0.04, `␣is` 0.04, `␣or` 0.04, `␣numbers` 0.02 |
| 51 | ? ← be divided by two… | `␣can` | 0.682 | 1 | `␣can` 0.68, `␣cannot` 0.18, `␣always` 0.02, `␣to` 0.02, `␣only` 0.01 |
| 52 | ? ← can be divided by… | `␣that` | 0.221 | 1 | `␣that` 0.22, `␣numbers` 0.11, `␣number` 0.11, `␣integer` 0.09, `␣it` 0.07 |
| 53 | ? ← that can be divided… | `␣integer` | 0.176 | 3 | `␣number` 0.38, `␣numbers` 0.21, `␣integer` 0.18, `␣integers` 0.08, `␣one` 0.03 |
| 54 | ? ← integer that can be… | `␣any` | 0.201 | 2 | `␣an` 0.44, `␣any` 0.20, `␣positive` 0.11, `␣smallest` 0.08, `␣largest` 0.03 |
| 55 | ? ← any integer that can… | `␣is` | 0.825 | 1 | `␣is` 0.83, `␣as` 0.06, `␣be` 0.03, `␣are` 0.01, `␣to` 0.01 |
| 56 | ? ← is any integer that… | `␣number` | 0.287 | 2 | `␣integer` 0.64, `␣number` 0.29, `er` 0.01, `␣integers` 0.01, `␣which` 0.01 |
| 57 | ? ← number is any integer… | `␣even` | 0.881 | 1 | `␣even` 0.88, `␣prime` 0.04, `␣odd` 0.03, `␣rational` 0.01, `␣Even` 0.01 |
| 58 | ? ← even number is any… | `An` | 0.415 | 1 | `An` 0.42, `␣An` 0.36, `␣an` 0.22, `␣or` 0.00, `,` 0.00 |

---

## 9. water_boils

*Category: logical*

> **Beginning:** Water boils when its vapour pressure equals the pressure of the surrounding air.  
> **Middle:** At high altitude the air pressure is lower, so less heat is needed to reach that point.  
> **Ending:** That is why water boils at a lower temperature on top of a mountain.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | at a lower temperature, water boils at a lower pressure. ↵ So, at a lower temperature, water boils at a lower pressure. ↵ So, at a lower temperature, water boils at a lower pressure. ↵ So, at a lower temperature, water boils at a lower pressure. ↵ So, at a lower temperature, water boils at a lower pressure. ↵ So, at a lower temperature, water boils at a lower pressure. ↵ So, at a lower pressure, water boils at a lower temperature. ↵ | That is why water boils at a lower temperature on top of a mountain. |
| sample | the temperature rises at the top of a mountain, the boiling point of water will go down. ↵ Thus, when the temperature rises at the top of a mountain, the pressure inside the mountains will increase. This will cause the water to rise to the top of the mountain. At the top of the mountain, the solid water becomes hotter than the liquid water. ↵ The boiling point of liquid water is lower at higher altitudes and decreases as the temperature rises. So this lowers the boiling temperature. ↵ | That is why water boils at a lower temperature on top of a mountain. |
| sample | the mountain (because of the temperature difference between the air at the bottom of Mount Everest and the lower pressure at the top of the mountain). ↵  ↵ The lower temperature of the air on Mount Everest is caused by the same force that makes Mount Everest hotter. It takes more energy to heat the air at the top of a mountain than Mount Everest, and so it boils at a lower temperature. ↵  ↵ This means that the air on the bottom of the mountain will stay warmer than the air above it. ↵  ↵ | That is why water boils at a lower temperature on top of a mountain. |
| sample | change with pressure? ↵  ↵ Decrease in atmospheric pressure increases the specific heat of water and makes it boil at lower temperature. The density of vapor of a given mass of water increases as the temperature also increases. The density of vapor of a liquid at a given pressure increases as the temperature decreases. Boiling point temperature of a liquid at a given pressure depends on the temperature and atmospheric pressure. A decrease in temperature/increase in pressure results in an increase in the boiling point temperature. | That is why water boils at a lower temperature on top of a mountain. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Water boils when its vapour pressure equals the pressure of the surrounding air. | The vapour pressure of water is 1 atm. The vapour pressure of water is 1 atm. The vapour pressure of water is 1 atm. The vapour pressure of water is 1 atm. The vapour pressure of water is 1 atm. The vapour pressure of water is 1 atm. The vapour pressure of water is 1 atm. The vapour pressure of water is 1 atm. The vapour pressure of water is 1 |
| sample | Water boils when its vapour pressure equals the pressure of the surrounding air. | The vapour pressure of a liquid, for example, is the pressure of the fluid at a given temperature and atmospheric pressure at which it boils. The boiling point of a liquid is the temperature at which it converts its vapour into a vapour pressure equivalent to atmospheric pressure. The vapour pressure of a liquid is higher than atmospheric pressure at the boiling point. When a liquid boils, its vapour pressure is greater than atmospheric pressure and is therefore lower than the vapour pressure of the solvent at which the liquid |
| sample | Water boils when its vapour pressure equals the pressure of the surrounding air. | This is because the water molecules in the liquid form above the boiling point, so they can escape from the liquid and become vapour. This process of evaporation starts from the surface of the liquid and builds up until the liquid is saturated with the vapour present from the surrounding air. The boiling point of water is defined as the temperature at which the vapour is entirely confined to the liquid. It is the same as the freezing point of water. ↵ Water is a supercooled liquid in which the |
| sample | Water boils when its vapour pressure equals the pressure of the surrounding air. | This is equal to the sum of the vapour pressure of the gas plus the pressure of the surrounding liquid. The pressure exerted by the gas is called the partial pressure of the gas. If the pressure P of the gas is doubled, the partial pressure of the gas is reduced to half the original value, and the temperature of the gas decreases by a factor of 2. (This is because the temperature of the gas is lowered by the vapour pressure of the gas.) ↵ The water vapour |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.567 | 48% |
| Backward | previous-token (right context) | 0.630 | 42% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Water` | 0.001 | 153 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Water → ? | `␣boils` | 0.001 | 199 | `␣is` 0.05, `color` 0.03, `␣Quality` 0.02, `proofing` 0.02, `␣and` 0.02 |
| 3 | Water boils → ? | `␣when` | 0.065 | 2 | `␣at` 0.79, `␣when` 0.07, `␣faster` 0.03, `,` 0.01, `␣and` 0.01 |
| 4 | Water boils when → ? | `␣its` | 0.054 | 4 | `␣the` 0.41, `␣it` 0.09, `␣a` 0.07, `␣its` 0.05, `␣there` 0.04 |
| 5 | Water boils when its → ? | `␣vapour` | 0.080 | 4 | `␣temperature` 0.32, `␣vapor` 0.29, `␣molecules` 0.10, `␣vapour` 0.08, `␣boiling` 0.02 |
| 6 | …boils when its vapour → ? | `␣pressure` | 0.876 | 1 | `␣pressure` 0.88, `␣is` 0.03, `-pressure` 0.01, `␣density` 0.01, `␣and` 0.01 |
| 7 | …when its vapour pressure → ? | `␣equals` | 0.229 | 2 | `␣is` 0.48, `␣equals` 0.23, `␣exceeds` 0.07, `␣equal` 0.04, `␣reaches` 0.02 |
| 8 | …its vapour pressure equals → ? | `␣the` | 0.550 | 1 | `␣the` 0.55, `␣atmospheric` 0.17, `␣its` 0.11, `␣that` 0.06, `␣` 0.02 |
| 9 | …vapour pressure equals the → ? | `␣pressure` | 0.144 | 2 | `␣atmospheric` 0.43, `␣pressure` 0.14, `␣external` 0.07, `␣surrounding` 0.06, `␣ambient` 0.04 |
| 10 | …pressure equals the pressure → ? | `␣of` | 0.613 | 1 | `␣of` 0.61, `␣at` 0.13, `␣exerted` 0.12, `␣on` 0.02, `␣in` 0.01 |
| 11 | …equals the pressure of → ? | `␣the` | 0.661 | 1 | `␣the` 0.66, `␣its` 0.14, `␣surrounding` 0.03, `␣liquid` 0.02, `␣atmospheric` 0.02 |
| 12 | …the pressure of the → ? | `␣surrounding` | 0.336 | 1 | `␣surrounding` 0.34, `␣liquid` 0.27, `␣vapour` 0.06, `␣saturated` 0.04, `␣water` 0.04 |
| 13 | …pressure of the surrounding → ? | `␣air` | 0.180 | 2 | `␣atmosphere` 0.24, `␣air` 0.18, `␣water` 0.12, `␣liquid` 0.10, `␣atmospheric` 0.09 |
| 14 | …of the surrounding air → ? | `.` | 0.468 | 1 | `.` 0.47, `,` 0.10, `.\n` 0.08, `␣at` 0.08, `␣(` 0.04 |
| 15 | …the surrounding air. → ? | `␣At` | 0.022 | 10 | `␣The` 0.14, `␣This` 0.10, `␣If` 0.07, `␣When` 0.06, `␣In` 0.05 |
| 16 | …surrounding air. At → ? | `␣high` | 0.029 | 9 | `␣sea` 0.17, `␣the` 0.14, `␣a` 0.12, `␣atmospheric` 0.06, `␣` 0.05 |
| 17 | …air. At high → ? | `␣altitude` | 0.056 | 6 | `␣pressure` 0.33, `␣altitudes` 0.16, `␣temperatures` 0.13, `␣pressures` 0.10, `␣temperature` 0.06 |
| 18 | …. At high altitude → ? | `␣the` | 0.126 | 2 | `,` 0.64, `␣the` 0.13, `␣and` 0.03, `␣(` 0.03, `␣water` 0.02 |
| 19 | …At high altitude the → ? | `␣air` | 0.187 | 2 | `␣pressure` 0.21, `␣air` 0.19, `␣vapour` 0.13, `␣atmospheric` 0.08, `␣temperature` 0.04 |
| 20 | …high altitude the air → ? | `␣pressure` | 0.329 | 2 | `␣is` 0.37, `␣pressure` 0.33, `␣has` 0.08, `␣above` 0.02, `␣contains` 0.02 |
| 21 | …altitude the air pressure → ? | `␣is` | 0.828 | 1 | `␣is` 0.83, `␣decreases` 0.03, `␣at` 0.02, `␣becomes` 0.01, `␣equals` 0.01 |
| 22 | …the air pressure is → ? | `␣lower` | 0.203 | 1 | `␣lower` 0.20, `␣less` 0.13, `␣low` 0.11, `␣much` 0.10, `␣higher` 0.05 |
| 23 | …air pressure is lower → ? | `,` | 0.168 | 3 | `␣than` 0.40, `␣and` 0.18, `,` 0.17, `.` 0.07, `␣so` 0.05 |
| 24 | …pressure is lower, → ? | `␣so` | 0.358 | 1 | `␣so` 0.36, `␣and` 0.29, `␣the` 0.05, `␣which` 0.04, `␣therefore` 0.03 |
| 25 | …is lower, so → ? | `␣less` | 0.016 | 8 | `␣the` 0.49, `␣water` 0.16, `␣there` 0.04, `␣boiling` 0.03, `␣it` 0.02 |
| 26 | …lower, so less → ? | `␣heat` | 0.031 | 5 | `␣water` 0.37, `␣vapour` 0.35, `␣energy` 0.05, `␣of` 0.03, `␣heat` 0.03 |
| 27 | …, so less heat → ? | `␣is` | 0.624 | 1 | `␣is` 0.62, `␣energy` 0.16, `␣can` 0.04, `␣will` 0.03, `␣escapes` 0.03 |
| 28 | …so less heat is → ? | `␣needed` | 0.182 | 2 | `␣required` 0.33, `␣needed` 0.18, `␣absorbed` 0.10, `␣lost` 0.07, `␣transferred` 0.06 |
| 29 | …less heat is needed → ? | `␣to` | 0.851 | 1 | `␣to` 0.85, `.` 0.05, `␣for` 0.04, `,` 0.01, `␣from` 0.01 |
| 30 | …heat is needed to → ? | `␣reach` | 0.010 | 13 | `␣boil` 0.43, `␣raise` 0.20, `␣bring` 0.05, `␣overcome` 0.03, `␣evaporate` 0.03 |
| 31 | …is needed to reach → ? | `␣that` | 0.008 | 8 | `␣the` 0.50, `␣boiling` 0.28, `␣a` 0.08, `␣its` 0.02, `␣saturation` 0.02 |
| 32 | …needed to reach that → ? | `␣point` | 0.344 | 1 | `␣point` 0.34, `␣temperature` 0.19, `␣pressure` 0.16, `␣boiling` 0.13, `␣same` 0.04 |
| 33 | …to reach that point → ? | `.` | 0.627 | 1 | `.` 0.63, `,` 0.09, `.\n` 0.09, `␣than` 0.04, `.\n\n` 0.03 |
| 34 | …reach that point. → ? | `␣That` | 0.016 | 14 | `␣The` 0.13, `␣At` 0.09, `␣This` 0.09, `␣As` 0.06, `␣In` 0.04 |
| 35 | …that point. That → ? | `␣is` | 0.211 | 2 | `'s` 0.29, `␣means` 0.21, `␣is` 0.21, `␣explains` 0.03, `␣makes` 0.02 |
| 36 | …point. That is → ? | `␣why` | 0.640 | 1 | `␣why` 0.64, `␣the` 0.09, `,` 0.07, `␣because` 0.04, `␣one` 0.02 |
| 37 | …. That is why → ? | `␣water` | 0.232 | 1 | `␣water` 0.23, `␣the` 0.13, `␣boiling` 0.07, `␣you` 0.06, `␣a` 0.05 |
| 38 | …That is why water → ? | `␣boils` | 0.600 | 1 | `␣boils` 0.60, `␣freezes` 0.07, `␣is` 0.04, `␣at` 0.02, `␣boiling` 0.02 |
| 39 | …is why water boils → ? | `␣at` | 0.817 | 1 | `␣at` 0.82, `␣faster` 0.05, `␣when` 0.02, `␣in` 0.01, `␣much` 0.01 |
| 40 | …why water boils at → ? | `␣a` | 0.325 | 1 | `␣a` 0.32, `␣` 0.24, `␣lower` 0.14, `␣higher` 0.08, `␣sea` 0.03 |
| 41 | …water boils at a → ? | `␣lower` | 0.680 | 1 | `␣lower` 0.68, `␣higher` 0.16, `␣temperature` 0.04, `␣much` 0.04, `␣low` 0.02 |
| 42 | …boils at a lower → ? | `␣temperature` | 0.971 | 1 | `␣temperature` 0.97, `␣temp` 0.00, `␣boiling` 0.00, `␣pressure` 0.00, `␣altitude` 0.00 |
| 43 | …at a lower temperature → ? | `␣on` | 0.034 | 5 | `␣at` 0.57, `␣than` 0.10, `␣in` 0.08, `␣when` 0.04, `␣on` 0.03 |
| 44 | …a lower temperature on → ? | `␣top` | 0.011 | 11 | `␣the` 0.52, `␣a` 0.13, `␣high` 0.06, `␣higher` 0.04, `␣mountains` 0.04 |
| 45 | …lower temperature on top → ? | `␣of` | 0.927 | 1 | `␣of` 0.93, `␣than` 0.02, `.` 0.01, `,` 0.01, `␣and` 0.01 |
| 46 | …temperature on top of → ? | `␣a` | 0.293 | 1 | `␣a` 0.29, `␣the` 0.25, `␣Mount` 0.11, `␣mountains` 0.08, `␣Mt` 0.05 |
| 47 | …on top of a → ? | `␣mountain` | 0.706 | 1 | `␣mountain` 0.71, `␣hill` 0.10, `␣high` 0.02, `␣tall` 0.02, `␣glacier` 0.02 |
| 48 | …top of a mountain → ? | `.` | 0.103 | 2 | `␣than` 0.48, `.` 0.10, `,` 0.08, `.\n` 0.07, `␣compared` 0.05 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣mountain` | 0.000 | 7458 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← mountain. | `␣a` | 0.181 | 2 | `␣the` 0.48, `␣a` 0.18, `␣or` 0.02, `␣high` 0.01, `␣this` 0.01 |
| 4 | ? ← a mountain. | `␣of` | 0.332 | 1 | `␣of` 0.33, `␣on` 0.10, `␣down` 0.06, `␣up` 0.05, `␣into` 0.03 |
| 5 | ? ← of a mountain. | `␣top` | 0.294 | 1 | `␣top` 0.29, `␣side` 0.23, `␣foot` 0.04, `␣base` 0.04, `␣summit` 0.03 |
| 6 | ? ← top of a mountain… | `␣on` | 0.312 | 2 | `␣the` 0.63, `␣on` 0.31, `␣The` 0.02, `␣On` 0.02, `␣very` 0.00 |
| 7 | ? ← on top of a… | `␣temperature` | 0.000 | 873 | `␣or` 0.07, `␣standing` 0.02, `␣sitting` 0.02, `␣located` 0.02, `␣up` 0.02 |
| 8 | ? ← temperature on top of… | `␣lower` | 0.009 | 15 | `␣the` 0.39, `␣in` 0.06, `␣air` 0.05, `␣The` 0.04, `␣and` 0.04 |
| 9 | ? ← lower temperature on top… | `␣a` | 0.343 | 1 | `␣a` 0.34, `␣the` 0.22, `␣and` 0.07, `␣at` 0.07, `␣much` 0.05 |
| 10 | ? ← a lower temperature on… | `␣at` | 0.430 | 1 | `␣at` 0.43, `␣and` 0.10, `␣to` 0.10, `␣in` 0.06, `␣with` 0.05 |
| 11 | ? ← at a lower temperature… | `␣boils` | 0.013 | 12 | `␣water` 0.04, `␣air` 0.03, `␣or` 0.02, `␣and` 0.02, `␣is` 0.02 |
| 12 | ? ← boils at a lower… | `␣water` | 0.492 | 1 | `␣water` 0.49, `␣and` 0.10, `␣Water` 0.07, `␣it` 0.06, `␣liquid` 0.05 |
| 13 | ? ← water boils at a… | `␣why` | 0.031 | 8 | `␣where` 0.16, `,` 0.15, `␣when` 0.12, `␣while` 0.09, `␣that` 0.08 |
| 14 | ? ← why water boils at… | `␣is` | 0.269 | 1 | `␣is` 0.27, `␣explain` 0.11, `␣explains` 0.08, `␣and` 0.08, `␣reason` 0.05 |
| 15 | ? ← is why water boils… | `␣That` | 0.088 | 3 | `␣This` 0.39, `␣which` 0.27, `␣That` 0.09, `␣this` 0.08, `␣that` 0.04 |
| 16 | ? ← That is why water… | `.` | 0.925 | 1 | `.` 0.93, `).` 0.03, `␣…` 0.01, `!` 0.00, `:` 0.00 |
| 17 | ? ← . That is why… | `␣point` | 0.024 | 4 | `␣temperature` 0.06, `␣pressure` 0.05, `␣water` 0.04, `␣increases` 0.02, `␣point` 0.02 |
| 18 | ? ← point. That is… | `␣that` | 0.005 | 8 | `␣boiling` 0.91, `␣freezing` 0.02, `␣triple` 0.01, `iling` 0.01, `␣melting` 0.01 |
| 19 | ? ← that point. That… | `␣reach` | 0.014 | 6 | `␣at` 0.69, `␣above` 0.09, `␣below` 0.06, `␣to` 0.05, `␣from` 0.02 |
| 20 | ? ← reach that point.… | `␣to` | 0.843 | 1 | `␣to` 0.84, `␣they` 0.02, `␣you` 0.02, `␣will` 0.02, `␣can` 0.02 |
| 21 | ? ← to reach that point… | `␣needed` | 0.044 | 5 | `␣energy` 0.18, `␣longer` 0.08, `␣heat` 0.06, `␣required` 0.06, `␣needed` 0.04 |
| 22 | ? ← needed to reach that… | `␣is` | 0.281 | 2 | `␣energy` 0.30, `␣is` 0.28, `␣heat` 0.14, `␣temperature` 0.05, `␣be` 0.04 |
| 23 | ? ← is needed to reach… | `␣heat` | 0.243 | 2 | `␣energy` 0.54, `␣heat` 0.24, `␣temperature` 0.04, `␣work` 0.02, `␣that` 0.02 |
| 24 | ? ← heat is needed to… | `␣less` | 0.205 | 2 | `␣more` 0.53, `␣less` 0.21, `␣More` 0.07, `␣of` 0.07, `␣much` 0.03 |
| 25 | ? ← less heat is needed… | `␣so` | 0.164 | 2 | `,` 0.18, `␣so` 0.16, `␣the` 0.15, `␣and` 0.10, `␣means` 0.09 |
| 26 | ? ← so less heat is… | `,` | 0.652 | 1 | `,` 0.65, `␣and` 0.12, `␣point` 0.03, `),` 0.02, `␣lower` 0.02 |
| 27 | ? ← , so less heat… | `␣lower` | 0.088 | 2 | `␣point` 0.18, `␣lower` 0.09, `␣temperature` 0.08, `␣pressure` 0.05, `␣water` 0.03 |
| 28 | ? ← lower, so less… | `␣is` | 0.762 | 1 | `␣is` 0.76, `␣much` 0.05, `␣be` 0.03, `␣are` 0.02, `␣gets` 0.02 |
| 29 | ? ← is lower, so… | `␣pressure` | 0.123 | 3 | `␣temperature` 0.24, `␣point` 0.23, `␣pressure` 0.12, `␣water` 0.08, `␣liquid` 0.03 |
| 30 | ? ← pressure is lower,… | `␣air` | 0.035 | 4 | `␣the` 0.57, `␣atmospheric` 0.09, `␣vapor` 0.08, `␣air` 0.04, `,` 0.03 |
| 31 | ? ← air pressure is lower… | `␣the` | 0.801 | 1 | `␣the` 0.80, `,` 0.05, `␣The` 0.03, `␣where` 0.02, `␣and` 0.01 |
| 32 | ? ← the air pressure is… | `␣altitude` | 0.016 | 7 | `,` 0.48, `␣where` 0.12, `␣because` 0.12, `␣mountain` 0.04, `␣and` 0.03 |
| 33 | ? ← altitude the air pressure… | `␣high` | 0.232 | 2 | `␣higher` 0.46, `␣high` 0.23, `␣lower` 0.07, `␣certain` 0.04, `␣At` 0.03 |
| 34 | ? ← high altitude the air… | `␣At` | 0.389 | 1 | `␣At` 0.39, `␣a` 0.31, `␣at` 0.16, `At` 0.08, `␣the` 0.02 |
| 35 | ? ← At high altitude the… | `.` | 0.881 | 1 | `.` 0.88, `).` 0.03, `:` 0.03, `␣…` 0.02, `?` 0.01 |
| 36 | ? ← . At high altitude… | `␣air` | 0.026 | 6 | `␣point` 0.12, `␣pressure` 0.11, `␣temperature` 0.07, `␣altitude` 0.05, `␣boils` 0.04 |
| 37 | ? ← air. At high… | `␣surrounding` | 0.085 | 2 | `␣the` 0.52, `␣surrounding` 0.08, `␣of` 0.07, `␣cold` 0.05, `␣cooler` 0.03 |
| 38 | ? ← surrounding air. At… | `␣the` | 0.945 | 1 | `␣the` 0.94, `␣of` 0.01, `␣and` 0.01, `␣its` 0.01, `␣than` 0.00 |
| 39 | ? ← the surrounding air.… | `␣of` | 0.247 | 2 | `␣than` 0.31, `␣of` 0.25, `␣and` 0.09, `␣to` 0.07, `␣in` 0.05 |
| 40 | ? ← of the surrounding air… | `␣pressure` | 0.444 | 1 | `␣pressure` 0.44, `␣that` 0.23, `␣temperature` 0.20, `␣point` 0.03, `␣density` 0.02 |
| 41 | ? ← pressure of the surrounding… | `␣the` | 0.914 | 1 | `␣the` 0.91, `␣and` 0.02, `␣vapor` 0.01, `␣higher` 0.01, `␣high` 0.01 |
| 42 | ? ← the pressure of the… | `␣equals` | 0.042 | 6 | `␣than` 0.26, `␣to` 0.14, `␣by` 0.14, `␣and` 0.10, `␣on` 0.05 |
| 43 | ? ← equals the pressure of… | `␣pressure` | 0.381 | 1 | `␣pressure` 0.38, `␣it` 0.09, `␣liquid` 0.08, `␣point` 0.04, `␣air` 0.03 |
| 44 | ? ← pressure equals the pressure… | `␣vapour` | 0.052 | 5 | `␣air` 0.29, `␣vapor` 0.27, `␣atmospheric` 0.16, `␣its` 0.07, `␣vapour` 0.05 |
| 45 | ? ← vapour pressure equals the… | `␣its` | 0.231 | 2 | `␣the` 0.49, `␣its` 0.23, `'s` 0.05, `␣water` 0.03, `␣saturated` 0.03 |
| 46 | ? ← its vapour pressure equals… | `␣when` | 0.185 | 2 | `␣until` 0.27, `␣when` 0.18, `␣which` 0.18, `␣where` 0.17, `␣that` 0.05 |
| 47 | ? ← when its vapour pressure… | `␣boils` | 0.435 | 1 | `␣boils` 0.43, `␣point` 0.19, `␣boil` 0.12, `␣boiling` 0.04, `␣temperature` 0.02 |
| 48 | ? ← boils when its vapour… | `Water` | 0.293 | 1 | `␣Water` 0.29, `Water` 0.29, `␣liquid` 0.17, `␣water` 0.17, `␣substance` 0.02 |

---

## 10. detective

*Category: logical*

> **Beginning:** The window had been forced open from the outside, and there was mud on the carpet.  
> **Middle:** The gardener was the only person with muddy boots, and he had been seen near the house at midnight.  
> **Ending:** The detective concluded that the gardener had broken into the study.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | some of the plants in the garden. ↵ The next day, the gardener noticed some brown spots on the leaves of some of the plants in the garden. ↵ The next day, the gardener noticed some brown spots on the leaves of some of the plants in the garden. ↵ The next day, the gardener noticed some brown spots on the leaves of some of the plants in the garden. ↵ The next day, the gardener noticed some brown spots on the leaves of some of the plants in the garden. ↵ | The detective concluded that the gardener had broken into the study. |
| sample | a gardener saw a curious child in the garden. When she saw her climbing a tree, she went to the child and told her to look at the tree where the girl would be found. ↵ The next day, the gardener found the girl, climbed the tree and looked at her. ↵ Then the detective came to the girl's home. She noticed that the girl, who was five years old, was hiding in the branches of a maple tree, which she found in the garden. ↵ | The detective concluded that the gardener had broken into the study. |
| sample | kitchen garden. Upon inspection, the detective revealed that a fungal disease had decimated some of the tomato plants in the area. The gardener worried that it would spread to other tomato plants in another area of the garden. ↵  ↵ About 10 days after realising that the plants had the disease, the roots were dug up and thrown away. They were contaminated with the spores of the fungus. As with other plants, this allowed the spores to spread to other plants growing in the area. ↵  ↵ | The detective concluded that the gardener had broken into the study. |
| sample | meaning that the gardener dug, indicating that the gardener had dug, meaning that the gardener had dug, indicating that the gardener had dug, indicating that the gardener had dug, indicating that the gardener had dug or dug, indicating that the gardener had dug or dug, indicating that there had not been any digging. The detective also asked if there had been any digging in the garden and found that there had not been any digging, indicating that the gardener had not dug from the garden. ↵  ↵ | The detective concluded that the gardener had broken into the study. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | The window had been forced open from the outside, and there was mud on the carpet. | The window was closed, and the door was opened. The window was closed, and the door was opened. The window was closed, and the door was opened. The window was closed, and the door was opened. The window was closed, and the door was opened. The window was closed, and the door was opened. The window was closed, and the door was opened. The window was closed, and the door was opened. The window was closed, and the door |
| sample | The window had been forced open from the outside, and there was mud on the carpet. | The window was shut and the air conditioner was turned on. The mud covered the window, and then a lot of the water came through the window, as if it was a giant sink. The water ran out at the bottom of the wall, and the window was a mess. The window was cleaned up, and the window was repaired. The window was cleaned up and the window was repaired. The window was fixed. The window was fixed. The window was fixed. ↵ The window |
| sample | The window had been forced open from the outside, and there was mud on the carpet. | I don't know how to explain that, because someone, I assume, must have left the door open for the purpose of letting in some breeze. ↵ Tyler, I can only assume that you are trying to describe a real life situation rather than just a fictional one. The door was opened for the purpose of letting in breeze, and you must have left the door open. Please explain why you think that is so. ↵ You're not a crackpot. If you want to |
| sample | The window had been forced open from the outside, and there was mud on the carpet. | I was also wearing a large silk gown on my head as it was a matter of personal choice. I had been wearing a silk gown for years, and the gown had been removed as a result of the way it held me up on my legs. It had been a very uncomfortable sight, and there was little or no way for me to find a place to lie down comfortably. I had been a member of the group for quite some time, but I wasn't |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.996 | 44% |
| Backward | previous-token (right context) | 1.076 | 38% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `The` | 0.066 | 1 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | The → ? | `␣window` | 0.000 | 2027 | `␣` 0.01, `␣first` 0.01, `␣most` 0.01, `␣Importance` 0.01, `␣best` 0.01 |
| 3 | The window → ? | `␣had` | 0.002 | 84 | `␣is` 0.09, `␣of` 0.07, `␣to` 0.02, `␣in` 0.02, `␣and` 0.02 |
| 4 | The window had → ? | `␣been` | 0.266 | 1 | `␣been` 0.27, `␣a` 0.19, `␣to` 0.06, `␣the` 0.02, `␣an` 0.02 |
| 5 | The window had been → ? | `␣forced` | 0.001 | 242 | `␣opened` 0.08, `␣open` 0.07, `␣closed` 0.07, `␣a` 0.02, `␣broken` 0.02 |
| 6 | …window had been forced → ? | `␣open` | 0.535 | 1 | `␣open` 0.53, `␣shut` 0.12, `␣to` 0.09, `␣down` 0.06, `␣closed` 0.03 |
| 7 | …had been forced open → ? | `␣from` | 0.007 | 22 | `,` 0.21, `␣and` 0.14, `␣by` 0.07, `.` 0.07, `␣for` 0.05 |
| 8 | …been forced open from → ? | `␣the` | 0.580 | 1 | `␣the` 0.58, `␣a` 0.06, `␣all` 0.03, `␣inside` 0.02, `␣` 0.02 |
| 9 | …forced open from the → ? | `␣outside` | 0.113 | 2 | `␣inside` 0.20, `␣outside` 0.11, `␣top` 0.10, `␣bottom` 0.09, `␣front` 0.03 |
| 10 | …open from the outside → ? | `,` | 0.276 | 1 | `,` 0.28, `.` 0.14, `␣and` 0.13, `␣by` 0.06, `␣with` 0.04 |
| 11 | …from the outside, → ? | `␣and` | 0.333 | 1 | `␣and` 0.33, `␣but` 0.14, `␣so` 0.06, `␣allowing` 0.03, `␣the` 0.03 |
| 12 | …the outside, and → ? | `␣there` | 0.020 | 6 | `␣the` 0.34, `␣a` 0.09, `␣it` 0.05, `␣I` 0.03, `␣when` 0.02 |
| 13 | …outside, and there → ? | `␣was` | 0.640 | 1 | `␣was` 0.64, `␣were` 0.25, `␣had` 0.03, `␣is` 0.01, `␣seemed` 0.01 |
| 14 | …, and there was → ? | `␣mud` | 0.000 | 264 | `␣a` 0.46, `␣no` 0.18, `␣an` 0.04, `␣nothing` 0.04, `␣only` 0.03 |
| 15 | …and there was mud → ? | `␣on` | 0.170 | 1 | `␣and` 0.17, `␣on` 0.17, `␣everywhere` 0.09, `␣in` 0.07, `␣all` 0.05 |
| 16 | …there was mud on → ? | `␣the` | 0.804 | 1 | `␣the` 0.80, `␣it` 0.05, `␣its` 0.04, `␣both` 0.02, `␣all` 0.02 |
| 17 | …was mud on the → ? | `␣carpet` | 0.000 | 192 | `␣inside` 0.19, `␣outside` 0.08, `␣floor` 0.07, `␣window` 0.06, `␣bottom` 0.05 |
| 18 | …mud on the carpet → ? | `.` | 0.344 | 1 | `.` 0.34, `,` 0.16, `␣and` 0.11, `.\n` 0.03, `␣inside` 0.02 |
| 19 | …on the carpet. → ? | `␣The` | 0.231 | 1 | `␣The` 0.23, `␣I` 0.08, `␣It` 0.06, `␣There` 0.03, `␣A` 0.03 |
| 20 | …the carpet. The → ? | `␣gardener` | 0.000 | 594 | `␣window` 0.07, `␣door` 0.03, `␣carpet` 0.02, `␣windows` 0.02, `␣house` 0.02 |
| 21 | …carpet. The gardener → ? | `␣was` | 0.112 | 2 | `␣had` 0.14, `␣was` 0.11, `,` 0.06, `'s` 0.05, `␣and` 0.03 |
| 22 | …. The gardener was → ? | `␣the` | 0.004 | 48 | `␣very` 0.04, `␣not` 0.03, `␣able` 0.03, `␣so` 0.03, `␣surprised` 0.03 |
| 23 | …The gardener was the → ? | `␣only` | 0.210 | 1 | `␣only` 0.21, `␣one` 0.17, `␣first` 0.13, `␣most` 0.05, `␣best` 0.03 |
| 24 | …gardener was the only → ? | `␣person` | 0.182 | 2 | `␣one` 0.65, `␣person` 0.18, `␣thing` 0.01, `␣gardener` 0.01, `␣woman` 0.01 |
| 25 | …was the only person → ? | `␣with` | 0.031 | 5 | `␣who` 0.34, `␣in` 0.16, `␣to` 0.09, `␣on` 0.04, `␣with` 0.03 |
| 26 | …the only person with → ? | `␣muddy` | 0.000 | 311 | `␣a` 0.29, `␣the` 0.18, `␣any` 0.06, `␣access` 0.04, `␣an` 0.03 |
| 27 | …only person with muddy → ? | `␣boots` | 0.241 | 2 | `␣shoes` 0.29, `␣boots` 0.24, `␣hands` 0.23, `␣feet` 0.05, `␣clothes` 0.05 |
| 28 | …person with muddy boots → ? | `,` | 0.222 | 1 | `,` 0.22, `.` 0.18, `␣and` 0.10, `␣on` 0.06, `␣to` 0.06 |
| 29 | …with muddy boots, → ? | `␣and` | 0.373 | 1 | `␣and` 0.37, `␣so` 0.20, `␣but` 0.12, `␣gloves` 0.07, `␣as` 0.02 |
| 30 | …muddy boots, and → ? | `␣he` | 0.196 | 1 | `␣he` 0.20, `␣the` 0.18, `␣she` 0.12, `␣they` 0.05, `␣it` 0.04 |
| 31 | …boots, and he → ? | `␣had` | 0.175 | 2 | `␣was` 0.19, `␣had` 0.17, `␣said` 0.02, `␣didn` 0.02, `␣used` 0.02 |
| 32 | …, and he had → ? | `␣been` | 0.106 | 2 | `␣to` 0.22, `␣been` 0.11, `␣a` 0.06, `␣no` 0.06, `␣never` 0.03 |
| 33 | …and he had been → ? | `␣seen` | 0.001 | 147 | `␣working` 0.06, `␣wearing` 0.04, `␣in` 0.03, `␣out` 0.03, `␣cleaning` 0.02 |
| 34 | …he had been seen → ? | `␣near` | 0.001 | 139 | `␣walking` 0.07, `␣in` 0.06, `␣by` 0.04, `␣to` 0.04, `␣on` 0.03 |
| 35 | …had been seen near → ? | `␣the` | 0.787 | 1 | `␣the` 0.79, `␣a` 0.04, `␣his` 0.01, `␣and` 0.01, `␣it` 0.01 |
| 36 | …been seen near the → ? | `␣house` | 0.053 | 3 | `␣window` 0.32, `␣door` 0.09, `␣house` 0.05, `␣entrance` 0.04, `␣front` 0.02 |
| 37 | …seen near the house → ? | `␣at` | 0.015 | 11 | `.` 0.17, `,` 0.13, `␣by` 0.06, `␣in` 0.04, `.\n` 0.04 |
| 38 | …near the house at → ? | `␣midnight` | 0.005 | 24 | `␣the` 0.30, `␣night` 0.11, `␣least` 0.07, `␣one` 0.05, `␣a` 0.04 |
| 39 | …the house at midnight → ? | `.` | 0.212 | 1 | `.` 0.21, `,` 0.17, `␣on` 0.06, `.\n` 0.04, `␣in` 0.03 |
| 40 | …house at midnight. → ? | `␣The` | 0.203 | 2 | `␣He` 0.22, `␣The` 0.20, `␣It` 0.04, `␣There` 0.03, `␣"` 0.03 |
| 41 | …at midnight. The → ? | `␣detect` | 0.000 | 764 | `␣gardener` 0.17, `␣mud` 0.07, `␣window` 0.04, `␣house` 0.04, `␣farmer` 0.01 |
| 42 | …midnight. The detect → ? | `ive` | 0.883 | 1 | `ive` 0.88, `ives` 0.11, `er` 0.00, `ions` 0.00, `ress` 0.00 |
| 43 | …. The detective → ? | `␣concluded` | 0.001 | 85 | `␣was` 0.18, `␣had` 0.12, `,` 0.09, `'s` 0.03, `␣who` 0.02 |
| 44 | …The detective concluded → ? | `␣that` | 0.861 | 1 | `␣that` 0.86, `␣the` 0.03, `,` 0.02, `␣from` 0.01, `␣he` 0.01 |
| 45 | …detective concluded that → ? | `␣the` | 0.507 | 1 | `␣the` 0.51, `␣he` 0.11, `␣there` 0.06, `␣it` 0.06, `␣a` 0.04 |
| 46 | …ive concluded that the → ? | `␣gardener` | 0.083 | 2 | `␣mud` 0.10, `␣gardener` 0.08, `␣house` 0.06, `␣window` 0.03, `␣person` 0.02 |
| 47 | …concluded that the gardener → ? | `␣had` | 0.376 | 1 | `␣had` 0.38, `␣was` 0.31, `'s` 0.05, `␣must` 0.03, `␣and` 0.02 |
| 48 | …that the gardener had → ? | `␣broken` | 0.016 | 6 | `␣been` 0.21, `␣left` 0.06, `␣not` 0.02, `␣used` 0.02, `␣fallen` 0.02 |
| 49 | …the gardener had broken → ? | `␣into` | 0.338 | 1 | `␣into` 0.34, `␣the` 0.22, `␣in` 0.15, `␣a` 0.06, `␣his` 0.05 |
| 50 | …gardener had broken into → ? | `␣the` | 0.899 | 1 | `␣the` 0.90, `␣a` 0.04, `␣his` 0.02, `␣an` 0.00, `␣it` 0.00 |
| 51 | …had broken into the → ? | `␣study` | 0.000 | 531 | `␣house` 0.57, `␣home` 0.04, `␣window` 0.04, `␣building` 0.03, `␣garden` 0.03 |
| 52 | …broken into the study → ? | `.` | 0.066 | 4 | `␣room` 0.21, `,` 0.16, `␣and` 0.13, `.` 0.07, `␣by` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣study` | 0.001 | 261 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← study. | `␣the` | 0.281 | 1 | `␣the` 0.28, `␣this` 0.13, `␣of` 0.06, `␣further` 0.04, `␣to` 0.03 |
| 4 | ? ← the study. | `␣into` | 0.003 | 24 | `␣of` 0.32, `␣in` 0.24, `␣to` 0.09, `␣for` 0.06, `␣on` 0.04 |
| 5 | ? ← into the study. | `␣broken` | 0.000 | 5386 | `␣incorporated` 0.08, `␣years` 0.03, `␣input` 0.03, `␣data` 0.02, `␣entered` 0.02 |
| 6 | ? ← broken into the study… | `␣had` | 0.032 | 9 | `␣be` 0.20, `␣was` 0.06, `␣is` 0.06, `␣are` 0.06, `␣were` 0.05 |
| 7 | ? ← had broken into the… | `␣gardener` | 0.000 | 9826 | `␣they` 0.11, `␣who` 0.08, `␣that` 0.07, `␣he` 0.05, `␣she` 0.03 |
| 8 | ? ← gardener had broken into… | `␣the` | 0.340 | 1 | `␣the` 0.34, `␣a` 0.10, `␣The` 0.08, `␣one` 0.02, `␣A` 0.02 |
| 9 | ? ← the gardener had broken… | `␣that` | 0.159 | 1 | `␣that` 0.16, `,` 0.08, `␣if` 0.07, `␣after` 0.06, `␣and` 0.06 |
| 10 | ? ← that the gardener had… | `␣concluded` | 0.003 | 61 | `␣fact` 0.03, `␣and` 0.03, `␣noticed` 0.03, `␣found` 0.02, `␣discovered` 0.02 |
| 11 | ? ← concluded that the gardener… | `ive` | 0.000 | 1347 | `␣and` 0.08, `␣They` 0.07, `␣was` 0.06, `␣He` 0.05, `␣She` 0.04 |
| 12 | ? ← ive concluded that the… | `␣detect` | 0.862 | 1 | `␣detect` 0.86, `␣Cl` 0.03, `␣mot` 0.02, `␣Collect` 0.01, `h` 0.01 |
| 13 | ? ← detective concluded that… | `␣The` | 0.463 | 1 | `␣The` 0.46, `␣the` 0.33, `The` 0.05, `␣police` 0.01, `␣a` 0.01 |
| 14 | ? ← The detective concluded… | `.` | 0.088 | 2 | `:` 0.90, `.` 0.09, `."` 0.00, `).` 0.00, `!` 0.00 |
| 15 | ? ← . The detective… | `␣midnight` | 0.000 | 4713 | `␣garden` 0.03, `␣it` 0.02, `␣plants` 0.01, `␣not` 0.01, `␣them` 0.01 |
| 16 | ? ← midnight. The detect… | `␣at` | 0.276 | 1 | `␣at` 0.28, `␣after` 0.15, `␣before` 0.12, `␣until` 0.10, `␣around` 0.05 |
| 17 | ? ← at midnight. The… | `␣house` | 0.013 | 5 | `␣garden` 0.04, `␣bed` 0.03, `,` 0.03, `␣again` 0.02, `␣house` 0.01 |
| 18 | ? ← house at midnight.… | `␣the` | 0.501 | 1 | `␣the` 0.50, `'s` 0.16, `␣his` 0.09, `␣her` 0.06, `’s` 0.03 |
| 19 | ? ← the house at midnight… | `␣near` | 0.003 | 30 | `␣in` 0.17, `␣of` 0.13, `␣into` 0.11, `␣to` 0.10, `␣at` 0.06 |
| 20 | ? ← near the house at… | `␣seen` | 0.014 | 8 | `␣found` 0.07, `␣garden` 0.03, `␣tree` 0.03, `␣bushes` 0.02, `␣growing` 0.02 |
| 21 | ? ← seen near the house… | `␣been` | 0.113 | 4 | `␣was` 0.37, `␣were` 0.17, `␣last` 0.12, `␣been` 0.11, `␣be` 0.05 |
| 22 | ? ← been seen near the… | `␣had` | 0.861 | 1 | `␣had` 0.86, `␣have` 0.03, `␣not` 0.02, `␣having` 0.01, `␣also` 0.01 |
| 23 | ? ← had been seen near… | `␣he` | 0.030 | 5 | `␣cat` 0.06, `␣that` 0.04, `␣dog` 0.03, `,` 0.03, `␣he` 0.03 |
| 24 | ? ← he had been seen… | `␣and` | 0.059 | 3 | `␣that` 0.45, `␣because` 0.07, `␣and` 0.06, `,` 0.06, `␣as` 0.04 |
| 25 | ? ← and he had been… | `,` | 0.382 | 1 | `,` 0.38, `␣night` 0.03, `␣morning` 0.02, `␣house` 0.02, `␣evening` 0.02 |
| 26 | ? ← , and he had… | `␣boots` | 0.000 | 1708 | `␣night` 0.04, `␣morning` 0.03, `␣house` 0.03, `␣day` 0.03, `␣evening` 0.03 |
| 27 | ? ← boots, and he… | `␣muddy` | 0.015 | 10 | `␣his` 0.27, `␣and` 0.12, `␣black` 0.06, `␣in` 0.04, `'s` 0.04 |
| 28 | ? ← muddy boots, and… | `␣with` | 0.088 | 4 | `␣in` 0.27, `␣his` 0.15, `␣and` 0.13, `␣with` 0.09, `,` 0.08 |
| 29 | ? ← with muddy boots,… | `␣person` | 0.000 | 482 | `␣covered` 0.14, `,` 0.08, `␣dressed` 0.03, `␣house` 0.03, `␣in` 0.03 |
| 30 | ? ← person with muddy boots… | `␣only` | 0.002 | 48 | `␣a` 0.49, `␣the` 0.06, `␣in` 0.02, `␣black` 0.02, `␣tall` 0.01 |
| 31 | ? ← only person with muddy… | `␣the` | 0.982 | 1 | `␣the` 0.98, `␣and` 0.01, `␣his` 0.00, `'s` 0.00, `,` 0.00 |
| 32 | ? ← the only person with… | `␣was` | 0.655 | 1 | `␣was` 0.65, `␣been` 0.09, `␣not` 0.06, `,` 0.05, `␣be` 0.03 |
| 33 | ? ← was the only person… | `␣gardener` | 0.108 | 3 | `␣he` 0.29, `␣He` 0.15, `␣gardener` 0.11, `,` 0.03, `␣man` 0.03 |
| 34 | ? ← gardener was the only… | `␣The` | 0.338 | 2 | `␣the` 0.52, `␣The` 0.34, `The` 0.04, `␣a` 0.02, `␣A` 0.01 |
| 35 | ? ← The gardener was the… | `.` | 0.918 | 1 | `.` 0.92, `:` 0.04, `."` 0.01, `).` 0.00, `?` 0.00 |
| 36 | ? ← . The gardener was… | `␣carpet` | 0.000 | 1433 | `␣house` 0.09, `␣garden` 0.02, `␣night` 0.02, `␣him` 0.02, `␣midnight` 0.01 |
| 37 | ? ← carpet. The gardener… | `␣the` | 0.503 | 1 | `␣the` 0.50, `␣a` 0.11, `␣red` 0.03, `␣of` 0.02, `␣his` 0.02 |
| 38 | ? ← the carpet. The… | `␣on` | 0.318 | 1 | `␣on` 0.32, `␣under` 0.14, `␣in` 0.10, `␣of` 0.07, `␣over` 0.03 |
| 39 | ? ← on the carpet.… | `␣mud` | 0.009 | 19 | `␣found` 0.05, `␣seen` 0.03, `␣lying` 0.03, `␣footprints` 0.02, `␣out` 0.02 |
| 40 | ? ← mud on the carpet… | `␣was` | 0.039 | 5 | `␣of` 0.24, `␣in` 0.13, `␣the` 0.12, `␣and` 0.06, `␣was` 0.04 |
| 41 | ? ← was mud on the… | `␣there` | 0.724 | 1 | `␣there` 0.72, `␣There` 0.22, `There` 0.02, `␣it` 0.00, `␣house` 0.00 |
| 42 | ? ← there was mud on… | `␣and` | 0.391 | 1 | `␣and` 0.39, `␣that` 0.18, `,` 0.16, `␣but` 0.04, `␣because` 0.03 |
| 43 | ? ← and there was mud… | `,` | 0.712 | 1 | `,` 0.71, `␣house` 0.04, `␣wet` 0.01, `␣floor` 0.01, `␣room` 0.01 |
| 44 | ? ← , and there was… | `␣outside` | 0.009 | 18 | `␣house` 0.11, `␣floor` 0.02, `␣wet` 0.02, `␣room` 0.02, `␣boots` 0.02 |
| 45 | ? ← outside, and there… | `␣the` | 0.062 | 2 | `␣went` 0.08, `␣the` 0.06, `␣was` 0.06, `␣been` 0.05, `␣from` 0.03 |
| 46 | ? ← the outside, and… | `␣from` | 0.289 | 2 | `␣on` 0.39, `␣from` 0.29, `␣to` 0.12, `␣around` 0.05, `␣of` 0.01 |
| 47 | ? ← from the outside,… | `␣open` | 0.001 | 130 | `␣house` 0.21, `␣seen` 0.09, `␣in` 0.05, `␣coming` 0.04, `␣visible` 0.03 |
| 48 | ? ← open from the outside… | `␣forced` | 0.003 | 41 | `␣was` 0.18, `␣door` 0.10, `␣were` 0.07, `␣torn` 0.05, `␣left` 0.04 |
| 49 | ? ← forced open from the… | `␣been` | 0.566 | 1 | `␣been` 0.57, `␣was` 0.27, `␣were` 0.06, `␣door` 0.02, `␣being` 0.02 |
| 50 | ? ← been forced open from… | `␣had` | 0.967 | 1 | `␣had` 0.97, `␣just` 0.01, `␣have` 0.00, `␣has` 0.00, `␣recently` 0.00 |
| 51 | ? ← had been forced open… | `␣window` | 0.064 | 4 | `␣door` 0.30, `␣house` 0.25, `␣windows` 0.07, `␣window` 0.06, `␣room` 0.05 |
| 52 | ? ← window had been forced… | `The` | 0.020 | 7 | `␣the` 0.32, `␣The` 0.23, `␣a` 0.10, `␣A` 0.07, `␣bedroom` 0.04 |

---

## 11. lost_dog

*Category: narrative*

> **Beginning:** When Max the dog went missing, the whole street joined the search.  
> **Middle:** They checked the park, the woods and the river bank until it grew dark.  
> **Ending:** The next morning, Max was found asleep in the neighbour's garden shed.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | . ↵  ↵ After he had settled down for the night, Max got up, got up, and went back to his bed. ↵  ↵ After he had settled down for the night, Max got up, got up, and went back to his bed. ↵  ↵ After he had settled down for the night, Max got up, got up, and went back to his bed. ↵  ↵ After he had settled down for the night, Max got up, went back to his bed, and settled in for the night. ↵  ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |
| sample | all night. I assumed I had allowed him to sleep all day. But, in fact, he had gone home for the night and refused to stay in bed at night. ↵  ↵ I wasn't able to get him to stay in bed at night, but I encouraged him to keep at it. Eventually, I realised that I couldn't allow him to stay in bed all night. ↵  ↵ So, in the morning, Max headed out to relieve himself and went back to bed for the night. ↵  ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |
| sample | . In the evening, the cat came to her garden, lay down, and stood up. That night, she let the cat into her garden. Within a day, he made friends with the neighbor (the son of the neighbor), who didn't let him in the door, and left him in his garden. The neighbor came out and found him, left him in his garden, and returned him to the cats, which attacked his house, only to be chased away. ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |
| sample | middle of the night," said the owner. ↵ After a short period of time, the dog was found by the police and returned to her. ↵ "My mum had never let me sleep in my bed every night before I go to sleep, and I never did anything that could potentially lead to my death," she said. ↵ Meanwhile, the owner was also warned that if the dog is allowed to sleep in her bed, she will be found dead, picked up by the dog during the night. ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | When Max the dog went missing, the whole street joined the search. | The police were called, and the dog was found. The police were called, and the dog was found. The police were called, and the dog was found. The police were called, and the dog was found. The police were called, and the dog was found. The police were called, and the dog was found. The police were called, and the dog was found. The police were called, and the dog was found. The police were called, and the dog |
| sample | When Max the dog went missing, the whole street joined the search. | The police quickly arrived and brought out a chain-smoke detector, giving the city a good idea that something was wrong. At the same time, a local detective noticed that a stray dog had taken over Max's house. "One by one, the dogs were walking around the house, and one by one, they were jumping on the kitchen table," the detective explained. "It was like they were going around, but they were not. They walked around, but they |
| sample | When Max the dog went missing, the whole street joined the search. | That's when the search team arrived and found him — on a hot day with a high temperature of 103 degrees Fahrenheit. He had heat stroke and was in a lot of pain. For that reason, the search team traveled to the local zoo where they found him. They also found the dog's owner who had recently brought him home with a cold, wet blanket. He had been brought to the zoo where Max was in a cage for a few days to be treated for |
| sample | When Max the dog went missing, the whole street joined the search. | He was first found in the subway, after which he ran out of the station. The police were called and the dog was found dead. The dog was found by the police and was sent to the Humane Society. The police and the Humane Society went around the streets of the city to find those who had the dog with them. The police found the dog and made it their pet. The dog was then found dead and the police called the Humane Society. They found the dog |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 1.030 | 40% |
| Backward | previous-token (right context) | 1.128 | 33% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `When` | 0.008 | 12 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | When → ? | `␣Max` | 0.000 | 561 | `␣it` 0.17, `␣you` 0.11, `␣the` 0.07, `␣I` 0.06, `␣a` 0.04 |
| 3 | When Max → ? | `␣the` | 0.011 | 10 | `im` 0.10, `␣and` 0.08, `␣was` 0.06, `ine` 0.02, `␣is` 0.02 |
| 4 | When Max the → ? | `␣dog` | 0.057 | 1 | `␣dog` 0.06, `␣cat` 0.05, `␣Cat` 0.04, `␣monkey` 0.03, `␣Dog` 0.02 |
| 5 | When Max the dog → ? | `␣went` | 0.019 | 6 | `␣was` 0.14, `␣is` 0.06, `␣and` 0.04, `␣first` 0.03, `,` 0.02 |
| 6 | …Max the dog went → ? | `␣missing` | 0.234 | 2 | `␣to` 0.39, `␣missing` 0.23, `␣on` 0.07, `␣into` 0.04, `␣for` 0.02 |
| 7 | …the dog went missing → ? | `,` | 0.413 | 1 | `,` 0.41, `␣in` 0.18, `␣on` 0.08, `␣last` 0.03, `␣for` 0.03 |
| 8 | …dog went missing, → ? | `␣the` | 0.113 | 3 | `␣he` 0.23, `␣his` 0.15, `␣the` 0.11, `␣it` 0.05, `␣a` 0.04 |
| 9 | …went missing, the → ? | `␣whole` | 0.014 | 11 | `␣family` 0.07, `␣police` 0.05, `␣owner` 0.02, `␣local` 0.02, `␣people` 0.02 |
| 10 | …missing, the whole → ? | `␣street` | 0.000 | 64 | `␣family` 0.42, `␣neighborhood` 0.11, `␣world` 0.10, `␣community` 0.06, `␣town` 0.05 |
| 11 | …, the whole street → ? | `␣joined` | 0.000 | 255 | `␣was` 0.56, `␣became` 0.03, `␣had` 0.03, `␣went` 0.03, `␣of` 0.02 |
| 12 | …the whole street joined → ? | `␣the` | 0.037 | 4 | `␣him` 0.39, `␣in` 0.26, `␣together` 0.12, `␣the` 0.04, `␣hands` 0.03 |
| 13 | …whole street joined the → ? | `␣search` | 0.131 | 1 | `␣search` 0.13, `␣police` 0.04, `␣family` 0.03, `␣crowd` 0.02, `␣fight` 0.02 |
| 14 | …street joined the search → ? | `.` | 0.309 | 1 | `.` 0.31, `␣for` 0.21, `,` 0.09, `␣and` 0.06, `.\n` 0.04 |
| 15 | …joined the search. → ? | `␣They` | 0.020 | 9 | `␣The` 0.11, `␣He` 0.07, `␣It` 0.05, `␣But` 0.04, `␣Max` 0.03 |
| 16 | …the search. They → ? | `␣checked` | 0.001 | 124 | `␣were` 0.11, `␣found` 0.10, `␣had` 0.09, `␣didn` 0.05, `␣searched` 0.04 |
| 17 | …search. They checked → ? | `␣the` | 0.310 | 1 | `␣the` 0.31, `␣all` 0.08, `␣every` 0.08, `␣everything` 0.04, `␣his` 0.03 |
| 18 | …. They checked the → ? | `␣park` | 0.007 | 24 | `␣streets` 0.08, `␣house` 0.04, `␣area` 0.03, `␣street` 0.03, `␣whole` 0.02 |
| 19 | …They checked the park → ? | `,` | 0.486 | 1 | `,` 0.49, `␣and` 0.22, `␣where` 0.04, `␣for` 0.04, `.` 0.03 |
| 20 | …checked the park, → ? | `␣the` | 0.441 | 1 | `␣the` 0.44, `␣and` 0.04, `␣but` 0.02, `␣they` 0.01, `␣streets` 0.01 |
| 21 | …the park, the → ? | `␣woods` | 0.024 | 6 | `␣streets` 0.04, `␣street` 0.04, `␣beach` 0.04, `␣park` 0.03, `␣school` 0.03 |
| 22 | …park, the woods → ? | `␣and` | 0.180 | 2 | `,` 0.78, `␣and` 0.18, `.` 0.01, `␣near` 0.00, `␣behind` 0.00 |
| 23 | …, the woods and → ? | `␣the` | 0.425 | 1 | `␣the` 0.43, `␣even` 0.19, `,` 0.02, `␣everywhere` 0.02, `␣all` 0.02 |
| 24 | …the woods and the → ? | `␣river` | 0.026 | 5 | `␣fields` 0.06, `␣streets` 0.06, `␣beach` 0.05, `␣city` 0.03, `␣river` 0.03 |
| 25 | …woods and the river → ? | `␣bank` | 0.031 | 8 | `.` 0.37, `,` 0.15, `␣and` 0.06, `␣for` 0.04, `␣banks` 0.03 |
| 26 | …and the river bank → ? | `␣until` | 0.001 | 33 | `.` 0.44, `,` 0.16, `␣for` 0.10, `␣and` 0.06, `␣to` 0.03 |
| 27 | …the river bank until → ? | `␣it` | 0.007 | 7 | `␣they` 0.83, `␣the` 0.04, `␣finally` 0.03, `,` 0.01, `␣a` 0.01 |
| 28 | …river bank until it → ? | `␣grew` | 0.000 | 64 | `␣was` 0.68, `␣became` 0.06, `␣turned` 0.05, `␣came` 0.03, `␣finally` 0.02 |
| 29 | …bank until it grew → ? | `␣dark` | 0.288 | 1 | `␣dark` 0.29, `␣to` 0.12, `␣quiet` 0.04, `␣into` 0.04, `␣clear` 0.04 |
| 30 | …until it grew dark → ? | `.` | 0.492 | 1 | `.` 0.49, `␣and` 0.18, `,` 0.10, `␣again` 0.05, `.\n` 0.03 |
| 31 | …it grew dark. → ? | `␣The` | 0.093 | 2 | `␣They` 0.25, `␣The` 0.09, `␣Then` 0.07, `␣Max` 0.04, `␣But` 0.03 |
| 32 | …grew dark. The → ? | `␣next` | 0.023 | 5 | `␣dog` 0.10, `␣dogs` 0.07, `␣police` 0.04, `␣search` 0.03, `␣next` 0.02 |
| 33 | …dark. The next → ? | `␣morning` | 0.278 | 2 | `␣day` 0.46, `␣morning` 0.28, `␣night` 0.10, `␣thing` 0.05, `␣evening` 0.02 |
| 34 | …. The next morning → ? | `,` | 0.557 | 1 | `,` 0.56, `␣they` 0.17, `␣the` 0.08, `␣Max` 0.04, `␣when` 0.02 |
| 35 | …The next morning, → ? | `␣Max` | 0.109 | 3 | `␣they` 0.30, `␣the` 0.16, `␣Max` 0.11, `␣a` 0.06, `␣when` 0.04 |
| 36 | …next morning, Max → ? | `␣was` | 0.284 | 1 | `␣was` 0.28, `␣and` 0.08, `,` 0.05, `␣had` 0.05, `'s` 0.04 |
| 37 | …morning, Max was → ? | `␣found` | 0.179 | 1 | `␣found` 0.18, `␣spotted` 0.05, `␣still` 0.04, `␣gone` 0.03, `␣in` 0.03 |
| 38 | …, Max was found → ? | `␣asleep` | 0.002 | 61 | `.` 0.14, `␣in` 0.12, `,` 0.08, `␣by` 0.07, `␣and` 0.05 |
| 39 | …Max was found asleep → ? | `␣in` | 0.338 | 1 | `␣in` 0.34, `␣on` 0.22, `␣under` 0.05, `.` 0.05, `␣at` 0.04 |
| 40 | …was found asleep in → ? | `␣the` | 0.560 | 1 | `␣the` 0.56, `␣a` 0.28, `␣his` 0.09, `␣one` 0.02, `␣an` 0.01 |
| 41 | …found asleep in the → ? | `␣neighbour` | 0.000 | 551 | `␣bushes` 0.07, `␣woods` 0.06, `␣middle` 0.05, `␣river` 0.05, `␣tree` 0.03 |
| 42 | …asleep in the neighbour → ? | `'s` | 0.877 | 1 | `'s` 0.88, `’s` 0.10, `'s` 0.00, `´s` 0.00, `␣tree` 0.00 |
| 43 | …in the neighbour's → ? | `␣garden` | 0.392 | 1 | `␣garden` 0.39, `␣yard` 0.07, `␣house` 0.06, `␣backyard` 0.05, `␣tree` 0.03 |
| 44 | …the neighbour's garden → ? | `␣shed` | 0.003 | 19 | `.` 0.47, `,` 0.18, `.\n` 0.09, `␣and` 0.05, `.\n\n` 0.03 |
| 45 | …neighbour's garden shed → ? | `.` | 0.480 | 1 | `.` 0.48, `,` 0.15, `.\n` 0.10, `␣and` 0.05, `.\n\n` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣shed` | 0.000 | 5297 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← shed. | `␣garden` | 0.046 | 5 | `␣the` 0.18, `␣to` 0.07, `␣a` 0.07, `␣or` 0.07, `␣garden` 0.05 |
| 4 | ? ← garden shed. | `'s` | 0.003 | 20 | `␣a` 0.27, `␣the` 0.19, `␣your` 0.11, `␣or` 0.07, `␣A` 0.03 |
| 5 | ? ← 's garden shed. | `␣neighbour` | 0.066 | 2 | `␣neighbor` 0.09, `␣neighbour` 0.07, `␣friend` 0.05, `␣children` 0.03, `␣child` 0.03 |
| 6 | ? ← neighbour's garden shed… | `␣the` | 0.158 | 3 | `␣a` 0.35, `␣your` 0.22, `␣the` 0.16, `␣their` 0.06, `␣my` 0.05 |
| 7 | ? ← the neighbour's garden… | `␣in` | 0.264 | 1 | `␣in` 0.26, `␣of` 0.11, `␣from` 0.07, `␣In` 0.06, `␣to` 0.05 |
| 8 | ? ← in the neighbour's… | `␣asleep` | 0.001 | 214 | `␣or` 0.05, `␣found` 0.04, `␣up` 0.02, `␣it` 0.02, `␣stored` 0.02 |
| 9 | ? ← asleep in the neighbour… | `␣found` | 0.030 | 7 | `␣fell` 0.15, `␣fall` 0.15, `␣falling` 0.10, `␣was` 0.07, `␣fallen` 0.05 |
| 10 | ? ← found asleep in the… | `␣was` | 0.537 | 1 | `␣was` 0.54, `␣were` 0.07, `␣been` 0.07, `␣be` 0.05, `␣is` 0.03 |
| 11 | ? ← was found asleep in… | `␣Max` | 0.000 | 508 | `␣It` 0.10, `␣He` 0.08, `␣he` 0.07, `␣cat` 0.06, `␣it` 0.06 |
| 12 | ? ← Max was found asleep… | `,` | 0.120 | 2 | `:` 0.62, `,` 0.12, `␣named` 0.04, `␣that` 0.04, `␣when` 0.02 |
| 13 | ? ← , Max was found… | `␣morning` | 0.006 | 10 | `␣Yes` 0.25, `␣No` 0.22, `␣day` 0.02, `␣night` 0.01, `␣time` 0.01 |
| 14 | ? ← morning, Max was… | `␣next` | 0.219 | 1 | `␣next` 0.22, `␣the` 0.16, `␣One` 0.10, `␣one` 0.09, `␣following` 0.04 |
| 15 | ? ← next morning, Max… | `␣The` | 0.694 | 1 | `␣The` 0.69, `␣the` 0.22, `The` 0.04, `␣very` 0.02, `␣early` 0.00 |
| 16 | ? ← The next morning,… | `.` | 0.455 | 2 | `:` 0.51, `.` 0.45, `!` 0.01, `).` 0.00, `."` 0.00 |
| 17 | ? ← . The next morning… | `␣dark` | 0.001 | 110 | `␣night` 0.05, `␣house` 0.02, `␣bed` 0.02, `␣him` 0.02, `␣home` 0.02 |
| 18 | ? ← dark. The next… | `␣grew` | 0.012 | 9 | `␣the` 0.44, `␣after` 0.13, `␣until` 0.07, `␣before` 0.07, `␣was` 0.05 |
| 19 | ? ← grew dark. The… | `␣it` | 0.722 | 1 | `␣it` 0.72, `␣sky` 0.04, `␣night` 0.03, `␣and` 0.02, `␣day` 0.02 |
| 20 | ? ← it grew dark.… | `␣until` | 0.184 | 2 | `␣as` 0.35, `␣until` 0.18, `␣before` 0.13, `␣when` 0.12, `␣and` 0.08 |
| 21 | ? ← until it grew dark… | `␣bank` | 0.000 | 704 | `,` 0.05, `␣night` 0.04, `␣house` 0.03, `␣him` 0.03, `␣sleep` 0.02 |
| 22 | ? ← bank until it grew… | `␣river` | 0.082 | 2 | `␣the` 0.55, `␣river` 0.08, `␣snow` 0.05, `␣a` 0.04, `␣opposite` 0.02 |
| 23 | ? ← river bank until it… | `␣the` | 0.863 | 1 | `␣the` 0.86, `␣a` 0.05, `␣nearby` 0.01, `␣dry` 0.01, `␣muddy` 0.01 |
| 24 | ? ← the river bank until… | `␣and` | 0.002 | 22 | `␣on` 0.44, `␣along` 0.21, `␣by` 0.08, `␣to` 0.04, `␣near` 0.03 |
| 25 | ? ← and the river bank… | `␣woods` | 0.010 | 17 | `␣house` 0.06, `␣trees` 0.06, `␣tree` 0.05, `␣garden` 0.03, `␣pond` 0.03 |
| 26 | ? ← woods and the river… | `␣the` | 0.917 | 1 | `␣the` 0.92, `␣nearby` 0.02, `␣surrounding` 0.01, `,` 0.00, `␣of` 0.00 |
| 27 | ? ← the woods and the… | `,` | 0.008 | 14 | `␣in` 0.42, `␣through` 0.09, `␣around` 0.09, `␣exploring` 0.06, `␣into` 0.05 |
| 28 | ? ← , the woods and… | `␣park` | 0.028 | 7 | `␣garden` 0.17, `␣house` 0.06, `␣field` 0.06, `␣fields` 0.04, `␣yard` 0.03 |
| 29 | ? ← park, the woods… | `␣the` | 0.648 | 1 | `␣the` 0.65, `␣car` 0.23, `␣local` 0.04, `␣dog` 0.01, `␣nearby` 0.01 |
| 30 | ? ← the park, the… | `␣checked` | 0.000 | 86 | `␣in` 0.24, `␣around` 0.19, `␣exploring` 0.11, `␣through` 0.07, `␣explored` 0.06 |
| 31 | ? ← checked the park,… | `␣They` | 0.085 | 3 | `␣and` 0.17, `␣He` 0.14, `␣They` 0.08, `␣he` 0.08, `␣Max` 0.07 |
| 32 | ? ← They checked the park… | `.` | 0.907 | 1 | `.` 0.91, `:` 0.04, `."` 0.01, `!` 0.01, `".` 0.00 |
| 33 | ? ← . They checked the… | `␣search` | 0.001 | 257 | `␣night` 0.03, `␣house` 0.02, `␣him` 0.02, `␣home` 0.02, `␣Max` 0.01 |
| 34 | ? ← search. They checked… | `␣the` | 0.089 | 3 | `␣their` 0.31, `␣a` 0.24, `␣the` 0.09, `␣to` 0.07, `␣his` 0.03 |
| 35 | ? ← the search. They… | `␣joined` | 0.044 | 6 | `␣on` 0.13, `␣began` 0.12, `␣continued` 0.08, `␣started` 0.07, `␣in` 0.07 |
| 36 | ? ← joined the search.… | `␣street` | 0.000 | 750 | `,` 0.13, `␣and` 0.07, `␣dogs` 0.05, `␣Max` 0.03, `␣dog` 0.02 |
| 37 | ? ← street joined the search… | `␣whole` | 0.003 | 15 | `␣the` 0.81, `␣nearby` 0.02, `␣neighbouring` 0.01, `␣main` 0.01, `'s` 0.01 |
| 38 | ? ← whole street joined the… | `␣the` | 0.855 | 1 | `␣the` 0.86, `␣The` 0.06, `␣a` 0.04, `The` 0.02, `'s` 0.00 |
| 39 | ? ← the whole street joined… | `,` | 0.220 | 1 | `,` 0.22, `␣and` 0.20, `␣from` 0.15, `␣in` 0.05, `␣on` 0.03 |
| 40 | ? ← , the whole street… | `␣missing` | 0.001 | 160 | `␣night` 0.06, `␣morning` 0.04, `␣evening` 0.03, `␣later` 0.03, `␣day` 0.03 |
| 41 | ? ← missing, the whole… | `␣went` | 0.349 | 1 | `␣went` 0.35, `␣was` 0.34, `␣Max` 0.07, `␣gone` 0.03, `␣were` 0.03 |
| 42 | ? ← went missing, the… | `␣dog` | 0.037 | 3 | `␣Max` 0.63, `␣he` 0.06, `␣dog` 0.04, `,` 0.04, `␣first` 0.01 |
| 43 | ? ← dog went missing,… | `␣the` | 0.290 | 1 | `␣the` 0.29, `␣their` 0.23, `'s` 0.16, `␣his` 0.10, `␣her` 0.05 |
| 44 | ? ← the dog went missing… | `␣Max` | 0.000 | 51 | `␣When` 0.24, `␣when` 0.18, `When` 0.13, `␣after` 0.12, `␣as` 0.07 |
| 45 | ? ← Max the dog went… | `When` | 0.232 | 1 | `When` 0.23, `␣When` 0.22, `␣when` 0.17, `␣after` 0.07, `␣as` 0.06 |

---

## 12. job_interview

*Category: narrative*

> **Beginning:** Tom spent the whole weekend preparing for his job interview.  
> **Middle:** He researched the company, practised his answers and chose his best suit.  
> **Ending:** On Friday, he received a phone call offering him the position.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | do it, but I don't know how to do it. I want to do it, but I don't know how to do it. I want to do it, but I don't know how to do it. I want to do it, but I don't know how to do it. I want to do it, but I don't know how to do it. I want to do it, but I don't know how to do it," he said. ↵ | On Friday, he received a phone call offering him the position. |
| sample | because there's a certain amount of money involved in the game. ↵ "So this is my brother, who is a professional baseball player, and he plays about a million games per year. That, combined with the fact that he has scored a certain number of points per game, gives him odds that are about 1 in 7 million. ↵ "On top of that, his chances are close to a million. I don't know why it's higher than that," he said. ↵ | On Friday, he received a phone call offering him the position. |
| sample | out of solar cells. ↵  ↵ A friend told Heath that the US government had set up restrictions on his invention, and that he couldn't file a patent to protect his invention. ↵  ↵ However, Heath continued with his research for years, eventually getting a patent on his product — the solar cell — for $1.5 million just last year. ↵  ↵ Now, he is trying to get a contract from Tesla Energy Systems, a Silicon Valley solar company, for $100,000. ↵  ↵ | On Friday, he received a phone call offering him the position. |
| sample | very well. ↵  ↵ "I'm very happy with my relationship with the company," he said. ↵  ↵ It is important to know, however, that until he gets used to this job, he will never make a career out of it. ↵  ↵ "It's like anything else in this world. I'm not looking for a job. I'm not looking for a job, but I have a passion for it, and I want to work for it and I want that role in the future," he said. ↵  ↵ | On Friday, he received a phone call offering him the position. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Tom spent the whole weekend preparing for his job interview. | He was a little nervous, but he was determined to get the job. He was also a little nervous about the interview process. He was a little nervous about the interview process. He was a little nervous about the interview process. He was a little nervous about the interview process. He was a little nervous about the interview process. He was a little nervous about the interview process. He was a little nervous about the interview process. He was a little nervous about the interview process. |
| sample | Tom spent the whole weekend preparing for his job interview. | He was given a lot of work to do, and he had to sit and listen to the interviews for a long time. He had to try and listen to the interviews in the right order, but he didn't have the time to prepare. He had to go over the material and ask questions and he had to go over the material and answer questions. He had to make sure that he made sure that he had everything in his head before he went to see the interviews. He |
| sample | Tom spent the whole weekend preparing for his job interview. | He attended a meeting of the Executive Director of the Washington Office of the Justice Department. The meeting included numerous speakers, including the Secretary of the Treasury, the Secretary of Homeland Security, and the Secretary of the Interior. He was amazed at the complexity of the issues that the President of the United States had to grapple with. As a result, he was nervous. Tom was eager to go to the White House, but was concerned that he might not be able to |
| sample | Tom spent the whole weekend preparing for his job interview. | The interview he gave was for a new job opportunity, and this involved a lot of preparation. He had to prepare his resume, his cover letter, his job interview, his interview, and his presentation. He had to learn the basics of the company and of the position. He had to learn how to effectively speak to different people at different points in the interview. He had to learn how to handle different situations with a group of people. ↵ When he got to his job interview, |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.912 | 36% |
| Backward | previous-token (right context) | 1.018 | 36% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Tom` | 0.000 | 906 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Tom → ? | `␣spent` | 0.000 | 2562 | `ato` 0.30, `atoes` 0.24, `orrow` 0.08, `:` 0.03, `at` 0.01 |
| 3 | Tom spent → ? | `␣the` | 0.218 | 1 | `␣the` 0.22, `␣a` 0.15, `␣his` 0.10, `␣` 0.07, `␣most` 0.04 |
| 4 | Tom spent the → ? | `␣whole` | 0.014 | 16 | `␣first` 0.14, `␣last` 0.09, `␣summer` 0.08, `␣day` 0.07, `␣next` 0.06 |
| 5 | Tom spent the whole → ? | `␣weekend` | 0.023 | 10 | `␣day` 0.26, `␣summer` 0.07, `␣of` 0.07, `␣time` 0.05, `␣week` 0.05 |
| 6 | …spent the whole weekend → ? | `␣preparing` | 0.005 | 27 | `␣in` 0.10, `␣at` 0.08, `␣with` 0.05, `␣working` 0.03, `␣making` 0.02 |
| 7 | …the whole weekend preparing → ? | `␣for` | 0.415 | 1 | `␣for` 0.42, `␣and` 0.10, `␣his` 0.09, `␣the` 0.08, `,` 0.04 |
| 8 | …whole weekend preparing for → ? | `␣his` | 0.184 | 2 | `␣the` 0.37, `␣his` 0.18, `␣a` 0.07, `␣this` 0.05, `␣my` 0.01 |
| 9 | …weekend preparing for his → ? | `␣job` | 0.001 | 88 | `␣first` 0.09, `␣trip` 0.05, `␣` 0.05, `␣upcoming` 0.04, `␣new` 0.02 |
| 10 | …preparing for his job → ? | `␣interview` | 0.143 | 2 | `␣as` 0.23, `␣interview` 0.14, `.` 0.10, `,` 0.10, `␣at` 0.06 |
| 11 | …for his job interview → ? | `.` | 0.316 | 1 | `.` 0.32, `,` 0.21, `␣and` 0.11, `␣with` 0.06, `␣at` 0.05 |
| 12 | …his job interview. → ? | `␣He` | 0.453 | 1 | `␣He` 0.45, `␣His` 0.03, `␣The` 0.03, `␣It` 0.02, `␣But` 0.02 |
| 13 | …job interview. He → ? | `␣researched` | 0.007 | 29 | `␣was` 0.11, `␣had` 0.08, `␣worked` 0.03, `␣went` 0.02, `␣spent` 0.02 |
| 14 | …interview. He researched → ? | `␣the` | 0.355 | 1 | `␣the` 0.35, `␣and` 0.08, `␣his` 0.05, `␣different` 0.04, `,` 0.03 |
| 15 | …. He researched the → ? | `␣company` | 0.204 | 1 | `␣company` 0.20, `␣job` 0.09, `␣different` 0.05, `␣city` 0.04, `␣industry` 0.02 |
| 16 | …He researched the company → ? | `,` | 0.294 | 1 | `,` 0.29, `'s` 0.24, `␣and` 0.21, `␣he` 0.04, `␣thoroughly` 0.03 |
| 17 | …researched the company, → ? | `␣pract` | 0.000 | 471 | `␣the` 0.09, `␣its` 0.08, `␣learned` 0.06, `␣interviewed` 0.04, `␣read` 0.04 |
| 18 | …the company, pract → ? | `ised` | 0.987 | 1 | `ised` 0.99, `ic` 0.01, `ising` 0.00, `ized` 0.00, `iced` 0.00 |
| 19 | …company, practised → ? | `␣his` | 0.425 | 1 | `␣his` 0.42, `␣the` 0.07, `␣for` 0.06, `␣interview` 0.05, `,` 0.03 |
| 20 | …, practised his → ? | `␣answers` | 0.008 | 20 | `␣presentation` 0.18, `␣speech` 0.17, `␣interview` 0.13, `␣resume` 0.03, `␣public` 0.03 |
| 21 | …practised his answers → ? | `␣and` | 0.158 | 3 | `,` 0.34, `␣to` 0.19, `␣and` 0.16, `␣in` 0.08, `␣on` 0.06 |
| 22 | …ised his answers and → ? | `␣chose` | 0.000 | 260 | `␣prepared` 0.05, `␣even` 0.04, `␣was` 0.03, `␣made` 0.03, `␣wrote` 0.03 |
| 23 | …his answers and chose → ? | `␣his` | 0.110 | 3 | `␣the` 0.50, `␣a` 0.18, `␣his` 0.11, `␣an` 0.03, `␣to` 0.03 |
| 24 | …answers and chose his → ? | `␣best` | 0.076 | 2 | `␣favourite` 0.16, `␣best` 0.08, `␣ideal` 0.07, `␣perfect` 0.05, `␣most` 0.03 |
| 25 | …and chose his best → ? | `␣suit` | 0.002 | 39 | `␣answer` 0.19, `␣answers` 0.12, `.` 0.07, `␣response` 0.05, `␣responses` 0.04 |
| 26 | …chose his best suit → ? | `.` | 0.473 | 1 | `.` 0.47, `␣for` 0.14, `␣of` 0.09, `␣to` 0.05, `,` 0.05 |
| 27 | …his best suit. → ? | `␣On` | 0.008 | 18 | `␣He` 0.42, `␣His` 0.04, `␣The` 0.04, `␣Tom` 0.03, `␣After` 0.03 |
| 28 | …best suit. On → ? | `␣Friday` | 0.060 | 4 | `␣the` 0.42, `␣Monday` 0.12, `␣his` 0.09, `␣Friday` 0.06, `␣Saturday` 0.04 |
| 29 | …suit. On Friday → ? | `,` | 0.383 | 1 | `,` 0.38, `␣he` 0.16, `␣morning` 0.12, `␣night` 0.09, `␣evening` 0.08 |
| 30 | …. On Friday, → ? | `␣he` | 0.505 | 1 | `␣he` 0.51, `␣Tom` 0.13, `␣the` 0.09, `␣his` 0.03, `␣` 0.02 |
| 31 | …On Friday, he → ? | `␣received` | 0.016 | 12 | `␣was` 0.11, `␣went` 0.06, `␣got` 0.04, `␣took` 0.03, `␣sat` 0.03 |
| 32 | …Friday, he received → ? | `␣a` | 0.263 | 2 | `␣his` 0.28, `␣a` 0.26, `␣the` 0.24, `␣an` 0.12, `␣feedback` 0.01 |
| 33 | …, he received a → ? | `␣phone` | 0.059 | 3 | `␣letter` 0.13, `␣call` 0.10, `␣phone` 0.06, `␣job` 0.05, `␣copy` 0.02 |
| 34 | …he received a phone → ? | `␣call` | 0.973 | 1 | `␣call` 0.97, `␣interview` 0.01, `␣invitation` 0.00, `␣message` 0.00, `␣from` 0.00 |
| 35 | …received a phone call → ? | `␣offering` | 0.002 | 24 | `␣from` 0.73, `.` 0.03, `␣and` 0.03, `,` 0.02, `␣to` 0.02 |
| 36 | …a phone call offering → ? | `␣him` | 0.125 | 3 | `␣to` 0.27, `␣a` 0.25, `␣him` 0.13, `␣an` 0.06, `␣his` 0.05 |
| 37 | …phone call offering him → ? | `␣the` | 0.120 | 2 | `␣a` 0.51, `␣the` 0.12, `␣an` 0.09, `␣$` 0.04, `␣his` 0.03 |
| 38 | …call offering him the → ? | `␣position` | 0.112 | 4 | `␣opportunity` 0.28, `␣job` 0.25, `␣chance` 0.16, `␣position` 0.11, `␣interview` 0.02 |
| 39 | …offering him the position → ? | `.` | 0.367 | 1 | `.` 0.37, `␣of` 0.20, `.\n` 0.08, `␣at` 0.04, `,` 0.04 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣position` | 0.000 | 286 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← position. | `␣the` | 0.023 | 3 | `'s` 0.03, `␣upright` 0.02, `␣the` 0.02, `␣original` 0.02, `␣this` 0.02 |
| 4 | ? ← the position. | `␣him` | 0.001 | 108 | `␣for` 0.29, `␣of` 0.13, `␣in` 0.07, `␣to` 0.06, `␣on` 0.05 |
| 5 | ? ← him the position. | `␣offering` | 0.012 | 15 | `␣give` 0.17, `␣offered` 0.07, `␣gave` 0.07, `␣giving` 0.06, `␣cost` 0.05 |
| 6 | ? ← offering him the position… | `␣call` | 0.000 | 195 | `␣for` 0.15, `␣by` 0.08, `␣before` 0.08, `␣and` 0.05, `␣is` 0.04 |
| 7 | ? ← call offering him the… | `␣phone` | 0.199 | 1 | `␣phone` 0.20, `␣a` 0.19, `␣the` 0.09, `␣to` 0.05, `␣conference` 0.05 |
| 8 | ? ← phone call offering him… | `␣a` | 0.614 | 1 | `␣a` 0.61, `␣the` 0.12, `'s` 0.02, `␣A` 0.01, `␣or` 0.01 |
| 9 | ? ← a phone call offering… | `␣received` | 0.221 | 1 | `␣received` 0.22, `␣got` 0.09, `␣him` 0.07, `␣made` 0.05, `␣get` 0.05 |
| 10 | ? ← received a phone call… | `␣he` | 0.172 | 1 | `␣he` 0.17, `␣He` 0.08, `␣and` 0.06, `␣just` 0.03, `,` 0.03 |
| 11 | ? ← he received a phone… | `,` | 0.213 | 1 | `,` 0.21, `␣when` 0.20, `␣after` 0.09, `␣that` 0.08, `␣and` 0.06 |
| 12 | ? ← , he received a… | `␣Friday` | 0.002 | 87 | `␣Yes` 0.09, `␣later` 0.06, `␣No` 0.04, `␣day` 0.03, `␣year` 0.01 |
| 13 | ? ← Friday, he received… | `␣On` | 0.398 | 1 | `␣On` 0.40, `␣on` 0.29, `␣Last` 0.05, `␣last` 0.05, `.` 0.04 |
| 14 | ? ← On Friday, he… | `.` | 0.890 | 1 | `.` 0.89, `:` 0.06, `."` 0.02, `).` 0.00, `.”` 0.00 |
| 15 | ? ← . On Friday,… | `␣suit` | 0.000 | 398 | `␣said` 0.02, `␣position` 0.01, `␣year` 0.01, `␣him` 0.01, `␣years` 0.01 |
| 16 | ? ← suit. On Friday… | `␣best` | 0.000 | 143 | `␣follow` 0.26, `␣the` 0.16, `␣law` 0.12, `␣followed` 0.10, `␣his` 0.04 |
| 17 | ? ← best suit. On… | `␣his` | 0.217 | 2 | `␣the` 0.53, `␣his` 0.22, `␣would` 0.07, `'s` 0.03, `␣their` 0.01 |
| 18 | ? ← his best suit.… | `␣chose` | 0.003 | 35 | `␣be` 0.17, `␣in` 0.15, `␣was` 0.08, `␣is` 0.07, `␣for` 0.03 |
| 19 | ? ← chose his best suit… | `␣and` | 0.164 | 2 | `␣he` 0.23, `␣and` 0.16, `␣to` 0.12, `'t` 0.02, `,` 0.02 |
| 20 | ? ← and chose his best… | `␣answers` | 0.000 | 1364 | `,` 0.09, `␣position` 0.02, `␣job` 0.02, `␣interview` 0.02, `␣him` 0.01 |
| 21 | ? ← answers and chose his… | `␣his` | 0.118 | 2 | `␣the` 0.33, `␣his` 0.12, `␣for` 0.08, `␣their` 0.03, `'s` 0.03 |
| 22 | ? ← his answers and chose… | `ised` | 0.001 | 77 | `␣reviewed` 0.19, `␣through` 0.06, `␣on` 0.04, `␣discussed` 0.04, `␣down` 0.04 |
| 23 | ? ← ised his answers and… | `␣pract` | 0.007 | 7 | `in` 0.68, `␣final` 0.17, `␣priorit` 0.04, `␣strateg` 0.03, `␣appra` 0.01 |
| 24 | ? ← practised his answers… | `,` | 0.191 | 2 | `␣he` 0.32, `,` 0.19, `␣He` 0.10, `␣then` 0.03, `␣and` 0.02 |
| 25 | ? ← , practised his… | `␣company` | 0.005 | 16 | `␣questions` 0.04, `␣interview` 0.03, `␣interviews` 0.02, `␣position` 0.02, `␣suit` 0.01 |
| 26 | ? ← company, practised… | `␣the` | 0.421 | 1 | `␣the` 0.42, `␣his` 0.07, `␣a` 0.02, `␣insurance` 0.02, `'s` 0.02 |
| 27 | ? ← the company, pract… | `␣researched` | 0.014 | 13 | `␣of` 0.15, `␣at` 0.14, `␣for` 0.13, `␣in` 0.10, `␣about` 0.06 |
| 28 | ? ← researched the company,… | `␣He` | 0.200 | 1 | `␣He` 0.20, `␣he` 0.19, `,` 0.13, `He` 0.02, `␣had` 0.02 |
| 29 | ? ← He researched the company… | `.` | 0.928 | 1 | `.` 0.93, `."` 0.02, `?` 0.01, `".` 0.01, `:` 0.01 |
| 30 | ? ← . He researched the… | `␣interview` | 0.014 | 4 | `␣position` 0.04, `␣job` 0.03, `␣company` 0.02, `␣interview` 0.01, `␣manager` 0.01 |
| 31 | ? ← interview. He researched… | `␣job` | 0.204 | 2 | `␣an` 0.31, `␣job` 0.20, `␣the` 0.16, `␣his` 0.03, `␣for` 0.02 |
| 32 | ? ← job interview. He… | `␣his` | 0.105 | 2 | `␣a` 0.52, `␣his` 0.10, `␣the` 0.08, `␣first` 0.03, `␣recent` 0.02 |
| 33 | ? ← his job interview.… | `␣for` | 0.483 | 1 | `␣for` 0.48, `␣before` 0.07, `␣in` 0.07, `␣during` 0.05, `␣to` 0.05 |
| 34 | ? ← for his job interview… | `␣preparing` | 0.045 | 3 | `␣prepare` 0.08, `␣suit` 0.07, `␣preparing` 0.04, `␣ready` 0.04, `␣position` 0.02 |
| 35 | ? ← preparing for his job… | `␣weekend` | 0.003 | 34 | `␣was` 0.30, `␣started` 0.03, `,` 0.03, `␣while` 0.03, `␣been` 0.03 |
| 36 | ? ← weekend preparing for his… | `␣whole` | 0.026 | 7 | `␣the` 0.66, `␣last` 0.06, `␣a` 0.06, `␣this` 0.04, `␣all` 0.03 |
| 37 | ? ← whole weekend preparing for… | `␣the` | 0.793 | 1 | `␣the` 0.79, `␣a` 0.19, `␣his` 0.01, `␣one` 0.00, `␣this` 0.00 |
| 38 | ? ← the whole weekend preparing… | `␣spent` | 0.916 | 1 | `␣spent` 0.92, `␣spend` 0.03, `␣spending` 0.01, `ent` 0.00, `␣of` 0.00 |
| 39 | ? ← spent the whole weekend… | `Tom` | 0.000 | 740 | `,` 0.12, `␣He` 0.06, `␣has` 0.06, `␣he` 0.06, `␣and` 0.05 |

---

## 13. photosynthesis

*Category: factual*

> **Beginning:** Plants capture energy from sunlight using a pigment called chlorophyll.  
> **Middle:** In a process called photosynthesis, they use this energy to turn carbon dioxide and water into glucose.  
> **Ending:** Oxygen is released into the air as a by-product of this process.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | of energy. ↵  ↵ Glucose is used as a source of energy. ↵  ↵ Glucose is used as a source of energy. ↵  ↵ Glucose is used as a source of energy. ↵  ↵ Glucose is used as a source of energy. ↵  ↵ Glucose is used as a source of energy. ↵  ↵ As a source of energy, cells store energy in the form of glucose. ↵  ↵ Glucose is used in the process of cellular respiration. ↵  ↵ In the process of cellular respiration, glucose is broken down into carbon dioxide and water. ↵  ↵ | Oxygen is released into the air as a by-product of this process. |
| sample | → carbon dioxide + water ↵  ↵ Photosynthesis is the process when a plant uses the sun's energy, and oxygen to produce carbohydrates from carbon dioxide and water in the presence of light. ↵  ↵ In order to carry out the process of photosynthesis, plants ↵ require oxygen. The chemical reaction for the process of ↵ photosynthesis is ↵  ↵ CO2 + 2H2O → carbon + ↵ oxygen ↵  ↵ When a carbon atom combines with oxygen, the products are ↵ carbon dioxide and water. ↵  ↵ | Oxygen is released into the air as a by-product of this process. |
| sample | the leaves of a plant that allow water, nutrients, and oxygen to move in and out of the cells. ↵  ↵ Stomata or stomata enable carbon dioxide to move out of the plant and water to move out of the plant. ↵  ↵ Plasmodesmata are tiny holes in the cell membrane that allow carbon dioxide and water to move in and move out of plant cells. ↵  ↵ Photosynthesis is a process through which carbon dioxide from the atmosphere is used to turn carbon dioxide and water into carbohydrates. ↵ | Oxygen is released into the air as a by-product of this process. |
| sample | components are hydrogen and a small amount of oxygen. Oxygen is denser than water. ↵ Oxygen is the lightest element found in Earth’s atmosphere. It is vital for life. ↵ Water consists of hydrogen and oxygen on Earth. Both are necessary for life on Earth. ↵ The main source of water on Earth is the atmosphere, which is made up of hydrogen and oxygen. ↵ During photosynthesis, hydrogen and oxygen react in the presence of air in the presence of sunlight, producing carbon dioxide and water. ↵ | Oxygen is released into the air as a by-product of this process. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Plants capture energy from sunlight using a pigment called chlorophyll. | Chlorophyll is a green pigment that absorbs light energy and converts it into chemical energy. This chemical energy is then used to power the plant's growth and development. ↵ The process of photosynthesis is a complex and intricate one. It involves the absorption of light energy by chlorophyll, which then converts it into chemical energy. This chemical energy is then used to power the plant's growth and development. ↵ The process of photosynthesis is a complex and intricate one. It involves the absorption of light energy by chlorophyll |
| sample | Plants capture energy from sunlight using a pigment called chlorophyll. | Chlorophyll molecules are packed like bricks in a solar cell. The absorption of photons by chlorophyll molecules, and the release of electrons, creates a flow of energy in the form of an electric current. This electric current runs through the wire filament that is the part of the cell that is exposed to the solar radiation and is therefore the part of the cell that is most exposed to the solar radiation. ↵ Each of the molecules on the solar cell is made up of a protein chain, which will |
| sample | Plants capture energy from sunlight using a pigment called chlorophyll. | The leaves of plants contain a lot of chlorophyll and each leaf is responsible for the green pigment. Chlorophyll is a green pigment that is found in plants and algae. It is found in the chloroplasts of leaves and also in the cell walls of fungi. ↵ Chlorophyll is the green pigment of plants and algae and is an important part of a plant’s photosynthesis process. Chlorophyll absorbs light energy from the sun and then converts that energy to chemical energy. This process is called photosynthesis |
| sample | Plants capture energy from sunlight using a pigment called chlorophyll. | This pigment consists of a copper-containing molecule called cupric oxide or Cu2O. It is a green pigment, but it is also the pigment that plants use to photosynthesise. It gives plants their green colour, which comes from the absorption of energy from light. ↵ How do plants absorb sunlight? ↵ Plants can absorb sunlight. When sunlight hits a plant, it causes an enzyme in the plant's cells to be broken down. This releases chemical energy, which the plant uses to |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.401 | 61% |
| Backward | previous-token (right context) | 0.406 | 57% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Plants` | 0.000 | 553 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Plants → ? | `␣capture` | 0.000 | 291 | `␣are` 0.11, `␣that` 0.06, `␣and` 0.06, `,` 0.04, `␣for` 0.04 |
| 3 | Plants capture → ? | `␣energy` | 0.049 | 6 | `␣carbon` 0.28, `␣the` 0.10, `␣CO` 0.09, `␣sunlight` 0.08, `␣light` 0.07 |
| 4 | Plants capture energy → ? | `␣from` | 0.728 | 1 | `␣from` 0.73, `␣through` 0.05, `␣and` 0.05, `␣in` 0.05, `␣by` 0.02 |
| 5 | Plants capture energy from → ? | `␣sunlight` | 0.206 | 2 | `␣the` 0.70, `␣sunlight` 0.21, `␣light` 0.03, `␣solar` 0.01, `␣sun` 0.01 |
| 6 | …capture energy from sunlight → ? | `␣using` | 0.052 | 5 | `␣and` 0.36, `,` 0.12, `␣through` 0.11, `␣to` 0.08, `␣using` 0.05 |
| 7 | …energy from sunlight using → ? | `␣a` | 0.119 | 4 | `␣the` 0.18, `␣chlorophyll` 0.16, `␣their` 0.12, `␣a` 0.12, `␣photosynthesis` 0.07 |
| 8 | …from sunlight using a → ? | `␣pigment` | 0.038 | 2 | `␣process` 0.58, `␣pigment` 0.04, `␣series` 0.03, `␣chemical` 0.03, `␣special` 0.03 |
| 9 | …sunlight using a pigment → ? | `␣called` | 0.627 | 1 | `␣called` 0.63, `␣in` 0.06, `␣known` 0.06, `,` 0.04, `␣molecule` 0.02 |
| 10 | …using a pigment called → ? | `␣chlorophyll` | 0.930 | 1 | `␣chlorophyll` 0.93, `␣Chlor` 0.01, `␣chloropl` 0.01, `␣"` 0.01, `␣the` 0.00 |
| 11 | …a pigment called chlorophyll → ? | `.` | 0.520 | 1 | `.` 0.52, `,` 0.23, `␣and` 0.03, `␣that` 0.03, `␣in` 0.03 |
| 12 | …pigment called chlorophyll. → ? | `␣In` | 0.031 | 8 | `␣Chlor` 0.19, `␣This` 0.15, `␣The` 0.14, `␣When` 0.04, `␣They` 0.03 |
| 13 | …called chlorophyll. In → ? | `␣a` | 0.058 | 6 | `␣the` 0.19, `␣photosynthesis` 0.09, `␣plants` 0.09, `␣this` 0.09, `␣order` 0.08 |
| 14 | …chlorophyll. In a → ? | `␣process` | 0.471 | 1 | `␣process` 0.47, `␣plant` 0.05, `␣leaf` 0.03, `␣typical` 0.02, `␣healthy` 0.01 |
| 15 | …. In a process → ? | `␣called` | 0.814 | 1 | `␣called` 0.81, `␣known` 0.13, `␣that` 0.01, `␣similar` 0.01, `␣of` 0.01 |
| 16 | …In a process called → ? | `␣photosynthesis` | 0.944 | 1 | `␣photosynthesis` 0.94, `␣phot` 0.02, `␣the` 0.01, `␣Photos` 0.00, `␣light` 0.00 |
| 17 | …a process called photosynthesis → ? | `,` | 0.931 | 1 | `,` 0.93, `␣plants` 0.02, `␣the` 0.01, `␣(` 0.00, `␣,` 0.00 |
| 18 | …process called photosynthesis, → ? | `␣they` | 0.022 | 8 | `␣plants` 0.32, `␣the` 0.21, `␣chlorophyll` 0.19, `␣a` 0.04, `␣sunlight` 0.03 |
| 19 | …called photosynthesis, they → ? | `␣use` | 0.368 | 1 | `␣use` 0.37, `␣convert` 0.17, `␣take` 0.07, `␣absorb` 0.05, `␣turn` 0.03 |
| 20 | …photosynthesis, they use → ? | `␣this` | 0.236 | 2 | `␣the` 0.25, `␣this` 0.24, `␣sunlight` 0.12, `␣that` 0.10, `␣carbon` 0.09 |
| 21 | …, they use this → ? | `␣energy` | 0.834 | 1 | `␣energy` 0.83, `␣light` 0.02, `␣to` 0.02, `␣chemical` 0.02, `␣sunlight` 0.02 |
| 22 | …they use this energy → ? | `␣to` | 0.942 | 1 | `␣to` 0.94, `␣and` 0.02, `␣in` 0.01, `,` 0.01, `␣from` 0.00 |
| 23 | …use this energy to → ? | `␣turn` | 0.079 | 4 | `␣convert` 0.23, `␣make` 0.19, `␣produce` 0.11, `␣turn` 0.08, `␣build` 0.05 |
| 24 | …this energy to turn → ? | `␣carbon` | 0.521 | 1 | `␣carbon` 0.52, `␣water` 0.33, `␣CO` 0.03, `␣the` 0.03, `␣it` 0.02 |
| 25 | …energy to turn carbon → ? | `␣dioxide` | 0.987 | 1 | `␣dioxide` 0.99, `␣from` 0.00, `-d` 0.00, `␣compounds` 0.00, `␣and` 0.00 |
| 26 | …to turn carbon dioxide → ? | `␣and` | 0.609 | 1 | `␣and` 0.61, `␣into` 0.21, `,` 0.09, `␣(` 0.05, `␣from` 0.02 |
| 27 | …turn carbon dioxide and → ? | `␣water` | 0.987 | 1 | `␣water` 0.99, `␣other` 0.00, `␣sunlight` 0.00, `␣the` 0.00, `␣light` 0.00 |
| 28 | …carbon dioxide and water → ? | `␣into` | 0.942 | 1 | `␣into` 0.94, `,` 0.01, `␣from` 0.01, `␣molecules` 0.01, `␣to` 0.01 |
| 29 | …dioxide and water into → ? | `␣glucose` | 0.242 | 1 | `␣glucose` 0.24, `␣sugars` 0.18, `␣carbohydrates` 0.12, `␣sugar` 0.11, `␣oxygen` 0.07 |
| 30 | …and water into glucose → ? | `.` | 0.142 | 3 | `␣and` 0.37, `,` 0.26, `.` 0.14, `␣(` 0.10, `.\n` 0.02 |
| 31 | …water into glucose. → ? | `␣Oxygen` | 0.011 | 13 | `␣This` 0.17, `␣The` 0.17, `␣Gl` 0.06, `␣Plants` 0.06, `␣In` 0.05 |
| 32 | …into glucose. Oxygen → ? | `␣is` | 0.677 | 1 | `␣is` 0.68, `,` 0.09, `␣and` 0.05, `␣gas` 0.03, `␣from` 0.03 |
| 33 | …glucose. Oxygen is → ? | `␣released` | 0.481 | 1 | `␣released` 0.48, `␣produced` 0.12, `␣a` 0.09, `␣also` 0.06, `␣the` 0.04 |
| 34 | …. Oxygen is released → ? | `␣into` | 0.151 | 2 | `␣as` 0.51, `␣into` 0.15, `,` 0.06, `␣from` 0.05, `␣during` 0.05 |
| 35 | …Oxygen is released into → ? | `␣the` | 0.988 | 1 | `␣the` 0.99, `␣our` 0.00, `␣their` 0.00, `␣a` 0.00, `␣atmosphere` 0.00 |
| 36 | …is released into the → ? | `␣air` | 0.230 | 2 | `␣atmosphere` 0.73, `␣air` 0.23, `␣environment` 0.02, `␣water` 0.01, `␣surrounding` 0.00 |
| 37 | …released into the air → ? | `␣as` | 0.254 | 1 | `␣as` 0.25, `,` 0.18, `.` 0.16, `.\n` 0.07, `␣and` 0.07 |
| 38 | …into the air as → ? | `␣a` | 0.885 | 1 | `␣a` 0.88, `␣waste` 0.03, `␣the` 0.03, `␣by` 0.01, `␣part` 0.01 |
| 39 | …the air as a → ? | `␣by` | 0.510 | 1 | `␣by` 0.51, `␣byproduct` 0.25, `␣waste` 0.21, `␣result` 0.02, `␣product` 0.00 |
| 40 | …air as a by → ? | `-product` | 0.963 | 1 | `-product` 0.96, `␣product` 0.03, `product` 0.00, `-` 0.00, `�` 0.00 |
| 41 | …as a by-product → ? | `␣of` | 0.357 | 1 | `␣of` 0.36, `.` 0.25, `.\n` 0.21, `,` 0.06, `.\n\n` 0.06 |
| 42 | …a by-product of → ? | `␣this` | 0.297 | 2 | `␣the` 0.39, `␣this` 0.30, `␣photosynthesis` 0.28, `␣respiration` 0.01, `␣their` 0.00 |
| 43 | …by-product of this → ? | `␣process` | 0.836 | 1 | `␣process` 0.84, `␣reaction` 0.10, `␣chemical` 0.03, `␣energy` 0.00, `.` 0.00 |
| 44 | …-product of this process → ? | `.` | 0.432 | 1 | `.` 0.43, `.\n` 0.36, `.\n\n` 0.10, `,` 0.06, `␣and` 0.01 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣process` | 0.002 | 21 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← process. | `␣this` | 0.036 | 2 | `␣the` 0.16, `␣this` 0.04, `␣learning` 0.03, `␣healing` 0.02, `␣manufacturing` 0.02 |
| 4 | ? ← this process. | `␣of` | 0.106 | 3 | `␣in` 0.24, `␣during` 0.11, `␣of` 0.11, `␣through` 0.07, `␣for` 0.05 |
| 5 | ? ← of this process. | `-product` | 0.002 | 78 | `␣part` 0.22, `␣result` 0.04, `␣understanding` 0.03, `␣step` 0.02, `␣example` 0.02 |
| 6 | ? ← -product of this process… | `␣by` | 0.912 | 1 | `␣by` 0.91, `␣end` 0.04, `␣bi` 0.03, `by` 0.00, `␣co` 0.00 |
| 7 | ? ← by-product of this… | `␣a` | 0.679 | 1 | `␣a` 0.68, `␣natural` 0.08, `␣inevitable` 0.02, `␣the` 0.02, `␣important` 0.01 |
| 8 | ? ← a by-product of… | `␣as` | 0.300 | 2 | `␣is` 0.39, `␣as` 0.30, `␣are` 0.06, `␣be` 0.04, `␣just` 0.02 |
| 9 | ? ← as a by-product… | `␣air` | 0.008 | 15 | `␣produced` 0.16, `␣created` 0.08, `␣formed` 0.05, `␣released` 0.03, `␣generated` 0.03 |
| 10 | ? ← air as a by… | `␣the` | 0.602 | 1 | `␣the` 0.60, `␣clean` 0.03, `␣of` 0.03, `␣hot` 0.02, `␣indoor` 0.02 |
| 11 | ? ← the air as a… | `␣into` | 0.592 | 1 | `␣into` 0.59, `␣from` 0.13, `␣in` 0.13, `␣to` 0.05, `␣of` 0.03 |
| 12 | ? ← into the air as… | `␣released` | 0.391 | 1 | `␣released` 0.39, `␣emitted` 0.05, `␣methane` 0.03, `␣back` 0.03, `␣dioxide` 0.03 |
| 13 | ? ← released into the air… | `␣is` | 0.457 | 1 | `␣is` 0.46, `␣are` 0.21, `␣be` 0.12, `␣also` 0.04, `␣being` 0.03 |
| 14 | ? ← is released into the… | `␣Oxygen` | 0.034 | 5 | `␣dioxide` 0.23, `2` 0.09, `␣which` 0.04, `␣gas` 0.04, `␣Oxygen` 0.03 |
| 15 | ? ← Oxygen is released into… | `.` | 0.751 | 1 | `.` 0.75, `:` 0.19, `).` 0.02, `␣…` 0.00, `!` 0.00 |
| 16 | ? ← . Oxygen is released… | `␣glucose` | 0.045 | 2 | `␣energy` 0.06, `␣glucose` 0.05, `␣water` 0.04, `␣sugars` 0.03, `␣dioxide` 0.03 |
| 17 | ? ← glucose. Oxygen is… | `␣into` | 0.201 | 1 | `␣into` 0.20, `␣of` 0.13, `␣make` 0.09, `␣and` 0.09, `␣produce` 0.09 |
| 18 | ? ← into glucose. Oxygen… | `␣water` | 0.149 | 2 | `␣dioxide` 0.25, `␣water` 0.15, `␣it` 0.11, `␣converted` 0.06, `␣down` 0.05 |
| 19 | ? ← water into glucose.… | `␣and` | 0.971 | 1 | `␣and` 0.97, `␣of` 0.00, `␣convert` 0.00, `␣plus` 0.00, `␣with` 0.00 |
| 20 | ? ← and water into glucose… | `␣dioxide` | 0.882 | 1 | `␣dioxide` 0.88, `,` 0.08, `2` 0.02, `)` 0.01, `␣air` 0.00 |
| 21 | ? ← dioxide and water into… | `␣carbon` | 0.998 | 1 | `␣carbon` 1.00, `␣Carbon` 0.00, `carbon` 0.00, `␣sulfur` 0.00, `,` 0.00 |
| 22 | ? ← carbon dioxide and water… | `␣turn` | 0.101 | 3 | `␣convert` 0.46, `␣converts` 0.12, `␣turn` 0.10, `␣transform` 0.07, `␣converting` 0.05 |
| 23 | ? ← turn carbon dioxide and… | `␣to` | 0.919 | 1 | `␣to` 0.92, `␣they` 0.01, `␣and` 0.01, `␣plants` 0.01, `␣that` 0.01 |
| 24 | ? ← to turn carbon dioxide… | `␣energy` | 0.211 | 2 | `␣sunlight` 0.29, `␣energy` 0.21, `␣used` 0.15, `␣sun` 0.08, `␣light` 0.02 |
| 25 | ? ← energy to turn carbon… | `␣this` | 0.039 | 5 | `␣light` 0.37, `'s` 0.21, `␣solar` 0.09, `␣sunlight` 0.08, `␣this` 0.04 |
| 26 | ? ← this energy to turn… | `␣use` | 0.694 | 1 | `␣use` 0.69, `␣uses` 0.19, `␣using` 0.05, `␣of` 0.02, `␣utilize` 0.01 |
| 27 | ? ← use this energy to… | `␣they` | 0.070 | 4 | `␣and` 0.29, `␣They` 0.12, `␣plants` 0.08, `␣they` 0.07, `␣then` 0.07 |
| 28 | ? ← they use this energy… | `,` | 0.377 | 2 | `␣and` 0.40, `,` 0.38, `␣where` 0.05, `␣then` 0.03, `␣Then` 0.02 |
| 29 | ? ← , they use this… | `␣photosynthesis` | 0.131 | 2 | `␣sunlight` 0.18, `␣photosynthesis` 0.13, `␣sun` 0.09, `␣energy` 0.06, `␣light` 0.04 |
| 30 | ? ← photosynthesis, they use… | `␣called` | 0.060 | 6 | `␣of` 0.37, `␣during` 0.12, `␣During` 0.08, `␣through` 0.07, `␣perform` 0.07 |
| 31 | ? ← called photosynthesis, they… | `␣process` | 0.925 | 1 | `␣process` 0.92, `,` 0.04, `␣reaction` 0.01, `␣is` 0.01, `␣procedure` 0.00 |
| 32 | ? ← process called photosynthesis,… | `␣a` | 0.958 | 1 | `␣a` 0.96, `␣the` 0.01, `␣chemical` 0.01, `␣natural` 0.00, `␣complex` 0.00 |
| 33 | ? ← a process called photosynthesis… | `␣In` | 0.290 | 1 | `␣In` 0.29, `␣Through` 0.23, `␣in` 0.21, `␣through` 0.14, `␣Using` 0.04 |
| 34 | ? ← In a process called… | `.` | 0.964 | 1 | `.` 0.96, `).` 0.02, `␣…` 0.00, `:` 0.00, `␣.` 0.00 |
| 35 | ? ← . In a process… | `␣chlorophyll` | 0.017 | 6 | `␣sunlight` 0.32, `␣sun` 0.21, `␣energy` 0.19, `␣light` 0.06, `␣food` 0.02 |
| 36 | ? ← chlorophyll. In a… | `␣called` | 0.595 | 1 | `␣called` 0.59, `␣pigment` 0.13, `␣using` 0.05, `␣contain` 0.04, `␣as` 0.02 |
| 37 | ? ← called chlorophyll. In… | `␣pigment` | 0.475 | 1 | `␣pigment` 0.47, `,` 0.09, `␣leaves` 0.07, `␣cells` 0.06, `␣pigments` 0.04 |
| 38 | ? ← pigment called chlorophyll.… | `␣a` | 0.348 | 2 | `␣green` 0.54, `␣a` 0.35, `␣special` 0.04, `bing` 0.01, `␣colored` 0.00 |
| 39 | ? ← a pigment called chlorophyll… | `␣using` | 0.446 | 1 | `␣using` 0.45, `␣by` 0.11, `␣contain` 0.10, `␣with` 0.07, `␣of` 0.04 |
| 40 | ? ← using a pigment called… | `␣sunlight` | 0.347 | 1 | `␣sunlight` 0.35, `␣energy` 0.29, `␣sun` 0.11, `,` 0.08, `␣light` 0.05 |
| 41 | ? ← sunlight using a pigment… | `␣from` | 0.780 | 1 | `␣from` 0.78, `␣in` 0.06, `␣absorb` 0.04, `␣of` 0.03, `␣capture` 0.03 |
| 42 | ? ← from sunlight using a… | `␣energy` | 0.978 | 1 | `␣energy` 0.98, `␣food` 0.00, `␣comes` 0.00, `␣directly` 0.00, `)` 0.00 |
| 43 | ? ← energy from sunlight using… | `␣capture` | 0.381 | 1 | `␣capture` 0.38, `␣absorb` 0.17, `␣the` 0.10, `␣in` 0.05, `␣trap` 0.04 |
| 44 | ? ← capture energy from sunlight… | `Plants` | 0.115 | 3 | `␣plants` 0.27, `␣Plants` 0.19, `Plants` 0.11, `asts` 0.10, `,` 0.06 |

---

## 14. python_function

*Category: factual*

> **Beginning:** In Python, a function is defined using the def keyword followed by its name.  
> **Middle:** The parameters are listed in parentheses, and the body of the function is indented below the definition.  
> **Ending:** The function sends a value back to the caller using the return statement.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | to a function. ↵  ↵ The function returns a value that is passed to a function. ↵  ↵ The function returns a value that is passed to a function. ↵  ↵ The function returns a value that is passed to a function. ↵  ↵ The function returns a value that is passed to a function. ↵  ↵ The function returns a value that is passed to a function. ↵  ↵ The function takes two arguments. ↵  ↵ The first argument is the value that is passed to the function. ↵  ↵ The second argument is the value that is passed to the function. ↵  ↵ | The function sends a value back to the caller using the return statement. |
| sample | end() function. ↵  ↵ Explanation ↵  ↵ The end() function puts either a string of characters or string of characters at the end of a string. The functions are used to put either a character or symbol at the beginning of a string or a string of characters at the end of a string. These functions are explained in the below code: ↵  ↵ The # symbol is placed at the beginning of the string which is used to accept strings. ↵  ↵ The function accepts a string to provide a value to the function. ↵  ↵ | The function sends a value back to the caller using the return statement. |
| sample | for each file. It also lists the path, directory, and file name for each file. ↵  ↵ Return Statement in Function ↵  ↵ There are various functions in a program. The functions of the return statement in a function are as follows:- ↵  ↵ Return statement ↵  ↵ The return statement is used to return a value. ↵  ↵ Let's see the Function of Return statement. ↵  ↵ Return Statement ↵  ↵ Purpose of the Function ↵  ↵ Function of Return ↵  ↵ The Return statement is used to return to the function ↵  ↵ | The function sends a value back to the caller using the return statement. |
| sample | use it to perform arithmetic operations on the data. ↵  ↵ The function performs all arithmetic operations on the data and returns the value of the function call. ↵  ↵ 12. Define the Return Value ↵  ↵ When we get the result of a function, we need to pass the result to the function, using the return statement. The return statement is used to define the return value of the function call. ↵  ↵ The function will return the value for the number and the result for the data. ↵  ↵ 13. Use the Return ↵  ↵ | The function sends a value back to the caller using the return statement. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | In Python, a function is defined using the def keyword followed by its name. | The def keyword is used to define a function in Python. The def keyword is used to define a function in Python. The def keyword is used to define a function in Python. The def keyword is used to define a function in Python. The def keyword is used to define a function in Python. The def keyword is used to define a function in Python. The def keyword is used to define a function in Python. The def keyword is used to define a function in Python. |
| sample | In Python, a function is defined using the def keyword followed by its name. | The def keyword is a block of code that indicates the function name, including variables, arguments, and other elements. Definitions are essential for programmers, as they provide a clear structure for describing the behavior of functions in code. ↵ Python:def(function1, function2, ..., functionn); ↵ This example defines a function called `save()` that takes three arguments: `function1`, `function2`, and `...`. Inside the `save |
| sample | In Python, a function is defined using the def keyword followed by its name. | For example, the following code is a function to square a number, where the number being squared is called "x". ↵  ↵ The function is called the function module and it is used to implement the function. The function is initialized with an argument. There are two types of arguments in the function module: one is an argument with the name of its type, and the other is the name of an argument with the type of the type argument. The function module is a special type of |
| sample | In Python, a function is defined using the def keyword followed by its name. | For example, foo() is defined as below. ↵ def getfoo(): ↵ foo() is a function defined in the Python module called foo that returns the current value. It is denoted by the Python keyword def. If you want to use functions in a module, you must use that module's functions keyword to use that function. ↵ foo() is defined in the Python module called foo, or foo.py, in the following way. ↵ def getf |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.657 | 52% |
| Backward | previous-token (right context) | 0.683 | 56% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `In` | 0.021 | 4 | `The` 0.07, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | In → ? | `␣Python` | 0.000 | 1057 | `␣the` 0.26, `␣this` 0.09, `␣a` 0.06, `␣` 0.06, `␣addition` 0.04 |
| 3 | In Python → ? | `,` | 0.763 | 1 | `,` 0.76, `␣` 0.04, `␣programming` 0.02, `␣we` 0.01, `␣the` 0.01 |
| 4 | In Python, → ? | `␣a` | 0.079 | 3 | `␣we` 0.24, `␣the` 0.14, `␣a` 0.08, `␣you` 0.07, `␣I` 0.03 |
| 5 | In Python, a → ? | `␣function` | 0.073 | 2 | `␣list` 0.10, `␣function` 0.07, `␣dictionary` 0.05, `␣string` 0.03, `␣variable` 0.03 |
| 6 | …Python, a function → ? | `␣is` | 0.645 | 1 | `␣is` 0.64, `␣can` 0.09, `␣that` 0.01, `␣or` 0.01, `␣has` 0.01 |
| 7 | …, a function is → ? | `␣defined` | 0.069 | 3 | `␣a` 0.56, `␣an` 0.09, `␣defined` 0.07, `␣used` 0.03, `␣just` 0.02 |
| 8 | …a function is defined → ? | `␣using` | 0.046 | 3 | `␣as` 0.52, `␣by` 0.32, `␣using` 0.05, `␣with` 0.03, `␣in` 0.02 |
| 9 | …function is defined using → ? | `␣the` | 0.405 | 1 | `␣the` 0.40, `␣a` 0.28, `␣curly` 0.04, `␣an` 0.03, `␣its` 0.01 |
| 10 | …is defined using the → ? | `␣def` | 0.020 | 10 | `␣keyword` 0.10, `␣function` 0.05, `␣'` 0.03, `␣following` 0.03, `␣module` 0.03 |
| 11 | …defined using the def → ? | `␣keyword` | 0.774 | 1 | `␣keyword` 0.77, `␣__` 0.04, `()` 0.03, `␣operator` 0.03, `␣statement` 0.02 |
| 12 | …using the def keyword → ? | `␣followed` | 0.091 | 3 | `.` 0.56, `,` 0.16, `␣followed` 0.09, `␣and` 0.04, `.\n` 0.02 |
| 13 | …the def keyword followed → ? | `␣by` | 0.996 | 1 | `␣by` 1.00, `␣with` 0.00, `\n` 0.00, `␣immediately` 0.00, `␣a` 0.00 |
| 14 | …def keyword followed by → ? | `␣its` | 0.029 | 4 | `␣a` 0.45, `␣the` 0.36, `␣an` 0.04, `␣its` 0.03, `␣one` 0.02 |
| 15 | …keyword followed by its → ? | `␣name` | 0.161 | 2 | `␣arguments` 0.25, `␣name` 0.16, `␣argument` 0.10, `␣type` 0.06, `␣return` 0.05 |
| 16 | …followed by its name → ? | `.` | 0.527 | 1 | `.` 0.53, `,` 0.13, `␣and` 0.10, `␣(` 0.05, `.\n` 0.04 |
| 17 | …by its name. → ? | `␣The` | 0.165 | 1 | `␣The` 0.16, `␣For` 0.12, `␣def` 0.07, `␣Def` 0.06, `␣A` 0.06 |
| 18 | …its name. The → ? | `␣parameters` | 0.001 | 49 | `␣def` 0.40, `␣function` 0.13, `␣name` 0.05, `␣syntax` 0.03, `␣first` 0.03 |
| 19 | …name. The parameters → ? | `␣are` | 0.148 | 2 | `␣of` 0.42, `␣are` 0.15, `␣passed` 0.04, `␣in` 0.04, `␣and` 0.03 |
| 20 | …. The parameters are → ? | `␣listed` | 0.004 | 30 | `␣passed` 0.17, `␣the` 0.16, `␣defined` 0.07, `␣declared` 0.03, `␣used` 0.03 |
| 21 | …The parameters are listed → ? | `␣in` | 0.375 | 1 | `␣in` 0.37, `␣after` 0.09, `␣below` 0.07, `␣as` 0.06, `␣inside` 0.05 |
| 22 | …parameters are listed in → ? | `␣parent` | 0.072 | 2 | `␣the` 0.66, `␣parent` 0.07, `␣a` 0.04, `␣brackets` 0.03, `␣square` 0.03 |
| 23 | …are listed in parent → ? | `heses` | 0.858 | 1 | `heses` 0.86, `hesis` 0.14, `hes` 0.00, `al` 0.00, `-ch` 0.00 |
| 24 | …listed in parentheses → ? | `,` | 0.130 | 3 | `␣after` 0.29, `.` 0.20, `,` 0.13, `␣following` 0.08, `␣and` 0.05 |
| 25 | …in parentheses, → ? | `␣and` | 0.303 | 1 | `␣and` 0.30, `␣separated` 0.10, `␣followed` 0.06, `␣after` 0.05, `␣with` 0.04 |
| 26 | …parentheses, and → ? | `␣the` | 0.625 | 1 | `␣the` 0.62, `␣a` 0.04, `␣they` 0.03, `␣each` 0.03, `␣you` 0.02 |
| 27 | …heses, and the → ? | `␣body` | 0.040 | 3 | `␣function` 0.31, `␣return` 0.22, `␣body` 0.04, `␣arguments` 0.03, `␣value` 0.02 |
| 28 | …, and the body → ? | `␣of` | 0.731 | 1 | `␣of` 0.73, `␣is` 0.14, `␣contains` 0.03, `␣follows` 0.01, `␣must` 0.01 |
| 29 | …and the body of → ? | `␣the` | 0.963 | 1 | `␣the` 0.96, `␣a` 0.02, `␣each` 0.00, `␣your` 0.00, `␣function` 0.00 |
| 30 | …the body of the → ? | `␣function` | 0.949 | 1 | `␣function` 0.95, `␣definition` 0.01, `␣code` 0.01, `␣program` 0.00, `␣block` 0.00 |
| 31 | …body of the function → ? | `␣is` | 0.675 | 1 | `␣is` 0.67, `␣must` 0.04, `␣follows` 0.03, `␣begins` 0.03, `␣starts` 0.03 |
| 32 | …of the function is → ? | `␣ind` | 0.002 | 42 | `␣enclosed` 0.45, `␣separated` 0.18, `␣followed` 0.07, `␣placed` 0.03, `␣surrounded` 0.02 |
| 33 | …the function is ind → ? | `ented` | 0.992 | 1 | `ented` 0.99, `ent` 0.00, `ended` 0.00, `icted` 0.00, `isc` 0.00 |
| 34 | …function is indented → ? | `␣below` | 0.007 | 17 | `.` 0.35, `.\n` 0.13, `␣to` 0.08, `,` 0.04, `␣with` 0.04 |
| 35 | …is indented below → ? | `␣the` | 0.583 | 1 | `␣the` 0.58, `.` 0.12, `␣them` 0.08, `.\n` 0.05, `␣it` 0.04 |
| 36 | …indented below the → ? | `␣definition` | 0.010 | 19 | `␣parameters` 0.20, `␣parent` 0.12, `␣parameter` 0.08, `␣function` 0.06, `␣def` 0.03 |
| 37 | …ented below the definition → ? | `.` | 0.487 | 1 | `.` 0.49, `.\n` 0.16, `␣of` 0.08, `,` 0.05, `.\n\n` 0.04 |
| 38 | …below the definition. → ? | `␣The` | 0.249 | 1 | `␣The` 0.25, `␣For` 0.13, `␣A` 0.04, `␣In` 0.04, `␣This` 0.03 |
| 39 | …the definition. The → ? | `␣function` | 0.164 | 1 | `␣function` 0.16, `␣body` 0.07, `␣def` 0.05, `␣return` 0.05, `␣parameters` 0.04 |
| 40 | …definition. The function → ? | `␣sends` | 0.000 | 455 | `␣is` 0.18, `␣name` 0.09, `␣body` 0.08, `'s` 0.07, `␣can` 0.06 |
| 41 | …. The function sends → ? | `␣a` | 0.355 | 1 | `␣a` 0.36, `␣the` 0.18, `␣an` 0.11, `␣data` 0.04, `␣its` 0.04 |
| 42 | …The function sends a → ? | `␣value` | 0.012 | 8 | `␣message` 0.45, `␣signal` 0.08, `␣request` 0.06, `␣response` 0.04, `␣string` 0.02 |
| 43 | …function sends a value → ? | `␣back` | 0.040 | 2 | `␣to` 0.79, `␣back` 0.04, `␣of` 0.03, `,` 0.02, `␣as` 0.01 |
| 44 | …sends a value back → ? | `␣to` | 0.907 | 1 | `␣to` 0.91, `␣when` 0.02, `␣as` 0.01, `,` 0.01, `␣in` 0.01 |
| 45 | …a value back to → ? | `␣the` | 0.841 | 1 | `␣the` 0.84, `␣its` 0.06, `␣a` 0.04, `␣Python` 0.01, `␣an` 0.01 |
| 46 | …value back to the → ? | `␣call` | 0.088 | 3 | `␣user` 0.17, `␣calling` 0.12, `␣call` 0.09, `␣client` 0.07, `␣specified` 0.06 |
| 47 | …back to the call → ? | `er` | 0.985 | 1 | `er` 0.98, `back` 0.01, `ers` 0.00, `␣handler` 0.00, `␣stack` 0.00 |
| 48 | …to the caller → ? | `␣using` | 0.021 | 11 | `,` 0.19, `.` 0.14, `.\n` 0.09, `␣when` 0.07, `␣if` 0.04 |
| 49 | …the caller using → ? | `␣the` | 0.701 | 1 | `␣the` 0.70, `␣a` 0.09, `␣its` 0.06, `␣return` 0.03, `␣an` 0.02 |
| 50 | …caller using the → ? | `␣return` | 0.354 | 1 | `␣return` 0.35, `␣function` 0.06, `␣def` 0.04, `␣send` 0.04, `␣returned` 0.04 |
| 51 | …er using the return → ? | `␣statement` | 0.289 | 2 | `␣keyword` 0.48, `␣statement` 0.29, `␣value` 0.08, `␣type` 0.06, `_` 0.01 |
| 52 | …using the return statement → ? | `.` | 0.365 | 1 | `.` 0.36, `.\n` 0.29, `,` 0.10, `.\n\n` 0.09, `␣followed` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.538 | 1 | `.` 0.54, `!` 0.03, `)` 0.02, `).` 0.01, `."` 0.01 |
| 2 | ? ← . | `␣statement` | 0.000 | 798 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣life` 0.00, `␣you` 0.00 |
| 3 | ? ← statement. | `␣return` | 0.003 | 41 | `␣a` 0.17, `␣this` 0.07, `␣the` 0.05, `␣fashion` 0.05, `␣thesis` 0.03 |
| 4 | ? ← return statement. | `␣the` | 0.461 | 1 | `␣the` 0.46, `␣a` 0.18, `␣␣␣` 0.05, `␣The` 0.02, `␣your` 0.02 |
| 5 | ? ← the return statement. | `␣using` | 0.015 | 13 | `␣in` 0.34, `␣of` 0.09, `␣after` 0.08, `␣before` 0.04, `␣to` 0.04 |
| 6 | ? ← using the return statement… | `er` | 0.001 | 234 | `␣by` 0.08, `,` 0.04, `␣without` 0.04, `␣it` 0.03, `␣when` 0.02 |
| 7 | ? ← er using the return… | `␣call` | 0.348 | 1 | `␣call` 0.35, `␣pars` 0.20, `ugg` 0.09, `␣check` 0.03, `␣link` 0.03 |
| 8 | ? ← caller using the… | `␣the` | 0.871 | 1 | `␣the` 0.87, `␣a` 0.01, `␣function` 0.01, `␣The` 0.01, `␣each` 0.00 |
| 9 | ? ← the caller using… | `␣to` | 0.493 | 1 | `␣to` 0.49, `␣by` 0.18, `␣from` 0.09, `␣of` 0.07, `␣for` 0.02 |
| 10 | ? ← to the caller… | `␣back` | 0.241 | 1 | `␣back` 0.24, `␣returned` 0.17, `␣message` 0.06, `␣it` 0.04, `␣return` 0.03 |
| 11 | ? ← back to the call… | `␣value` | 0.043 | 7 | `␣it` 0.09, `␣passed` 0.08, `␣returned` 0.08, `␣message` 0.05, `␣result` 0.05 |
| 12 | ? ← value back to the… | `␣a` | 0.041 | 5 | `␣the` 0.32, `␣return` 0.14, `␣returned` 0.10, `␣that` 0.05, `␣a` 0.04 |
| 13 | ? ← a value back to… | `␣sends` | 0.023 | 7 | `␣return` 0.41, `␣returns` 0.16, `␣returning` 0.07, `␣Return` 0.05, `␣pass` 0.04 |
| 14 | ? ← sends a value back… | `␣function` | 0.079 | 3 | `␣and` 0.22, `␣It` 0.14, `␣function` 0.08, `␣then` 0.07, `␣it` 0.06 |
| 15 | ? ← function sends a value… | `␣The` | 0.129 | 2 | `()` 0.14, `␣The` 0.13, `back` 0.11, `'` 0.10, `␣the` 0.09 |
| 16 | ? ← The function sends a… | `.` | 0.112 | 2 | `:` 0.87, `.` 0.11, `).` 0.00, `)` 0.00, `-` 0.00 |
| 17 | ? ← . The function sends… | `␣definition` | 0.001 | 135 | `␣function` 0.10, `␣False` 0.07, `␣value` 0.06, `␣statement` 0.03, `␣call` 0.02 |
| 18 | ? ← definition. The function… | `␣the` | 0.053 | 2 | `␣function` 0.56, `␣the` 0.05, `␣method` 0.05, `␣class` 0.05, `␣a` 0.02 |
| 19 | ? ← the definition. The… | `␣below` | 0.001 | 42 | `␣in` 0.36, `␣of` 0.20, `␣to` 0.07, `␣from` 0.05, `␣by` 0.04 |
| 20 | ? ← below the definition.… | `ented` | 0.000 | 470 | `␣statement` 0.11, `␣function` 0.07, `␣line` 0.06, `␣just` 0.06, `␣code` 0.05 |
| 21 | ? ← ented below the definition… | `␣ind` | 0.964 | 1 | `␣ind` 0.96, `ind` 0.01, `res` 0.01, `␣Ind` 0.00, `-ind` 0.00 |
| 22 | ? ← indented below the… | `␣is` | 0.311 | 1 | `␣is` 0.31, `␣are` 0.11, `␣be` 0.06, `␣line` 0.04, `,` 0.04 |
| 23 | ? ← is indented below… | `␣function` | 0.146 | 1 | `␣function` 0.15, `␣statement` 0.13, `␣which` 0.09, `␣that` 0.07, `␣and` 0.04 |
| 24 | ? ← function is indented… | `␣the` | 0.493 | 1 | `␣the` 0.49, `␣a` 0.13, `␣The` 0.06, `()` 0.03, `␣this` 0.02 |
| 25 | ? ← the function is ind… | `␣of` | 0.598 | 1 | `␣of` 0.60, `␣to` 0.09, `␣for` 0.07, `␣and` 0.04, `,` 0.04 |
| 26 | ? ← of the function is… | `␣body` | 0.447 | 1 | `␣body` 0.45, `␣name` 0.14, `␣code` 0.09, `␣line` 0.09, `␣definition` 0.04 |
| 27 | ? ← body of the function… | `␣the` | 0.251 | 2 | `␣The` 0.61, `␣the` 0.25, `The` 0.10, `␣main` 0.01, `␣function` 0.01 |
| 28 | ? ← the body of the… | `␣and` | 0.283 | 1 | `␣and` 0.28, `,` 0.26, `␣that` 0.11, `␣in` 0.04, `␣of` 0.03 |
| 29 | ? ← and the body of… | `,` | 0.492 | 1 | `,` 0.49, `␣function` 0.06, `␣statement` 0.05, `␣definition` 0.05, `),` 0.02 |
| 30 | ? ← , and the body… | `heses` | 0.025 | 7 | `␣function` 0.12, `␣statement` 0.10, `␣definition` 0.09, `␣line` 0.03, `␣body` 0.03 |
| 31 | ? ← heses, and the… | `␣parent` | 0.995 | 1 | `␣parent` 1.00, `ant` 0.00, `parent` 0.00, `arent` 0.00, `␣Parent` 0.00 |
| 32 | ? ← parentheses, and… | `␣in` | 0.474 | 1 | `␣in` 0.47, `␣the` 0.13, `␣within` 0.06, `␣between` 0.06, `␣by` 0.05 |
| 33 | ? ← in parentheses,… | `␣listed` | 0.001 | 56 | `␣enclosed` 0.40, `␣statement` 0.05, `␣wrapped` 0.04, `␣placed` 0.03, `␣is` 0.03 |
| 34 | ? ← listed in parentheses… | `␣are` | 0.469 | 1 | `␣are` 0.47, `␣is` 0.46, `␣variables` 0.00, `,` 0.00, `␣and` 0.00 |
| 35 | ? ← are listed in parent… | `␣parameters` | 0.109 | 3 | `␣functions` 0.14, `␣arguments` 0.12, `␣parameters` 0.11, `␣function` 0.09, `␣definition` 0.05 |
| 36 | ? ← parameters are listed in… | `␣The` | 0.226 | 1 | `␣The` 0.23, `␣function` 0.09, `␣the` 0.06, `␣optional` 0.05, `␣its` 0.05 |
| 37 | ? ← The parameters are listed… | `.` | 0.770 | 1 | `.` 0.77, `:` 0.18, `).` 0.03, `".` 0.01, `."` 0.00 |
| 38 | ? ← . The parameters are… | `␣name` | 0.013 | 12 | `␣function` 0.17, `␣parameters` 0.07, `␣definition` 0.06, `␣statement` 0.05, `␣arguments` 0.03 |
| 39 | ? ← name. The parameters… | `␣its` | 0.044 | 3 | `␣function` 0.56, `␣a` 0.07, `␣variable` 0.04, `␣its` 0.04, `␣by` 0.03 |
| 40 | ? ← its name. The… | `␣by` | 0.172 | 1 | `␣by` 0.17, `␣after` 0.17, `␣of` 0.12, `␣to` 0.06, `␣in` 0.05 |
| 41 | ? ← by its name.… | `␣followed` | 0.632 | 1 | `␣followed` 0.63, `␣identified` 0.05, `␣defined` 0.05, `␣called` 0.04, `␣function` 0.03 |
| 42 | ? ← followed by its name… | `␣keyword` | 0.080 | 4 | `,` 0.24, `␣function` 0.19, `␣statement` 0.08, `␣keyword` 0.08, `␣is` 0.06 |
| 43 | ? ← keyword followed by its… | `␣def` | 0.029 | 6 | `␣function` 0.15, `␣a` 0.14, `'` 0.12, `␣return` 0.11, `␣the` 0.08 |
| 44 | ? ← def keyword followed by… | `␣the` | 0.839 | 1 | `␣the` 0.84, `␣a` 0.07, `␣or` 0.03, `␣its` 0.01, `␣using` 0.01 |
| 45 | ? ← the def keyword followed… | `␣using` | 0.537 | 1 | `␣using` 0.54, `␣with` 0.23, `␣by` 0.04, `␣uses` 0.04, `␣use` 0.03 |
| 46 | ? ← using the def keyword… | `␣defined` | 0.314 | 1 | `␣defined` 0.31, `␣declared` 0.09, `␣by` 0.07, `␣function` 0.07, `␣definition` 0.06 |
| 47 | ? ← defined using the def… | `␣is` | 0.938 | 1 | `␣is` 0.94, `␣be` 0.02, `␣are` 0.01, `␣typically` 0.01, `␣usually` 0.00 |
| 48 | ? ← is defined using the… | `␣function` | 0.723 | 1 | `␣function` 0.72, `␣It` 0.04, `␣def` 0.03, `␣method` 0.03, `␣statement` 0.02 |
| 49 | ? ← function is defined using… | `␣a` | 0.077 | 4 | `␣A` 0.24, `␣The` 0.17, `A` 0.13, `␣a` 0.08, `␣def` 0.07 |
| 50 | ? ← a function is defined… | `,` | 0.795 | 1 | `,` 0.80, `␣of` 0.13, `␣that` 0.01, `␣where` 0.00, `␣for` 0.00 |
| 51 | ? ← , a function is… | `␣Python` | 0.271 | 1 | `␣Python` 0.27, `␣Java` 0.21, `++` 0.07, `␣JavaScript` 0.05, `#` 0.04 |
| 52 | ? ← Python, a function… | `In` | 0.517 | 1 | `In` 0.52, `␣In` 0.40, `␣in` 0.08, `␣of` 0.00, `.In` 0.00 |
